Description:
- This is a Pure Pursuit implementation project
- An autonomous vehicle follows a chosen paths formed by multiple waypoints

Approach:
- Camera (bird-view) to detect the vehicle position (x-y coordinates) and its vector : Done
- Create a simple GUI to interact and get waypoints : Done
- Use computer to Stream - Calculate (Pure Pursuit algorithm) - Sending rpm (Pure Pursuit angular velocity output ...) : Done
- ESP32 to receive left and right motor speed from client : Done

How-to:
- Simple GUI
- Click to choose waypoints to create the desired path
- Press START for the car to run according to the waypoints
- Press RESET to clear all previous waypoints
