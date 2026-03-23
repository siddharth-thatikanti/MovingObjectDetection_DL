import numpy as np

def estimate_speed(prev_center, curr_center, fps):
    distance = np.linalg.norm(
        np.array(curr_center) - np.array(prev_center)
    )
    return distance * fps
