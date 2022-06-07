from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    # Found how to have optional parameter on StackOverflow
    path("edit/", views.edit, name="edit"),
    path("edit/<str:title>", views.edit, name="edit_redirect"),
    path("random", views.random, name="random"),
    path("<str:title>", views.entry, name="entry")
]
