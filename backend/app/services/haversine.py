import math
from typing import Tuple

class HaversineGeoProvider:
    @staticmethod
    def calculate_distance_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate the great circle distance in meters between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a)) 
        r = 6371000 # Radius of earth in meters
        return c * r

    @staticmethod
    def filter_within_radius(lat: float, lon: float, candidates: list, radius_meters: float = 500) -> list:
        nearby = []
        for candidate in candidates:
            dist = HaversineGeoProvider.calculate_distance_meters(lat, lon, candidate.latitude, candidate.longitude)
            if dist <= radius_meters:
                nearby.append((candidate, dist))
        return nearby
