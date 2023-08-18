from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.utils import OperationalError
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import User, Post, UserLikes


def index(request):
    user = request.user
    if request.method == "POST":
        post = Post()
        post.text = request.POST["message"]
        post.user = user
        post.save()

    # Check if there are any posts
    try:
        posts = Post.objects.order_by('-date')
        users = posts.values_list("user__username", flat=True)
        post_ids = posts.values_list("id", flat=True)
        texts = posts.values_list("text", flat=True)
        dates = posts.values_list("date", flat=True)
        likes = posts.values_list("like", flat=True)
        print("liketype", type(likes))

        userlikes = []
        for post in posts:
            userlike = UserLikes.objects.filter(post_id=post, user=user).exists()
            print("userlikes", userlikes)
            userlikes.append(userlike)
        

        context = list(zip(users, post_ids, texts, dates, likes, userlikes))
        paginator = Paginator(context, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "page_obj": page_obj
        }

        return render(request, "network/index.html", context)
    except OperationalError:
        # If there are no posts, render the template without the context
        return render(request, "network/index.html")
    
def edit(request):
    if request.method == "POST":
        post_id = request.POST["post_id"]
        post = Post.objects.get(pk=post_id)
        post_content = request.POST["content"]
        post.text = post_content
        post.save(update_fields=['text'])
    
    return JsonResponse({"content": post_content})


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
    user = get_object_or_404(User, username=username)
    user_id = user.id
    n_followers = user.followers.count()
    n_following = user.following.count()
    posts = Post.objects.filter(user_id=user_id)

    paginator = Paginator(posts, 10)  # Set the number of posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    current_user = request.user
    if user in current_user.following.all():
        follow = "Unfollow"
    else:
        follow = "Follow"

    context = {
        "n_followers": n_followers,
        "n_following": n_following,
        "username": user,
        "user_id": user_id,
        "follow": follow,
        "page_obj": page_obj  # Use the paginated page object
    }

    return render(request, 'network/user.html', context)

def toggle_follow(request, target_user_id):
    # Assuming that the current user is logged in and stored in request.user
    current_user = request.user
    print(target_user_id)
    # Fetch the target user by ID
    target_user = User.objects.get(pk=target_user_id)

    # Check if the current user is already following the target user
    if target_user in current_user.following.all():
        # Unfollow
        current_user.following.remove(target_user)
        return JsonResponse({"action": "unfollow"})
    else:
        # Follow
        current_user.following.add(target_user)
        return JsonResponse({"action": "follow"})
    
def toggle_like(request, target_post_id):
    # Assuming that the current user is logged in and stored in request.user
    print(target_post_id)
    # Fetch the target user by ID
    userlikes = UserLikes()
    userlikes.post_id = target_post_id
    userlikes.save()
    users_likes_list = userlikes.filter(post_id=target_post_id)
    if request.user in users_likes_list:
        userlikes.get(post_id=target_post_id).delete()
        return JsonResponse({"action": "like"})
    else:
        userlikes.user_id = request.user
        userlikes.save()
        return JsonResponse({"action": "unlike"})
    
def following(request):
    current_user = request.user
    following_users = current_user.following.all()

    # Check if there are any posts
    try:
        posts = Post.objects.filter(user_id__in=following_users).order_by('-date')
        users = posts.values_list("user__username", flat=True)
        texts = posts.values_list("text", flat=True)
        dates = posts.values_list("date", flat=True)
        likes = posts.values_list("like", flat=True)

        context = list(zip(users, texts, dates, likes))
        paginator = Paginator(context, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "page_obj": page_obj
        }

        return render(request, "network/following.html", context)
    except OperationalError:
        # If there are no posts, render the template without the context
        return render(request, "network/following.html")

