## Question 4

def dfs(left_bank, right_bank, path, visited, curr_time, TOTAL_TIME, boat_position):
    if((curr_time >= TOTAL_TIME) or ((tuple(sorted(left_bank)), tuple(sorted(right_bank)), boat_position) in visited)):
        return

    visited.add((tuple(sorted(left_bank)), tuple(sorted(right_bank)), boat_position))

    if(not(left_bank)):
        print("Solution found:\n","\n".join(path))
        return

    if(boat_position == 'left'):
        for i, item1 in enumerate(left_bank):
            new_left_bank = left_bank[:]
            new_left_bank.remove(item1)

            dfs(new_left_bank, right_bank, path + [f"Move person with travel time {item1} second(s) to right bank"], visited, curr_time + item1, TOTAL_TIME, 'right')

            for j, item2 in enumerate(new_left_bank):
                if(item1 != item2):
                    new_left_bank_2 = new_left_bank[:]
                    new_left_bank_2.remove(item2)
                    new_right_bank = right_bank + [item1, item2]

                    dfs(new_left_bank_2, new_right_bank, path + [f"Move persons with travel times {item1} and {item2} second(s) to right bank"], visited, curr_time + max(item1, item2), TOTAL_TIME, 'right')

    else:
        for i, item1 in enumerate(right_bank):
            new_right_bank = right_bank[:]
            new_right_bank.remove(item1)

            dfs(left_bank + [item1], new_right_bank, path + [f"Move person with travel time {item1} second(s) to left bank"], visited, curr_time + item1, TOTAL_TIME, 'left')

            for j, item2 in enumerate(new_right_bank):
                if(item1 != item2):
                    new_right_bank_2 = new_right_bank[:]
                    new_right_bank_2.remove(item2)
                    new_left_bank = left_bank + [item1, item2]

                    dfs(new_left_bank, new_right_bank_2, path + [f"Move persons with travel time {item1} and {item2} second(s) to left bank"], visited, curr_time + max(item1, item2), TOTAL_TIME, 'left')

# Initial values
TOTAL_TIME = 30
left_bank = [1, 3, 6, 8, 12]
right_bank = []
visited = set()

# Start DFS
dfs(left_bank, right_bank, [], visited, 0, TOTAL_TIME, 'left')