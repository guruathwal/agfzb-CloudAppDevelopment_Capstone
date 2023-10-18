from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarDealer, CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_by_id_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

#DEALERSHIP_URL = "https://tez2yl63hwr2rgin3pfi2c2oii0dtsrf.lambda-url.us-east-1.on.aws"
DEALERSHIP_URL = "https://us-south.functions.appdomain.cloud/api/v1/web/01dfa25f-f28f-447a-8fc3-88e1da14da5a/dealership-package/get-dealership"
REVIEW_URL = "https://us-south.functions.appdomain.cloud/api/v1/web/01dfa25f-f28f-447a-8fc3-88e1da14da5a/dealership-package/review"

# Create your views here.

def get_about(request):
    return render(request, 'djangoapp/about.html')

def get_contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}

    # Check if 'next' is specified in the URL parameters
    next_page = request.GET.get('next')

    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['password']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)

            # If 'next' is provided, redirect to that page
            if next_page:
               # If next_page, return to last page again
                return redirect(next_page)
            else:
                return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/user_login.html', context)
    else:
        # If not, return to login page again
        return render(request, 'onlinecourse/user_login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)

    # Check if 'next' is specified in the URL parameters
    next_page = request.GET.get('next')

    # Redirect user back to the previous page or 'djangoapp:index' if 'next' is not provided
    return redirect(next_page) if next_page else redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name )
            login(request, user)
            # redirect to course list page
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(DEALERSHIP_URL)
        # Concat all dealer's short name
        context["dealerships"] = dealerships
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    context["dealership"] = get_dealer_by_id_from_cf(DEALERSHIP_URL, dealer_id)[0]
    context["reviews"] = get_dealer_reviews_from_cf(REVIEW_URL, dealer_id)

    return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    print("add review dealer ID:" + str(dealer_id))
    dealership = get_dealer_by_id_from_cf(DEALERSHIP_URL, dealer_id)[0]
    print(dealership)

    context["dealership"] = dealership

    if request.method == 'GET':
        # Get cars for the dealer
        cars = CarModel.objects.all()
        context["cars"] = cars

        if not request.user.is_authenticated:
            context["error"] = "Please login to add a review."

        return render(request, 'djangoapp/add_review.html', context)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect("djangoapp:add_review", dealer_id=dealer_id)

        # Get user's name from logged-in user
        user_name = request.user.username

        # Get review details from request arguments
        purchase = request.POST.get("purchase")

        review = {
            "name": user_name,
            "dealership": dealer_id,
            "review": request.POST.get("review"),
            "purchase": purchase
        }

        # Conditionally add fields if 'purchase' is True
        if purchase:
            car_id = request.POST.get("car_model")
            review["purchase_date"] = request.POST.get("purchase_date")
            review["car_make"] = CarModel.objects.get(id=car_id).car_make.name
            review["car_model"] = CarModel.objects.get(id=car_id).name
            review["car_year"] = CarModel.objects.get(id=car_id).year.strftime("%Y")

        response = post_request(REVIEW_URL, json_payload={"review": review})

        if response.status_code == 200:
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        else:
            print(response.content)
            context["error"] = response.content
            return render(request, 'djangoapp/add_review.html', context)

def custom_404(request, exception):
    return render(request, 'djangoapp/404.html', status=404)

def custom_500(request):
    return render(request, 'djangoapp/500.html', status=500)
