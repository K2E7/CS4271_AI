def solve_mislabeled_boxes(labels):
  """
  Solves the mislabeled boxes problem for any number of boxes and comma-separated labels.

  Args:
      labels: A list of strings representing the labels for each box.

  Returns:
      A dictionary mapping the correct labels to their corresponding box index, 
      or None if no solution is found.
  """

  class DFSNode:
    def __init__(self, box_contents, visited):
      self.box_contents = box_contents
      self.visited = visited

  def dfs(node):
    """
    Performs the DFS exploration from a given node (box contents and visited states).

    Args:
        node: A DFSNode object representing the current state.

    Returns:
        A dictionary mapping the correct labels to their corresponding box index, 
        or None if no solution is found.
    """
    if tuple(node.box_contents.values()) in node.visited:
      return None
    node.visited.add(tuple(node.box_contents.values()))

    # Check if all boxes have their correct labels
    if all(len(box_contents) == 1 for box_index, box_contents in node.box_contents.items()):
      return {i: box_contents[i][0] for i in range(len(labels))}

    # Choose a box and take an item from it
    for box_index, contents in node.box_contents.items():
      if len(contents) > 1:
        item = contents.pop(0)
        # Check if the item matches any other box's label
        for other_box in range(len(labels)):
          if item in labels[other_box].split(",") and other_box != box_index:
            # Update box contents and explore the new state
            new_contents = node.box_contents.copy()
            new_contents[other_box].append(item)
            new_node = DFSNode(new_contents, node.visited.copy())
            result = dfs(new_node)
            if result:
              return result
        # No match found, put the item back and continue searching
        node.box_contents[box_index].append(item)

    return None

  # Initialize box contents with their labels (corrected for comma-separated handling)
  box_contents = {i: labels[i].split(",") for i in range(len(labels))}
  solution = dfs(DFSNode(box_contents, set()))
  if solution:
    print("Steps to solve:")
    for step, state in enumerate(solution):  # Access DFS exploration steps
      print(f"Step {step+1}: {state}")
    return solution
  else:
    print("No solution found.")

# Example usage with three boxes and comma-separated labels
labels = ["apple", "orange", "apple,orange"]
solution = solve_mislabeled_boxes(labels)
if solution:
  print("Correct labels:", solution)
