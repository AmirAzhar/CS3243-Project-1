# CS3243 Introduction to Artificial Intelligence
# Project 1: k-Puzzle

import os
import sys
import math
import heapq
# Running script on your own - given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

class Node(object):
    # state is a list of lists representing the configuration of the puzzle
    # parent is reference to the state before the current state
    # action is what you did in the previous state to reach the current state.
    # location of zero in the puzzle as a tuple
    def __init__(self, state, parent=None, action=None, location=None,pathcost = None):
        self.state = state
        self.parent = parent
        self.dimension = len(state)
        self.action = action
        self.location = location
        self.string = str(state)
        self.pathcost = pathcost
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
                Node(self.move(x, y-1, x, y), self, "RIGHT", (x, y-1),self.pathcost + 1))

        # tries to add the up movement
        if(y+1 < self.dimension):
            new_states.append(
                Node(self.move(x, y+1, x, y), self, "LEFT", (x, y+1),self.pathcost+1))

        # tries to add the left movement
        if(x+1 < self.dimension):
            new_states.append(
                Node(self.move(x+1, y, x, y), self, "UP", (x+1, y),self.pathcost+1))

        # tries to add the right movement
        if(x-1 >= 0):
            new_states.append(
                Node(self.move(x-1, y, x, y), self, "DOWN", (x-1, y),self.pathcost+1))

        return new_states


class Puzzle(object):
    def __init__(self, init_state, goal_state):
        self.init_state = init_state
        self.goal_state = goal_state
        self.goalstringhash = hash(str(goal_state))
        self.set=set()

    def rowconflict(self,candidate_row,goal_row):
        x = len(candidate_row)
        total = 0
        while (True):
            conflicts = [0] * x
            conflictfound = False
            for index1,tile1 in enumerate(candidate_row):
                for index2,tile2 in enumerate(candidate_row):
                    if index1 == index2 or tile1 not in goal_row or tile2 not in goal_row or tile1 <= 0 or tile2 <= 0 :
                        continue
                    if (goal_row.index(tile1) > goal_row.index(tile2) and index1 < index2):
                        conflicts[index1] += 1
                        conflictfound = True
                    elif (goal_row.index(tile1)<goal_row.index(tile2) and index1 > index2):
                        conflicts[index1] += 1
                        conflictfound = True
            if not conflictfound:
                break
            i = conflicts.index(max(conflicts))
            candidate_row[i] = -1
            total +=1
        return total * 2

    def conflicts (self,candidate_state, goal_state):
        conflicts = 0
        for i in range(len(candidate_state)):
            conflicts += self.rowconflict(candidate_state[i][:],goal_state[i][:])
        transposed_candidate = [[candidate_state[j][i] for j in range(len(candidate_state))] for i in range(len(candidate_state[0]))] 
        transposed_goal = [[goal_state[j][i] for j in range(len(goal_state))] for i in range(len(goal_state[0]))]
        for i in range(len(candidate_state)):
            conflicts += self.rowconflict(transposed_candidate[i][:],transposed_goal[i][:])
        return conflicts


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
        
        return output

    def solve(self):
        source = Node(self.init_state,None,None,None,0)
        if self.isSolvable(source.state) == False:
            return ["UNSOLVABLE"]

        #Trivial case: if the init state is already a goal state
        frontier = []
        heapq.heapify(frontier)
        #trivial case
        if (hash(source.string)==self.goalstringhash):
            return None
        heap_item = (source.pathcost + source.getMD() + self.conflicts(source.state,self.goal_state),source)
        heapq.heappush(frontier,heap_item)
        while (len(frontier)>0):

            node = heapq.heappop(frontier)[1]
            for neighbour in node.get_neighbours():
                if (neighbour.string not in self.set):
                    self.set.add(neighbour.string)
                    if (hash(neighbour.string)==self.goalstringhash):
                        return self.terminate(neighbour)
                    heapq.heappush(frontier,(neighbour.pathcost+ neighbour.getMD()
                     + self.conflicts(neighbour.state,self.goal_state),neighbour))


if __name__ == "__main__":
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

