def solve(missionaries, cannibals, boat_location):
  """
  This function iteratively explores possible moves and returns a list of steps
  to get all missionaries and cannibals across the river.

  Args:
      missionaries: Number of missionaries on the starting side.
      cannibals: Number of cannibals on the starting side.
      boat_location: 'Start' or 'End' indicating the current location of the boat.

  Returns:
      A list of strings representing the steps to solve the puzzle, 
      or None if there's no solution.
  """
  # Define the initial state as a dictionary
  state = {'missionaries_start': missionaries, 'cannibals_start': cannibals, 'boat': boat_location}
  visited_states = set()  # Keep track of visited states to avoid loops
  solution_queue = [state]  # Queue to store states for exploration

  while solution_queue:
    current_state = solution_queue.pop(0)
    visited_states.add(tuple(current_state.values()))  # Convert state to hashable tuple

    # Check if goal state is reached
    if current_state['missionaries_start'] == 0 and current_state['cannibals_start'] == 0 and current_state['boat'] == 'End':
      # Reconstruct the solution path from visited states
      solution = []
      while current_state:
        # Find the previous state that led to the current state
        for prev_state in visited_states:
          if current_state != prev_state and all(current_state[key] == prev_state[key] + (val if key in ('boat', ) else -val) for key, val in current_state.items()):
            if prev_state in solution_queue:
              solution_queue.remove(prev_state)
            solution.append(get_move_description(current_state, prev_state))
            current_state = prev_state
            break
      return solution[::-1]  # Reverse the solution path

    # Generate all possible valid moves for the current state
    for move in generate_moves(current_state):
      new_state = make_move(current_state.copy(), move)
      if new_state not in visited_states:
        solution_queue.append(new_state)

  # No solution found
  return None

def generate_moves(state):
  """
  This function generates all valid combinations of missionaries and cannibals
  that can be transported in the boat based on the current state.

  Args:
      state: A dictionary representing the current state (missionaries, cannibals, boat location).

  Returns:
      A list of dictionaries representing valid moves (updated state after the move).
  """
  moves = []
  boat_location = state['boat']
  missionaries_on_side = state[f'missionaries_{boat_location}']
  cannibals_on_side = state[f'cannibals_{boat_location}']
  
  # Add all combinations from 1 to capacity (2) for both missionaries and cannibals
  for m in range(1, min(missionaries_on_side, 3) + 1):
    for c in range(max(0, m - 1), min(cannibals_on_side, 3) + 1):
      # Ensure missionaries are not outnumbered (except when returning to starting side)
      if missionaries_on_side - m >= cannibals_on_side - c or boat_location == 'End':
        new_state = {
          f'missionaries_{boat_location}': missionaries_on_side - m,
          f'cannibals_{boat_location}': cannibals_on_side - c,
          'boat': 'End' if boat_location == 'Start' else 'Start'
        }
        moves.append(new_state)
  return moves

def get_move_description(current_state, previous_state):
  """
  This function constructs a string describing the move taken.
  """
  missionaries_moved = current_state['missionaries_start'] - previous_state['missionaries_start']
  cannibals_moved = current_state['cannibals_start'] - previous_state['cannibals_start']
  move_description = f"{missionaries_moved}M {cannibals_moved}C"
  return move_description

# Example usage
solution = solve(3, 3, 'Start')

if solution:
  print("Solution found in", len(solution), "steps:")
  for step in solution:
    print(step)
else:
  print("No solution found!")

