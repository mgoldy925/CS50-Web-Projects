from statistics import mode
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True, related_name="potential_buyers")

    def __str__(self):
        return f"{self.username}"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, related_name="listings")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    active = models.BooleanField()
    # Might move this to Bids
    current_bid = models.ForeignKey('Bid', on_delete=models.CASCADE, related_name="items", null=True)
    # Maybe change to ImageField
    image = models.CharField(max_length=500, blank=True)

    def __str__(self):
        status = "Active" if self.active else "Not Active"
        return f"{self.title} from {self.seller.username}, {status}\n{self.description}"

class Bid(models.Model):
    amount = models.FloatField(default=0)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid_type = models.CharField(max_length=16, default="BID")

    def __str__(self):
        return f"${self.amount:.2f} on {self.item.title} by {self.bidder.username}"

class Comment(models.Model):
    content = models.CharField(max_length=1000)
    op = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    page = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    posted = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.op.username} on {self.page.title} at {self.posted}: {self.content}"
