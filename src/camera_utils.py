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
    X, Y, Z = world_point
    x = camera.fx * (X / Z)
    y = camera.fy * (Y / Z)
    u = x + camera.cx
    v = y + camera.cy
    return np.array([u, v], dtype=np.float32)


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
    # Reproject image corners (0,0) and (image_size_x_px, image_size_y_px) at Z = distance_from_surface
    X0 = (0 - camera.cx) * distance_from_surface / camera.fx
    Y0 = (0 - camera.cy) * distance_from_surface / camera.fy

    X1 = (camera.image_size_x_px - camera.cx) * distance_from_surface / camera.fx
    Y1 = (camera.image_size_y_px - camera.cy) * distance_from_surface / camera.fy

    footprint_x = abs(X1 - X0)
    footprint_y = abs(Y1 - Y0)

    return np.array([footprint_x, footprint_y], dtype=np.float32)


def compute_ground_sampling_distance(
    camera: Camera, distance_from_surface: float
) -> float:
    """Compute the ground sampling distance (GSD) at a given distance from the surface.

    Args:
        camera: the camera model.
        distance_from_surface: distance from the surface (in m).

    Returns:
        The GSD in meters (smaller among x and y directions).
    """
    footprint = compute_image_footprint_on_surface(camera, distance_from_surface)
    gsd_x = footprint[0] / camera.image_size_x_px
    gsd_y = footprint[1] / camera.image_size_y_px
    return min(gsd_x, gsd_y)

def reproject_image_point_to_world(camera: Camera, image_point: np.ndarray, depth: float) -> np.ndarray:
    """
    Reproject a 2D image point (u, v) to a 3D world point (X, Y, Z) given the depth (Z).

    Args:
        camera: Camera object with intrinsic parameters.
        image_point: np.ndarray of shape (2,) representing (u, v).
        depth: float, the Z value (distance from camera).

    Returns:
        np.ndarray of shape (3,) representing (X, Y, Z).
    """
    u, v = image_point
    X = (u - camera.cx) * depth / camera.fx
    Y = (v - camera.cy) * depth / camera.fy
    Z = depth
    return np.array([X, Y, Z], dtype=np.float32)