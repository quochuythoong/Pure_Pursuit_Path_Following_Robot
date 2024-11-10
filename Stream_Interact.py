import cv2
import numpy as np

# Global variables to store clicked points
clicked_points = []

# Define the mouse callback function
def mouse_callback(event, x, y, flags, param):
    global clicked_points
    if event == cv2.EVENT_LBUTTONDOWN:  # Left mouse button click
        # Check if the click is within the reset button area
        if reset_button_pos[0] <= x <= reset_button_pos[0] + button_width and reset_button_pos[1] <= y <= reset_button_pos[1] + button_height:
            clicked_points.clear()  # Clear all clicked points if reset button is clicked
            print("Reset button clicked. All points cleared.")
        else:
            clicked_points.append((x, y))  # Add the clicked point to the list
            print(f"Mouse clicked at: X = {x}, Y = {y}")

# Load the ArUco dictionary (Original ArUco)
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
parameters = cv2.aruco.DetectorParameters()

# Initialize the camera (streaming from camera 0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# Create a simple GUI window
cv2.namedWindow("2D ArUco Marker Detection and Vector")
cv2.setMouseCallback("2D ArUco Marker Detection and Vector", mouse_callback)

# Button position and size
start_button_pos = (10, 30)
reset_button_pos = (10, 70)
button_width = 80
button_height = 30

def draw_buttons(frame):
    # Draw Start Button
    cv2.rectangle(frame, start_button_pos, (start_button_pos[0] + button_width, start_button_pos[1] + button_height), (0, 255, 0), -1)
    cv2.putText(frame, "Start", (start_button_pos[0] + 15, start_button_pos[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Draw Reset Button
    cv2.rectangle(frame, reset_button_pos, (reset_button_pos[0] + button_width, reset_button_pos[1] + button_height), (0, 0, 255), -1)
    cv2.putText(frame, "Reset", (reset_button_pos[0] + 15, reset_button_pos[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

# Main loop
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        break

    # Convert the frame to grayscale (helps with ArUco detection)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect the ArUco markers in the grayscale image
    corners, ids, rejected = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if ids is not None:
        # Draw the detected markers
        frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        for i, corner in enumerate(corners):
            # Get the coordinates of the corner points of the marker
            points = corner[0]

            # Calculate the center of the marker (mean of the corner points)
            cx = int(np.mean(points[:, 0]))  # X coordinate of the center
            cy = int(np.mean(points[:, 1]))  # Y coordinate of the center
            center_coordinate = (cx, cy)
            # Draw a circle at the center of the marker
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)  # Green circle at the center

            # Calculate 2D orientation (angle of the top side of the marker)
            vec_x = points[1][0] - points[0][0]  # X direction between top-left and top-right corners
            vec_y = points[1][1] - points[0][1]  # Y direction between top-left and top-right corners
            angle = np.arctan2(vec_y, vec_x) * 180 / np.pi  # Angle in degrees

            # Draw the orientation as an arrow from the center
            arrow_length = 50  # Length of the arrow to indicate orientation
            end_x = int(cx + arrow_length * np.cos(angle * np.pi / 180))
            end_y = int(cy + arrow_length * np.sin(angle * np.pi / 180))
            cv2.arrowedLine(frame, (cx, cy), (end_x, end_y), (0, 255, 0), 2)  # Green arrow
            end_point_arrow = (end_x, end_y)
            # Increase offsets to move the text further from the center
            text_offset_x = 100
            text_offset_y = 50

            # Print the 2D coordinates and orientation
            cv2.putText(frame, f"ID: {ids[i][0]} X: {cx}, Y: {cy}", 
                        (cx + text_offset_x, cy - text_offset_y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(frame, f"Angle: {angle:.2f} deg", 
                        (cx + text_offset_x, cy + text_offset_y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Draw the clicked points and connect them with lines
    if len(clicked_points) > 0:
        for i in range(len(clicked_points)):
            # Draw each clicked point as a red circle
            cv2.circle(frame, clicked_points[i], 5, (0, 0, 255), -1)  # Red circle for clicked point

            # If there is more than one point, connect the points with lines
            if i > 0:
                cv2.line(frame, clicked_points[i - 1], clicked_points[i], (255, 0, 0), 2)  # Blue line between points

        # Automatically connect the last dot to the first dot if there are 3 or more points
        if len(clicked_points) >= 3:
            cv2.line(frame, clicked_points[-1], clicked_points[0], (255, 0, 0), 2)  # Blue line to close the shape

    # Draw buttons
    draw_buttons(frame)

    # Display the frame with detection and vector
    cv2.imshow("2D ArUco Marker Detection and Vector", frame)

    # Check for exit condition
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
