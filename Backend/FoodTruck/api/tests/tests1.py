from django.test import TestCase

from api.models import Truck
from api.utils import findOpenClosed, filterTrucks
from api.utils import toRad, toDeg, destPoint, dayExpander
from api.utils import timeTo24, timeExpander, timeInRange
from datetime import time
import json
import math

class TruckTest(TestCase):

   def create_truck(self, applicant, facilityType, address, permit, foodItems,
	 lat, lon, daysHours, status):
      return Truck.objects.create(applicant=applicant, facilityType=facilityType,
	    address=address, permit=permit, foodItems=foodItems, lat=lat, lon=lon,
	    daysHours=daysHours, status=status)

   def create_trucks(self):
      trucks = []
      f = open('test_data.json')
      data = json.loads(f.read())
      for row in data:
	 truck = self.create_truck(row[9], row[10], row[11], row[12], row[13],
	       row[14], row[15], row[16], row[17])
	 trucks.append(truck)
      return trucks

   def findTrucks(self, latLng, radius, query):
      trucks = filterTrucks(latLng, radius, query)
      #Cannot hard-code "isOpen" field as it is time-dependent, hence dynamic
      trucksList = findOpenClosed(trucks)
      return trucksList

   def test_truck_creation(self):
      trucks = self.create_trucks()
      for truck in trucks:
	 self.assertTrue(isinstance(truck, Truck))

   def test_truck_list_view(self):
      trucks = self.create_trucks()

      trucksList = self.findTrucks(latLng=None, radius=None, query=None)
      response = self.client.get('/api/v1/trucks/')
      self.assertEqual(response.status_code, 200)
      self.assertEqual(response.data, trucksList)

      trucksList = self.findTrucks(latLng="37.77543786515106,-122.41800360381603", radius="2.5", query="hot,dogs")
      response = self.client.get('/api/v1/trucks/?latLng=37.77543786515106,-122.41800360381603&rad=2.5&q=hot,dogs')
      self.assertEqual(response.status_code, 200)
      self.assertEqual(response.data, trucksList)

      trucksList = self.findTrucks(latLng="37.77543786515106,-122.41800360381603", radius="1", query="hot,dogs")
      response = self.client.get('/api/v1/trucks/?latLng=37.77543786515106,-122.41800360381603&rad=1&q=hot,dogs')
      self.assertEqual(response.status_code, 200)
      self.assertEqual(response.data, trucksList)

      trucksList = self.findTrucks(latLng="37.77543786515106,-122.41800360381603", radius="2.5", query="chips")
      response = self.client.get('/api/v1/trucks/?latLng=37.77543786515106,-122.41800360381603&rad=2.5&q=chips')
      self.assertEqual(response.status_code, 200)
      self.assertEqual(response.data, trucksList)

   def test_utility_functions(self):

      assert toRad(180) == math.pi
      assert toDeg(math.pi) == 180
      assert destPoint(37.77543786515106, -122.41800360381603, 90, 1.5) == \
		  (37.77543663443524, -122.40093690077843)
      assert sorted(dayExpander('Mo-We/Fr-Su')) == ['Fr', 'Mo', 'Sa', 'Su', 'Tu', 'We']
      assert timeTo24("12AM") == 0
      assert timeTo24("12PM") == 1200
      assert timeTo24("3AM") == 300
      assert timeTo24("3PM") == 1500
      assert timeExpander("9AM-1PM/3PM-5PM/10PM-1AM") == \
	 [ [time(9, 00), time(13, 00)], [time(15, 00), time(17, 00)], [time(22, 00), time(1, 00)] ]
      assert timeInRange(time(2, 0), time(6, 0), time(4, 0)) == True
      assert timeInRange(time(20, 0), time(2, 0), time(23, 0)) == True






