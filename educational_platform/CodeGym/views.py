from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.models import Permission
from django.shortcuts import render
from django.urls import reverse
from django.db.utils import OperationalError
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Exercises, Student, Tutor, Headmaster, User
import json
import docker
import os

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
        user_type = request.POST["user_type"]
        
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "CodeGym/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            if user_type == "HEADMASTER":
                user = Headmaster.objects.create_user(username, email, password)
                tutor_permission = Permission.objects.get(codename='can_access_headmaster_dashboard')
                user.user_permissions.add(tutor_permission)
            if user_type == "TUTOR":
                user = Tutor.objects.create_user(username, email, password)
                tutor_permission = Permission.objects.get(codename='can_access_tutor_dashboard')
                user.user_permissions.add(tutor_permission)
            if user_type == "STUDENT":
                user = Student.objects.create_user(username, email, password)
                student_permission = Permission.objects.get(codename='can_access_student_dashboard')
                user.user_permissions.add(student_permission)
            user.user_type = user_type
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


def has_tutor_or_headmaster_perms(user):
    return user.has_perm('CodeGym.can_access_tutor_dashboard') or user.has_perm('CodeGym.can_access_headmaster_dashboard')

@user_passes_test(has_tutor_or_headmaster_perms)
def groups(request):
    if request.method == "GET":
        user_type = request.user.user_type
        if user_type == "HEADMASTER":
            students = User.objects.filter(user_type="STUDENT")

    return render(request, 'CodeGym/groups.html', {'students': students})


def run_code(request):
    if request.method == "POST":
        # Parse the JSON data
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        code = body_data.get('code_in')    

    # Save the code to a file
    with open('script.py', 'w') as file:
        file.write(code)

    # Connect to Docker
    client = docker.from_env()
    script_path = os.path.abspath('script.py').rstrip('script.py')
    print(script_path)
    # Run the container
    try:
        print("I am here 1")
        container = client.containers.run(
            "codegym:latest",
            detach = True,
            volumes={script_path: {'bind': '/app', 'mode': 'rw'}},
            # remove=True,  # remove the container when it's done
            mem_limit='100m',  # limit the memory usage
            network_disabled=True,  # disable network access for security
            # stdout=True,
            # stderr=True,
            command=["python", "/app/script.py"],
        )
        # # Wait for the container to finish execution
        # exit_code, output = container.wait(condition='not-running')
        # print("Container exited with code:", exit_code)
        print("after docker run")
        container.wait()  # This line will block until the container stops.
        print("Container execution finished.")
        # Get the logs (output)
        logs = container.logs()
        print("Logs1", logs)
        print("Logs", logs.decode("utf-8"))
        print("I am here 3")
        container.remove()

    except docker.errors.ContainerError as e:
        # The container exited with a non-zero exit code
        return JsonResponse({'error': str(e)})
    except Exception as e:
        # Handle other exceptions
        return JsonResponse({'error': 'An unexpected error occurred'})

    # Return the container's output as a response
    return JsonResponse({'output': logs.decode('utf-8')})
