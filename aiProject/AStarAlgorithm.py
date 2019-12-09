import importlib

# # #INIT
# Algorithm = importlib.import_module(sys.argv[1]) #Import Module
# heuristic_choice = sys.argv[2]
# print(Algorithm)
# print(type(Algorithm))
# print(heuristic_choice)


Algorithm = importlib.import_module("KlotskiStates")
heuristicChoice = "heuristicFunction"
startState = Algorithm.START_STATE()
heuristics = Algorithm.heuristic[heuristicChoice]

# Counting # of iterations
iterationCount = None

# To trace steps
backTrackingLinks = {}


def initializeAStar():
    print("Starting State of the Puzzle:")
    print(Algorithm.printCurrentState(startState))
    global iterationCount, backTrackingLinks
    iterationCount = 0
    backTrackingLinks = {}
    startAStar(startState)
    print(str(iterationCount) + " states examined.")


# iterates through initial state using A* with given hueristics
# to solve until goal state
def startAStar(startState):
    global iterationCount, backTrackingLinks

    openStates = [[startState, heuristics(startState)]]
    closedStates = []

    # print(initial_state)
    COST = {Algorithm.HASHCODE(startState): 0}

    backTrackingLinks[Algorithm.HASHCODE(startState)] = -1

    while openStates != []:
        S = openStates[0]
        del openStates[0]
        closedStates.append(S)

        if Algorithm.goalTest(S[0]):
            print(Algorithm.goalMessage(S[0]))
            backtrace(S[0])
            return

        iterationCount += 1
        if (iterationCount % 32) == 0:
            print(".", end="")
            if (iterationCount % 128) == 0:
                print("iterationCount = " + str(iterationCount))
                print("len(openStates)=" + str(len(openStates)))
                print("len(closedStates)=" + str(len(closedStates)))
        L = []

        # for each possible child in S (state)
        for op in Algorithm.getOperations:
            # is a child
            if op.precondition(S[0]):
                new_state = op.state_transfer(S[0])

                # index of occurrence in closedStates
                occur_closed = occurs_in(new_state, closedStates)

                # index of occurence in openStates
                occur_open = occurs_in(new_state, openStates)

                # the moves made so far + 1
                new_cost = COST[Algorithm.HASHCODE(S[0])] + 1
                # place in neighbor if new state
                if occur_closed == -1 and occur_open == -1:
                    L.append([new_state, heuristics(new_state)])
                    backTrackingLinks[Algorithm.HASHCODE(new_state)] = S[0]
                    COST[Algorithm.HASHCODE(new_state)] = new_cost

                elif occur_open > -1:
                    # check to see if this move is more efficient
                    if COST[Algorithm.HASHCODE(new_state)] > new_cost:
                        COST[Algorithm.HASHCODE(new_state)] = new_cost
                        openStates[occur_open] = [new_state, new_cost]

        openStates = L + openStates
        openStates.sort(key=lambda x: x[1])


# determines if the given state is equal to any of the state
# within the list and returns the index if it does exist
# otherwise, return -1 implying it wasn't found
def occurs_in(s1, lst):
    index = 0
    for s2 in lst:
        if Algorithm.DEEP_EQUALS(s1, s2[0]):
            return index
        else:
            index = index + 1
    return -1


def backtrace(S):
    global backTrackingLinks

    path = []
    while not S == -1:
        path.append(S)
        S = backTrackingLinks[Algorithm.HASHCODE(S)]
    path.reverse()
    print("Solution path: ")
    for s in path:
        print(Algorithm.describeCurrentState(s))
    return path


if __name__ == '__main__':
    initializeAStar()
