import cv2
import numpy as np
from utils import frame_height, frame_width, start_button_pos, reset_button_pos, button_width, button_height
from FUNC_mouse_callback import mouse_callback
from FUNC_interpolate_waypoints import interpolate_waypoints
from FUNC_find_closest_point import find_closest_point
from FUNC_calculate_signed_AH_and_projection import calculate_signed_AH_and_projection
from FUNC_draw_buttons import draw_buttons
from pure_pursuit import calculate_omega, calculate_wheel_velocities

# Shared variables
clicked_points = []
center_coordinate = ()
end_point_arrow = ()
start_pressed = [False]
# ---------------------
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
parameters = cv2.aruco.DetectorParameters()
cap = cv2.VideoCapture(0)

cv2.namedWindow("2D ArUco Marker Detection and Vector")
cv2.setMouseCallback(
    "2D ArUco Marker Detection and Vector", 
    mouse_callback,  # Callback function
    (clicked_points, reset_button_pos, start_button_pos, button_width, button_height, frame_height, start_pressed)  # Tuple of parameters
)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        break
    
    # Convert the frame to grayscale (helps with ArUco detection)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect the ArUco markers in the grayscale image
    corners, ids, rejected = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # Draw detected ArUco markers and calculate their center and orientation
    if ids is not None and start_pressed[0]:
        # Draw detected ArUco markers
        frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)

    # Display X, Y, Angle, and Degree information in the top right corner
    for i, corner in enumerate(corners):
        points = corner[0]
        cx, cy = int(np.mean(points[:, 0])), frame_height - int(np.mean(points[:, 1]))
        center_coordinate = (cx, cy)
        vec_x, vec_y = points[1][0] - points[0][0], points[0][1] - points[1][1]
        angle = np.arctan2(vec_y, vec_x) * 180 / np.pi
        
        # Draw the center and orientation as usual
        cv2.circle(frame, (cx, frame_height - cy), 5, (0, 255, 0), -1)  # Green circle at the center
        arrow_length = 50
        end_x = int(cx + arrow_length * np.cos(angle * np.pi / 180))
        end_y = int(cy + arrow_length * np.sin(angle * np.pi / 180))
        end_point_arrow = (end_x, end_y)
        cv2.arrowedLine(frame, (cx, frame_height - cy), (end_x, frame_height - end_y), (0, 255, 0), 2)  # Green arrow

        # Display coordinates and angle in the top right corner
        text_x_y = f"X: {cx}, Y: {cy}"
        text_angle = f"Angle: {angle:.2f} deg"
        
        # Calculate positions for the text
        top_right_x = frame_width - 200  # Offset 200 pixels from the right edge
        top_right_y = 30  # Offset from the top edge for the first line of text
        line_spacing = 30  # Space between lines of text

        # Display the X, Y coordinates
        cv2.putText(frame, text_x_y, (top_right_x, top_right_y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Display the Angle
        cv2.putText(frame, text_angle, (top_right_x, top_right_y + line_spacing), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Draw the clicked points and connect them with lines
    if len(clicked_points) > 0:
        for i in range(len(clicked_points)):
            # Draw each clicked point as a red circle
            cv2.circle(frame, (clicked_points[i][0], frame_height - clicked_points[i][1]), 5, (0, 0, 255), -1)

            # Connect the points with blue lines
            if i > 0:
                cv2.line(frame, (clicked_points[i - 1][0], frame_height - clicked_points[i - 1][1]), 
                         (clicked_points[i][0], frame_height - clicked_points[i][1]), (255, 0, 0), 2)

        # Automatically connect the last dot to the first dot if there are 3 or more points
        if len(clicked_points) >= 3:
            cv2.line(frame, (clicked_points[-1][0], frame_height - clicked_points[-1][1]),
                     (clicked_points[0][0], frame_height - clicked_points[0][1]), (255, 0, 0), 2)

    # Interpolation and signed distance calculation if there are enough clicked points
    if len(clicked_points) > 2:
        interpolated_waypoints = interpolate_waypoints(clicked_points)
        
        # Check if interpolated waypoints are generated correctly
        if interpolated_waypoints:          
            look_ahead_distance = 20
            closest_point = find_closest_point(center_coordinate, interpolated_waypoints, look_ahead_distance)

            if closest_point:
                projection, signed_distance = calculate_signed_AH_and_projection(center_coordinate, end_point_arrow, closest_point)
                print(f"Projection: {projection}, Signed Distance: {signed_distance}")

    # Draw buttons
    draw_buttons(frame, start_button_pos, reset_button_pos, button_width, button_height)
    
    # Display the frame
    cv2.imshow("2D ArUco Marker Detection and Vector", frame)
    
    # Press "ESC" to close the window
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
