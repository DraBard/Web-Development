from email.policy import default
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    pass

# Automatically populate this table with fixed set of categories
# Data Migrations
# https://docs.djangoproject.com/en/1.8/topics/migrations/#data-migrations
class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    categories = models.CharField(max_length=20)

class Listings(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=400)
    open = models.BooleanField(default=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="categories_listings")

    def __str__(self) -> str:
        return f"{self.title}"

class Bids(models.Model):
    id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="auction_bid")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bid = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="auction_comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentator")
    comment = models.CharField(max_length=500)

class Watchlists(models.Model):
    id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="auction_watchlist")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")
    watchlist = models.BooleanField()

