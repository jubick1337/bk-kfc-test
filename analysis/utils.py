from dataclasses import dataclass
from math import radians, cos, sin, asin, sqrt


@dataclass
class Point:
    lon: float
    lat: float

    def __hash__(self):
        return hash(hash(self.lon) + hash(self.lat))


@dataclass
class Store:
    id: int
    location: Point

    def __hash__(self):
        return hash(self.id) + hash(self.location)


def distance(p1: Point, p2: Point):
    lon_1 = radians(p1.lon)
    lon_2 = radians(p2.lon)
    lat_1 = radians(p1.lat)
    lat_2 = radians(p2.lat)

    lon_diff = lon_2 - lon_1
    lat_diff = lat_2 - lat_1

    alpha = sin(lat_diff / 2) ** 2 + cos(lat_1) * cos(lat_2) * sin(lon_diff / 2) ** 2
    c = 2 * asin(sqrt(alpha))
    radius = 6371

    return c * radius * 1000


