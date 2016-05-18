from django.shortcuts import render


from api.models import Truck
from api.serializers import TruckSerializer
import math, re
from haversine import haversine
import datetime
from pytz import timezone

def toRad(x):
   """
   Converts Degrees to Radians

   Parameters
   ==========
   x : Double
       a Double number in Radians
   """
   return x * math.pi / 180

def toDeg(x):
   """
   Converts Radians to Degrees

   Parameters
   ==========
   x : Double
       a Double number in Radians
   """
   return x * 180 / math.pi

def destPoint(lat1, lon1, brng, dist):
   """
   Given a (latitude, latitude) coordinate of an origin point, angle and distance,
   return the resulting destiantion coordinate

   Parameters
   ==========
   lat1 : Double
	  a Double number that represents latitude
   lon1 : Double
	  a Double number that represents longitude
   brng : Double
	  a Double number that represents angle in Degrees
	  eg. 0 -> North , 45 -> North-East, 90 -> East, 135 -> South-East, 180 -> South

   Notes
   =====
   In this project, this method is used for finding the bounding latitudes and longitudes from a given
   points, resulting in a square boundary box. Food Trucks that lie within these bounds are filtered
   down by using the haversine.haversine(lat1, lon1, lat2, lon2) method that uses the Haversine formula
   to find distances between two points on the globe.

   """
   dist = dist / 6371.0
   brng = toRad(brng)

   lat1 = toRad(lat1)
   lon1 = toRad(lon1)

   lat2 = math.asin(math.sin(lat1) * math.cos(dist) + math.cos(lat1) * math.sin(dist) * math.cos(brng))
   lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(dist) * math.cos(lat1), math.cos(dist) - math.sin(lat1) * math.sin(lat2))

   return (toDeg(lat2), toDeg(lon2))

def dayExpander(dayRanges):
   """
   Given a series of slash-seperated 'day ranges', returns the list of days that are part of the 'day ranges'

   Parameters
   ==========
   dayRanges : String
	       a String that represents day ranges

   Examples
   ========

   >>> from utils import dayExpander
   >>> dayExpander('Th-Mo')
   ['Th', 'Fr', 'Sa', 'Su', 'Mo']
   >>> dayExpander('Mo-We/Fr-Su')
   ['Mo', 'Tu', 'We', 'Fr', 'Sa', 'Su']
   >>> dayExpander('Mo/Fr/Su')
   ['Mo', 'Fr', 'Su']

   """
   dayIdx = {'Mo':0, 'Tu':1, 'We':2, 'Th':3, 'Fr':4, 'Sa':5, 'Su':6}
   days = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
   dayRanges = dayRanges.split('/')
   dayRanges = map(lambda x: x.split('-'), dayRanges)
   res = []
   for dayRange in dayRanges:
      if(len(dayRange) == 1):
	 res += dayRange[0]
      elif (len(dayRange) == 2):
	 if(dayIdx[dayRange[0]] <= dayIdx[dayRange[1]]):
	    res+= days[ dayIdx[dayRange[0]] : dayIdx[dayRange[1]]+1 ]
	 else:
	    res+= days[ dayIdx[dayRange[0]] : 8]
	    res+= days[ : dayIdx[dayRange[1]]+1 ]
   return list(set(res))

def timeTo24(timeVal):
   '''
   Given a time in 12-hour AM/PM format, return time in 24-hour format

   Parameters
   ==========
   timeVal : String
	     a String that denotes time in 12-hour AM/PM format
   '''
   if timeVal[-2:].lower() == 'am':
      if int(timeVal[:-2]) == 12:
	 return 0
      else:
	 return int(float(timeVal[:-2])*100)
   elif timeVal[-2:].lower() == 'pm':
      if float(timeVal[:-2]) == 12:
	 return 1200
      else:
	 return int(float(timeVal[:-2])*100 + 1200)

def timeExpander(timeRanges):
   """
   Given a string of slash-separated time-ranges, return a list datatime.time object lists

   Parameters
   ==========
   timeRanges : String
	        a String that denotes time-ranges

   Examples
   ========
   >>> import datetime
   >>> from utils import timeExpander
   >>> timeExpander("9AM-1PM/3PM-5PM/10PM-1AM")
   [ [time(9, 00), time(13, 00)], [time(15, 00), time(17, 00)], [time(22, 00), time(1, 00)] ]

   See Also
   ========
   datetime.time

   """
   timeRanges = timeRanges.split('/')
   timeRanges = map(lambda x: x.split('-'), timeRanges)
   #We have list(resTimeRanges) that holds the final 'valid' timeRanges as
   #some timeRanges in the dataset are invalid. eg '9AM-1'
   resTimeRanges = []
   for i in range(len(timeRanges)):
      try:
	 timeRanges[i][0] = timeTo24(timeRanges[i][0])
	 timeRanges[i][1] = timeTo24(timeRanges[i][1])
	 timeRanges[i][0] = datetime.time(timeRanges[i][0]/100, timeRanges[i][0]%100, 0)
	 timeRanges[i][1] = datetime.time(timeRanges[i][1]/100, timeRanges[i][1]%100, 0)
	 resTimeRanges.append(timeRanges[i])
      except:
	 pass
   return resTimeRanges

def timeInRange(start, end, x):
   """
   Return true if x is in the range [start, end]

   Parameters
   ==========
   start : datetime.time
	   datatime.time object that denotes start time
   end : datetime.time
	 datetime.time object that denotes end time
   x : datetime.time
       datetime.time object that is being checked for condition start <= x <= end

   Examples
   ========
   >>> from datetime import time
   >>> from utils import timeInRange
   >>> timeInRange(time(2, 0), time(6, 0), time(4, 0))
   True

   """
   if start <= end:
      return start <= x <= end
   else:
      return start <= x or x <= end


def filterByLatLonBounds(lat1, lat2, lon1, lon2):
   return  Truck.objects.filter(
	       lat__gt=lat1, lat__lt=lat2,
	       lon__gt=lon1, lon__lt=lon2)

def filterByRadius(trucks, latLng, radius):
   trucks2 = []
   if radius:
      for tr in trucks:
	 a = latLng
	 b = (tr.lat, tr.lon)
	 if(haversine(a,b) <= radius):
	    trucks2.append(tr)
      return trucks2
   else:
      return []

def filterByQuery(trucks, query):
   trucks2 = []
   if query:
      print 'Entered'
      query = map(lambda x: x.strip().lower(), query.split(','))
      for tr in trucks:
	 items = re.sub(r'\W+', ' ', str(tr.foodItems)).split()
	 items = map(lambda x: x.lower(), items)
	 for q in query:
	    if q in items:
	       trucks2.append(tr)
	       break
      return trucks2
   else:
      return trucks

def filterTrucks(latLng, radius, query):
   if latLng and radius:
      latLng = latLng.split(',')
      latLng[0] = float(latLng[0])
      latLng[1] = float(latLng[1])
      radius = float(radius)

      #Building a bounding box. Refer to utils.destPoint docs
      north = destPoint(latLng[0], latLng[1], 0, float(radius))
      east = destPoint(latLng[0], latLng[1], 90, float(radius))
      south = destPoint(latLng[0], latLng[1], 180, float(radius))
      west = destPoint(latLng[0], latLng[1], 270, float(radius))

      #Filtering trucks using latitude and longitude bounds
      trucks = filterByLatLonBounds(south[0], north[0], west[1], east[1])

      #Filtering trucks by radius using haversine.haversine method
      trucks = filterByRadius(trucks, (latLng[0], latLng[1]), radius)

      #Filtering trucks by query
      trucks = filterByQuery(trucks, query)
   else:
      trucks = Truck.objects.all()

   return trucks

def findOpenClosed(trucks):
   trucksList = []
   for tr in trucks:
      dayTimes = str(tr.daysHours)
      dayTimes = dayTimes.split(';')
      isOpen = "NO"
      for dT in dayTimes:
	 dT = dT.split(':')
	 days = dT[0]
	 timeRanges = dT[1]
	 days = dayExpander(days)
	 timeRanges = timeExpander(timeRanges)
	 today = datetime.datetime.now(timezone('America/Los_Angeles'))
	 now_day = today.strftime("%A")[:2]
	 now_time = today.time()
	 if now_day in days:
	    for timeRange in timeRanges:
	       if timeInRange(timeRange[0], timeRange[1], now_time):
		  isOpen = "YES"
		  break
	 if isOpen == "YES":
	    break
      d = {}
      d["data"] = TruckSerializer(tr).data
      d["meta"] = dict({"isOpen":isOpen})
      trucksList.append(d)

   return trucksList


