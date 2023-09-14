from vacuum import VacuumAgent

class AkeehanVacuumAgent(VacuumAgent):

    def __init__(self):
        super().__init__()
        # visited will store all the plaecs I have been to
        self.visited = ([])
        # Used to tell where I am
        self.row = 0
        # Used to tell where I am
        self.col = 0
        # Keep track of next places to visit
        self.queue = []
        # Where I am am in the room
        self.pos = [0,0]
        # Last move made
        self.last_move = ""
        # Stores the direction of a bump if there is one
        self.bump_direction = "None"
        # Used to get me out of tight corners
        self.failed_moves = []
        # End condition
        self.turns_between_dirt = 0


    def program(self, percept):
        # End condition, so that it doesn't run forever
        if (self.turns_between_dirt >= 30):
            return 'NoOp'
        # If it spawns in a box, then end it
        elif(len(self.failed_moves) == 4):
            return 'NoOp'
        
        # If there is no bump, then rest failed moves
        if (percept[1] == "None"):
            self.failed_moves = []
            
        # Moving the position of the vacuum
        # Taking into account if there is a bump
        if (self.last_move == "Left" and percept[1] != 'Bump'):
            self.col = self.col - 1
        elif (self.last_move == "Right" and percept[1] != 'Bump'):
            self.col = self.col + 1
        elif (self.last_move == "Up" and percept[1] != 'Bump'):
            self.row = self.row + 1
        elif (self.last_move == "Down" and percept[1] != 'Bump'):
            self.row = self.row - 1;

        # pos stores the position of the vacuum
        self.pos = [self.row, self.col]

        # Adding nodes into visited
        # Taking into account whether the node is already in visited
        # ad whether the vacuum actually moved last turn
        if [self.row, self.col] not in self.visited and self.last_move != "NoOp" and self.last_move != "Suck":
            self.visited += ([self.col, self.row],)
        
        # If there is a bump, then store the direction into bump_direction
        if (percept[1] == 'Bump'):
                self.bump_direction = self.last_move
        
        # Checking if the vacuum hits a wall. If so, then add it to failed moves
        if self.bump_direction != "None":
            # Adding the direction to failed moves
            if self.bump_direction == "Left" and "Left" not in self.failed_moves:
                self.failed_moves.append("Left")
            elif self.bump_direction == "Up" and "Up" not in self.failed_moves:
                self.failed_moves.append("Up")
            elif self.bump_direction == "Right" and "Right" not in self.failed_moves:
                self.failed_moves.append("Right")
            elif self.bump_direction == "Down" and "Down" not in self.failed_moves:
                self.failed_moves.append("Down")
            
        # Storing the potential moves in these variables for ease of use
        left = [self.col - 1, self.row]
        right = [self.col + 1, self.row]
        up = [self.col, self.row + 1]
        down = [self.col, self.row - 1]
        
        # 0 = left
        # 1 = up
        # 2 = right
        # 3 = down
        # Adding elements to the queue if they have not been visited, 
        # if there isn't a wall, 
        # if there wasn't a failed move there, 
        # if the vacuum actually moved last turn,
        # and to remove infinte looping, don't go back where we just came from
        if left not in self.visited and self.bump_direction != "Left" and "Left" not in self.failed_moves and self.last_move != "Suck" and self.last_move != "Right":
            self.queue.append(0)
        if up not in self.visited and self.bump_direction != "Up" and "Up" not in self.failed_moves and self.last_move != "Suck" and self.last_move != "Down":
            self.queue.append(1)
        if right not in self.visited and self.bump_direction != "Right" and "Right" not in self.failed_moves and self.last_move != "Suck" and self.last_move != "Left":
            self.queue.append(2)
        if down not in self.visited and self.bump_direction != "Down" and "Down" not in self.failed_moves and self.last_move != "Suck" and self.last_move != "Up":
            self.queue.append(3)


        # Movement
        # First check if the square we are on is dirty. If so, then clean it
        if (percept[0] == "Dirty"):
            self.last_move = "Suck"
            # Reset turns between dirt, which is the end condition
            self.turns_between_dirt = 0
            return 'Suck'
        # Check if the vacuum is almost surrounded.
        # If so, then move whichever direction is not blocked
        # Increment turns between dirt for every move that is not sucking up dirt
        elif (len(self.failed_moves) == 3):
            if ("Left" not in self.failed_moves):
                self.last_move = "Left"   
                self.turns_between_dirt = self.turns_between_dirt + 1
                self.queue.pop()
                return 'Left'
            elif ("Up" not in self.failed_moves):
                self.last_move = "Up"   
                self.turns_between_dirt = self.turns_between_dirt + 1
                self.queue.pop()
                return 'Up'
            elif ("Right" not in self.failed_moves):
                self.last_move = "Right"   
                self.turns_between_dirt = self.turns_between_dirt + 1
                self.queue.pop()
                return 'Right'
            elif ("Down" not in self.failed_moves):
                self.last_move = "Down"   
                self.turns_between_dirt = self.turns_between_dirt + 1
                self.queue.pop()
                return 'Down'
        # "Normal" moves
        # Only move if the queue matches the direction,
        # There isn't a wall in the way,
        # and there wasn't a failed move in that direction
        elif (self.queue[len(self.queue) - 1] == 0 and self.bump_direction != "Left" and "Left" not in self.failed_moves):
            self.last_move = "Left"   
            self.turns_between_dirt = self.turns_between_dirt + 1
            self.queue.pop()
            return 'Left'
        elif (self.queue[len(self.queue) - 1] == 1 and self.bump_direction != "Up" and "Up" not in self.failed_moves):
            self.last_move = "Up"
            self.turns_between_dirt = self.turns_between_dirt + 1
            self.queue.pop()
            return 'Up'
        elif (self.queue[len(self.queue) - 1] == 2 and self.bump_direction != "Right" and "Right" not in self.failed_moves):
            self.last_move = "Right"
            self.queue.pop()
            self.turns_between_dirt = self.turns_between_dirt + 1
            return 'Right'
        elif (self.queue[len(self.queue) - 1] == 3 and self.bump_direction != "Down" and "Down" not in self.failed_moves):
            self.last_move = "Down"
            self.queue.pop()
            self.turns_between_dirt = self.turns_between_dirt + 1
            return 'Down'
        else:
            self.queue.pop()
            self.last_move = "NoOp"
            return 'NoOp'
