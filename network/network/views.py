from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.utils import OperationalError
from django.http import JsonResponse

from .models import User, Post


def index(request):

    if request.method == "POST":
        post = Post()
        post.text = request.POST["message"]
        post.user = request.user
        post.save()

    # Check if there are any posts
    try:
        posts = Post.objects.order_by('-date')
        users = posts.values_list("user__username", flat=True)
        texts = posts.values_list("text", flat=True)
        dates = posts.values_list("date", flat=True)
        likes = posts.values_list("like", flat=True)

        contexts = zip(users, texts, dates, likes)

        context = {
            "context": contexts
        }

        return render(request, "network/index.html", context)
    except OperationalError:
        # If there are no posts, render the template without the context
        return render(request, "network/index.html")



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def user(request, username):
    user = User.objects.get(username=username)
    user_id = user.id
    n_followers = user.followers.count()
    n_following = user.following.count()
    posts = Post.objects.filter(user_id=user_id)

    current_user = request.user
    if user in current_user.following.all():
        follow = "Unfollow"
    else:
        follow = "Follow"

    return render(request, "network/user.html", {
        "n_followers": n_followers,
        "n_following": n_following,
        "posts": posts,
        "username": user,
        "user_id": user_id,
        "follow": follow
    })

def toggle_follow(request, target_user_id):
    # Assuming that the current user is logged in and stored in request.user
    current_user = request.user
    print(current_user)

    # Fetch the target user by ID
    target_user = User.objects.get(pk=target_user_id)
    print(target_user)

    # Check if the current user is already following the target user
    if target_user in current_user.following.all():
        # Unfollow
        current_user.following.remove(target_user)
        return JsonResponse({"action": "unfollow"})
    else:
        # Follow
        current_user.following.add(target_user)
        return JsonResponse({"action": "follow"})