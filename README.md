# Uber-Food-Trucks


<img src="https://cloud.githubusercontent.com/assets/2352723/15359014/54a71a0e-1d18-11e6-8551-85233bc86e97.png" width="150">
<img src="https://cloud.githubusercontent.com/assets/2352723/15359159/2107c896-1d19-11e6-89d8-7ca1097fd750.png" width="150">

A full stack solution for finding food trucks in San Francisco (Food trucks that have been 'Approved' are listed)

## DEMO
Demo video : https://youtu.be/hw406JX4wPI (Duration: 1 min)

[![gif demo](https://j.gifs.com/31pMyR.gif)](https://www.youtube.com/upload)

## Features
- Given a range from origin (Latitude, Longitude), shows all food trucks that lie within the radius
- Search for food trucks that cater specific food types
	- Search is OR based, thus if a food truck sells any of the food items mentioned in the query, then it will be listed in results
- Map markers indicate whether the food truck is currently open (Green marker) or closed (Red Marker) in San Francisco based on local san francisco time

## Architecture/Technical Choices

- Front-End : Android
	- Experience : 2 years of building Android applications at Hackathons, University projects and Hobby projects
- Back-End : Django Rest Framework
	- Experience : Used DRF for building APIs at an internship in Summer 2015. 3 years of general python experience spanning Open source contributions, Hackathons, University projects and Hobby projects/scripts
- Testing : Back-end API tested using django.test library and coverage package (http://coverage.readthedocs.io/en/latest/) 
- Hosting : Digital Ocean droplet running nginx
- Database : SQLite
	- Chose over MySQL/PostgreSQL as project is mostly read-heavy
- Notable Libraries used:
	- Used Rerofit (http://square.github.io/retrofit/) for consuming the REST API in Android.(Understanding Retrofit was fun!) Retrofit features that improved performance and general UX of the app include:
		- Multi threading. 
		- Ability to cancel ongoing network calls
		- JSON parsing done using GSON

## Architectural Tradeoffs
- Database choice
	- SQLite performace would decrease if write-intensive features are added to the app. Such as ability for Truck owners to change working hours, food items, location, etc. This brings down general app performance and UX, and increases concurrency issues
	- In the above case, we would have to migrate to DBs such as MySQL/PostgreSQL
- Hosting Service
	- Scalability will be an issue, as services such as load-balancing are not offered on Digital Ocean and will have to be setup manually, unlike AWS 

## API Endpoint & API Docs
http://139.59.168.223:8000/api/v1/trucks/?latLng=37.77543786515106,-122.41800360381603&rad=2.5&q=hot,dogs

## Code Written
#### Backend
- FoodTruck/api/models.py
- FoodTruck/api/serializers.py
- FoodTruck/api/views.py
- FoodTruck/api/utils.py
- FoodTruck/api/urls.py
- FoodTruck/database_script.py

#### API tests
- FoodTruck/api/tests/test1.py

#### Android
- app/src/main/java.com.example.faisal.fd5.MapsActivity.java
- app/src/main/java.com.example.faisal.interfaces.RestApi.java
- app/src/main/java.com.example.faisal.models.MetaData.java
- app/src/main/java.com.example.faisal.models.ResponseData.java
- app/src/main/java.com.example.faisal.models.TruckData.java
- app/src/main/java.com.example.faisal.models.TruckItem.java
- app/src/main/res.layout.activity_maps.xml

## Setting Up Project Locally
#### Backend
> cd FoodTrucks

> source env/bin/activate

> python manage.py runserver 0.0.0.0:8000

#### API Tests
> cd FoodTrucks

> source env/bin/activate

> coverage run manage.py test api/tests -v 2

#### Android
You can install the app using the .apk file from root directory or can run from source
(Please note that the app does not have a splash screen. Thus you will see a white background when the app initially loads)

## Resume
- Resume (https://www.dropbox.com/s/bmzecmdtjgeffta/Resume_Faisal.pdf?dl=0)
- LinkedIn (https://in.linkedin.com/in/faisalanees)

## Other Code Contributions
- Egyptian Fractions module [Sympy]
	- https://github.com/sympy/sympy/blob/master/sympy/ntheory/egyptian_fraction.py








