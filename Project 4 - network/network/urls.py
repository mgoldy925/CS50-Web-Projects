
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("error/<str:msg>", views.error, name="error"),
    path("following", views.following, name="following"),
    path("p/<str:username>", views.profile, name="profile"),

    # API routes
    path("create", views.create_post, name="create"),
    path("edit", views.edit, name="edit"),
    path("get/<str:which>", views.get_posts, name="get_posts"),
    path("get/<str:which>/<int:current>", views.get_posts, name="get_posts_page"),
    path("follow", views.follow_user, name="follow_user"),
    path("like", views.like, name="like")
]
