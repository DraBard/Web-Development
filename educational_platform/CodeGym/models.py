from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id = models.AutoField(primary_key=True)

    USER_TYPE_CHOICES = (
        ('HEADMASTER', 'HEADMASTER'),
        ('TUTOR', 'Tutor'),
        ('STUDENT', 'Student'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, null=False)

class Headmaster(User):

    class Meta:
        permissions = [
            ("can_access_headmaster_dashboard", "Can access headmaster dashboard"),
            # Other tutor-specific permissions
        ]

class Tutor(User):
    expertise_area = models.CharField(max_length=200)

    class Meta:
        permissions = [
            ("can_access_tutor_dashboard", "Can access tutor dashboard"),
            # Other tutor-specific permissions
        ]

class Student(User):

    class Meta:
        permissions = [
            ("can_access_student_dashboard", "Can access student dashboard"),
            # Other student-specific permissions
        ]

class Exercises(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    prompt = models.CharField(max_length=1000)
    example = models.CharField(max_length=1000)


