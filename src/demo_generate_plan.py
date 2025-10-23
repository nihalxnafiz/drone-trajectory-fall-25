import pprint
from src.data_model import Camera, DatasetSpec
from src.plan_computation import generate_photo_plan_on_grid

camera_x10 = Camera(
    fx=4938.56, fy=4936.49, cx=4095.5, cy=3071.5,
    sensor_size_x_mm=13.107, sensor_size_y_mm=9.830,
    image_size_x_px=8192, image_size_y_px=6144
)

dataset_spec = DatasetSpec(
    overlap=0.7, sidelap=0.7, height=100.0,
    scan_dimension_x=150.0, scan_dimension_y=150.0,
    exposure_time_ms=2, camera_angle=0.0
)

plan = generate_photo_plan_on_grid(camera_x10, dataset_spec)
print(f"Computed plan with {len(plan)} waypoints")
for i, wp in enumerate(plan[:20]):
    print(f"Idx {i}: {wp}")
if len(plan) > 20:
    print("...")