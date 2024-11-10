import numpy as np

def calculate_signed_AH_and_projection(A, B, C):
    A, B, C = np.array(A), np.array(B), np.array(C)
    AB, AC = B - A, C - A
    t = np.dot(AB, AC) / np.dot(AB, AB)
    projection_point = A + t * AB
    AH = projection_point - A
    signed_distance = np.linalg.norm(AH) * (1 if np.dot(AB, AH) > 0 else -1)

    return projection_point.tolist(), signed_distance
