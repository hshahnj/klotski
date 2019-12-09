GOAL_BLOCK = 'A'

# START_STATE = lambda: ["B", "A", "A", "C",
#                        "B", "A", "A", "C",
#                        "D", "E", "E", "F",
#                        "D", "G", "H", "F",
#                        "I", "_", "_", "J"]


START_STATE = lambda: ["E", "E", "_", "H",
                       "B", "G", "_", "C",
                       "B", "A", "A", "C",
                       "D", "A", "A", "F",
                       "D", "I", "J", "F"]


# id = id of CHARACTER
# x = top left starting x
# y = top left starting y
# w = how wide to the right
# h = how long to the bottom

# defining can move precond
class Object:
    def __init__(self, id, x, y, w, h):
        self.id = id
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    # Algorithm to determine whether we can move or not
    def can_move(self, state, direction):
        w = int(self.w)
        h = int(self.h)
        x = int(self.x)
        y = int(self.y)
        # MAXIMUM MOVEMENT

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
                        if state[4 * (y + i) + x + move] != "_":
                            return False
                    else:
                        return False
            else:
                for i in range(w):
                    if 0 <= y + move < 5:
                        if state[4 * (y + move) + (x + i)] != "_":
                            return False
                    else:
                        return False
            return True

        except (Exception) as e:
            print(e)


def goal_message(state):
    return "Solution found."


# Copies state -- used by Operators
def copy_state(state):
    new_state = list(state)
    return new_state


# deep equals check for two states
def DEEP_EQUALS(state1, state2):
    for i in range(len(state1)):
        if state1[i] != state2[i]:
            return False
    return True


# String representation
def printCurrentState(state):
    result = ""
    for row in range(5):
        result = result + "   "
        for col in range(4):
            result = result + (str(state[4 * row + col]) + " ")
        result = result + "\n"
    return result


# hashes the current state given such that all states
# are guaranteed to be unique
def HASHCODE(state):
    return printCurrentState(state)


class Operator:
    def __init__(self, name, precondition, state_transfer):
        self.name = name
        self.precondition = precondition
        self.state_transfer = state_transfer

    def is_applicable(self, state):
        return self.precondition(state)

    def apply(self, state):
        return self.state_transfer(state)


# movement function to move the tile into the right place
def move(state, tile, direction):
    # Based on the assumption it is legal to move and tile is available
    new_state = copy_state(state)
    current_index = tile.y * 4 + tile.x
    for width in range(tile.w):
        for height in range(tile.h):
            tile_index = int(current_index + width + height * 4)

            if direction == 3:
                new_state[tile_index + 4] = state[tile_index]
                if height == 0:
                    new_state[tile_index] = "_"

            elif direction == 1:
                new_state[tile_index - 4] = state[tile_index]
                if height == tile.h - 1:
                    new_state[tile_index] = "_"

            elif direction == 0:
                new_state[tile_index + 1] = state[tile_index]
                if width == 0:
                    new_state[tile_index] = "_"

            else:
                new_state[tile_index - 1] = state[tile_index]
                if width == tile.w - 1:
                    new_state[tile_index] = "_"
    return new_state


# determines whether or not the state is a goal state
# implying that 2x2 square is on the center bottom
def goal_test(state):
    return state[13] == GOAL_BLOCK and state[14] == GOAL_BLOCK and \
           state[17] == GOAL_BLOCK and state[18] == GOAL_BLOCK


# 1 = NORTH, 3 = SOUTH, 2 = WEST, 0 = EAST
#    1
# 2     0
#    3
def translate_direction(num):
    if num == 0:
        direction = 'east'
    elif num == 1:
        direction = 'north'
    elif num == 2:
        direction = 'west'
    else:
        direction = 'south'
    return direction


def can_move(state, piece, direction):
    return piece.can_move(state, direction)


# generates a combo list of tiles to direction and returns it
def combo_list():
    ls = []
    for tile in sorted(list(set(START_STATE()) - set(['_']))):
        for i in range(4):
            ls.append((tile, i))
    return ls


# Piece object generator
def make_piece(state, tile):
    index = state.index(tile)
    curr_col = index % 4
    curr_row = int(index / 4)

    shape = [1, 1]
    if state[(index + 1) % len(state)] == state[index]:  # finds the axb value
        shape[0] += 1
    if state[(index + 4) % len(state)] == state[index]:
        shape[1] += 1
    return Object(state[index], curr_col, curr_row, shape[0], shape[1])


getOperations = [Operator("Move tile " + str(tile) + " to the " + str(translate_direction(direction)),
                          lambda s, p=tile, q=direction: can_move(s, make_piece(s, p), q),
                          lambda s, p=tile, q=direction: move(s, make_piece(s, p), q))
                 for (tile, direction) in combo_list()]

goalTest = lambda s: goal_test(s)

goalMessage = lambda s: goal_message(s)


# Prefers adjacency criteria for blank spaces + totals up single # of tiles underneath lower Y of Goal Block A.
def heuristicFunction(s):
    goal_y = int(s.index(GOAL_BLOCK) / 4) + 1
    total = 0
    empty_index = int(s.index('_'))
    # check if edge case
    # First case shows that empty index is below so prioritized
    # Second case checks if the spaces are adjacent
    if ((empty_index + 1) % 4 != 0 and s[(empty_index + 1) % 4] != '_') or (s[(empty_index + 4) % 20] != '_'):
        total += 2

    for key in sorted(set(s) - set(['_'])):  # all tiles
        piece = make_piece(s, key)  # now you have piece object
        # starting coordinate Y of piece is lower than lower Y coordinate of Goal Block then increase heuristic
        if (piece.y > goal_y):
            total += piece.w * piece.h
    return int(total)


# define what kind of heuristic for import_sys privileges to run from command line
heuristic = {'heuristicFunction': heuristicFunction}


# useless
def render_state(s):
    return printCurrentState(s)


def describeCurrentState(state):
    result = ""
    for row in range(5):
        result = result + "   "
        for col in range(4):
            result = result + (str(state[4 * row + col]) + " ")
        result = result + "\n"
    return result
