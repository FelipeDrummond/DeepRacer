def reward_function(params):
    '''
    Reward function for DeepRacer on Smiley Speedway (counterclockwise)
    '''
    
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params["speed"]
    steering_angle = abs(params["steering_angle"])
    all_wheels_on_track = params["all_wheels_on_track"]
    
    # Initialize reward
    reward = 1.0
    
    # Strong penalty for going off track
    if not all_wheels_on_track:
        return 1e-3
    
    # Center waypoints (main racing line)
    center_waypoints = list(range(26, 38)) + [44,58, 59, 60, 61, 77, 78] + list(range(1, 18))
    
    # Outer waypoints (for wider turns)
    outer_waypoints = list(range(38, 44)) + list(range(62, 70))

    # Inner waypoints (for tighter turns)
    inner_waypoints = list(range(45, 59)) + list(range(70, 77)) + list(range(18, 26))
    
    # Speed zones
    fast = list(range(62, 66)) + list(range(13, 17)) + list(range(28, 37))
    moderate = list(range(37, 41)) + list(range(58, 62)) + list(range(66, 73)) + list(range(2, 6)) + list(range(10, 13)) + list(range(17, 20)) + list(range(25, 28))
    slow = list(range(73, 79)) + list(range(1, 2)) + list(range(6, 10)) + list(range(20, 25))
    
    # Calculate markers for track position
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    # Position-based reward
    if params["closest_waypoints"][1] in center_waypoints:
        if distance_from_center <= marker_1:
            reward *= 1.0
        elif distance_from_center <= marker_2:
            reward *= 0.8
        elif distance_from_center <= marker_3:
            reward *= 0.5
        else:
            reward *= 0.1
    elif params["closest_waypoints"][1] in outer_waypoints:
        if params["is_right_of_center"]:
            if distance_from_center <= marker_2:
                reward *= 1.0
            elif distance_from_center <= marker_3:
                reward *= 0.7
            else:
                reward *= 0.1
    elif params["closest_waypoints"][1] in inner_waypoints:
        if params["is_left_of_center"]:
            if distance_from_center <= marker_2:
                reward *= 1.0
            elif distance_from_center <= marker_3:
                reward *= 0.7
            else:
                reward *= 0.1
    
    # Speed and steering control
    current_waypoint = params["closest_waypoints"][1]
    
    if current_waypoint in slow:
        # For slow sections (tight corners)
        if speed < 1.5 and speed > 0.5:
            reward *= 1.0
            # Additional reward for appropriate steering in tight corners
            if steering_angle > 10 and steering_angle < 30:
                reward *= 1.2
        else:
            reward *= 0.5
    elif current_waypoint in moderate:
        # For moderate sections
        if speed >= 1.5 and speed <= 2.5:
            reward *= 1.0
            # Moderate steering reward
            if steering_angle > 5 and steering_angle < 20:
                reward *= 1.1
        else:
            reward *= 0.7
    elif current_waypoint in fast:
        # For fast sections
        if speed > 2.5:
            reward *= 1.0
            # Small steering reward for stability
            if steering_angle < 10:
                reward *= 1.1
        else:
            reward *= 0.8
    
    # Progress reward
    if params["steps"] > 0:
        reward += params["progress"] / params["steps"]
    
    return float(reward)