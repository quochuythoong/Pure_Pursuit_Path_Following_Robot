import cv2

def initialize_camera():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("Error: Could not open the camera.")
        return None
    cv2.namedWindow("2D ArUco Marker Detection and Vector")
     # Query default frame width and height
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"Default frame size: {width}x{height}")
    return cap

cap = initialize_camera()
if cap:
    cap.release()