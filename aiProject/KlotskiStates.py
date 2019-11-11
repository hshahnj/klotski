
GOAL_BLOCK = 'A'
CREATE_INITIAL_STATE = lambda : ["B", "A", "A", "C",
                                 "B", "A", "A", "C",
                                 "D", "E", "E", "F",
                                 "D", "G", "H", "F",
                                 "I", "_", "_", "J"]
#</INITIAL_STATE>



# id = ALPHA_CHAR
# x = top left starting x
# y = top left starting y
# w = how wide to the right
# h = how long to the bottom

# defining can move precond
class Piece:
    # constructor
    def __init__(self, id, x, y, w, h):
        self.id = id
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    # string representation of the piece
    # for DEBUG purposes
    def __str__(self):
        return self.id + " " + str(int(self.x)) + " " + str(int(self.y)) \
        + " " + str(int(self.w)) + " " + str(int(self.h))

    # Algorithm to determine whether we can move or not
    # precond defining whether or not this piece can move in a certain
    # direction given a current state
    def can_move(self, state, direction):
        w = int(self.w)
        h = int(self.h)
        x = int(self.x)
        y = int(self.y)
        #MAXIMUM MOVEMENT
        try:
            move = 1
            if direction == 1 or direction == 2:
                move = -1
            if direction == 0:
                move += w - 1
            if direction == 3:
                move += h - 1
            if direction % 2 == 0:
                for i in range(h):
                    if 0 <= x + move < 4:
                        if state[4*(y + i) + x + move] != "_":
                            return False
                    else:
                        return False
            else:
                for i in range(w):
                    if 0 <= y + move < 5:
                        if state[4*(y + move) + (x + i)] != "_":
                            return False
                    else:
                        return False
            return True

        except (Exception) as e:
            print(e)



# returns a message when the goal is reached
def goal_message(s):
    return "Solved!"



# Performs an appropriately deep copy of a state,
# for use by operators in creating new states.
def copy_state(s):
    new_state = list(s)
    return new_state

# determines whether or not the two states are indentical by value
def DEEP_EQUALS(s1, s2):
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            return False
    return True


# string representation of the state of the game as shown:
# A B B C
# A B B C
# D E E F
# D G H F
# I _ _ J
def printCurrentState(state):
    result = ""
    for row in range(5):
        result = result + "   "
        for col in range (4):
            result = result + (str(state[4 * row + col]) + " ")
        result = result + "\n"
    return result


# hashes the current state given such that all states
# are guaranteed to be unique
def HASHCODE(state):
    return printCurrentState(state)



class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)

#WIP
def move(s, tile, dir):
    
      #Based on the assumption it is legal to move and tile is available
    new_state = copy_state(s)

    return new_state


# determines whether or not the state is a goal state
# implying that 2x2 square is on the center bottom
def goal_test(state):
    return state[13] == GOAL_BLOCK and state[14] == GOAL_BLOCK and \
           state[17] == GOAL_BLOCK and state[18] == GOAL_BLOCK



#    1
# 2     0
#    3
def translate_dir(num):
    dir = ''
    if num == 0:
        dir = 'east'
    elif num == 1:
        dir = 'north'
    elif num == 2:
        dir = 'west'
    else:
        dir = 'south'
    return dir



def can_move(s, piece, direction):
    return piece.can_move(s, direction)



# creates a list of all possible combinations of tiles to
# direction = (0, 1, 2, 3) and returns it
def combo_list():
    ls = []
    for tile in sorted(list(set(CREATE_INITIAL_STATE()) - set(['_']))):
        for i in range(4):
            ls.append((tile, i))
    return ls


# makes a piece object given a tile and the state locating that tile
# and returns it
def make_piece(state, tile):
    index = state.index(tile)
    curr_col = index % 4
    curr_row = int(index / 4)

    shape = [1,1]
    if state[(index + 1)%len(state)] == state[index]: #finds the axb value
        shape[0] += 1
    if state[(index + 4)%len(state)] == state[index]:
        shape[1] += 1
    return Piece(state[index], curr_col, curr_row, shape[0], shape[1])



#<OPERATORS>
OPERATORS = [Operator("Move tile " + str(tile) + " to the " + str(translate_dir(direction)),
                      lambda s, p=tile, q=direction: can_move(s, make_piece(s, p), q),
                      lambda s, p=tile, q=direction: move(s, make_piece(s, p), q))
             for (tile, direction) in combo_list()]
#</OPERATORS>


#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>


#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>



# totals up the number of tile square beneath the goal block
# including whether or not the empty spaces are adjacent
# and returns that value
def heuristicFunction(s):
    goal_y = int(s.index(GOAL_BLOCK) / 4) + 1
    total = 0
    empty_index = int(s.index('_'))
    #check if edge case
    #First case shows that empty index is below so prioritized
    #Second case checks if the spaces are adjacent
    #Not perfect yet
    if ((empty_index+1)%4 != 0 and s[(empty_index+1)%4] != '_') or (s[(empty_index + 4) % 20] != '_'):
        total += 2

    for key in sorted(set(s) - set(['_'])): #all tiles
        piece = make_piece(s, key) #now you have piece object
        if (piece.y > goal_y):
            total += piece.w * piece.h
    return int(total)



HEURISTICS = {'heuristicFunction':heuristicFunction}


def render_state(s):
    return printCurrentState(s)