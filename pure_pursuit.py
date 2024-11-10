import numpy as np
import math

def calculate_signed_AH_and_projection(A, B, C):
    A = np.array(A)
    B = np.array(B)
    C = np.array(C)
    AB = B - A
    AC = C - A
    dot_product = np.dot(AB, AC)
    AB_length_squared = np.dot(AB, AB)
    # Calculate the projection scalar t
    t = dot_product / AB_length_squared
    # Calculate the projection point coordinates
    projection_point = A + t * AB
    # Calculate signed distance from A to the projection point
    AH = projection_point - A
    dot_product_AH = np.dot(AB, AH)
    AH_magnitude = np.linalg.norm(AH)
    if dot_product_AH > 0:
        signed_distance = AH_magnitude  # H is on the same side as B with respect to A
    else:
        signed_distance = -AH_magnitude  # H is on the opposite side of B with respect to A

    return projection_point.tolist(), signed_distance  
A = (2, 2)
B = (6, 2)
C = (4, 4)
H, AH_distance = calculate_signed_AH_and_projection(A, B, C)
print("AH:",AH_distance)

def calculate_omega(v, de, lt):
    omega = (2 * de * v) / (lt ** 2)
    return omega
def calculate_wheel_velocities(omega, R, Ld):
    v1 = omega * (R + Ld)
    v2 = omega * (R - Ld)
    return v1, v2

v = 0.17           
lt = 0.10  
Ld = 0.05       
de = 0.075
omega = calculate_omega(v, de, lt)
print("omega =", omega)
R = v / omega if omega != 0 else float('inf')
# Calculate wheel velocities
v1, v2 = calculate_wheel_velocities(omega, R, Ld)
print("v1:", v1)
print("v2:", v2)
rpm1 = (v1*60)/(2*3.14*0.0215)
rpm2 = (v2*60)/(2*3.14*0.0215)
print ("rpm1:",rpm1)
print ("rpm2:",rpm2)

