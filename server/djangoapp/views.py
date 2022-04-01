from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarModel, DealerReview
# from .restapis import related methods
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from random import randrange
# from server.djangoapp.restapis import get_dealers_from_cf

unique_id = randrange(1000)

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)
# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
# add user login
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # if not, return to login page again
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
# add user logout
def logout_request(request):
    logout(request)
    print(f"Log out the user '{request.user.username}'")
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
# add registration request
def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        user_exist = False
        try:
            user = User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug(f"{username} does not exist")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            # user.save()
            login(request, user)
            logger.debug(f"{username} has been created")
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url= "https://d8a168f8.us-south.apigw.appdomain.cloud/api/getDealerships"
        dealerships = get_dealers_from_cf(url)
        context['dealerships'] = dealerships
        print(f"CARLOS LOOK HERE!!!: {type(context)}")
        
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    print(type(dealer_id))
    print(dealer_id)
    context = {}
    if request.method == "GET":
        url = "https://d8a168f8.us-south.apigw.appdomain.cloud/api/getReviews"
        dealer_reviews = get_dealer_reviews_from_cf(url, dealer_id=dealer_id)
        print(f"look for dealer details here {dealer_reviews}")
        inventory = CarModel.objects.filter(dealer_id=dealer_id)
        context = {
            "dealer_id": dealer_id,
            "reviews": dealer_reviews,
            "inventory": inventory,
        }
        return render(request, 'djangoapp/dealer_details.html', context)
# Create a `add_review` view to submit a review
# Create a `add_review` view to submit a review
# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# def add_review(request, dealer_id):
# def add_review(request, dealer_id):
# ...


def add_review(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = 'https://d8a168f8.us-south.apigw.appdomain.cloud/api/getDealerships'
        context = {
            "dealer_id": dealer_id,
            "dealer_name": get_dealers_from_cf(url)[dealer_id-1].full_name,
            "cars": CarModel.objects.all(),
        }
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == "POST":
        if (request.user.is_authenticated):
            username = request.user.username
            payload = dict()
            payload["id"] = unique_id # placeholder
            payload["name"] = request.POST["name"]
            payload["dealership"] = dealer_id
            payload["review"] = request.POST["content"]
            if ("purchasecheck" in request.POST):
                payload["purchase"] = True
            else:
                payload["purchase"] = False
            print(request.POST["car"])
            if payload["purchase"] == True:
                print(request.POST['car'])
                car_parts = request.POST["car"].split("|")
                payload["purchase_date"] = request.POST["purchase_date"]
                payload["car_make"] = car_parts[0]
                payload["car_model"] = car_parts[1]
                payload["car_year"] = car_parts[2]

            else:
                payload["purchase_date"] = None
                payload["car_make"] = None
                payload["car_model"] = None
                payload["car_year"] = None
            new_payload = {}
            new_payload['docs'] = payload
            print(new_payload)
            json_result = post_request("https://d8a168f8.us-south.apigw.appdomain.cloud/api/postReview", new_payload, dealerId=dealer_id)
            print(json_result)
            # return JsonResponse(json_result)
            
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)