def solve_water_jug_dfs(jug1_capacity, jug2_capacity, target):
  visited = set()  # Store visited states to avoid loops

  def dfs(state, path):
    if state in visited:
      return None
    visited.add(state)

    if state[0] == target or state[1] == target:
      return path + [state]

    # Try all possible operations
    for next_state in generate_next_states(state, jug1_capacity, jug2_capacity):
      result = dfs(next_state, path + [state])
      if result:
        return result
    return None

  def generate_next_states(state, jug1_capacity, jug2_capacity):
    next_states = []
    # Fill jug1
    next_states.append((min(jug1_capacity, jug1_capacity - state[0]), state[1]))
    # Fill jug2
    next_states.append((state[0], min(jug2_capacity, jug2_capacity - state[1])))
    # Empty jug1
    next_states.append((0, state[1]))
    # Empty jug2
    next_states.append((state[0], 0))
    # Pour from jug1 to jug2
    amount = min(state[0], jug2_capacity - state[1])
    next_states.append((state[0] - amount, state[1] + amount))
    # Pour from jug2 to jug1
    amount = min(state[1], jug1_capacity - state[0])
    next_states.append((state[0] + amount, state[1] - amount))
    return [s for s in next_states if s[0] >= 0 and s[1] >= 0]  # Filter invalid states

  initial_state = (0, 0)  # Initially both jugs are empty
  solution = dfs(initial_state, [])
  if solution:
    print("Steps to reach the target:")
    for step, state in enumerate(solution):
      print(f"Step {step+1}: Jug1 = {state[0]}, Jug2 = {state[1]}")
  else:
    print("No solution found for the given target.")

# Example usage
jug1_capacity = 3
jug2_capacity = 4
target = 2
solve_water_jug_dfs(jug1_capacity, jug2_capacity, target)
