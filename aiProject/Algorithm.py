import sys
import importlib


#INIT
Problem = importlib.import_module(sys.argv[1]) #Import Module
heuristic_choice = sys.argv[2]
Initial_state = Problem
init_state = Initial_state.CREATE_INITIAL_STATE()
heuristics = Problem.HEURISTICS[heuristic_choice]

#Counting # of iterations
COUNT = None

#To trace steps
BACKLINKS = {}

def runAStar():
    print("Initial State:")
    print(Problem.printCurrentState(init_state))
    global COUNT, BACKLINKS
    COUNT = 0
    BACKLINKS = {}
    IterateAStar(init_state)
    print(str(COUNT)+" states examined.")


# iterates through initial state using A* with given hueristics
# to solve until goal state
def IterateAStar(initial_state):
    global COUNT, BACKLINKS

    OPEN = [[initial_state, heuristics(initial_state)]]
    CLOSED = []

    # print(initial_state)
    COST = {Problem.HASHCODE(initial_state): 0}

    BACKLINKS[Problem.HASHCODE(initial_state)] = -1

    while OPEN != []:
        S = OPEN[0]
        del OPEN[0]
        CLOSED.append(S)

        if Problem.GOAL_TEST(S[0]):
            print(Problem.GOAL_MESSAGE_FUNCTION(S[0]))
            backtrace(S[0])
            return

#TEMPORARY COUNTING AND PRINTING MEASURE
        COUNT += 1
        if (COUNT % 32)==0:
            # print(".",end="")
            if (COUNT % 128)==0:
                print("COUNT = "+str(COUNT))
                print("len(OPEN)="+str(len(OPEN)))
                print("len(CLOSED)="+str(len(CLOSED)))
        L = []
###############################################
        # for each possible child in S (state)
        for op in Problem.OPERATORS:
            # is a child
            if op.precond(S[0]):
                new_state = op.state_transf(S[0])

#                 # index of occurrence in CLOSED
#                 occur_closed = occurs_in(new_state, CLOSED)

#                 # index of occurence in OPEN
#                 occur_open = occurs_in(new_state, OPEN)

#                 # the moves made so far + 1
#                 new_cost = COST[Problem.HASHCODE(S[0])] + 1
#                 # place in neighbor if new state
#                 if occur_closed == -1 and occur_open == -1:
#                     L.append([new_state, heuristics(new_state)])
#                     BACKLINKS[Problem.HASHCODE(new_state)] = S[0]
#                     COST[Problem.HASHCODE(new_state)] = new_cost

#                 elif occur_open > -1:
#                     # check to see if this move is more efficient
#                     if COST[Problem.HASHCODE(new_state)] > new_cost:
#                         COST[Problem.HASHCODE(new_state)] = new_cost
#                         OPEN[occur_open] = [new_state, new_cost]


        # OPEN = L + OPEN
        # OPEN.sort(key=lambda x: x[1])

# determines if the given state is equal to any of the state
# within the list and returns the index if it does exist
# otherwise, return -1 implying it wasn't found
def occurs_in(s1, lst):
    index = 0
    for s2 in lst:
        if Problem.DEEP_EQUALS(s1, s2[0]):
            return index
        else:
            index = index + 1
    return -1


def backtrace(S):
    global BACKLINKS

    path = []
    while not S == -1:
        path.append(S)
        S = BACKLINKS[Problem.HASHCODE(S)]
    path.reverse()
    print("Solution path: ")
    for s in path:
        print(Problem.DESCRIBE_STATE(s))
    return path   


if __name__=='__main__':
    runAStar()