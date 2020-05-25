# CS3243 Introduction to Artificial Intelligence
# Project 1: k-Puzzle

import os
import sys
from queue import *
import copy

# Running script on your own - given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

class Node(object):
    def __init__(self, puzzle, parent=None, action=None):
        self.puzzle = puzzle
        self.action = action
        self.parent = parent
    
    #Create a copy of the puzzle
    def duplicatePuzzle(self):
        copy = []
        for i in range(len(self.puzzle)):
            temp = []
            for j in range(len(self.puzzle)):
                temp.append(self.puzzle[i][j])
            copy.append(temp)
        return copy

    #Find the 0 in the puzzle
    def findBlank(self, puzzle):
        (y,x) = (0,0)
        for i in range(len(puzzle)):
            for j in range(len(puzzle)):
                if puzzle[i][j] == 0:
                    (y, x) = (i, j)
                    print("The blank is in", (y,x))
        print("")
        return (y,x)

    #Swap a 0 with an adjacent tile
    def swapTile(self, puzzle, tile1, tile2):
        (y1,x1) = tile1
        (y2,x2) = tile2

        print("Swapping tile", (y1,x1), "with tile", (y2,x2))
        print("Swapping tile value", puzzle[y1][x1], "with tile value", puzzle[y2][x2])
        print("")

        temp = puzzle[y1][x1]
        puzzle[y1][x1] = puzzle[y2][x2]
        puzzle[y2][x2] = temp


    #Create children for a given state/node
    def createChildren(self, currNode):
        children = []
        (y,x) = self.findBlank(self.puzzle)

        #up, down, left and right
        actions = [(y-1, x), (y+1, x), (y, x-1), (y, x+1)] 
        
        for action in range(len(actions)):
            canMove = False
            (y1, x1) = actions[action]
            #Blank can be moved UP or DOWN
            if (action == 0 and y > 0):
                canMove = True
            elif (action == 1 and y < (len(self.puzzle) - 1)):
                canMove = True
            #Blank can be moved LEFT or RIGHT
            elif (action == 2 and x > 0):
                canMove = True
            elif (action == 3 and x < (len(self.puzzle) - 1)):
                canMove = True
            #If blank can be swapped, create new child node where the blank tile is swapped with the adjacent tile
            if canMove == True:
                tempPuzzle = self.duplicatePuzzle()
                self.swapTile(tempPuzzle, (y,x), (y1,x1))
                newChild = Node(tempPuzzle, currNode, action)
                children.append(newChild)
        return children 

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = []
    
    #Check if current state is goal state
    def isGoalState(self, puzzle):
        if puzzle == self.goal_state:
            return True

    #Once goal is found, backtrack to parent and collate the steps
    def backtrack(self,currNode):
        while currNode.puzzle != init_state:
            if currNode.action == 0:
                movement = 'UP'
            elif currNode.action == 1:
                movement = 'DOWN'
            elif currNode.action == 2:
                movement = 'LEFT'
            else:
                movement = 'RIGHT'
            self.actions.append(movement)
            currNode = currNode.parent
        print("It took", len(self.actions), "steps to solve")
        return self.actions
        
    #Print puzzle for debugging
    def printPuzzle(self,puzzle):
        print("")
        for i in range(len(puzzle)):
            for j in range(len(puzzle)):
                print (puzzle[i][j], " ", end = '')
            print ("")
        print("")

    #Solve the puzzle
    def solve(self):
        # Goal test first node if it is alr solved
        currNode = Node(self.init_state)

        # if not self.isSolvable(currNode.puzzle):
        #     self.actions.append("Puzzle is unsolvable!")
        #     return self.actions

        if self.isGoalState(currNode.puzzle):
            self.actions.append("Puzzle already solved!")
            return self.actions

        #Initialize a frontier with currNode and explored set
        explored = []
        frontier = Queue()
        frontier.put(currNode)
        exploredNodes = 0

        #Loop until goal is found
        while exploredNodes <= 500:
            if frontier.empty():
               return "Empty Frontier!"
            currNode = frontier.get()
            self.printPuzzle(currNode.puzzle)
            for child in currNode.createChildren(currNode):
                if child.puzzle not in explored:
                    if self.isGoalState(currNode.puzzle):
                        return self.backtrack(currNode)
                    explored.append(currNode.puzzle)
                    exploredNodes += 1
                    frontier.put(child)
        return "Took too long"

if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    #Open() takes in file name and mode -> r is Read
    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")
    
    #Returns a list containing each line in the file as a list item
    lines = f.readlines()
    
    # n = num rows in input file
    n = len(lines)
    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]
    
    #Creating the init_state based on input file
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
    

    #Create the goal state, where 0 is in the last tile
    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    #Open() takes in file name and mode -> a is append
    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')
        os.startfile(sys.argv[2])
        







