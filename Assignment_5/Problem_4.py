def river_crossing_algorithm_with_steps(starter):
    # Initialize variables
    first_array = sorted(starter)
    print(first_array)
    second_array = []
    x = 0
    steps = []

    while first_array:
        print(first_array)
        if not second_array : 
        # Move fastest two from first array to second array
            second_array.extend(first_array[:2])
            first_array = first_array[2:]
            steps.append((list(first_array), list(second_array), x))
        else: 
        # Move slowest two from first array to second array 
            second_array.extend(first_array[-2:])
            first_array = first_array[-2:]
            steps.append((list(first_array), list(second_array), x))

        # Update logger variable x
        x += max(second_array[-2:]) if len(second_array) >= 2 else 0

        if first_array:
            # Move fastest back from second array to first array
            first_array.append(min(second_array))
            second_array.remove(min(second_array))
            x += min(second_array)
            steps.append((list(first_array), list(second_array), x))

    return steps

# Test the function with the provided starter array
starter = [1, 3, 6, 8, 12]
steps = river_crossing_algorithm_with_steps(starter)

# Print the steps and logger variable x after each step
for i, step in enumerate(steps):
    first_array, second_array, x = step
    print(f"Step {i+1}: First Array: {first_array}, Second Array: {second_array}, x = {x}")

print("\nFinal Logger variable x after completing the river crossing algorithm:", x)
