import copy
import numpy as np
from src.data_model import Camera, DatasetSpec
from src.plan_computation import compute_speed_during_photo_capture

# Camera definitions
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

# Dataset specifications
dataset_spec = DatasetSpec(
    overlap=0.7,
    sidelap=0.7,
    height=100,
    scan_dimension_x=150,
    scan_dimension_y=150,
    exposure_time_ms=2
)

dataset_spec2 = DatasetSpec(
    overlap=0.85,
    sidelap=0.85,
    height=100,
    scan_dimension_x=150,
    scan_dimension_y=150,
    exposure_time_ms=2
)

dataset_spec3 = DatasetSpec(
    overlap=0.7,
    sidelap=0.7,
    height=50,
    scan_dimension_x=150,
    scan_dimension_y=150,
    exposure_time_ms=2
)
# ...existing code...
# add these lines before the assert
# ...existing code...

# compute speed and then print debug info
computed_speed = compute_speed_during_photo_capture(camera_x10, dataset_spec, allowed_movement_px=1)
expected_speed = 3.09

from src.camera_utils import compute_ground_sampling_distance
gsd = compute_ground_sampling_distance(camera_x10, dataset_spec.height)
max_movement_m = gsd * 1  # allowed_movement_px=1
exposure_time_s = dataset_spec.exposure_time_ms / 1000.0

print(f"GSD (m/px): {gsd}")
print(f"Max movement (m): {max_movement_m}")
print(f"Exposure time (s): {exposure_time_s}")
print(f"Computed speed: {computed_speed}")
print(f"Expected speed: {expected_speed}")

print(f"Computed speed during photo captures: {computed_speed:.2f}")
assert np.allclose(computed_speed, expected_speed, atol=1e-2)

# Try with other camera/dataset specs
for cam, spec, label in [
    (camera2, dataset_spec, "Camera 2, Nominal Spec"),
    (camera3, dataset_spec, "Camera 3, Nominal Spec"),
    (camera_x10, dataset_spec2, "Camera X10, High Overlap"),
    (camera_x10, dataset_spec3, "Camera X10, Low Altitude"),
]:
    cam_ = copy.copy(cam)
    spec_ = copy.copy(spec)
    computed_speed_ = compute_speed_during_photo_capture(cam_, spec_)
    print(f"{label}: Computed speed: {computed_speed_:.2f}")
# ...existing code...