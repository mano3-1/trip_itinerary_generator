import geopy
import folium
import pandas as pd
from geopy.geocoders import Nominatim
from config import TRIP_LOCATION, START_POINT, TOKEN, RADIUS
from functools import partial
from utils import get_icon_and_prefix, get_distance_matrix_v2, Location
import tsp_solver.greedy as tsp
import openrouteservice as ors
import numpy as np

df = pd.read_excel("locations.xlsx")
locations = []
geolocator=Nominatim(user_agent="Goa_trip")
geocode = partial(geolocator.geocode, language="es")
location = geolocator.geocode(TRIP_LOCATION)
map=folium.Map(location=[location.latitude, location.longitude])

#adding start point
locations.append(geocode(START_POINT))
folium.Marker([locations[0].latitude, locations[0].longitude], popup = "Start", icon=folium.Icon(icon = "fa-play", prefix="fa")).add_to(map)


print("#"*25)
print("adding indicators...")
print("#"*25)
for i in range(len(df)):
    if np.isnan(df.loc[i, "lat"]):
        location = geocode(df.loc[i, "places"].strip()+ ", " + TRIP_LOCATION)
        if location is not None:
            print("Location found: ", df.iloc[i,0].strip())
            prefix, icon = get_icon_and_prefix(df.loc[i, "category"])
            folium.Marker([location.latitude, location.longitude] , popup = df.loc[i,"places"].strip(), icon=folium.Icon(icon = icon, prefix=prefix)).add_to(map)
            locations.append(location)
            df.loc[i, "lat"] = location.latitude
            df.loc[i, "lon"] = location.longitude
        else:
            print("Location not found: ", df.iloc[i,0].strip())
    else:
        prefix, icon = get_icon_and_prefix(df.loc[i, "category"])
        locations.append(Location(latitude=df.loc[i,"lat"], longitude=df.loc[i, "lon"]))
        folium.Marker([df.loc[i,"lat"], df.loc[i, "lon"]] , popup = df.loc[i,"places"].strip(), icon=folium.Icon(icon = icon, prefix=prefix)).add_to(map)
        print(f"Latitude and longitude of location {df.iloc[i,0].strip()} is taken from excel file...")
df.to_excel("locations.xlsx", index=False)

print("#"*25)
print("figuring out shortest route....")
print("#"*25)
#calculate distances
distance_matrix = get_distance_matrix_v2([(loc.latitude, loc.longitude) for loc in locations])
#heavy value for starting point
for i in range(len(locations)):
    if i != 0:
        distance_matrix[0][i] = 999999999 # A very high value

route = tsp.solve_tsp(distance_matrix)

print("#"*25)
print("plotting and saving the map..")
print("#"*25)
route_long_lats = [(locations[i].latitude, locations[i].longitude) for i in route]


#drawing routes
client = ors.Client(key=TOKEN) # Replace with your OpenRouteService API key

for i in range(len(route_long_lats) - 1):

    # Get the latitude and longitude coordinates for the start and end route_long_lats
    start_lat, start_lon = route_long_lats[i]
    end_lat, end_lon = route_long_lats[i+1]

    # Call the ORS directions() function to retrieve the driving directions between the locations
    r = 350
    while True:
        try:    
            _ = client.directions(
                coordinates=[[start_lon, start_lat], [end_lon, end_lat]],
                profile='driving-car',
                format='geojson',
                radiuses = [r, r]
            )
            break
        except:
            r+=100

    # Extract the GeoJSON LineString from the route
    line_coords = _['features'][0]['geometry']['coordinates']
    line_coords = [(lat, lng) for lng,lat in line_coords]
    # Create a Folium PolyLine from the coordinates
    line = folium.PolyLine(locations=line_coords, weight=5, opacity=1, color='blue').add_to(map)

map.save('index.html')