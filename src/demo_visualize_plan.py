import copy
from src.data_model import Camera, DatasetSpec
from src.plan_computation import generate_photo_plan_on_grid, compute_distance_between_images
from src.visualization import plot_photo_plan

camera_x10 = Camera(
    fx=4938.56, fy=4936.49, cx=4095.5, cy=3071.5,
    sensor_size_x_mm=13.107, sensor_size_y_mm=9.830,
    image_size_x_px=8192, image_size_y_px=6144
)

base_spec = DatasetSpec(
    overlap=0.7, sidelap=0.7, height=100.0,
    scan_dimension_x=150.0, scan_dimension_y=150.0,
    exposure_time_ms=2, camera_angle=0.0
)

def run_and_show(spec, title=None):
    plan = generate_photo_plan_on_grid(camera_x10, spec)
    distances = compute_distance_between_images(camera_x10, spec)
    print(f"{title or 'Spec'} -> waypoints: {len(plan)}, distances (x,y): {distances}")
    fig = plot_photo_plan(plan, title=title)
    fig.show()

# Experiment 1: change overlap (affects consecutive images distance)
spec1 = copy.deepcopy(base_spec)
spec1.overlap = 0.5
run_and_show(spec1, title="Overlap 0.5 (lower)")

spec1b = copy.deepcopy(base_spec)
spec1b.overlap = 0.85
run_and_show(spec1b, title="Overlap 0.85 (higher)")

# Experiment 2: change sidelap (should affect cross-row spacing only)
spec2 = copy.deepcopy(base_spec)
spec2.sidelap = 0.5
run_and_show(spec2, title="Sidelap 0.5")

# Experiment 3: change height (affects footprint and spacing)
spec3 = copy.deepcopy(base_spec)
spec3.height = 50.0
run_and_show(spec3, title="Height 50m (lower)")

spec3b = copy.deepcopy(base_spec)
spec3b.height = 200.0
run_and_show(spec3b, title="Height 200m (higher)")

# Experiment 4: change exposure time (does not affect plan layout but affects allowed speed)
spec4 = copy.deepcopy(base_spec)
spec4.exposure_time_ms = 1000
plan4 = generate_photo_plan_on_grid(camera_x10, spec4)
print("Exposure time changed to 1000ms -> plan len:", len(plan4))
fig4 = plot_photo_plan(plan4, title="Exposure time 1000ms")
fig4.show()