from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='following')

    def __str__(self):
        return self.username

    def serialize(self):
        return {
            "username": self.username
        }


class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=2000)
    datetime_posted = models.DateTimeField(auto_now_add=True)
    datetime_edited = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, blank=True, related_name='liked_posts')
    url = models.CharField(max_length=100, default=f"error/Error with profile URL.")

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "content": self.content,
            "posted": self.datetime_posted.strftime("%I:%M %p, %B %d, %Y"),
            "edited": self.datetime_edited.strftime("%I:%M %p, %B %d, %Y"),
            "likes": [user.serialize() for user in self.likes.all()],
            "url": self.url
        }

    def __str__(self):
        return f"{self.poster.username} at {self.datetime_posted}:  {self.content}"