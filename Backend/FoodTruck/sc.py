

import os
os.environ["DJANGO_SETTINGS_MODULE"] = "FoodTruck.settings"
import django
django.setup()

from api.models import Truck
from api.serializers import TruckSerializer

truck = Truck(applicant='a', facilityType='b', address='c', permit='dd', foodItems='d', lat=float('1.2'), lon=float('2.2'), daysHours='fdd', geohash='fdf')

truck.save()

