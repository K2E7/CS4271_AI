state = {'man': 'left', 'wolf': 'left', 'goat': 'left', 'cabbage': 'left'}
final_state={'man': 'right', 'wolf': 'right', 'goat': 'right', 'cabbage': 'right'}
import copy

# Define a function to check if the state is valid
def is_valid(state):
    if((state['goat'] == state['wolf']) and (state['man'] != state['wolf'])):
        return False
    if((state['goat'] == state['cabbage']) and (state['man'] != state['cabbage'])):
        return False
    return True

def find_moves(state):
    moves = [['man']]
    for objs in ['wolf','goat','cabbage']:
        if(state[objs] == state['man']):
            moves.append(['man',objs])
    #print(moves)
    return moves

def update_state(state, move):
    new_state = copy.deepcopy(state)
    for m1 in move:
        if(state[m1] == 'left'):
            new_state[m1] = 'right'
        else:
            new_state[m1] = 'left'
    if is_valid(new_state):
        return new_state
    else:
        return False

# use backtracking to find the solution to get from state to final_state using the moves
def solve(state, final_state, moves):
    if(state == final_state):
        return True
    else:
        for move in moves:
            new_state = update_state(state,move)
            if new_state and new_state not in stateL:  # avoid loops
                stateL.append(new_state)
                new_moves = find_moves(new_state)  # find the moves from the new state
                if solve(new_state,final_state,moves):
                    return True
        return False

stateL=[state]
solve(state,final_state,find_moves(state))
for state1 in stateL:
    print(state1)