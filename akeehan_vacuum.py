from vacuum import VacuumAgent
from collections import deque as queue
import random


class AkeehanVacuumAgent(VacuumAgent):

    def __init__(self):
        super().__init__()
        self.grid = (
                        [-10, 10], [-9,10],[-8,10],[-7,10],[-6,10],[-5,10],[-4,10],[-3,10],[-2,10],[-1,10],
                        [0,10],[1,10],[2,10],[3,10],[4,10],[5,10],[6,10],[7,10],[8,10],[9,10],[10,10],
                        [-10,9],[-9,9],[-8,9],[-7,9],[-6,9],[-5,9],[-4,9],[-3,9],[-2,9],[-1,9],
                        [0,9],[1,9],[2,9],[3,9],[4,9],[5,9],[6,9],[7,9],[8,9],[9,9],[10,9],
                        [-10,8],[-9,8],[-8,8],[-7,8],[-6,8],[-5,8],[-4,8],[-3,8],[-2,8],[-1,8],
                        [0,8],[1,8],[2,8],[3,8],[4,8],[5,8],[6,8],[7,8],[8,8],[9,8],[10,8],
                        [-10,7],[-9,7],[-8,7],[-7,7],[-6,7],[-5,7],[-4,7],[-3,7],[-2,7],[-1,7],
                        [0,7],[1,7],[2,7],[3,7],[4,7],[5,7],[6,7],[7,7],[8,7],[9,7],[10,7],
                        [-10,6],[-9,6],[-8,6],[-7,6],[-6,6],[-5,6],[-4,6],[-3,6],[-2,6],[-1,6],
                        [0,6],[1,6],[2,6],[3,6],[4,6],[5,6],[6,6],[7,6],[8,6],[9,6],[10,6],
                        [-10,5],[-9,5],[-8,5],[-7,5],[-6,5],[-5,5],[-4,5],[-3,5],[-2,5],[-1,5],
                        [0,5],[1,5],[2,5],[3,5],[4,5],[5,5],[6,5],[7,5],[8,5],[9,5],[10,5],
                        )
        self.visited = ([])
        self.row = 0
        self.col = 0
        self.queue = queue(([]))
        self.starting_point = 0.0
        self.pos = [0,0]
        self.last_move = ""
        self.bump_direction = ""
        self.move_made = False


    def program(self, percept):
        if (self.last_move == "Left" and percept[1] != 'Bump'):
            self.col = self.col - 1
        elif (self.last_move == "Right" and percept[1] != 'Bump'):
            self.col = self.col + 1
        elif (self.last_move == "Up" and percept[1] != 'Bump'):
            self.row = self.row + 1
        elif (self.last_move == "Down" and percept[1] != 'Bump'):
            self.row = self.row - 1;

        if [self.row, self.col] not in self.visited and percept[1] != 'Bump' and self.last_move != "NoOp" and self.last_move != "Suck":
            self.visited += ([self.col, self.row],)
        
        if (self.move_made):
            if (percept[0] == 'Dirty'):
                self.last_move = 'Suck'
                self.move_made = False
                return 'Suck'

            if (percept[1] == 'Bump'):
                self.bump_direction = self.last_move
            else:
                self.bump_direction = "None"
        
        
        self.visited.append([self.col,self.row])
        left = [self.col - 1, self.row]
        right = [self.col + 1, self.row]
        up = [self.col, self.row + 1]
        down = [self.col, self.row - 1]
        
        # 0 = left
        # 1 = up
        # 2 = right
        # 3 = down
        if left not in self.visited:
            self.queue.appendleft(0)
        if up not in self.visited:
            self.queue.appendleft(1)
        if right not in self.visited:
            self.queue.appendleft(2)
        if down not in self.visited:
            self.queue.appendleft(3)
        
        
        print(self.queue[0])
        if (self.queue[0] == 0 and left not in self.visited and self.bump_direction != "Left"):
            self.last_move = "Left"
            self.move_made = True
            self.queue.popleft()
            return 'Left'
        elif (self.queue[0] == 1 and up not in self.visited and self.bump_direction != "Up"):
            self.last_move = "Up"
            self.move_made = True
            self.queue.popleft()
            return 'Up'
        elif (self.queue[0] == 2 and right not in self.visited and self.bump_direction != "Right"):
            self.last_move = "Right"
            self.move_made = True
            self.queue.popleft()
            return 'Right'
        elif (self.queue[0] == 3 and down not in self.visited and self.bump_direction != "Down"):
            print("Down")
            self.last_move = "Down"
            self.move_made = True
            self.queue.popleft()
            return 'Down'
        else:
            print("else")
            self.queue.popleft()
            return 'NoOp'
        rand = random.randint(1,4)
        '''
        self.pos = [self.col, self.row]
        print(self.bump_direction)
        if ("Left" != self.bump_direction and self.last_move != "Left" and left not in self.visited):
            self.last_move = "Left"
            self.move_made = True
            return 'Left'
        elif ("Up" != self.bump_direction and self.last_move != "Up" and up not in self.visited):
            self.last_move = "Up"
            self.move_made = True
            return 'Up'
        elif ("Right" != self.bump_direction and self.last_move != "Right" and right not in self.visited):
            self.last_move = "Right"
            self.move_made = True
            return 'Right'
        elif ("Down" != self.bump_direction and self.last_move != "Down" and down not in self.visited):
            self.last_move = "Down"
            self.move_made = True
            return 'Down'
        else:
            return 'NoOp'

        '''
