from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.utils import OperationalError
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import User, Exercises
import json
import docker

def index(request):
    return render(request, "CodeGym/index.html")


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
            return render(request, "CodeGym/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "CodeGym/login.html")


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
            return render(request, "CodeGym/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "CodeGym/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "CodeGym/register.html")
    

def user(request):
    return render(request, 'CodeGym/user.html')


def exercises(request):
    exercise_ids = Exercises.objects.values_list('id', flat=True)
    titles = Exercises.objects.values_list('title', flat=True)
    context = zip(exercise_ids, titles)

    context = { 
        "context": context
    }
    return render(request, 'CodeGym/exercises.html', context)


def exercise(request, exercise_id):
    exercises = Exercises.objects.get(pk=exercise_id)
    title = exercises.title
    description = exercises.description
    prompt = exercises.prompt
    example = exercises.example

    context = {
        "title": title,
        "description": description,
        "prompt": prompt,
        "example": example
    }
    return render(request, 'CodeGym/exercise.html', context)

def run_code(request):
    if request.method == 'POST':
        print("here")
        try:
            data = json.loads(request.body)
            code = data.get('code', '')
            print(code)
            client = docker.from_env()
            try:
                # Note: This is a very basic way of running the code, and it's limited to Python.
                result = client.containers.run("python:3.8", command=["python", "-c", code], remove=True, timeout=10)
                return JsonResponse({'output': result.decode()})
            except Exception as e:
                return JsonResponse({'error': str(e)})
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON format")

    return JsonResponse({'error': 'Invalid request'})
