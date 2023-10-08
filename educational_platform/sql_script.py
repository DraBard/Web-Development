import sqlite3

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

# Commit changes and close connection
conn.commit()
conn.close()
