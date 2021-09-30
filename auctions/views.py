from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import CreateForm, BidForm, CommentForm

def index(request):
    """ Default view of the app. Lists all the available products """
    listings=Listing.objects.all()
    context={
        "listings": listings
    }
    return render(request, "auctions/index.html", context)


def login_view(request):
    """ Allow users to log in """
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
    """ ALlow users to log out """
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    """ Register new users """
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


def on_watchlist(user,listing_id):
    """ Helper function to determine if a listing is on a user's watchlist """
    listing = Listing.objects.get(pk=listing_id)
    on_watchlist = True if (Watchlist.objects.filter(user=user, listing=listing).count()) == 1 else False    
    return on_watchlist


@login_required
def listing_view(request, listing_id):
    """ Contains all the information of a specific listing. """
    listing = Listing.objects.get(pk=listing_id)
    comments = listing.comments.all().order_by("-timestamp")
    bid_form = BidForm()
    comment_form = CommentForm()
    winner = listing.has_winner()
    context={
        "obj": listing,
        "comments": comments,
        "bid_form": bid_form,
        "comment_form": comment_form,
        "winner": winner,
        "on_watchlist": on_watchlist(request.user, listing_id)
    }
    if request.method == "GET":
        return render(request, "auctions/listing_view.html", context)
            

@login_required
def create(request):
    """ 
    View to create a new listing 
    Renders success message and redirects the user 
    to the main page on successful creation
    """
    if request.method == "GET":
        return render(request, "auctions/create.html", {"create_form": CreateForm()})
    else:
        create_form = CreateForm(request.POST, request.FILES)
        if create_form.is_valid():
            listing = create_form.save(commit=False)
            listing.seller = request.user
            listing.save()
            messages.success(request, "Listing successfully created")
            return redirect("index")
        else:
            messages.warning(request, "Please complete all required fields.")
            return render(request, "auctions/create.html", {create_form: CreateForm()})

@login_required
def bid(request, listing_id):
    """
    Handles the bidding logic.
    The get_max_bid() method of the Listing class is called
    to ensure that all new bids are higher than the current maximum.
    User is presented with appropriate messages depending on bid amount.
    """
    listing = Listing.objects.get(pk=listing_id)
    comments = listing.comments.all().order_by("-timestamp")
    user = request.user
    context = {
        "bid_form": BidForm(),
        "comment_form": CommentForm(),
        "obj": listing,
        "comments": comments,
        "on_watchlist": on_watchlist(request.user, listing_id)
    }
    if request.method == "POST":
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            bid = bid_form.save(commit=False)
            bid.amount = request.POST["amount"]
            bid.user = user
            bid.save()
            if float(bid.amount) < listing.price:
                messages.warning(request, "Invalid amount!")
                return render(request, "auctions/listing_view.html", context)
            if float(bid.amount) <= float(listing.get_max_bid()):
                messages.warning(request, f"Must offer higher than {listing.get_max_bid()}")
                return render(request, "auctions/listing_view.html", context)
            else:
                listing.bids.add(bid)
                listing.save()
                messages.success(request, "Success!")
                return render(request, "auctions/listing_view.html", context)
    return render(request, "auctions/listing_view.html", context)
    

@login_required
def manage_listing(request, listing_id):
    """
    Handles the logic of closing a listing.
    Notifies the seller about the listing's availability.
    """
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        if listing.is_active and "close" in request.POST:
            listing.is_active = False
            listing.save()
            messages.info(request, "You closed this listing")
            return redirect("listing_view", listing_id=listing.id)
    return redirect("listing_view", listing_id=listing.id)
                
@login_required
def toggle_watchlist(request, listing_id):
    """
    Add or remove from user's watchlist.
    User is presented with appropriate messages depending on action
    as well as a visual indication.
    """
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        if "watchlist" in request.POST and not on_watchlist(user, listing_id):
            Watchlist.objects.create(user=user, listing=listing)
            messages.info(request, "Added to Watchlist")
            return redirect("listing_view", listing_id=listing.id)
        else:
            Watchlist.objects.filter(user=user, listing=listing).delete()
            messages.info(request, "Removed from Wathclist")
            return redirect("listing_view", listing_id=listing.id)
    return redirect("listing_view", listing_id=listing.id)

@login_required
def view_watchlist(request):
    """ Return a list of items in the user's watchlist """
    user = request.user
    qs = user.watchlist.all()
    context = {"watchlist": qs}
    return render(request, "auctions/view_watchlist.html", context)

@login_required
def comment(request, listing_id):
    """ Handles the posting of comments """
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = user
            comment.text = request.POST["text"]
            comment.save()
            listing.comments.add(comment)
            listing.save()
            comments = listing.comments.all().order_by("-timestamp")
            context = {
                "obj": listing,
                "comments": comments,
                "comment_form": CommentForm(),
                "bid_form": BidForm(),
                "on_watchlist": on_watchlist(user,listing_id)
            }
            return render(request, "auctions/listing_view.html", context)
        else:
            context = {
                "obj": listing,
                "comment_form": CommentForm(),
                "bid_form": BidForm(),
                "on_watchlist": on_watchlist(user,listing)
            }
            return render(request, "auctions/listing_view.html", context)
    else:
        context = {
            "obj": listing,
            "comment_form": CommentForm(),
            "bid_form": BidForm(),
            "on_watchlist": on_watchlist(user,listing_id)
        }
    return render(request, "auctions/listing_view.html", context)

@login_required
def categories(request):
    """ Returns a view of all categories """
    categories = Category.objects.all()
    context = {
        "categories": categories
    }
    return render(request, "auctions/categories.html", context)
    
    

@login_required
def listings_by_category(request, category_id):
    """ Returns a view of all listings in a given category """
    category = Category.objects.get(pk=category_id)
    listings_by_category = Listing.objects.filter(category__id=category.id)
    context = {
        "qs": listings_by_category,
    }
    return render(request, "auctions/listings_by_category.html", context)
    





    
    
    
    
    