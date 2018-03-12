# The Weather Sensor App
This application is a showcase of some developing skills, inspired by Semios product. It has a tool to register and follow some weather information based on the latitude and longitude. The application is completely developed and hosted on Amazon AWS services.

The demo is available [here](http://weather-client.s3-website-us-west-2.amazonaws.com/#/).

## API
The API folder contains the serverless files that form the public API for the application. Written in JavaScript based on a NodeJS application

## Client
This folder contains a client Website to visualize sensor's data and add new ones. It is written in Vue.js and uses Google Maps API to print the map showing the sensor's location.

## Utils
This folder contains the backend python scripts that run based on events to make the sensor's data always updated.