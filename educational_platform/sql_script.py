import random
from datetime import datetime
import os
import django

# Setting up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "educational_platform.settings")
django.setup()

from django.contrib.auth import get_user_model
from CodeGym.models import Exercises, Student, Tutor, Headmaster

# Connect to Django's user model
UserModel = get_user_model()

# Clear existing data
UserModel.objects.all().delete()
Exercises.objects.all().delete()

# Define exercise data
exercises = [
    {
        "title": "How Much Will My Pets Cost?",
        "description": "Imagine you are visiting a pet shop. You notice that each goldfish costs $10, every parrot costs $20, and each rabbit is $15. Write a Python program that asks the user how many of each pet they want to buy and then calculates the total cost!",
        "prompt": "1. Ask the user: \"How many goldfish would you like to buy?\"\n2. Ask the user: \"How many parrots would you like to buy?\"\n3. Ask the user: \"How many rabbits would you like to buy?\"\n4. Calculate the total cost and display it to the user.",
        "example": "How many goldfish would you like to buy? 2\nHow many parrots would you like to buy? 1\nHow many rabbits would you like to buy? 3\nTotal cost: $85"
    },
    {
        "title": "Fill in the Story",
        "description": "Who doesn't love a fun story? Let's create a Python program that lets the user fill in the blanks to create their own silly story!",
        "prompt": "1. Ask the user to give you a name.\n2. Ask the user for their favorite color.\n3. Ask the user for their favorite food.\n4. Print out a story using the inputs from the user.",
        "example": "What's your name? Lily\nWhat's your favorite color? Blue\nWhat's your favorite food? Pizza\n\nOnce upon a time, there was a young girl named Lily. Everywhere she went, she wore her blue dress that matched the color of the sky. One day, she found a magical pizza that granted her three wishes. And her adventures began..."
    }
    # Add more exercises as needed
]

# Insert exercises data using Django ORM
for exercise in exercises:
    Exercises.objects.create(
        title=exercise['title'],
        description=exercise['description'],
        prompt=exercise['prompt'],
        example=exercise['example']
    )

# Dummy data for users
names = ["Alice", "Bob", "Charlie", "David", "Eva", "Frank", "Grace", "Hannah", "Ian", "Jane", "Karl", "Lucy", "Mike", "Nina", "Oscar", "Polly", "Quinn", "Rachel"]
password = "password"  # Dummy password for all users
user_types = [("HEADMASTER", 2), ("TUTOR", 5), ("STUDENT", 10)]

for user_type, count in user_types:
    for _ in range(count):
        if names:
            name = random.choice(names)
            first_name, last_name = (name.split() + ["Doe"])[:2]  # Handles names without spaces
            names.remove(name)
            email = name.lower() + "@example.com"

            if user_type == "STUDENT":
                user = Student.objects.create_user(
                    username=name,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    user_type = "STUDENT"
                )
            elif user_type == "TUTOR":
                user = Tutor.objects.create_user(
                    username=name,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    user_type = "TUTOR"
                )
            elif user_type == "HEADMASTER":
                user = Headmaster.objects.create_user(
                    username=name,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    is_staff=True,
                    user_type = "HEADMASTER"
                )

            user.save()

# No need for explicit commit and close as Django ORM handles it
