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
- Map markers indicate whether the food truck is currently open (Green marker) or closed (Red Marker) in San Francisco based on local san francisco time

## Architecture/Technical Choices
(I would like to mention that I had chosen Android as my preferred front end for this project, as I believe I have relatively more experience and am more comfortable in building native mobile applications. I also wanted to give my best attempt at displaying my skillset and thus the decision)

- Front-End : Android
	- Experience : 2 years of building Android applications at Hackathons, University projects and Hobby projects
- Back-End : Django Rest Framework
	- Experience : Used DRF for building APIs at an internship in Summer 2015. 3 years of general python experience spanning Open source contributions, Hackathons, University projects and Hobby projects/scripts
- Testing : Back-end API tested using django.test library and coverage package (http://coverage.readthedocs.io/en/latest/) 
- Hosting : Digital Ocean droplet running nginx
- Database : SQLite
	- Chose over MySQL/PostgreSQL as project is mostly read-heavy
- Notable Libraries used:
	- Used Rerofit (http://square.github.io/retrofit/) for consuming the REST API in Android. Retrofit feautures that improved performance and general UX of the app include:
		- Multi threading. 
		- Ability to cancel ongoing network calls
		- JSON parsing done using GSON

## Architectural Tradeoffs
- Database choice
	- SQLite performace would decrease if write-intensive features are add to the app. Such as ability for Truck owners to change working hours, food items, location, etc. This brings down general app performance and UX, and increases concurrency issues
	- In the above case, we would have to migrate to DBs such as MySQL/PostgreSQL
- Hosting Service
	- Scalability will be an issue, as services such as load-balancing are not offered on Digital Ocean and will have to be setup manually, unlike AWS 

## API Endpoint & API Docs
http://46.101.87.96:8000/api/v1/trucks/?latLng=37.77543786515106,-122.41800360381603&rad=2.5&q=hot,dogs

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
- java.com.example.faisal.fd5.MapsActivity.java
- java.com.example.faisal.interfaces.RestApi
- java.com.example.faisal.models.MetaData
- java.com.example.faisal.models.ResponseData
- java.com.example.faisal.models.TruckData
- java.com.example.faisal.models.TruckItem
- res.layout.activity_maps.xml






