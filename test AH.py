import numpy as np
import math

def calculate_signed_AH_and_projection(A, B, C):
    """
    Calculate the signed distance from A to the projection of C onto line AB,
    with positive or negative sign depending on the position of the projection point
    relative to A and B.

    Parameters:
    - A: Coordinates of point A as a tuple (Ax, Ay)
    - B: Coordinates of point B as a tuple (Bx, By)
    - C: Coordinates of point C as a tuple (Cx, Cy)

    Returns:
    - (projection_point, signed_distance): A tuple containing the coordinates
      of the projection point and the signed distance from A to the projection point.
    """
    # Convert points to numpy arrays for easy vector calculations
    A = np.array(A)
    B = np.array(B)
    C = np.array(C)

    # Calculate vectors AB and AC
    AB = B - A
    AC = C - A

    # Calculate the dot product and length squared of AB
    dot_product = np.dot(AB, AC)
    AB_length_squared = np.dot(AB, AB)

    # Calculate the projection scalar t
    t = dot_product / AB_length_squared

    # Calculate the projection point coordinates
    projection_point = A + t * AB

    # Calculate signed distance from A to the projection point
    AH = projection_point - A
    dot_product_AH = np.dot(AB, AH)

    # Calculate the magnitude of AH
    AH_magnitude = np.linalg.norm(AH)

    # Determine the sign based on the dot product
    if dot_product_AH > 0:
        signed_distance = AH_magnitude  # H is on the same side as B with respect to A
    else:
        signed_distance = -AH_magnitude  # H is on the opposite side of B with respect to A

    return projection_point.tolist(), signed_distance  # Return as list for consistency

# Example usage:
A = (0, 0)
B = (2, 2)
C = (0, -1)

projection_point, signed_distance = calculate_signed_AH_and_projection(A, B, C)
print(f"Projection Point: {projection_point}, Signed Distance: {signed_distance}")
