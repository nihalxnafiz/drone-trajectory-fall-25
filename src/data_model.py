"""Data models for the camera and user specification."""


from dataclasses import dataclass
from typing import List, Tuple, Optional

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
    """
    Waypoint for the flight plan.

    x_m, y_m: planar coordinates in meters (local frame, origin = scan center)
    z_m: altitude above ground in meters
    speed_m_s: desired speed while capturing at this waypoint (m/s)
    yaw_deg: optional yaw for the drone in degrees
    look_at_x_m, look_at_y_m, look_at_z_m: optional point the camera should look at (useful for non-nadir)
    """
    x_m: float
    y_m: float
    z_m: float
    speed_m_s: float = 0.0
    yaw_deg: float = 0.0
    look_at_x_m: Optional[float] = None
    look_at_y_m: Optional[float] = None
    look_at_z_m: Optional[float] = None
