from django.conf.urls import url
from api import views

urlpatterns = [
   url(r'^v1/trucks/$', views.truck_list),
]
