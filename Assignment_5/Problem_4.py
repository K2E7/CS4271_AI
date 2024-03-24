from collections import deque

class State:
    def __init__(self, people, boat, time):
        self.people = people
        self.boat = boat
        self.time = time

    def __eq__(self, other):
        return self.people == other.people and self.boat == other.boat

    def __hash__(self):
        return hash((tuple(self.people), tuple(self.boat)))

def is_valid(state):
    left_bank = state.people[:]
    right_bank = [1, 3, 6, 8, 12]
    for person in state.boat:
        if person not in left_bank:
            return False
        left_bank.remove(person)
        right_bank.append(person)
    return all(p in right_bank for p in left_bank)

def get_next_states(state):
    next_states = []
    possible_moves = [(p1, p2) for p1 in state.people for p2 in state.people if p1 != p2]
    for move in possible_moves:
        new_people = state.people[:]
        new_boat = state.boat[:]
        new_time = max(state.time, max(move))
        new_boat.extend(move)
        for person in move:
            new_people.remove(person)
        new_state = State(new_people, new_boat, new_time)
        if is_valid(new_state):
            next_states.append(new_state)
    return next_states

def bfs():
    start_state = State([1, 3, 6, 8, 12], [], 0)
    queue = deque([start_state])
    solutions = []
    while queue:
        current_state = queue.popleft()
        if current_state.time > 30:
            continue
        if not current_state.people:
            solutions.append(current_state)
            continue
        next_states = get_next_states(current_state)
        for next_state in next_states:
            queue.append(next_state)
    return solutions

solutions = bfs()
if solutions:
    print("Multiple solutions found within the time constraint:")
    for i, solution in enumerate(solutions, 1):
        print(f"Solution {i}:")
        print("Time taken:", solution.time, "seconds")
        print("People on the other side:", solution.boat)
        print()
else:
    print("No solutions found within the time constraint.")
