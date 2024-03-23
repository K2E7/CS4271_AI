def transfer_family_optimized(transfer_times, max_transfer_time):
    # Sort the transfer_times in descending order
    transfer_times.sort(reverse=True)

    # Initialize variables
    left_side = transfer_times[:]
    right_side = []
    time_elapsed = 0

    # Logic for crossing the river
    while left_side:
        # Cross the fastest person and the second fastest person
        if len(left_side) >= 2:
            if left_side[0] + left_side[1] + time_elapsed <= max_transfer_time:
                right_side.extend([left_side.pop(0), left_side.pop(0)])
                time_elapsed += max(right_side[-2], right_side[-1])
            else:
                break
        else:
            # Cross the remaining person
            if left_side[0] + time_elapsed <= max_transfer_time:
                right_side.append(left_side.pop(0))
                time_elapsed += right_side[-1]
            else:
                break

        # Return the fastest person back to the left side
        left_side.append(right_side.pop(0))
        time_elapsed += left_side[-1]

    return time_elapsed if not left_side else -1  # Return -1 if time constraint is exceeded

# Family member travel times in seconds
transfer_times = [1, 3, 6, 8, 12]
max_transfer_time = 30  # Maximum time allowed for transfer

min_time_required = transfer_family_optimized(transfer_times, max_transfer_time)
if min_time_required != -1:
    print("Minimum time required:", min_time_required)
else:
    print("No valid path found within the time constraint.")
