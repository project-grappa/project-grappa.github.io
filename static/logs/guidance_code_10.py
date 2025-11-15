from motor_cortex.common.perception_functions import get_position, get_size, get_orientation
import numpy as np

# Helper function to calculate distance
def calculate_distance(pos1, pos2):
    return np.linalg.norm(np.array(pos1) - np.array(pos2))

# Improved path planning function (to be implemented)
def plan_path(start_pos, target_pos):
    # Implement a path planning algorithm (e.g., A* or Dijkstra's) here
    # For now, return a direct line to the target position
    return target_pos

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
        score += max(0, 1 - distance_to_maroon)  # Score increases as robot gets closer
        
        # Check if the robot is close enough to press the maroon button
        if distance_to_maroon < maroon_button_size[0] / 2:  # Dynamic pressing distance
            # Confirm pressing action with actual sensor feedback
            if confirm_button_press('maroon_button', robot_pos):
                vars_dict['pressed_maroon'] = True
                score += 1.0  # Bonus for pressing the button
    elif not vars_dict['pressed_green']:
        # Calculate distance to green button
        distance_to_green = calculate_distance(robot_pos, green_button_pos)
        score += max(0, 1 - distance_to_green)  # Score increases as robot gets closer
        
        # Check if the robot is close enough to press the green button
        if distance_to_green < green_button_size[0] / 2:  # Dynamic pressing distance
            # Confirm pressing action with actual sensor feedback
            if confirm_button_press('green_button', robot_pos):
                vars_dict['pressed_green'] = True
                score += 1.0  # Bonus for pressing the button

    # Direct movement towards the green button after pressing the maroon button
    if vars_dict['pressed_maroon'] and not vars_dict['pressed_green']:
        # Plan a path to the green button
        target_position = plan_path(robot_pos, green_button_pos)
        # Update robot's position towards the target position
        robot_pos = target_position  # Simulate movement towards the target
        distance_to_green_after_press = calculate_distance(robot_pos, green_button_pos)
        score -= max(0, distance_to_green_after_press - 0.2)  # Penalty for moving away

    return score, vars_dict

def confirm_button_press(button_name, robot_pos):
    # Implement actual sensor feedback to confirm button press
    button_pos = get_position(button_name)
    distance_to_button = calculate_distance(robot_pos, button_pos)
    return distance_to_button < 0.05  # Assume success if within 5 cm
