import numpy as np
import matplotlib.pyplot as plt

def interpolate_waypoints(waypoints, step_distance=1.0):
    interpolated_points = []
    previous_point = None  # Track the last added point to avoid duplicates

    for i in range(len(waypoints) - 1):
        start = np.array(waypoints[i])
        end = np.array(waypoints[i + 1])

        distance = np.linalg.norm(end - start)
        direction = (end - start) / distance

        num_steps = int(distance // step_distance) + 1  # +1 to include the end point

        for step in range(num_steps):
            interpolated_point = start + step * step_distance * direction
            rounded_point = (int(round(interpolated_point[0])), int(round(interpolated_point[1])))

            if rounded_point != previous_point:
                interpolated_points.append(rounded_point)
                previous_point = rounded_point

    last_point = (int(round(waypoints[-1][0])), int(round(waypoints[-1][1])))
    if last_point != previous_point:
        interpolated_points.append(last_point)

    return interpolated_points

def find_closest_point(current_position, waypoints, look_ahead_distance):
    closest_point = None
    min_distance_diff = float('inf')

    for point in waypoints:
        # Calculate the distance between the current position and each waypoint
        distance = np.linalg.norm(np.array(current_position) - np.array(point))

        # Check if this distance is closest to the desired look-ahead distance
        if abs(distance - look_ahead_distance) < min_distance_diff:
            min_distance_diff = abs(distance - look_ahead_distance)
            closest_point = point

    return closest_point

def plot_waypoints_and_closest(waypoints, interpolated_points, current_position, closest_point, look_ahead_distance):
    waypoint_x, waypoint_y = zip(*waypoints)
    interp_x, interp_y = zip(*interpolated_points)
    
    plt.figure(figsize=(8, 8))
    plt.plot(waypoint_x, waypoint_y, 'ro-', label="Original Waypoints")
    plt.plot(interp_x, interp_y, 'bo', label="Interpolated Points")
    plt.plot(current_position[0], current_position[1], 'go', label="Current Position")
    plt.plot(closest_point[0], closest_point[1], 'mo', label="Look-Ahead Point")

    # Draw the look-ahead distance as a circle
    look_ahead_circle = plt.Circle(current_position, look_ahead_distance, color='cyan', fill=False, linestyle='--', label="Look-Ahead Distance")
    plt.gca().add_patch(look_ahead_circle)
    plt.grid(True)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Waypoint Interpolation with Look-Ahead Distance")
    plt.legend()
    plt.axis('equal')  # Ensure the circle appears round
    plt.show()

waypoints = [(1, 1), (6, 4), (6, 12)]
step_distance = 1.0
interpolated_waypoints = interpolate_waypoints(waypoints, step_distance)
print(interpolated_waypoints)
current_position = (3, 2)
look_ahead_distance = 1.5

closest_point = find_closest_point(current_position, interpolated_waypoints, look_ahead_distance)

#print(closest_point)

# Plot the waypoints, current position, look-ahead point, and look-ahead distance circle
plot_waypoints_and_closest(waypoints, interpolated_waypoints, current_position, closest_point, look_ahead_distance)
