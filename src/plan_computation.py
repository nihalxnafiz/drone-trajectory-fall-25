
import math
import copy
import numpy as np
from typing import List
from src.data_model import Camera, DatasetSpec, Waypoint
from src.camera_utils import (
    compute_image_footprint_on_surface,
    compute_ground_sampling_distance,
)

def compute_distance_between_images(
    camera: Camera, dataset_spec: DatasetSpec
) -> np.ndarray:
    angle_rad = math.radians(getattr(dataset_spec, "camera_angle", 0.0))
    effective_height = dataset_spec.height / math.cos(angle_rad)
    footprint = compute_image_footprint_on_surface(camera, effective_height)
    distance_x = footprint[0] * (1.0 - dataset_spec.overlap)
    distance_y = footprint[1] * (1.0 - dataset_spec.sidelap)
    return np.array([distance_x, distance_y], dtype=np.float32)


def compute_speed_during_photo_capture(
    camera: Camera, dataset_spec: DatasetSpec, allowed_movement_px: float = 1
) -> float:
    gsd = compute_ground_sampling_distance(camera, dataset_spec.height)
    max_movement_m = gsd * allowed_movement_px
    exposure_time_s = dataset_spec.exposure_time_ms / 1000.0
    speed = max_movement_m / exposure_time_s
    return float(speed)


def _tilted_image_footprint(camera: Camera, height_m: float, camera_angle_deg: float = 0.0):
    """
    Reproject the four image corners to the ground plane (z=0) taking into account a single-axis
    camera tilt about the local X axis (pitch = camera_angle_deg). Returns footprint_x, footprint_y
    (width, height) in meters and the reprojection center (ground point under image center).
    """
    angle_rad = math.radians(camera_angle_deg)
    # rotation about camera X axis (pitch)
    Rx = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, math.cos(angle_rad), -math.sin(angle_rad)],
            [0.0, math.sin(angle_rad), math.cos(angle_rad)],
        ],
        dtype=np.float64,
    )

    corners_uv = [
        (0.0, 0.0),
        (float(camera.image_size_x_px), 0.0),
        (float(camera.image_size_x_px), float(camera.image_size_y_px)),
        (0.0, float(camera.image_size_y_px)),
    ]

    cam_pos = np.array([0.0, 0.0, float(height_m)], dtype=np.float64)  # local frame origin at scan center
    ground_points = []
    cx, cy, fx, fy = camera.cx, camera.cy, camera.fx, camera.fy

    for (u, v) in corners_uv:
        d_cam = np.array([(u - cx) / fx, (v - cy) / fy, 1.0], dtype=np.float64)
        d_world = Rx.dot(d_cam)  # direction in world frame (assuming camera frame aligned with world axes except pitch)
        # avoid rays parallel to ground
        if abs(d_world[2]) < 1e-8:
            # fallback to nadir direction
            d_world[2] = 1e-8
        t = -cam_pos[2] / d_world[2]
        p = cam_pos + t * d_world
        ground_points.append(p)

    pts = np.array(ground_points)  # shape (4,3)
    min_x, max_x = pts[:, 0].min(), pts[:, 0].max()
    min_y, max_y = pts[:, 1].min(), pts[:, 1].max()
    footprint_x = float(max_x - min_x)
    footprint_y = float(max_y - min_y)

    # compute ground point under image center (u=cx,v=cy)
    d_cam_center = np.array([0.0, 0.0, 1.0], dtype=np.float64)
    d_world_center = Rx.dot(d_cam_center)
    t_center = -cam_pos[2] / d_world_center[2]
    center_ground = cam_pos + t_center * d_world_center

    return footprint_x, footprint_y, center_ground


def generate_photo_plan_on_grid(
    camera: Camera, dataset_spec: DatasetSpec
) -> List[Waypoint]:
    """
    Full geometric plan generation:
    - Compute nominal distances from tilted footprint (accounts for camera_angle).
    - Compute number of images per axis with ceil to guarantee coverage.
    - Evenly space images to cover scan area (centred).
    - For non-nadir (camera_angle != 0), compute simple look_at ground point for each waypoint
      by reprojecting the image center to the ground (using the same tilt model).
    - Assign capture speed to each waypoint.
    """
    # 1) compute tilted footprint at origin to get nominal spacing
    cam_angle = getattr(dataset_spec, "camera_angle", 0.0)
    footprint_x, footprint_y, _ = _tilted_image_footprint(camera, dataset_spec.height, cam_angle)

    nominal_dx = max(1e-6, footprint_x * (1.0 - dataset_spec.overlap))
    nominal_dy = max(1e-6, footprint_y * (1.0 - dataset_spec.sidelap))

    # 2) number of images needed along each axis
    n_x = max(1, math.ceil(dataset_spec.scan_dimension_x / nominal_dx))
    n_y = max(1, math.ceil(dataset_spec.scan_dimension_y / nominal_dy))

    # 3) actual spacing to evenly cover the scan area while centering grid
    spacing_x = dataset_spec.scan_dimension_x / n_x
    spacing_y = dataset_spec.scan_dimension_y / n_y

    x0 = -dataset_spec.scan_dimension_x / 2.0 + spacing_x / 2.0
    y0 = -dataset_spec.scan_dimension_y / 2.0 + spacing_y / 2.0

    waypoints: List[Waypoint] = []
    capture_speed = compute_speed_during_photo_capture(camera, dataset_spec)

    # For each grid cell, compute look_at using the same tilted reprojection model (camera at (x,y,height))
    for row in range(n_y):
        y = y0 + row * spacing_y
        cols = range(n_x) if (row % 2 == 0) else range(n_x - 1, -1, -1)
        for col in cols:
            x = x0 + col * spacing_x

            # Compute look_at ground point by reprojecting center pixel with camera at (x,y,height)
            angle_rad = math.radians(cam_angle)
            Rx = np.array(
                [
                    [1.0, 0.0, 0.0],
                    [0.0, math.cos(angle_rad), -math.sin(angle_rad)],
                    [0.0, math.sin(angle_rad), math.cos(angle_rad)],
                ],
                dtype=np.float64,
            )

            # direction for image center in camera frame
            d_cam_center = np.array([0.0, 0.0, 1.0], dtype=np.float64)
            d_world_center = Rx.dot(d_cam_center)
            cam_pos = np.array([x, y, float(dataset_spec.height)], dtype=np.float64)
            if abs(d_world_center[2]) < 1e-8:
                d_world_center[2] = 1e-8
            t_center = -cam_pos[2] / d_world_center[2]
            look_at_pt = cam_pos + t_center * d_world_center  # [x,y,0] on ground

            yaw_deg = float(math.degrees(math.atan2(look_at_pt[1] - y, look_at_pt[0] - x)))
            wp = Waypoint(
                x_m=float(x),
                y_m=float(y),
                z_m=float(dataset_spec.height),
                speed_m_s=float(capture_speed),
                yaw_deg=yaw_deg,
                look_at_x_m=float(look_at_pt[0]),
                look_at_y_m=float(look_at_pt[1]),
                look_at_z_m=0.0,
            )
            waypoints.append(wp)

    return waypoints
