# Overview

This application's main purpose is displaying fatal car accidents that happened in Texas in 2017. Features of the application are:
- Search accidents by proximity to point chosen on map
- Show accidents that happened on chosen road
- Show accidents that occured in chosen county
- Show accidents heatmap for the chosen county

Application screenshots:

![Screenshot](screenshot.png)

The application consists of following parts:
- frontend web application client written in vue.js
- backend application written in python
- spatial database (postgreSQL with postgis extension)

# Frontend
The frontend application is a single page web applciation and was written in Vue.js. It's main intent is to display car accidents on roads and near them, so I modified visibility of roads in the map style and changed their color. To work with map I used [vue2leaflet](https://www.npmjs.com/package/@lulibrary/vue2-leaflet) library, which provides leaflet map components for Vue.js. Additionaly I use [Bootstrap-Vue](https://bootstrap-vue.js.org/) library for vue-friendly bootstrap components and [vue2-leaflet-heatmap](https://www.npmjs.com/package/vue2-leaflet-heatmap) library to display heatmaps.

All relevant code is in folder *fe*/. Responsibilities of frontend code are:
- side control panel allowing user to choose search distance and perform actions
- displaying geo features (accidents, counties, roads) by overlaying the map with a geojson layer. The geojson is provided directly by backend APIs.


# Backend

The backend application is written in Python, using [flask](http://flask.pocoo.org) microframework to provide REST api. Communication with the database is provided by [psycopg2](http://initd.org/psycopg/docs/) database adapter.
It is responsible for querying geo data and responds with GeoJSON format. GeoJSON is built directly in queries using *json_build_object* to build the json itself and add properties and ST_AsGeoJSON to retrieve geo-information from geometry.


## Data

Data of accidents were retrieved from Fatality Analysis Reporting System ([FARS](https://www.nhtsa.gov/research-data/fatality-analysis-reporting-system-fars)). These data were available in .csv format. In order to import these data into the database I first created table containing same columns as said .csv file and then [copied](http://www.postgresqltutorial.com/import-csv-file-into-posgresql-table/) them into the database. I created an indexes on geometry and geography in order to speed up the queries execution. 
Other data (roads, counties, texas itself) were retrieved from OSM, specifically by downloading .osm.pbf file of Texas from [here](https://download.geofabrik.de/north-america.html). I imported these data into the database using osm2pgsql and created indexes where it was needed to speed up the execution. 


## Api

**Find accidents in proximity to coordinates**

`GET /accidentsProximity?lat=32.78960155122409&lng=-96.81293964385986&distance=1000`

**Find accidents that happened near chosen road (road closest to coordinates)**

`GET /accidentsOnRoad?lat=32.78960155122409&lng=-96.81293964385986&distance=1000`

**Gets all counties**

`GET /allCounties`

**Searches all accidents in clicked county**

`GET /accidentsInCounty?county_id=-18473546`

**Generates points of heatmap for chosen county**

`GET /heatmapInCounty?county_id=-18473546`


### Response

API calls return json responses made of single or multiple geojsons. GeoJSONs follow the format and additional information (f.e. number of accidents in the county) are sent in the properties part of the geojson. 
