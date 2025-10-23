import numpy as np
from src.data_model import Camera
from src.camera_utils import project_world_point_to_image, reproject_image_point_to_world

# Define camera parameters for Skydio VT300L - Wide camera
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

# Original 3D point
point_3d = np.array([25, -30, 50], dtype=np.float32)

# Project to image
uv = project_world_point_to_image(camera_x10, point_3d)

# Reproject back to 3D
reprojected_3d = reproject_image_point_to_world(camera_x10, uv, point_3d[2])

print("Original 3D:", point_3d)
print("Image point:", uv)
print("Reprojected 3D:", reprojected_3d)

# Check if the reprojection matches the original
assert np.allclose(point_3d, reprojected_3d, atol=1e-4)