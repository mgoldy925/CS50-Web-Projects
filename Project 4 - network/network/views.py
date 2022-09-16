import json
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
# from django.middleware.csrf import CsrfViewMiddleware
# from django.core.paginator import Paginator

from .models import User, Post
from math import ceil


def index(request):
    return render(request, "network/index.html")

def following(request):
    if request.user.is_authenticated:
        return render(request, "network/following.html")
    else:
        return HttpResponseRedirect(reverse("error", args=("You must be signed it to view this page.",)))

def profile(request, username):
    try:
        profile = User.objects.get(username=username)
        return render(request, "network/profile.html", {
            "profile": {
                "username": profile.username,
                "followers": profile.followers.all()
            },
            "not_profile": not request.user == profile
        })
    except:
        return HttpResponseRedirect(reverse("error", args=(f"{username} is not a valid user.",)))

def error(request, msg):
    return render(request, "network/error.html", {
        "msg": msg
    })


# API views
POSTS_PER_PAGE = 10

@csrf_exempt
def create_post(request):

    # Found on stack overflow to deal w/ csrf
    # request.csrf_processing_done = False
    # reason = CsrfViewMiddleware().process_view(request, None, (), {})
    # if reason is not None:
    #     return JsonResponse({"error": "Invalid CSRF token."}, status=403)

    # Ensure POST request
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "You must be logged in to make a post."}, status=401)

    # Get info for post
    data = json.loads(request.body)
    poster = request.user
    content = data.get("content")
    url = reverse("profile", args=(f"{poster.username}",))

    # Ensure post content isn't empty
    if content is None:
        return JsonResponse({"error": "You cannot make an empty post."}, status=403)

    # Create and save post
    post = Post(
        poster = poster,
        content = content,
        url = url
    )
    post.save()

    return JsonResponse({"message": "Post created successfully."}, status=201)


@csrf_exempt
def edit(request):
    # Ensure user is logged in
    if not request.user.is_authenticated:
        return JsonResponse({"error": "You must be logged in to make a post."}, status=401)
    
    # Ensure POST request
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get data from request
    data = json.loads(request.body)
    post = Post.objects.get(id=data.get("id"))
    content = data.get("content")

    # Ensure post exists
    if post is None:
        return JsonResponse({"error": "Post does not exist."}, status=400)

    # Ensure content is not empty
    if content is None:
        return JsonResponse({"error": "Cannot make empty post."}, status=403)
    
    # Ensure user making edit is poster
    if request.user != post.poster:
        return JsonResponse({"error": "Cannot edit other users' posts."}, status=403)

    # Edit post content (time edited is changed automatically), then save post object
    post.content = content
    post.save()

    return JsonResponse({"message": f"Post edited successfully.", "time": post.datetime_edited.strftime("%I:%M %p, %B %d, %Y")}, status=200)


def get_posts(request, which, current=0):  # Current is page number, NOT post number

    # Get all posts
    if which == "all":
        posts = Post.objects.all().order_by("-datetime_posted")
    
    # Get posts for users that current user is following
    elif which == "following":

        if request.user.is_authenticated:

            # Get accounts following
            accounts = request.user.following.all()
            
            # Get all posts from accounts being followed
            posts = Post.objects.filter(poster__in=accounts)
            posts = posts.order_by("-datetime_posted")

        else:
            return JsonResponse({
                "error": "You must be logged in."
            }, status=401)
    
    # Get posts for specific user
    else:
        
        # Check for profile name
        for user in User.objects.all():
            if which == user.username:
                posts = user.posts.order_by("-datetime_posted")
                break
        
        # If not found
        else:
            return JsonResponse({"error": "Invalid profile page."}, status=400)

    n = len(posts)
    # Check page is valid page number
    if current < 0 or current > ceil(n / POSTS_PER_PAGE) - 1:
        return JsonResponse({"error": "Invalid page number."}, status=404)
    
    # Return posts for page
    else:
        posts = posts[current*POSTS_PER_PAGE:min((current+1)*POSTS_PER_PAGE, n)]
        info = {
            "first": 0,
            "last": ceil(n / POSTS_PER_PAGE) - 1,  # Note the -1, bc 1-9 are page 0, 10-19 are page 1, etc.
            "current": current,
            "which": which,
            "user": request.user.serialize() if request.user.is_authenticated else None,
            "authenticated": request.user.is_authenticated
        }
        posts = [post.serialize() for post in posts]
        elements = {
            "info": info,
            "posts": posts
        }
        return JsonResponse(elements, safe=False, status=200)    


@csrf_exempt
def follow_user(request):

    # Ensure user is logged in
    if not request.user.is_authenticated:
        return JsonResponse({"error": "You must be logged in to make a post."}, status=401)

    # Ensue POST method is used
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get data from request
    data = json.loads(request.body)
    acc_to_follow = User.objects.get(username=data["name"])
    
    # Ensure user to follow is not user
    if (request.user == acc_to_follow):
        return JsonResponse({"error": "You cannot follow yourself."}, status=403)
    
    following = request.user.following
    # Check is user is currently following or not
    if following.contains(acc_to_follow):
        following.remove(acc_to_follow)
        action = "unfollowed"
    else:
        following.add(acc_to_follow)
        action = "followed"
    
    return JsonResponse({"message": f"Account {action} successfully.", "followed": action == "followed", "num_followers": acc_to_follow.followers.all().count()}, status=200)


@csrf_exempt
def like(request):

    # Ensure user is logged in
    if not request.user.is_authenticated:
        return JsonResponse({"error": "You must be looged in."}, status=401)

    # Ensue POST method is used
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get data from request
    data = json.loads(request.body)
    likes = Post.objects.get(id=data.get("id")).likes
    
    # Check is user is currently following or not
    if likes.contains(request.user):
        likes.remove(request.user)
        action = "unliked"
    else:
        likes.add(request.user)
        action = "liked"
    
    return JsonResponse({"message": f"Post {action} successfully.", "liked": action == "liked", "num_likes": likes.all().count()}, status=200)



# Login/register views, given from CS50

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")





