def get_icon_and_prefix(category):
    from config import icons
    if category.lower() in icons.keys():
        return icons[category.lower()][0], icons[category.lower()][1]
  
    return "info-sign", "glyphicon"


class Location:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

def get_distance_matrix_v2(locations):
    from config import DEG_TO_RAD, EARTH_RADIUS
    import math
    matrix = []
    for i in range(len(locations)):
        row = []
        for j in range(len(locations)):
            if i == j:
                row.append(0.0)
            else:
                lat1, lon1 = locations[i]
                lat2, lon2 = locations[j]
                d_lat = (lat2 - lat1) * DEG_TO_RAD
                d_lon = (lon2 - lon1) * DEG_TO_RAD
                a = math.sin(d_lat / 2) ** 2 + math.cos(lat1 * DEG_TO_RAD) * math.cos(lat2 * DEG_TO_RAD) * math.sin(d_lon / 2) ** 2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                distance = EARTH_RADIUS * c
                row.append(distance)
        matrix.append(row)
    return matrix

def get_distance_matrix_v1(locations):
    matrix = []
    for i in range(len(locations)):     
        row = []
        for j in range(len(locations)):
            if i == j:
                row.append(0.0)
            else:
                lat1, lon1 = locations[i].latitude, locations[i].longitude
                lat2, lon2 = locations[j].latitude, locations[j].longitude
                distance = ((lat1 - lat2)**2 + (lon1 - lon2)**2)**0.5
                row.append(distance)
        matrix.append(row)
    return matrix
