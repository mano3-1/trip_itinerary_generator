
import folium
import pandas as pd
from geopy.geocoders import Nominatim
from config import TRIP_LOCATION, START_POINT
from functools import partial
from utils import get_icon_and_prefix, get_distance_matrix_v2
import tsp_solver.greedy as tsp
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
loc_names = []
category = []
for i in range(len(df)):
    location = geocode(df.iloc[i, 0].strip()+ ", " + TRIP_LOCATION)
    if location is not None:
        prefix, icon = get_icon_and_prefix(df.loc[i, "category"])
        folium.Marker([location.latitude, location.longitude], popup = df.iloc[i,0].strip(), icon=folium.Icon(icon = icon, prefix=prefix)).add_to(map)
        print("Found location: ", df.iloc[i,0].strip())
        locations.append(location)
        loc_names.append(df.iloc[i,0].strip())
        category.append(df.iloc[i,1])
    else:
       # raise e
        print("Location not found: ", df.iloc[i,0].strip())



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
final_df = pd.DataFrame(columns = ["places", "category", "shortest route"])
final_df["shortest route"] = route
final_df["latitudes"] = [loc.latitude for loc in locations]
final_df["longitude"] = [loc.longitude for loc in locations]
final_df["places"] = loc_names
final_df = final_df.sort(on = "shortest route")
final_df.to_excel("edited.xlsx")
# route_long_lats = [(locations[i].latitude, locations[i].longitude) for i in route]

