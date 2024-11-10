import cv2

def mouse_callback(event, x, y, flags, param):
    clicked_points, reset_button_pos, button_width, button_height, frame_height = param
    if event == cv2.EVENT_LBUTTONDOWN:
        y = frame_height - y
        if reset_button_pos[0] <= x <= reset_button_pos[0] + button_width and reset_button_pos[1] <= y <= reset_button_pos[1] + button_height:
            clicked_points.clear()
            print("Reset button clicked. All points cleared.")
        else:
            clicked_points.append((x, y))
            print(f"Mouse clicked at: X = {x}, Y = {y}")
