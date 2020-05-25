# CS3243 Introduction to Artificial Intelligence
# Project 1: k-Puzzle

import os
import sys
import math
from collections import deque


class Node(object):
    #State: list of lists representing the configuration of the puzzle
    #Parent: reference to the state before the current state
    #Action: what you did in the previous state to reach the current state.
    #Location: Position of zero in the puzzle as a tuple
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

    #List all the neigihbours of a given node
    def move(self, xsrc, xdest):
        output = [i for i in self.state]
        output[xsrc], output[xdest] = output[xdest], output[xsrc]
        return output

    #Create the children/neighbours of a given node
    def get_neighbours(self):
        
        new_states = []

        #Get coordinate of the blank
        if (self.location == None):
            x = self.findBlank()
        else:
            x = self.location

        #Tries to add the right movement
        if(x % self.static_dimension != 0  and  (x-1) >= 0):
            new_states.append(
                Node(self.move(x-1 ,x), self, "RIGHT", x-1,self.static_dimension))

        #Tries to add the left movement
        if(x % self.static_dimension != self.static_dimension-1 and (x+1) < self.dimension): 
            new_states.append(
                Node(self.move(x+1,x), self, "LEFT", x+1,self.static_dimension))

        #Tries to add the up movement
        if(x+self.static_dimension < self.dimension):
            new_states.append(
                Node(self.move(x+self.static_dimension, x), self, "UP", x+self.static_dimension,self.static_dimension))

        #Tries to add the down movement
        if(x-self.static_dimension >= 0):
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

    #Convert 2D array to 1D
    def flatten_state(self,state):
        output = []
        for list in state:
            output.extend(list)
        return output

    #Returns the list of actions once the goal state is found
    def terminate(self, node):
        output = []
        while(node.parent != None):
            output.insert(0, node.action)
            node = node.parent
        
        return output

    #BFS Implementation
    def solve(self):
        source = Node(self.init_state,None,None,None,self.static_dimension)
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







