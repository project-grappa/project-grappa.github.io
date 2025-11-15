from motor_cortex.common.perception_functions import get_position, get_size, get_orientation
import numpy as np

# Helper function to calculate distance
def calculate_distance(pos1, pos2):
    return np.linalg.norm(np.array(pos1) - np.array(pos2))

def guidance(state, previous_vars_dict={'pressed_maroon': False, 'pressed_green': False}):
    score = 0.0
    vars_dict = previous_vars_dict.copy()
    
    # Get positions and sizes of the buttons
    maroon_button_pos = get_position('maroon_button')
    green_button_pos = get_position('green_button')
    maroon_button_size = get_size('maroon_button')
    green_button_size = get_size('green_button')
    
    # Robot's current position and orientation
    robot_pos = state[:3]  # x, y, z
    robot_orientation = state[3:6]  # rotation_x, rotation_y, rotation_z
    
    if not vars_dict['pressed_maroon']:
        # Calculate distance to maroon button
        distance_to_maroon = calculate_distance(robot_pos, maroon_button_pos)
        score = max(0, 1 - distance_to_maroon)  # Score increases as robot gets closer
        
        # Check if the robot is close enough to press the maroon button
        if distance_to_maroon < maroon_button_size[0] / 2:  # Dynamic pressing distance
            # Confirm pressing action (placeholder for actual sensor check)
            if confirm_button_press('maroon_button'):
                vars_dict['pressed_maroon'] = True
                score += 1.0  # Bonus for pressing the button
    elif not vars_dict['pressed_green']:
        # Calculate distance to green button
        distance_to_green = calculate_distance(robot_pos, green_button_pos)
        score = max(0, 1 - distance_to_green)  # Score increases as robot gets closer
        
        # Check if the robot is close enough to press the green button
        if distance_to_green < green_button_size[0] / 2:  # Dynamic pressing distance
            # Confirm pressing action (placeholder for actual sensor check)
            if confirm_button_press('green_button'):
                vars_dict['pressed_green'] = True
                score += 1.0  # Bonus for pressing the button

    # Penalty for moving away from the buttons after pressing
    if vars_dict['pressed_maroon'] and not vars_dict['pressed_green']:
        distance_to_green_after_press = calculate_distance(robot_pos, green_button_pos)
        score -= max(0, distance_to_green_after_press - 0.2)  # Penalty for moving away

    return score, vars_dict

def confirm_button_press(button_name):
    # Placeholder function for actual button press confirmation logic
    return True  # Assume the button press is successful for now
