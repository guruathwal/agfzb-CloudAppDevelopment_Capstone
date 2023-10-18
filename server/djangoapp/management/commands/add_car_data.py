
### Run 'python manage.py add_car_data' to add data

from datetime import datetime
from djangoapp.models import CarMake, CarModel

data = [
          ("Alfa Romeo", "Spider", "CONVERTIBLE", 45 , datetime(1994,1,1)),
          ("Audi", "A6", "SEDAN", 15 , datetime(2010,1,1)),
          ("Audi", "A6", "SEDAN", 13 , datetime(1999,1,1)),
          ("BMW", "530", "SEDAN", 17 , datetime(2006,1,1)),
          ("BMW", "550", "SEDAN", 27 , datetime(2006,1,1)),
          ("BMW", "760", "SEDAN", 2 , datetime(2005,1,1)),
          ("BMW", "M5", "SEDAN", 25 , datetime(2008,1,1)),
          ("BMW", "Z3", "CONVERTIBLE", 45 , datetime(2001,1,1)),
          ("Buick", "Terraza", "VAN", 17 , datetime(2006,1,1)),
          ("Cadillac", "DeVille", "SEDAN", 34 , datetime(1995,1,1)),
          ("Cadillac", "Escalade ESV", "SUV", 41 , datetime(2003,1,1)),
          ("Chevrolet", "Aveo", "SEDAN", 49 , datetime(2007,1,1)),
          ("Chevrolet", "Suburban 1500", "SUV", 49 , datetime(2001,1,1)),
          ("Chevrolet", "TrailBlazer", "SUV", 10 , datetime(2004,1,1)),
          ("Dodge", "Ram Van 3500", "VAN", 22 , datetime(1997,1,1)),
          ("Ford", "Explorer Sport Trac", "SUV", 10 , datetime(2000,1,1)),
          ("Ford", "F-Series", "TRUCK", 34 , datetime(2007,1,1)),
          ("Ford", "Taurus", "SEDAN", 40 , datetime(1996,1,1)),
          ("GMC", "Yukon", "SUV", 46 , datetime(1992,1,1)),
          ("Honda", "Odyssey", "VAN", 22 , datetime(1996,1,1)),
          ("Isuzu", "i-350", "TRUCK", 39 , datetime(2006,1,1)),
          ("Isuzu", "Rodeo", "SUV", 23 , datetime(1999,1,1)),
          ("Kia", "Sedona", "VAN", 22 , datetime(2006,1,1)),
          ("Kia", "Spectra", "SEDAN", 13 , datetime(2002,1,1)),
          ("Lexus", "IS F", "SEDAN", 15 , datetime(2009,1,1)),
          ("Lotus", "Exige", "SPORTSCAR", 42 , datetime(2004,1,1)),
          ("Maybach", "57", "SEDAN", 12 , datetime(2012,1,1)),
          ("Mazda", "B-Series", "TRUCK", 42 , datetime(2005,1,1)),
          ("Mazda", "Mazda6", "SEDAN", 9 , datetime(2013,1,1)),
          ("Mazda", "MX-5", "CONVERTIBLE", 29 , datetime(2003,1,1)),
          ("Mazda", "RX-8", "COUPE", 35 , datetime(2009,1,1)),
          ("Mercedes-Benz", "CL-Class", "COUPE", 18 , datetime(2010,1,1)),
          ("Mercedes-Benz", "CL-Class", "COUPE", 7 , datetime(1999,1,1)),
          ("Mercedes-Benz", "S-Class", "SEDAN", 2 , datetime(2003,1,1)),
          ("Mitsubishi", "Endeavor", "SUV", 45 , datetime(2004,1,1)),
          ("Mitsubishi", "Lancer", "SEDAN", 31 , datetime(2010,1,1)),
          ("Nissan", "Altima", "SEDAN", 17 , datetime(2008,1,1)),
          ("Plymouth", "Voyager", "VAN", 44 , datetime(1998,1,1)),
          ("Pontiac", "Firebird", "COUPE", 23 , datetime(1995,1,1)),
          ("Pontiac", "GTO", "COUPE", 12 , datetime(2004,1,1)),
          ("Pontiac", "GTO", "COUPE", 17 , datetime(2004,1,1)),
          ("Porsche", "911", "COUPE", 11 , datetime(2007,1,1)),
          ("Saab", "9-5", "SEDAN", 28 , datetime(1999,1,1)),
          ("Saturn", "L-Series", "SEDAN", 15 , datetime(2001,1,1)),
          ("Saturn", "S-Series", "SEDAN", 6 , datetime(2001,1,1)),
          ("Toyota", "4Runner", "SUV", 11 , datetime(1994,1,1)),
          ("Volkswagen", "New Beetle", "HATCHBACK", 21 , datetime(2001,1,1)),
          ("Volkswagen", "Passat", "SEDAN", 46 , datetime(1987,1,1)),
          ("Volkswagen", "Passat", "SEDAN", 14 , datetime(1996,1,1)),
          ("Volkswagen", "riolet", "CONVERTIBLE", 34 , datetime(1993,1,1)),
        ]

for make, model, car_type, dealer_id, car_year in data:
    car_make, created = CarMake.objects.get_or_create(name=make, description=make)
    CarModel.objects.create(
        car_make=car_make,
        dealer_id=dealer_id,
        name=model,
        type=car_type,
        year=car_year
    )

print("Data added successfully.")
