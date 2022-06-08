from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from requests_toolbelt import user_agent
# from django import forms
from .models import *


def index(request):
    # Get all currently active listings
    active_listings = Listing.objects.all().filter(active=True).order_by('-id')

    return render(request, "auctions/index.html", {
        "listings": active_listings,
        "categories": Category.objects.all()
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
        # Make sure starting bid is a number
        try:
            starting_bid = float(request.POST["starting-bid"])
            # Make sure starting bid is >=0
            if starting_bid >= 0:
                # Create listing object with data from request
                listing = Listing(
                    title = request.POST["title"],
                    description = request.POST["description"],
                    category = Category.objects.get(name=request.POST["category"]),
                    seller = request.user,
                    active = True,
                    current_bid = None,
                    image = request.POST["image"]
                )
                # Must save this now, won't allow bid.save() after this if this isn't saved
                listing.save()
                # Create bid for starting bid
                bid = Bid(
                    amount = round(float(request.POST["starting-bid"]), 2),
                    bidder = request.user,
                    item = listing,
                    bid_type = "START"
                )
                bid.save()
                listing.current_bid = bid
                listing.save()
                return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
        except:
            return HttpResponseRedirect(reverse("error", args=("Starting Bid must be a number.",)))

    categories = Category.objects.all()
    return render(request, "auctions/create.html", {
        'categories': categories
    })


def listing(request, id):
    # Get comments for this page
    item = Listing.objects.get(id=id)
    comments = Comment.objects.filter(page=item).order_by('-id')
    comments_posted = [comment.posted.strftime("%c") for comment in comments]
    comments_dict = dict(zip(comments, comments_posted))

    # Check if item is in watchlist for watchlist purposes
    in_watchlist = False
    if request.user.is_authenticated:
        in_watchlist = item in request.user.watchlist.all()

    watchers = item.potential_buyers.all()

    return render(request, "auctions/listing.html", {
        "listing": item,
        "in_watchlist": in_watchlist,
        "comments_dict": comments_dict,
        "winner": item.current_bid.bidder == request.user and item.current_bid.bid_type == "WIN",
        "categories": Category.objects.all(),
        "num_watching": len(watchers)
    })


def category(request, name):
    # Get listings in this category
    category = Category.objects.get(name=name)
    listings = category.listings.all().order_by('-id')

    return render(request, "auctions/category.html", {
        "name": name,
        "listings": listings,
        "categories": Category.objects.all()
    })


@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        'watchlist': request.user.watchlist.all(),
        "categories": Category.objects.all()
    })


@login_required
def watchlist_edit(request, edit, listing_id):
    # Make default error message and get listing for simpler code
    err_msg = "Item neither added or removed from watchlist."
    listing = Listing.objects.get(id=listing_id)

    # Check if editing or removing watchlist
    if edit == "ADD":
        # Ensure listing is not already in watchlist
        if listing not in request.user.watchlist.all():
            request.user.watchlist.add(listing)
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
        else:
            err_msg = f"{listing.title} is already in your watchlist."
    elif edit == "REMOVE":
        # Ensure listing is in watchlist
        if listing in request.user.watchlist.all():
            request.user.watchlist.remove(listing)
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
        else:
            err_msg = f"{listing.title} is not in your watchlist."

    # If an error occurs such as not add or remove, go here
    return HttpResponseRedirect(reverse("error", args=(err_msg,)))


@login_required
def my_listings(request):
    listings = Listing.objects.filter(seller=request.user).order_by('-id')
    return render(request, "auctions/my_listings.html", {
        "listings": listings,
        "categories": Category.objects.all()
    })


@login_required
def bid(request, id):
    # Only do this is posting info for bid
    if request.method == "POST":
        # Ensure bid is a number
        try:
            bid = float(request.POST["bid"])
            listing = Listing.objects.get(id=id)
            # Check if bid is bigger than current bid
            if listing.active and bid > listing.current_bid.amount:
                new_bid = Bid(
                    amount = round(bid, 2),
                    bidder = request.user,
                    item = listing,
                    bid_type = "BID"
                )
                listing.current_bid = new_bid
                new_bid.save()
                listing.save()
                return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
            else:
                return HttpResponseRedirect(reverse("error", args=("Bid must be greater than the current bid.",)))
        except:
            return HttpResponseRedirect(reverse("error", args=("Bid must be a number.",)))
    else:
        return HttpResponseRedirect(reverse("index"))


@login_required
def comment(request, id):
    Comment(
        content = request.POST["comment"],
        op = request.user,
        page = Listing.objects.get(id=id)
    ).save()
    return HttpResponseRedirect(reverse("listing", args=(id,)))


@login_required
def close(request, id):
    listing = Listing.objects.get(id=id)
    # Check seller is the user sending the request
    if listing.seller == request.user:
        winning_bid = listing.current_bid
        # Check either closing or opening listing
        if request.POST["open_close"] == "Close":
            listing.active = False
            winning_bid.bid_type = "WIN"
        elif request.POST["open_close"] == "Open":
            listing.active = True
            winning_bid.bid_type = "BID"
        else:
            return HttpResponseRedirect(reverse("error", args=("Value must either be 'Open' or 'Close'.",)))
        # Make sure to save
        listing.save()
        winning_bid.save()
        return HttpResponseRedirect(reverse("listing", args=(id,)))
    else:
        return HttpResponseRedirect(reverse("error", args=(f"You are not the seller of {listing.title}.",)))


def error(request, msg):
    return render(request, "auctions/error.html", {
        "error_message": msg,
        "categories": Category.objects.all()
    })