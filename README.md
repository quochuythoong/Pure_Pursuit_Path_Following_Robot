Description:
- This is a Pure Pursuit implementation project
- An autonomous vehicle follows a chosen paths formed by multiple waypoints

Approach:
- Camera (bird-view) to detect the vehicle position (x-y coordinates) and its vector
- Create a simple GUI to interact
- Use computer to Stream - Calculate (Pure Pursuit algorithm) - Sending PWM (Pure Pursuit angular velocity output ...)
- ESP32 to receive PWM and drive the vehicle

How-to:
- Simple GUI
- Click to choose waypoints to create the desired path
- Press START for the car to run according to the waypoints
- Press RESET to clear all previous waypoints
