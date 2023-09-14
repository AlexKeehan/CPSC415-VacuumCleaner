from vacuum import VacuumAgent
from collections import deque as queue
import random


class AkeehanVacuumAgent(VacuumAgent):

    def __init__(self):
        super().__init__()
        self.visited = ([])
        self.row = 0
        self.col = 0
        self.queue = []
        self.pos = [0,0]
        self.last_move = ""
        self.bump_direction = "None"
        self.failed_moves = []
        self.counter = 0
        self.sucked_dirt = 0
        self.turns_between_dirt = 0


    def program(self, percept):
        #print("Counter: " + str(self.counter))
        #print("Sucked dirt: " + str(self.sucked_dirt))
        if (self.turns_between_dirt >= 15):
            return 'NoOp'
        #if (self.sucked_dirt >= 30 or self.counter >=75):
         #   return 'NoOp'
        print("Failed moves")
        print(self.failed_moves)
        
        if (percept[1] == "None"):
            self.failed_moves = []
            
        
        if (self.last_move == "Left" and percept[1] != 'Bump'):
            self.col = self.col - 1
        elif (self.last_move == "Right" and percept[1] != 'Bump'):
            self.col = self.col + 1
        elif (self.last_move == "Up" and percept[1] != 'Bump'):
            self.row = self.row + 1
        elif (self.last_move == "Down" and percept[1] != 'Bump'):
            self.row = self.row - 1;

        self.pos = [self.row, self.col]
        #if [self.row, self.col] not in self.visited and self.last_move != "NoOp" and self.last_move != "Suck":
        if (percept[1] == "Bump"):
            self.visited += ([self.col, self.row],)
        

        if (percept[1] == 'Bump'):
                self.bump_direction = self.last_move
        
        if self.bump_direction != "None":
            if self.bump_direction == "Left" and "Left" not in self.failed_moves:
                self.failed_moves.append("Left")
            elif self.bump_direction == "Up" and "Up" not in self.failed_moves:
                self.failed_moves.append("Up")
            elif self.bump_direction == "Right" and "Right" not in self.failed_moves:
                self.failed_moves.append("Right")
            elif self.bump_direction == "Down" and "Down" not in self.failed_moves:
                self.failed_moves.append("Down")
            
        
        
        left = [self.col - 1, self.row]
        right = [self.col + 1, self.row]
        up = [self.col, self.row + 1]
        down = [self.col, self.row - 1]
       
        if (self.last_move == "Left"):
            self.queue.append(2)
        elif (self.last_move == "Up"):
            self.queue.append(3)
        elif (self.last_move == "Right"):
            self.queue.append(0)
        elif (self.last_move == "Down"):
            self.queue.append(1)
        
        # 0 = left
        # 1 = up
        # 2 = right
        # 3 = down
        if left not in self.visited and self.bump_direction != "Left" and "Left" not in self.failed_moves and self.last_move != "Suck" and self.last_move != "Right":
            self.queue.append(0)
        if up not in self.visited and self.bump_direction != "Up" and "Up" not in self.failed_moves and self.last_move != "Suck" and self.last_move != "Down":
            self.queue.append(1)
        if right not in self.visited and self.bump_direction != "Right" and "Right" not in self.failed_moves and self.last_move != "Suck" and self.last_move != "Left":
            self.queue.append(2)
        if down not in self.visited and self.bump_direction != "Down" and "Down" not in self.failed_moves and self.last_move != "Suck" and self.last_move != "Up":
            self.queue.append(3)
         
        i = 0
        while i < len(self.queue):
            print(self.queue[i])
            i = i + 1
        

        if (percept[0] == "Dirty"):
            self.last_move = "Suck"
            self.turns_between_dirt = 0
            return 'Suck'
        if (self.queue[len(self.queue) - 1] == 0 and self.bump_direction != "Left" and "Left" not in self.failed_moves):
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
