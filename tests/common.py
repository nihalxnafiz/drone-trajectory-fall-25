from src.data_model import Camera

fx = 700
fy = 700
cx = 500
cy = 500
sensor_size_x_mm = 10
sensor_size_y_mm = 10
image_size_x_px = 1000
image_size_y_px = 1000

TEST_CAMERA = Camera(
    fx,
    fy,
    cx,
    cy,
    sensor_size_x_mm,
    sensor_size_y_mm,
    image_size_x_px,
    image_size_y_px
)
