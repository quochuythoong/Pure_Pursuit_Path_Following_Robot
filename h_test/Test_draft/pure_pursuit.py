import math

def calculate_omega(AH, lt):
    omega = (2 * AH) / (lt ** 2)
    return omega

def calculate_wheel_velocities(omega, R, Ld):
    v1 = omega * (R + Ld)
    v2 = omega * (R - Ld)
    return v1, v2

def velocities_to_RPM(v1, v2):
    rpm1 = (v1 * 60) / (2 * math.pi * 0.0215)
    rpm2 = (v2 * 60) / (2 * math.pi * 0.0215)
    return rpm1, rpm2
