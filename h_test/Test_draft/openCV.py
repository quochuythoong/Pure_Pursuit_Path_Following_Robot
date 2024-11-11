import cv2
import numpy as np

# Initialize OpenCV components and shared variables
def initialize_camera():
    cap = cv2.VideoCapture(0)
    return cap

def initialize_window(window_name, mouse_callback, callback_params):
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, mouse_callback, callback_params)

def process_frame(cap):
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        return None
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return frame, gray

def detect_aruco_markers(gray, aruco_dict, parameters):
    corners, ids, rejected = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    return corners, ids

def draw_detected_markers(frame, corners, ids):
    return cv2.aruco.drawDetectedMarkers(frame, corners, ids)

def draw_center_and_orientation(frame, corners, frame_height):
    for i, corner in enumerate(corners):
        points = corner[0]
        cx, cy = int(np.mean(points[:, 0])), frame_height - int(np.mean(points[:, 1]))
        vec_x, vec_y = points[1][0] - points[0][0], points[0][1] - points[1][1]
        angle = np.arctan2(vec_y, vec_x) * 180 / np.pi

        # Center and orientation drawing
        cv2.circle(frame, (cx, frame_height - cy), 5, (0, 255, 0), -1)
        arrow_length = 50
        end_x = int(cx + arrow_length * np.cos(angle * np.pi / 180))
        end_y = int(cy + arrow_length * np.sin(angle * np.pi / 180))
        cv2.arrowedLine(frame, (cx, frame_height - cy), (end_x, frame_height - end_y), (0, 255, 0), 2)

        return (cx, cy), (end_x, end_y), angle

def draw_clicked_points(frame, clicked_points, frame_height):
    for i in range(len(clicked_points)):
        cv2.circle(frame, (clicked_points[i][0], frame_height - clicked_points[i][1]), 5, (0, 0, 255), -1)
        if i > 0:
            cv2.line(frame, (clicked_points[i - 1][0], frame_height - clicked_points[i - 1][1]), 
                     (clicked_points[i][0], frame_height - clicked_points[i][1]), (255, 0, 0), 2)
    if len(clicked_points) >= 3:
        cv2.line(frame, (clicked_points[-1][0], frame_height - clicked_points[-1][1]),
                 (clicked_points[0][0], frame_height - clicked_points[0][1]), (255, 0, 0), 2)

def display_text(frame, text, position):
    cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

def release_camera(cap):
    cap.release()
    cv2.destroyAllWindows()
