import cv2
import numpy as np
import openCV
from utils import frame_height, frame_width, start_button_pos, reset_button_pos, button_width, button_height, ConstVelocity, LookAHead_dist, Wheels_dist
from pure_pursuit import calculate_omega, calculate_wheel_velocities, velocities_to_RPM
from FUNC_mouse_callback import mouse_callback
from FUNC_interpolate_waypoints import interpolate_waypoints
from FUNC_find_closest_point import find_closest_point
from FUNC_calculate_signed_AH_and_projection import calculate_signed_AH_and_projection
from FUNC_draw_buttons import draw_buttons

# Shared variables
clicked_points = []
center_coordinate = ()
end_point_arrow = ()
start_pressed = [False]

# Setup camera and window
cap = openCV.initialize_camera()
openCV.initialize_window(
    "2D ArUco Marker Detection and Vector",
    mouse_callback,
    (clicked_points, reset_button_pos, start_button_pos, button_width, button_height, frame_height, start_pressed)
)

# ArUco setup
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
parameters = cv2.aruco.DetectorParameters()

#__main__
while True:
    result = openCV.process_frame(cap)
    if result is None:
        break
    frame, gray = result

    # Detect ArUco markers
    corners, ids = openCV.detect_aruco_markers(gray, aruco_dict, parameters)
    
    if ids is not None and start_pressed[0]:
        frame = openCV.draw_detected_markers(frame, corners, ids)

    # Draw center and orientation
    if corners:
        center_coordinate, end_point_arrow, angle = openCV.draw_center_and_orientation(frame, corners, frame_height, frame_width)

    # Draw clicked points
    if clicked_points:
        openCV.draw_clicked_points(frame, clicked_points, frame_height)

    # Interpolation and signed distance calculation
    if len(clicked_points) > 2:
        interpolated_waypoints = interpolate_waypoints(clicked_points)
        if interpolated_waypoints:
            closest_point = find_closest_point(center_coordinate, interpolated_waypoints, LookAHead_dist)
            if closest_point:
                projection, signed_distance = calculate_signed_AH_and_projection(center_coordinate, end_point_arrow, closest_point)
                print(f"Projection: {projection}, Signed Distance: {signed_distance}")

                # Calculate omega and wheel velocities
                omega = calculate_omega(signed_distance, LookAHead_dist)
                R = ConstVelocity / omega if omega != 0 else float('inf')
                v1, v2 = calculate_wheel_velocities(omega, R, Wheels_dist)
                rpm1, rpm2 = velocities_to_RPM(v1, v2)
                print("RPM Left Wheel:", rpm1)
                print("RPM Right Wheel:", rpm2)

    # Draw buttons
    draw_buttons(frame, start_button_pos, reset_button_pos, button_width, button_height)
    
    # Display the frame
    cv2.imshow("2D ArUco Marker Detection and Vector", frame)
    
    # Press "ESC" to close the window
    if cv2.waitKey(1) & 0xFF == 27:
        break

openCV.release_camera(cap)
