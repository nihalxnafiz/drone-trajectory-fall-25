import copy
import numpy as np
from src.data_model import Camera, DatasetSpec
from src.plan_computation import compute_distance_between_images

# Camera 1: Skydio VT300L - Wide camera (already defined)
camera_x10 = Camera(
    fx=4938.56,
    fy=4936.49,
    cx=4095.5,
    cy=3071.5,
    sensor_size_x_mm=13.107,
    sensor_size_y_mm=9.830,
    image_size_x_px=8192,
    image_size_y_px=6144
)

# Camera 2: Lower resolution, larger sensor
camera2 = Camera(
    fx=3500.0,
    fy=3500.0,
    cx=2000.0,
    cy=1500.0,
    sensor_size_x_mm=20.0,
    sensor_size_y_mm=15.0,
    image_size_x_px=4000,
    image_size_y_px=3000
)

# Camera 3: Higher resolution, smaller sensor
camera3 = Camera(
    fx=6000.0,
    fy=6000.0,
    cx=3000.0,
    cy=2000.0,
    sensor_size_x_mm=10.0,
    sensor_size_y_mm=7.5,
    image_size_x_px=6000,
    image_size_y_px=4000
)

# Dataset spec 1: Nominal
dataset_spec = DatasetSpec(
    overlap=0.7,
    sidelap=0.7,
    height=100,
    scan_dimension_x=150,
    scan_dimension_y=150,
    exposure_time_ms=2
)

# Dataset spec 2: Higher overlap
dataset_spec2 = DatasetSpec(
    overlap=0.85,
    sidelap=0.85,
    height=100,
    scan_dimension_x=150,
    scan_dimension_y=150,
    exposure_time_ms=2
)

# Dataset spec 3: Lower altitude
dataset_spec3 = DatasetSpec(
    overlap=0.7,
    sidelap=0.7,
    height=50,
    scan_dimension_x=150,
    scan_dimension_y=150,
    exposure_time_ms=2
)
# Dataset spec 4: Non-nadir (30 degree tilt)
dataset_spec4 = DatasetSpec(
    overlap=0.7,
    sidelap=0.7,
    height=100,
    scan_dimension_x=150,
    scan_dimension_y=150,
    exposure_time_ms=2,
    camera_angle=30.0  # 30 degrees from nadir
)

computed_distances_4 = compute_distance_between_images(camera_x10, dataset_spec4)
print(f"Camera X10, 30 deg tilt: Computed distance: {computed_distances_4}")


# Check computed distances
for cam, spec, label in [
    (camera_x10, dataset_spec, "Camera X10, Nominal Spec"),
    (camera2, dataset_spec, "Camera 2, Nominal Spec"),
    (camera3, dataset_spec, "Camera 3, Nominal Spec"),
    (camera_x10, dataset_spec2, "Camera X10, High Overlap"),
    (camera_x10, dataset_spec3, "Camera X10, Low Altitude"),
]:
    cam_ = copy.copy(cam)
    spec_ = copy.copy(spec)
    computed_distances_ = compute_distance_between_images(cam_, spec_)
    print(f"{label}: Computed distance: {computed_distances_}")
