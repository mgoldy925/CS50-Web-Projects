from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("watchlist/<str:edit>/<str:listing_id>", views.watchlist_edit, name="watchlist_edit"),
    path("category/<str:name>", views.category, name="category"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("close/<int:id>", views.close, name="close"),
    path("error/<str:msg>", views.error, name="error")
]
