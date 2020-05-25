# CS3243 Introduction to Artificial Intelligence
# Project 1: k-Puzzle

import os
import sys

# Running script on your own - given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.visited_states=[init_state]
        self.goalhash = Node(goal_state).hash
        self.hashTable = self.generateHashTable()

    def solve(self):
        #TODO
        # implement your search algorithm here

        
        source = Node(self.init_state)
        self.hashTable[source.hash] = 1 ## The source has been visited so mark it as 1
        #trivial case
        if (source.hash==self.goalhash):
            return None
        
        frontier = [source]
        while (len(frontier)!=0):
            node = frontier.pop(0)

            for neighbour in node.get_neighbours():
                if (self.hashTable[neighbour.hash]==0):
                    self.hashTable[neighbour.hash]=1
                    if (neighbour.hash==self.goalhash):
                        return self.terminate(neighbour)
                    frontier.append(neighbour)




        return ["UNSOLVABLE"] # sample output 


    def terminate(self,node):
        output=[]
        while(node.parent!=None):
            output.insert(0,node.action)
            node = node.parent
        return output
    # you may add more functions if you think is useful

    def generateHashTable(self):
        n = len(self.init_state)
        n *= n
        factorial = 1
        for i in range(1,n+1):
            factorial *= i
        return [0]*factorial




class Node(object):
    #state is a list of lists representing the configuration of the puzzle
    #parent is reference to the state before the current state
    #action is what you did in the previous state to reach the current state. 
    #location of zero in the puzzle as a tuple
    def __init__(self, state ,parent=None, action = None,location = None):
        self.state = state
        self.parent = parent
        self.dimension = len(state)
        self.action = action
        self.location = location
        self.hash = self.gethash()

    def findBlank(self):
        (y,x) = (0,0)
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.state[i][j] == 0:
                    return (i,j)
        print("There's no zero in the puzzle error")

    # Given a particular node, this method allows you to list all the neigihbours of the node and calculate
    def move(self,xsrc,ysrc,xdest,ydest):
        output = []
        for i in range(len(self.state)):
            list=[]
            for j in range(len(self.state)):
                list.append(self.state[i][j])
            output.append(list)
        output[xsrc][ysrc],output[xdest][ydest] = output[xdest][ydest],output[xsrc][ysrc]
        return output

    def gethash(self):
        temp = []
        total = 0
        for list in self.state:
            for i in list:
                temp.append(i)
        x = len(temp)
        for i in range(x-1):
            greater = 0
            y = x-i-1
            factorial = 1
            if (temp[i]==0):
                continue
            for j in range (i+1,x):
                factorial *= y
                y-=1
                if (temp[j]<temp[i]):
                    greater+=1
            total += greater * factorial
        return total 





    def get_neighbours(self):
        # UP,DOWN,LEFT,RIGHT

        new_states=[]

        #get coordinate of the blank
        if (self.location == None):
            (x,y) = self.findBlank()
        else:
            (x,y) = self.location

        #tries add the down movement
        if(y-1>=0):
            new_states.append(Node(self.move(x,y-1,x,y),self,"RIGHT",(x,y-1)))

        #tries to add the up movement
        if(y+1<self.dimension):
            new_states.append(Node(self.move(x,y+1,x,y),self,"LEFT",(x,y+1)))

        #tries to add the left movement
        if(x+1<self.dimension):
            new_states.append(Node(self.move(x+1,y,x,y),self,"UP",(x+1,y)))

        #tries to add the right movement
        if(x-1>=0):
            new_states.append(Node(self.move(x-1,y,x,y),self,"DOWN",(x-1,y)))
        
        return new_states



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







