import math

def calculate_omega(v, de, lt):
    omega = (2 * de * v) / (lt ** 2)
    return omega

def calculate_wheel_velocities(omega, R, Ld):
    v1 = omega * (R + Ld)
    v2 = omega * (R - Ld)
    return v1, v2

# Execute the main algorithm
if __name__ == "__main__":
    v = 0.17           # Velocity in m/s
    lt = 0.10          # Distance to look-ahead point in meters
    Ld = 0.05          # Distance between wheels
    de = 0.075         # Error distance to path
    omega = calculate_omega(v, de, lt)
    print("omega =", omega)
    
    R = v / omega if omega != 0 else float('inf')
    # Calculate wheel velocities
    v1, v2 = calculate_wheel_velocities(omega, R, Ld)
    print("v1:", v1)
    print("v2:", v2)

    # Convert velocities to RPM
    rpm1 = (v1 * 60) / (2 * math.pi * 0.0215)
    rpm2 = (v2 * 60) / (2 * math.pi * 0.0215)
    print("rpm1:", rpm1)
    print("rpm2:", rpm2)
