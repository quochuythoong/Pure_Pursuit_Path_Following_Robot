import numpy as np
import matplotlib.pyplot as plt

def interpolate_waypoints(waypoints, step_distance=1.0):
    interpolated_points = []
    previous_point = None  # Track the last added point to avoid duplicates
    for i in range(len(waypoints) - 1):
        start = np.array(waypoints[i])
        end = np.array(waypoints[i + 1])
        # Calculate the distance and direction between the two waypoints
        distance = np.linalg.norm(end - start)
        direction = (end - start) / distance
        # Calculate the number of steps needed
        num_steps = int(distance // step_distance) + 1  # +1 to include the end point
        # Add interpolated points along the line
        for step in range(num_steps):
            interpolated_point = start + step * step_distance * direction
            rounded_point = (int(round(interpolated_point[0])), int(round(interpolated_point[1])))
            # Only add point if it's different from the last added point
            if rounded_point != previous_point:
                interpolated_points.append(rounded_point)
                previous_point = rounded_point
    # Append the last waypoint, ensuring it's not a duplicate
    last_point = (int(round(waypoints[-1][0])), int(round(waypoints[-1][1])))
    if last_point != previous_point:
        interpolated_points.append(last_point)

    return interpolated_points

def plot_waypoints_and_interpolations(waypoints, interpolated_points):
    # Unzip waypoints and interpolated points for plotting
    waypoint_x, waypoint_y = zip(*waypoints)
    interp_x, interp_y = zip(*interpolated_points)
    plt.figure(figsize=(8, 8))
    plt.plot(waypoint_x, waypoint_y, 'ro-', label="Original Waypoints")  
    plt.plot(interp_x, interp_y, 'bo', label="Interpolated Points")  
    plt.grid(True)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Waypoint Interpolation")
    plt.legend()
    plt.show()

waypoints = [(1, 1), (6, 4), (6, 12),(3,15)]
step_distance = 1.0
interpolated_waypoints = interpolate_waypoints(waypoints, step_distance)

print("Interpolated Waypoints:")
for point in interpolated_waypoints:
    print(point)

# Plot the waypoints and interpolated path
plot_waypoints_and_interpolations(waypoints, interpolated_waypoints)
