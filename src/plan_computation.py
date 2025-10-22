import numpy as np
from src.data_model import Camera, DatasetSpec, Waypoint
from src.camera_utils import compute_image_footprint_on_surface
from typing import List

def compute_distance_between_images(
    camera: Camera, dataset_spec: DatasetSpec
) -> np.ndarray:
    import math

def compute_distance_between_images(
    camera: Camera, dataset_spec: DatasetSpec
) -> np.ndarray:
    angle_rad = math.radians(getattr(dataset_spec, "camera_angle", 0.0))
    effective_height = dataset_spec.height / math.cos(angle_rad)
    footprint = compute_image_footprint_on_surface(camera, effective_height)
    distance_x = footprint[0] * (1 - dataset_spec.overlap)
    distance_y = footprint[1] * (1 - dataset_spec.sidelap)
    return np.array([distance_x, distance_y], dtype=np.float32)

from src.camera_utils import compute_ground_sampling_distance

def compute_speed_during_photo_capture(
    camera: Camera, dataset_spec: DatasetSpec, allowed_movement_px: float = 1
) -> float:
    """
    Compute the maximum speed (in m/s) the drone can move during photo capture to restrict motion blur to <= allowed_movement_px.
    """
    gsd = compute_ground_sampling_distance(camera, dataset_spec.height)
    max_movement_m = gsd * allowed_movement_px
    exposure_time_s = dataset_spec.exposure_time_ms / 1000.0
    speed = max_movement_m / exposure_time_s
    return speed


def generate_photo_plan_on_grid(
    camera: Camera, dataset_spec: DatasetSpec
) -> List[Waypoint]:
    """Generate the complete photo plan as a list of waypoints in a lawn-mower pattern.

    Args:
        camera: Camera model used for image capture.
        dataset_spec: user specification for the dataset.

    Returns:
        Scan plan as a list of waypoints.

    """
    raise NotImplementedError()