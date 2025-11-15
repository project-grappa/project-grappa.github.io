from grappa.common.perception_functions import get_position, get_size, get_orientation
import numpy as np

# Helper function to calculate distance
def calculate_distance(pos1, pos2):
    return np.linalg.norm(np.array(pos1) - np.array(pos2))

def guidance(state, previous_vars_dict={'pressed_maroon': False, 'pressed_green': False}):
    score = 0.0
    vars_dict = previous_vars_dict.copy()
    
    # Get positions of the buttons
    maroon_button_pos = get_position('maroon_button')
    green_button_pos = get_position('green_button')
    
    # Robot's current position
    robot_pos = state[:3]  # x, y, z
    
    if not vars_dict['pressed_maroon']:
        # Calculate distance to maroon button
        distance_to_maroon = calculate_distance(robot_pos, maroon_button_pos)
        score = max(0, 1 - distance_to_maroon)  # Score increases as robot gets closer
        
        # Check if the robot is close enough to press the maroon button
        if distance_to_maroon < 0.1:  # Assuming 0.1m is the pressing distance
            vars_dict['pressed_maroon'] = True
            score += 1.0  # Bonus for pressing the button
    elif not vars_dict['pressed_green']:
        # Calculate distance to green button
        distance_to_green = calculate_distance(robot_pos, green_button_pos)
        score = max(0, 1 - distance_to_green)  # Score increases as robot gets closer
        
        # Check if the robot is close enough to press the green button
        if distance_to_green < 0.1:  # Assuming 0.1m is the pressing distance
            vars_dict['pressed_green'] = True
            score += 1.0  # Bonus for pressing the button

    return score, vars_dict
