"""
Helper functions for navigation
"""
from math import atan2, pi


def dir_to_waypoint(x1, y1, x2, y2):
    """
    Finds the direction [0, 365] from the point (x1, y1) to (x2, y2)
    """
    theta = atan2(y2-y1, x2-x1) * 180 / pi
    if theta < 0:
        theta = 360 + theta
    return theta


def smallest_angle_between(angle1, angle2):
    """
    Returns the size of the smallest angle between angle1 and angle2
    Parameters:
        angle1: positive angle in degrees [0,359]
        angle2: positive angle in degrees [0, 359]

    Returns:
        The smallest angle in degrees between the two angles [0, 180].
    """
    return min((angle1 - angle2) % 360, (angle2 - angle1) % 360)

def shortest_path(desired, current):
    """
    Returns the shortest distance to the desired angle from the current angle

    Parameters:
        desired: Angle to reach [0,359]
        current: Current angle [0, 359]

    Returns:
        The shortest distance in degrees between the two angles.
        Negative values imply counter clockwise rotation
    """
    if desired >= current:
        if desired - current <= 180:
            return desired - current
        else:
            return -1 * (current + 360 - desired)
    else:
        if current - desired <= 180:
            return desired - current
        else:
            return desired + 360 - current
