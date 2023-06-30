from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following", blank=True)

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_post")
    text = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)


