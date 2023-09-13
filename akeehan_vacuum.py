from vacuum import VacuumAgent
from collections import deque as queue
import random


class AkeehanVacuumAgent(VacuumAgent):

    def __init__(self):
        super().__init__()
        self.visited = ([])
        self.row = 0
        self.col = 0
        self.queue = queue([(0,0)])
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
            self.visited.append([self.col, self.row])
        print(self.visited)
        if (self.move_made):
            if (percept[0] == 'Dirty'):
                self.last_move = 'Suck'
                self.move_made = False
                return 'Suck'


