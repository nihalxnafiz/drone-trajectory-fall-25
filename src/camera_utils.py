"""Utility functions for the camera model.
"""

import numpy as np

from src.data_model import Camera


def compute_focal_length_in_mm(camera: Camera) -> np.ndarray:
    """Computes the focal length in mm for the given camera

    Args:
        camera: the camera model.

    Returns:
        [fx, fy] in mm as a 2-element array.
    """
    # pixel_to_mm_x = camera.sensor_size_x_mm / camera.image_size_x_px
    # pixel_to_mm_y = camera.sensor_size_y_mm / camera.image_size_y_px

    # return np.array([camera.fx * pixel_to_mm_x, camera.fy * pixel_to_mm_y])


def project_world_point_to_image(camera: Camera, world_point: np.ndarray) -> np.ndarray:
    """Project a 3D world point into the image coordinates.

    Args:
        camera: the camera model
        world_point: the 3D world point

    Returns:
        [u, v] pixel coordinates corresponding to the 3D world point.
    """
    raise NotImplementedError()


def compute_image_footprint_on_surface(
    camera: Camera, distance_from_surface: float
) -> np.ndarray:
    """Compute the footprint of the image captured by the camera at a given distance from the surface.

    Args:
        camera: the camera model.
        distance_from_surface: distance from the surface (in m).

    Returns:
        [footprint_x, footprint_y] in meters as a 2-element array.
    """
    raise NotImplementedError()


def compute_ground_sampling_distance(
    camera: Camera, distance_from_surface: float
) -> float:
    """Compute the ground sampling distance (GSD) at a given distance from the surface.

    Args:
        camera: the camera model.
        distance_from_surface: distance from the surface (in m).

    Returns:
        The GSD in meters (smaller among x and y directions). You should return a float and not a numpy data type.
    """
    raise NotImplementedError()
