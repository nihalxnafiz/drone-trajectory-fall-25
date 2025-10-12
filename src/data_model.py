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
    overlap: float                # Ratio (0 to 1) of scene shared between consecutive images
    sidelap: float                # Ratio (0 to 1) of scene shared between images in adjacent rows
    height: float                 # Scan height above ground (meters)
    scan_dimension_x: float       # Horizontal size of scan area (meters)
    scan_dimension_y: float       # Vertical size of scan area (meters)
    exposure_time_ms: float
    camera_angle: float = 0.0     # Angle from nadir (in degrees), default is 0 (nadir) 

@dataclass
class Waypoint:
    latitude: float
    longitude: float
    altitude_m: float