from array import *
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
            self.row = self.row - 1
        return 'NoOp'
