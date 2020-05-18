class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.visited_states=[init_state]

    def solve(self):
        #TODO
        # implement your search algorithm here

        #trivial case
        if(self.init_state==self.goal_state):
        	return None 


        source = Node(init_state)
        frontier = [source]
        while (len(frontier)!=0):
        	node = frontier.pop(0)

        	for neighbour in node.get_neighbours():
        		if (neighbour.state not in self.visited_states):
        			self.visited_states.append(neighbour.state)
        			if (neighbour.state==self.goal_state):
        				return self.terminate(neighbour)
        			frontier.append(neighbour)

        return ["UNSOLVABLE"] # sample output 

    def isequalStates(self,state1,state2):
    	for i in range(len(state1)):
    		for j in range(len(state2)):
    			if state1[i][j] != state2[i][j]:
    				return False
    	return True

    def isGoalState(self,state):
    	return self.isequalStates(self.goal_state,state)

    def visited_node(self,node):
    	for state in self.visited_states:
    		if (self.isequalStates(node.state,state)):
    			return True
    	return False

    def terminate(self,node):
    	output=[]
    	while(node.parent!=None):
    		output.insert(0,node.action)
    		node = node.parent
    	return output
    # you may add more functions if you think is useful



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

	def findBlank(self):
		(y,x) = (0,0)
		for i in range(self.dimension):
			for j in range(self.dimension):
				if self.state[i][j] == 0:
					return (i,j)
		print("There's no zero in the puzzle error")

	# Given a particular node, this method allows you to list all the neigihbours of the node
	def move(self,xsrc,ysrc,xdest,ydest):
		output = []
		for i in range(len(self.state)):
			list=[]
			for j in range(len(self.state)):
				list.append(self.state[i][j])
			output.append(list)
		output[xsrc][ysrc],output[xdest][ydest] = output[xdest][ydest],output[xsrc][ysrc]
		return output


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







#Dont copy the lines below to the actual file
init_state = [[5,2,1],[4,8,3],[7,6,0]]
goal_state = [[1, 2, 3],[4, 5,6],[7,8,0]]

puzzle = Puzzle(init_state,goal_state)
x=puzzle.solve()
print(x)







