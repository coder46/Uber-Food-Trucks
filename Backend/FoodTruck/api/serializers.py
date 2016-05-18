from rest_framework import serializers
from api.models import Truck

class TruckSerializer(serializers.ModelSerializer):
   class Meta:
      model = Truck
      fields = ('id', 'applicant', 'facilityType', 'address', 'permit', 'foodItems'
	    , 'lat', 'lon', 'daysHours', 'status')
