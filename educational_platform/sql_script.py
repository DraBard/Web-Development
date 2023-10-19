import sqlite3
import random
from datetime import datetime
import os
import django

# Setting up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "educational_platform.settings")
django.setup()

from django.contrib.auth import get_user_model
from CodeGym.models import Exercises, User

# Connect to Django's user model
User = get_user_model()

# Clear existing data
User.objects.all().delete()
Exercises.objects.all().delete()

# Connect to database (it will create 'exercises.db' if it doesn't exist)
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

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
]

# Insert data into the table
for exercise in exercises:
    cursor.execute('''
    INSERT INTO CodeGym_exercises (title, description, prompt, example)
    VALUES (?, ?, ?, ?)
    ''', (exercise['title'], exercise['description'], exercise['prompt'], exercise['example']))

# Dummy data for users
names = ["Alice", "Bob", "Charlie", "David", "Eva", "Frank", "Grace", "Hannah", "Ian", "Jane", "Karl", "Lucy", "Mike", "Nina", "Oscar", "Polly", "Quinn", "Rachel"]
password = "password"  # Dummy password for all users
current_datetime = datetime.now()

for user_type in [("HEADMASTER", 2), ("TUTOR", 5), ("STUDENT", 10)]:
    for _ in range(user_type[1]):
        name = random.choice(names)
        first_name = name.split()[0] if ' ' in name else name
        last_name = name.split()[1] if ' ' in name else 'Doe'
        names.remove(name)
        user = User(username=name, email=name.lower() + "@example.com", first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.user_type = user_type[0]
        if user_type[0] == "HEADMASTER":
            user.is_staff = True
        user.save()

# # Insert 2 headmasters
# for i in range(2):
#     name = random.choice(names)
#     first_name = name.split()[0] if ' ' in name else name  # Extracting first name
#     last_name = name.split()[1] if ' ' in name else 'Doe'  # Extracting last name or using a default
#     names.remove(name)  # Ensure unique names
#     cursor.execute('''
#     INSERT INTO CodeGym_user (username, password, email, user_type, is_superuser, first_name, last_name, is_staff, is_active, date_joined)
#     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#     ''', (name, password, name.lower() + "@example.com", "HEADMASTER", 0, first_name, last_name, 1, 1, current_datetime))

# # Insert 5 tutors
# for i in range(5):
#     name = random.choice(names)
#     first_name = name.split()[0] if ' ' in name else name  # Extracting first name
#     last_name = name.split()[1] if ' ' in name else 'Doe'  # Extracting last name or using a default
#     names.remove(name)  # Ensure unique names
#     cursor.execute('''
#     INSERT INTO CodeGym_user (username, password, email, user_type, is_superuser, first_name, last_name, is_staff, is_active, date_joined)
#     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#     ''', (name, password, name.lower() + "@example.com", "TUTOR", 0, first_name, last_name, 0, 1, current_datetime))

# # Insert 10 students
# for i in range(10):
#     name = random.choice(names)
#     first_name = name.split()[0] if ' ' in name else name  # Extracting first name
#     last_name = name.split()[1] if ' ' in name else 'Doe'  # Extracting last name or using a default
#     names.remove(name)  # Ensure unique names
#     cursor.execute('''
#     INSERT INTO CodeGym_user (username, password, email, user_type, is_superuser, first_name, last_name, is_staff, is_active, date_joined)
#     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#     ''', (name, password, name.lower() + "@example.com", "STUDENT", 0, first_name, last_name, 0, 1, current_datetime))




# Commit changes and close connection
conn.commit()
conn.close()