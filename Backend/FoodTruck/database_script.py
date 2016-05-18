import os, django, json

if __name__ == "__main__":
   os.environ["DJANGO_SETTINGS_MODULE"] = "FoodTruck.settings"
   django.setup()

   from api.models import Truck
   from api.serializers import TruckSerializer

   fo = open('data.json')
   data = json.loads(fo.read())
   cnt = 0
   for row in data['data']:
      if None not in row[8:]:
	 cnt += 1
	 print cnt
	 print row
	 truck = Truck(applicant=row[9], facilityType=row[10], address=row[11],
	    permit=row[12], foodItems=row[13], lat=float(row[14]), lon=float(row[15]),
	    daysHours=row[16],  status=row[17])
	 truck.save()
   fo.close()

