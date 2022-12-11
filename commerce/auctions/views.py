from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listings, Bids, Watchlists, Comments, Categories
from django.db.models import Max
from django.contrib import messages
from django.shortcuts import render, redirect


def index(request):
    # Query all listings and related highest price
    listing = Listings.objects.raw("SELECT auctions_listings.*, MAX(auctions_bids.bid) AS highest_bid FROM auctions_listings, auctions_bids WHERE auctions_listings.id=auctions_bids.auction_id GROUP BY auctions_bids.auction_id")

    return render(request, "auctions/index.html", {
    "listings": listing
    })



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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):
    if request.method == "POST":
        listing = Listings()
        listing.title = request.POST.get("title")
        listing.description = request.POST.get("description")
        listing.image = request.POST.get("image")
        listing.starting_bid = request.POST.get("starting_bid")
        listing.category = Categories.objects.get(pk=request.POST.get("category"))
        listing.user = request.user
        listing.save()
        # Save the starting bid as the first one in the Bids table
        listing = Listings.objects.get(pk=listing.pk)
        starting_bid = Bids(auction=listing, bidder=request.user, bid=request.POST.get("starting_bid"))
        starting_bid.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        categories = Categories.objects.all()
        return render(request, "auctions/create.html", {
            "categories": categories
        })

def auction(request, listing_pk):
    listing = Listings.objects.get(pk=listing_pk)
    highest_bid = Bids.objects.filter(auction_id=listing_pk).aggregate(Max("bid"))['bid__max']
    # When there are no bids
    if listing.starting_bid == highest_bid:
        highest_bid = listing.starting_bid
        highest_bidder = None    
    # When there is at least one bid 
    else:
        highest_bidder = Bids.objects.filter(auction_id=listing_pk).annotate(Max('bid')).order_by('-bid').first().bidder
    # Get the comments on that auction
    comments = Comments.objects.filter(auction_id=listing_pk).values_list("comment", flat=True)
    context = {
        "title": listing.title,
        "description": listing.description,
        "highest_bid": highest_bid,
        "image": listing.image,
        "listing_pk": listing_pk,
        "listing_user": listing.user,
        "open": listing.open,
        "highest_bidder": highest_bidder,
        "comments": comments
    }

    return render(request, "auctions/listing.html", context)

def categories_view(request):
    categories = Categories.objects.all()

    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def categories_listings(request, category_pk):
    listings = Listings.objects.filter(category_id=category_pk)
    categories = Categories.objects.get(pk=category_pk)
    category = categories.categories

    return render(request, "auctions/categories_listings.html", {
        "category": category,
        "listings": listings
    })


@login_required
def bid(request, listing_pk):
    # get info from database
    listing = Listings.objects.get(pk=listing_pk)
    user = request.user
    try:
        bid = float(request.POST.get("bid"))
    except ValueError:
        messages.success(request, "You must place a bid")
        return redirect("listing", listing_pk=listing_pk)
    # Update db for Bids model
    # Check if there is a bid on that auction
    if Bids.objects.filter(auction_id=listing_pk):
        highest_bid = Bids.objects.filter(auction_id=listing_pk).aggregate(Max("bid"))['bid__max']        
        if bid > highest_bid:
            new_bid = Bids(auction=listing, bidder=user, bid=bid)
            new_bid.save()
            messages.success(request, "Your bid has been saved")
        else:
            messages.success(request, "Your bid must be higher then the current price")
    elif bid > listing.starting_bid:    
        new_bid = Bids(auction=listing, bidder=user, bid=bid)
        new_bid.save()
        messages.success(request, "Your bid has been saved")
    else:
        messages.success(request, "Your bid must be higher than the current price")

    return redirect("listing", listing_pk=listing_pk)
    
@login_required
def watchlist_add(request, listing_pk):
    watchlist = Watchlists()
    watchlist.watchlist = True
    listing = Listings.objects.get(pk=listing_pk)
    watchlist.auction = listing
    watchlist.user = request.user
    watchlist.save()

    return redirect("listing", listing_pk=listing_pk)

@login_required
def watchlist_view(request):
    # Extract the listings that are on the watchlist
    # Extract by raw query in Django works so that the created
    # instance can only be iterated later on like in 'watchlist.html'
    listings = Listings.objects.raw('SELECT auctions_listings.id, image, title, auctions_watchlists.id AS watchlist_pk\
    FROM auctions_listings, auctions_watchlists WHERE auctions_listings.id=auctions_watchlists.auction_id')
    return render(request, "auctions/watchlist.html",    {
    "listings": listings,
    })

@login_required
def watchlist_delete(request, watchlist_pk):
    Watchlists.objects.filter(pk=watchlist_pk).delete()

    return HttpResponseRedirect(reverse("watchlist_view"))

@login_required
def close(request, listing_pk):
    Listings.objects.filter(pk=listing_pk).update(open="False")

    return HttpResponseRedirect(reverse("index"))

@login_required
def comment(request, listing_pk):

    comment = request.POST.get("comment")
    listing = Listings.objects.get(pk=listing_pk)
    new_comment = Comments(auction=listing, user=request.user, comment=comment)
    new_comment.save()

    return redirect("listing", listing_pk=listing_pk)
