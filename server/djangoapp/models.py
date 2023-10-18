from django.db import models
from django.core import serializers
from django.utils.timezone import now
import uuid
import json

# Create your models here.

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Add any other fields you'd like for CarMake

    def __str__(self):
        return f"{self.name}"

class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()  # Assuming it refers to an ID in your Cloudant database
    name = models.CharField(max_length=100)
    TYPE_CHOICES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('HATCHBACK', 'Hatchback'),
        ('WAGON', 'Wagon'),
        ('VAN', 'Van'),
        ('COUPE', 'Coupe'),
        ('CONVERTIBLE', 'Convertible'),
        ('TRUCK', 'Truck'),
        ('SPORTS CAR', 'Sports Car'),
    ]
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    year = models.DateField()
    # Add any other fields you'd like for CarModel

    def __str__(self):
        return f"{self.car_make.name} - {self.name} - {self.type} - {self.year} - {self.dealer_id}"

class Review(models.Model):
    dealership = models.IntegerField()
    name = models.CharField(max_length=100)
    purchase = models.BooleanField()
    review = models.TextField()
    purchase_date = models.DateField()
    car_make = models.CharField(max_length=50)
    car_model = models.CharField(max_length=50)
    car_year = models.IntegerField()
    sentiment = models.CharField(max_length=50)
    id = models.IntegerField(primary_key=True)

    def __str__(self):
        return "Review: Dealer Id:" + str(self.dealership) + ", " + "review:" + self.review


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, state, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.state = state
        # Dealer state Short
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review, id, purchase_date=None, car_make=None, car_model=None, car_year=None, sentiment=None):
        # review id
        self.id = id
        # Dealer id
        self.dealership = dealership
        # reviewer name
        self.name = name
        # review text
        self.review = review
        # purchase true or false
        self.purchase = purchase
        # Sentiment
        self.sentiment = sentiment

        if purchase:
            # purchase date
            self.purchase_date = purchase_date
            # Car make
            self.car_make = car_make
            # Car model
            self.car_model = car_model
            # Car_year
            self.car_year = car_year
        else:
            self.purchase_date = None
            self.car_make = None
            self.car_model = None
            self.car_year = None
            self.sentiment = None

    def __str__(self):
        return "Review: Dealer Id:" + self.dealership + ", " + "review:" + self.review
