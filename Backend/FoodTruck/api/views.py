from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Truck
from api.serializers import TruckSerializer
import math, re
from haversine import haversine
import datetime
from pytz import timezone

from utils import toRad, toDeg, destPoint, dayExpander
from utils import timeTo24, timeExpander, timeInRange
from utils import filterByLatLonBounds, filterByRadius
from utils import filterByQuery, filterTrucks, findOpenClosed


@api_view(['GET'])
def truck_list(request):
   """
   View for API endpoint "GET /api/v1/trucks"

   Returns list of api.models.Truck objects that satisfy queries in request.GET
   If there are no queries, return all api.models.Truck objects

   Response also includes metadata about the food truck. Such as an "isOpen" field
   that denotes if the Food Truck is currently open according to San Francisco Local Time

   An example Response data looks like
   [
      {
	 "meta": { "isOpen": "YES" },
	 "data" : { api.models.Truck object }
      },
      .
      .
      .
   ]

   Query Parameters
   ================
   latLng: (float, float) tuple
	   Tuple signifies (Latitude, Longitude) of position on map
   rad: float
        float number that denotes radius of search in Kilometers
   q: String
      Comma seperated string that denotes food items

   Notes
   =====
   1) Food items search is an OR based search. i.e, if a food truck sells any of the food items
      mentioned in the query, then it will be included in results

   """
   trucksList = []
   if request.method == 'GET':
      latLng = request.GET.get('latLng', None)
      radius = request.GET.get('rad', None)
      query = request.GET.get('q', None)

      #filter trucks by latLng, radius and query
      trucks = filterTrucks(latLng, radius, query)

      #Find if trucks are open or closed
      trucksList = findOpenClosed(trucks)

   return Response(trucksList)

