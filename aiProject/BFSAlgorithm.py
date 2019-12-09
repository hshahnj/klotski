import importlib
import sys

Algorithm = importlib.import_module(sys.argv[1])  # Import Module
startState = Algorithm.START_STATE()

# Algorithm = importlib.import_module('KlotskiStates')


print('\nBFS Algorithm')
iterationCount = None
backTrackingLinks = {}


def initializeBFS():
    startState = Algorithm.START_STATE()
    print("Starting State of the Puzzle: ")
    print(Algorithm.describeCurrentState(startState))

    global iterationCount, backTrackingLinks
    iterationCount = 0
    backTrackingLinks = {}
    startBFS(startState)
    print(str(iterationCount) + " states examined.")


def startBFS(startState):
    global iterationCount, backTrackingLinks

    openStates = [startState]
    closedStates = []
    backTrackingLinks[Algorithm.HASHCODE(startState)] = -1

    while openStates != []:
        currentState = openStates[0]
        del openStates[0]
        closedStates.append(currentState)

        if Algorithm.goalTest(currentState):
            print(Algorithm.goalMessage(currentState))
            backtrace(currentState)
            return

        iterationCount += 1
        if iterationCount % 32 == 0:
            print(".", end="")
            if iterationCount % 128 == 0:
                print("iterationCount = " + str(iterationCount))
                print("len(openStates) = " + str(len(openStates)))
                print("len(closedStates) = " + str(len(closedStates)))

        statesArray = []
        for op in Algorithm.getOperations:
            if op.precondition(currentState):
                newState = op.state_transfer(currentState)
                if not occurs_in(newState, closedStates) and openStates.count(newState) == 0:
                    statesArray.append(newState)
                    backTrackingLinks[Algorithm.HASHCODE(newState)] = currentState

        for states in statesArray:
            for index in range(len(openStates)):
                if Algorithm.DEEP_EQUALS(states, openStates[index]):
                    del openStates[index]
                    break;

        openStates = openStates + statesArray


def backtrace(state):
    global backTrackingLinks

    traceArray = []
    while not state == -1:
        traceArray.append(state)
        state = backTrackingLinks[Algorithm.HASHCODE(state)]

    traceArray.reverse()
    print("Traced Solution: ")
    for state in traceArray:
        print(Algorithm.describeCurrentState(state))
    return traceArray


def occurs_in(currentState, statesArray):
    for state in statesArray:
        if Algorithm.DEEP_EQUALS(currentState, state):
            return True
    return False


if __name__ == "__main__":
    initializeBFS()
