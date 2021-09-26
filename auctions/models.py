from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=180)

    def __str__(self):
        return f"{self.user.username} added a comment on {self.timestamp.strftime('%d/%m/%Y, %H:%M')}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid")
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} placed a bid for {self.amount} on {self.timestamp.strftime('%d/%m/%Y, %H:%M')}"

class Category(models.Model):
    CATEGORIES = (
        ("0","Uncategorised"),
        ("1", "Clothing"),
        ("2", "Home/Kitchen"),
        ("3", "Electronics"),
        ("4", "Books"),
        ("5", "Shoes"),
        ("6", "Sports"),
    )
    name = models.CharField(max_length=60, choices=CATEGORIES, default="Uncategorised")

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    title = models.CharField(max_length=60)
    description = models.TextField()
    image = models.ImageField(upload_to="images", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name="listing_category")
    comments = models.ManyToManyField(Comment, blank=True)
    bids = models.ManyToManyField(Bid, blank=True)

    def __str__(self):
        return f"{self.seller.username} added a new listing on {self.timestamp.strftime('%d/%m/%Y, %H:%M')}"
    
    """
    As per assignment specs, any new offers must be higher
    than the current highest.
    This method will return the current highest bid for the listing
    or the value 0 (cast to float) if no bids have been placed for that listing.
    """
    def get_max_bid(self):
        qs = self.bids.all()
        bids = [ obj.amount for obj in qs ]
        return max(bids) if len(bids) > 0 else float(0)

    """ 
    Returns the user id of highest bidder
    for a closed listing (i.e. winner's id)
    """
    def has_winner(self):
        qs = self.bids.all()
        while len(qs) != 0 and not self.is_active:
            bid_info = [ tuple((float(obj.amount), obj.user.id)) for obj in qs ]
            return max(bid_info)[1] if float(self.get_max_bid()) == max(bid_info)[0] else None 

    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing")

    def __str__(self):
        return f"{self.user.username} added '{self.listing.title}' to their watchlist"

            


        




        






