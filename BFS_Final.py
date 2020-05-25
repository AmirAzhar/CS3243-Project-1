# CS3243 Introduction to Artificial Intelligence
# Project 1: k-Puzzle

import os
import sys
import math
from collections import deque
# Running script on your own - given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt


class Node(object):
    # state is a list of lists representing the configuration of the puzzle
    # parent is reference to the state before the current state
    # action is what you did in the previous state to reach the current state.
    # location of zero in the puzzle as a tuple
    def __init__(self, state, parent=None, action=None, location=None,static_dimension=None):
        self.state = state
        self.parent = parent
        self.dimension = len(state)
        self.action = action
        self.location = location
        self.string = str(state)
        self.static_dimension = static_dimension

    #Find the blank/0 in a given state
    def findBlank(self):
        for i in range(self.dimension):
            if self.state[i] == 0:
                return i
        print("There's no zero in the puzzle error")

    #Given a particular node, this method allows you to list all the neigihbours of the node
    def move(self, xsrc, xdest):
        output = [i for i in self.state]
        output[xsrc], output[xdest] = output[xdest], output[xsrc]
        return output

    #Create the children/neighbours of a given node
    def get_neighbours(self):
        # UP,DOWN,LEFT,RIGHT

        new_states = []

        # get coordinate of the blank
        if (self.location == None):
            x = self.findBlank()
        else:
            x = self.location

        # tries to add the right movement
        if(x % self.static_dimension != 0  and  (x-1) >= 0):
            #print("RIGHT ") 
            #print(self.move(x-1 ,x))
            new_states.append(
                Node(self.move(x-1 ,x), self, "RIGHT", x-1,self.static_dimension))


        # tries to add the left movement
        if(x % self.static_dimension != self.static_dimension-1 and (x+1) < self.dimension):
            #print ("LEFT " )
            #print(self.move(x+1,x)) 
            new_states.append(
                Node(self.move(x+1,x), self, "LEFT", x+1,self.static_dimension))

        # tries to add the up movement
        if(x+self.static_dimension < self.dimension):
            #print("UP" + " ") 
            #print(self.move(x+self.static_dimension,x))
            new_states.append(
                Node(self.move(x+self.static_dimension, x), self, "UP", x+self.static_dimension,self.static_dimension))

        # tries add the down movement
        if(x-self.static_dimension >= 0):
            #print("DOWN"+ " ")
            #print(self.move(x-self.static_dimension, x) )
            new_states.append(
                Node(self.move(x-self.static_dimension, x), self, "DOWN",x-self.static_dimension,self.static_dimension))



        return new_states


class Puzzle(object):
    def __init__(self, init_state, goal_state):
        self.init_state = self.flatten_state(init_state)
        self.goal_state = self.flatten_state(goal_state)
        self.static_dimension = len(init_state)
        self.goalstringhash = hash(str(self.flatten_state(goal_state)))
        self.set=set()


    def flatten_state(self,state):
        output = []
        for list in state:
            output.extend(list)
        return output

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
        #if self.isSolvable(Node(self.init_state).state) == False:
        #    return ["UNSOLVABLE"]

        #Trivial case: if the init state is already a goal state
        source = Node(self.init_state,None,None,None,self.static_dimension)
        #trivial case
        if (hash(source.string)==self.goalstringhash):
            return None
        frontier = deque()
        frontier.append(source)
        while (len(frontier)>0):
            node = frontier.popleft()

            for neighbour in node.get_neighbours():
                if (neighbour.string not in self.set):
                    self.set.add(neighbour.string)
                    if (hash(neighbour.string)==self.goalstringhash):
                        return self.terminate(neighbour)
                    frontier.append(neighbour)
        return ["UNSOLVABLE"]

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







