## CS3243 Introduction to Artificial Intelligence
# Project 1: k-Puzzle

import os
import sys
import math
from collections import deque
from Queue import PriorityQueue #use Queue when putting in codepost since it runs python 2.7, use queue for python 3 and above
import time

# Running script on your own - given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

#Class used for Priority Queue
class PriorityEntry(object):
    def __init__(self, priority, data):
        self.data = data
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

class Node(object):
    # state is a list of lists representing the configuration of the puzzle
    # parent is reference to the state before the current state
    # action is what you did in the previous state to reach the current state.
    # location of zero in the puzzle as a tuple
    def __init__(self, state, parent=None, action=None, location=None):
        self.state = state
        self.parent = parent
        self.dimension = len(state)
        self.action = action
        self.location = location
        self.string = str(state)
        self.pathCost = 0

    #Get Manhattan Distance heuristic
    def getMD(self):
        totalDist = 0
        size = len(self.state)
        for i in range(0, size):
            for j in range(0, size):
                num = self.state[i][j]
                if num != 0:
                    actualRow = (num - 1) // size
                    actualCol = (num - 1) % size
                    rowDiff = abs(actualRow - i)
                    colDiff = abs(actualCol - j)
                    currDist = colDiff + rowDiff
                    totalDist += currDist
        return totalDist

    #Get Linear Conflict heuristic
    def getLC(self):
        size = len(self.state)
        rowPos = [0] * (size**2)
        colPos = [0] * (size**2)
        totalConflicts = 0
        
        #Fill up the 1D array with the index's corresponding row and col pos eg. rowTiles[1] and colTiles[1] will hold the y nd x coordinates of the goal tile, respectively
        for i in range(0, size):
            for j in range(0, size):
                num = self.state[i][j]
                if num != 0:
                    actualRow = (num - 1) // size
                    actualCol = (num - 1) % size
                    rowPos[num] = actualRow
                    colPos[num] = actualCol

        #Calculate row conflicts
        for row in range(size):
            for currTile in range(size):
                # (1) compTile goal to the right of currTile goal
                for compTile in range(currTile+1, size):
                    # (2) Both tiles on the same line
                    # (3) currTile is to the right of comparingTile
                    # (4) Goal positions are both in that line
                    if rowPos[self.state[row][currTile]] == rowPos[self.state[row][compTile]] and colPos[self.state[row][currTile]] > colPos[self.state[row][compTile]]and row == rowPos[self.state[row][currTile]]:
                        totalConflicts += 1

        #Calculate col conflicts (repeat)
        for col in range(size):
            for currTile in range(size):
                # (1) compTile goal to the right of currTile goal
                for compTile in range(currTile+1, size):
                    # (2) Both tiles on the same line
                    # (3) currTile is to the right of comparingTile
                    # (4) Goal positions are both in that line
                    if colPos[self.state[currTile][col]] == colPos[self.state[compTile][col]] and rowPos[self.state[currTile][col]] > rowPos[self.state[compTile][col]]and row == colPos[self.state[currTile][col]]:
                        totalConflicts += 1
        
        #Return h(s) = MD(s) + LC(s)  (where LC(s) is totalConflicts*2)
        return totalConflicts*2 + self.getMD()
        


    #Find the blank/0 in a given state
    def findBlank(self):
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.state[i][j] == 0:
                    return (i, j)
        print("There's no zero in the puzzle error")

    #Given a particular node, this method allows you to list all the neigihbours of the node
    def move(self, xsrc, ysrc, xdest, ydest):
        output = [row[:] for row in self.state]
        output[xsrc][ysrc], output[xdest][ydest] = output[xdest][ydest], output[xsrc][ysrc]
        return output

    #Create the children/neighbours of a given node
    def get_neighbours(self):
        # UP,DOWN,LEFT,RIGHT

        new_states = []

        # get coordinate of the blank
        if (self.location == None):
            (x, y) = self.findBlank()
        else:
            (x, y) = self.location

        # tries add the down movement
        if(y-1 >= 0):
            new_states.append(
                Node(self.move(x, y-1, x, y), self, "RIGHT", (x, y-1)))

        # tries to add the up movement
        if(y+1 < self.dimension):
            new_states.append(
                Node(self.move(x, y+1, x, y), self, "LEFT", (x, y+1)))

        # tries to add the left movement
        if(x+1 < self.dimension):
            new_states.append(
                Node(self.move(x+1, y, x, y), self, "UP", (x+1, y)))

        # tries to add the right movement
        if(x-1 >= 0):
            new_states.append(
                Node(self.move(x-1, y, x, y), self, "DOWN", (x-1, y)))

        return new_states


class Puzzle(object):
    def __init__(self, init_state, goal_state):
        self.init_state = init_state
        self.goal_state = goal_state
        self.visited_states = [init_state]
        self.goalstringhash = hash(str(goal_state))
        self.set=set()

    #Check if a puzzle is solvable
    def isSolvable(self, state):
        inversions = 0
        singleDim = []
        (y, x) = (0, 0)

        #Calculate the number of inversions in a given state
        for i in range(0, len(state)):
            for j in range(0, len(state)):
                singleDim.append(state[i][j])
                if state[i][j] == 0:
                    (y, x) = (i, j)
        for i in range(0, len(singleDim)-1):
            for j in range(i+1, len(singleDim)):
                if singleDim[j] and singleDim[i] and singleDim[i] > singleDim[j]:
                    inversions += 1

        #If there is an odd no. of states
        if len(state) % 2 == 1:
            #Solvable if there is an even no. of inversions
            if (inversions % 2) == 0:
                return True
            else:
                return False

        #If there is an even no. of states
        else:
            #Solvable if blank is (1) on even row counting from bottom and inversions is odd or (2) odd row counting from bottom and inversions is even
            if (y % 2 == 0 and inversions % 2 == 1) or \
               (y % 2 == 1 and inversions % 2 == 0):
                return True
            else:
                return False


    #Returns the list of actions once the goal state is found
    def terminate(self, node):
        output = []
        while(node.parent != None):
            output.insert(0, node.action)
            node = node.parent
            
        print("The puzzle was solved in", len(output), "steps!")
        return output

    #Solving using Linear Conflict heuristic
    def solve(self):
        if self.isSolvable(Node(self.init_state).state) == False:
            return ["UNSOLVABLE"]

        source = Node(self.init_state)

        #Trivial case: if the init state is already a goal state
        if (hash(source.string)==self.goalstringhash):
            return None
        frontier = PriorityQueue()
        frontier.put(PriorityEntry(source.getLC(),source))

        while (not frontier.empty()):
            node = frontier.get().data
            for neighbour in node.get_neighbours():
                neighbour.pathCost = node.pathCost + 1
                if (neighbour.string not in self.set):
                    self.set.add(neighbour.string)
                    if (hash(neighbour.string)==self.goalstringhash):
                        return self.terminate(neighbour)
                    evaluation = neighbour.pathCost + neighbour.getLC()
                    frontier.put(PriorityEntry(evaluation, neighbour))
        
        return ["UNSOLVABLE"]


if __name__ == "__main__":
    start_time = time.time()
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    lines = f.readlines()
    
    # n = num rows in input file
    n = len(lines)
    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]
    

    i,j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number , base = 10)
            if  0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')
    
    end_time = time.time()
    print("It took", end_time-start_time, "seconds!")