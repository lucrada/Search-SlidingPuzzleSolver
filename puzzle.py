class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def empty(self):
        return (len(self.frontier) == 0)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def remove(self):
        if self.empty():
            raise Exception("Frontier is empty")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class QueueFrontier(StackFrontier):
    def remove(self):
        node = self.frontier[0]
        self.frontier = self.frontier[1:]
        return node

class Puzzle:
    def __init__(self, filename):
        self.solutions = None

        with open(filename) as f:
            contents = f.read()

        contents = contents.splitlines()
        contents = [list(line) for line in contents]
        self.dimension = int(len(contents) / 2)
        if self.dimension != max(len(line) for line in contents):
            raise Exception("Puzzle dimension should be the same")
        self.start = contents[:self.dimension]
        self.goal = contents[self.dimension:]

    def printPuzzle(self):
        print()
        print("Starting state:")
        print()
        for i in range(self.dimension):
            for j in range(self.dimension):
                print(self.start[i][j], end='')
            print()
        print()
        print("Ending state:")
        print()
        for i in range(self.dimension):
            for j in range(self.dimension):
                print(self.goal[i][j], end='')
            print()

    def getPossibleActions(self, state):
        hi = hj = 0
        for i in range(self.dimension):
            for j in range(self.dimension):
                if state[i][j] == ' ':
                    hi = i
                    hj = j
        if hi != self.dimension-1:
            up = list(state)
            up[hi] = [up[hi+1][hj] if item == up[hi][hj] else item for item in up[hi]]
            up[hi+1] = [' ' if item == up[hi+1][hj] else item for item in up[hi+1]]
        else:
            up = None
        if hi != 0:
            down = list(state)
            down[hi] = [down[hi-1][hj] if item == down[hi][hj] else item for item in down[hi]]
            down[hi-1] = [' ' if item == down[hi-1][hj] else item for item in down[hi-1]]
        else:
            down = None
        if hj != self.dimension-1:
            left = [list(line) for line in list(state)]
            left[hi][hj] = left[hi][hj+1]
            left[hi][hj+1] = ' '
        else:
            left = None
        if hj != 0:
            right = [list(line) for line in list(state)]
            right[hi][hj] = right[hi][hj-1]
            right[hi][hj-1] = ' '
        else:
            right = None
        candidates = [
            ("up", up),
            ("right", right),
            ("down", down),
            ("left", left)
        ]
        results = []
        for action, corr_state in candidates:
            if corr_state is not None:
                results.append((action, corr_state))
        return results

    def printSol(self):
        print("Starting state: ")
        print()
        for line in self.start:
            print(line)
            print()
        print()
        for action, state in self.solutions:
            for i in range(len(action)):
                print(action[i])
                print()
                for line in state[i]:
                    print(line)
                    print()
                print()

    def solve(self):
        frontier = QueueFrontier()
        init_node = Node(self.start, None, None)
        frontier.add(init_node)
        self.explored_states = []
        print("Solving...")
        print()
        while True:
            if frontier.empty():
                raise Exception("No solution possible")
            node = frontier.remove()
            if node.state == self.goal:
                action = []
                state = []
                while node.parent is not None:
                    action.append(node.action)
                    state.append(node.state)
                    node = node.parent
                action.reverse()
                state.reverse()
                self.solutions = [(action, state)]
                print("-------------------------------------")
                print()
                self.printSol()
                print()
                print("Solution found!")
                print()
                return
            self.explored_states.append(node.state)
            for action, corr_state in self.getPossibleActions(node.state):
                if corr_state not in self.explored_states and not frontier.contains_state(node.state):
                    new_node = Node(corr_state, node, action)
                    frontier.add(new_node)

import sys
p = Puzzle(sys.argv[1])
print()
p.solve()

