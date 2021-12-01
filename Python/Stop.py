from mesa import Agent

class Stop(Agent):
    def __init__(self, unique_id, model, x, y):
        super().__init__(unique_id, model)
        self.x = x
        self.y = y
        self.tot = 0
        self.persons = []

    def addPeople(self, person):
        self.tot += 1
        self.persons.append(person)