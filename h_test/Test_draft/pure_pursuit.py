import math

def calculate_omega(AH, v, lt):
    omega = (2 * AH * v) / (lt ** 2)
    return omega

def calculate_wheel_velocities(omega, R, Ld):
    v1 = omega * (R + Ld)
    v2 = omega * (R - Ld)
    return v1, v2

def velocities_to_RPM(v1, v2):
    rpm1 = (v1 * 60) / (2 * math.pi * 0.0215) #radius of wheels = 0.0215 meter
    rpm2 = (v2 * 60) / (2 * math.pi * 0.0215)
    PWM1 = (rpm1 / 250) * 255 + 5  #250 max RPM of motor, 255 max PWM of ESP, 5 random calib
    PWM2 = (rpm2 / 250) * 255 + 5
    return PWM1, PWM2


