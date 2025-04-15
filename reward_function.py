def reward_function(params):
    '''
    Reward function for DeepRacer on Smiley Speedway (counterclockwise)
    '''
    
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params["speed"]
    all_wheels_on_track = params["all_wheels_on_track"]
    is_offtrack = params["is_offtrack"]
    closest_waypoints = params["closest_waypoints"]
    is_left_of_center = params["is_left_of_center"]
    
    # Initialize reward
    reward = 1.0  # Start with a base reward
    
    # Progressive penalty for going off track
    if is_offtrack:
        return 1e-3  # Small positive reward instead of negative
    
    # Additional penalty for wheels going off track but center still on track
    if not all_wheels_on_track and not is_offtrack:
        reward *= 0.5  # Reduce reward instead of subtracting
    
    # Center waypoints (main racing line)
    center_waypoints = list(range(26, 38)) + [44,58, 59, 60, 61, 77, 78] + list(range(1, 18))
    
    # Outer waypoints (for wider turns)
    outer_waypoints = list(range(38, 44)) + list(range(62, 70))

    # Inner waypoints (for tighter turns)
    inner_waypoints = list(range(45, 59)) + list(range(70, 77)) + list(range(18, 26))
    
    # Calculate markers for track position
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    # Position-based reward
    if closest_waypoints[1] in center_waypoints:
        if distance_from_center <= marker_1:
            reward *= 1.2
        elif distance_from_center <= marker_2:
            reward *= 1.0
        elif distance_from_center <= marker_3:
            reward *= 0.8
        else:
            reward *= 0.5
        
    elif closest_waypoints[1] in outer_waypoints:
        if not is_left_of_center:
            if distance_from_center <= marker_2:
                reward *= 1.2
            elif distance_from_center <= marker_3:
                reward *= 1.0
            else:
                reward *= 0.5
        else:
            reward *= 0.8
    
    elif closest_waypoints[1] in inner_waypoints:
        if is_left_of_center:
            if distance_from_center <= marker_2:
                reward *= 1.2
            elif distance_from_center <= marker_3:
                reward *= 1.0
            else:
                reward *= 0.5
        else:
            reward *= 0.8
    
    # Basic speed reward - encourage maintaining reasonable speed
    if speed > 0.5 and speed < 3:
        reward *= 1.1
    
    # Progress reward
    if params["steps"] > 0:
        reward += params["progress"] / params["steps"]
    
    return float(reward)