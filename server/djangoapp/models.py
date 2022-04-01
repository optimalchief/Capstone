from django.db import models
from django.utils import timezone
from django.contrib import admin

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    """Model definition for CarMake."""

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)

    # class Meta:
    #     """Meta definition for CarMake."""

    #     verbose_name = 'CarMake'
    #     verbose_name_plural = 'CarMakes'

    def __str__(self):
        """Unicode representation of CarMake."""
        return self.name

class CarModel(models.Model):
    """Model definition for CarModel."""

    vehicle_choices = (('Sedan', 'Sedan'), ('SUV', "SUV"), ('WAGON', 'WAGON'),
                   ("Coupe", "Coupe"), ("Van", "Van"), ("Pickup", "Pickup"))

    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=50)
    vehicle_type = models.CharField(max_length=50, choices=vehicle_choices, default=vehicle_choices[1])
    dealer_id = models.IntegerField()
    year = models.DateField(default=timezone.now())

    # class Meta:
    #     """Meta definition for CarModel."""

    #     verbose_name = 'CarModel'
    #     verbose_name_plural = 'CarModels'

    def __str__(self):
        """Unicode representation of CarModel."""
        return "Name: " + self.name + \
            " Make Name: " + self.make.name + \
            " Type: " + self.vehicle_type + \
            " Dealer ID: " + str(self.dealer_id) + \
            " Year: " + str(self.year)

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, state, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.state = state
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, id, dealership, name, purchase, review):
        self.id = id
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review

    def set_purchase_details(self, purchase_date, car_make, car_model, car_year):
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year

    def __str__(self):
        return "Review: " + self.review