
from vacuum import VacuumAgent

class AkeehanVacuumAgent(VacuumAgent):

    def __init__(self):
        super().__init__()


    def program(self, percept):
        return 'NoOp'
