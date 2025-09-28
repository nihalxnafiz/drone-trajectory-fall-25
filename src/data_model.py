"""Data models for the camera and user specification."""

from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Camera:
    fx: float  # focal length in x (pixels)
    fy: float  # focal length in y (pixels)
    cx: float  # principal point x (pixels)
    cy: float  # principal point y (pixels)
    sensor_size_x_mm: float  # sensor width in mm
    sensor_size_y_mm: float  # sensor height in mm
    image_size_x_px: int     # image width in pixels
    image_size_y_px: int     # image height in pixels

@dataclass
class DatasetSpec:
    area_corners: List[Tuple[float, float]]  # List of (lat, lon) tuples
    flight_height_m: float
    front_overlap: float
    side_overlap: float
    camera: Camera

@dataclass
class Waypoint:
    latitude: float
    longitude: float
    altitude_m: float