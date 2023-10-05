import math
import numpy as np


def calculate_bearing(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Calculate bearing
    y = math.sin(lon2 - lon1) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(lon2 - lon1)
    theta = math.atan2(y, x)
    bearing = (theta * 180 / math.pi + 360) % 360  # in degrees
    return round(0 if np.isnan(bearing) else bearing, 2)


def calculate_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in meters
    R = 6371e3

    # Convert latitude and longitude from degrees to radians
    latOrig = math.radians(lat1)
    latDest = math.radians(lat2)
    destLatMinOrigLat = math.radians(lat2 - lat1)
    destLonMinOrigLon = math.radians(lon2 - lon1)

    # Haversine formula
    a = math.sin(destLatMinOrigLat/2) * math.sin(destLatMinOrigLat/2) + \
        math.cos(latOrig) * math.cos(latDest) * \
        math.sin(destLonMinOrigLon/2) * math.sin(destLonMinOrigLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    # Calculate the distance in meters
    d = R * c

    return 50000 if np.isnan(d) else d


def calculate_new_point(lat1, lon1, lat2, lon2, f, delta):
    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Calculate a and b
    a = math.sin((1 - f) * delta) / math.sin(delta)
    b = math.sin(f * delta) / math.sin(delta)

    # Calculate x, y, and z
    x = a * math.cos(lat1) * math.cos(lon1) + b * math.cos(lat2) * math.cos(lon2)
    y = a * math.cos(lat1) * math.sin(lon1) + b * math.cos(lat2) * math.sin(lon2)
    z = a * math.sin(lat1) + b * math.sin(lat2)

    # Calculate the new latitude and longitude
    phi_i = math.atan2(z, math.sqrt(x**2 + y**2))
    lambda_i = math.atan2(y, x)

    # Convert back to degrees
    phi_i = math.degrees(phi_i)
    lambda_i = math.degrees(lambda_i)

    return phi_i, lambda_i
