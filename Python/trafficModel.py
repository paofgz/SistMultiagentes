from mesa import Agent, Model

class CarAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.availabeSeats = 4
        self.passengers = []

    def move(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
            if len(cellmates) > 1:
                other = cellmates[0]
                if type(other) == TrafficLightAgent:
                    if other.state == 0 or other.state == 1:
                        possible_steps = self.model.grid.get_neighborhood(
                            self.pos,
                            moore=True,
                            include_center=False)
                        new_position = self.random.choice(possible_steps)
                        self.model.grid.move_agent(self, new_position)

    def pickUp(self, cellmates):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = cellmates[0]
            if type(other) == PersonAgent:
                other.in_car = True
                other.car = self.unique_id
                self.availabeSeats -= 1
                self.passengers.append(other.unique_id)


    def step(self):
        self.move()
        if self.availabeSeats > 0:
            self.pickUp

class TrafficLightAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = 0

    def changeState(self):
        if seltf.state = 0:
            self.state = 1
        elif self.state = 1:
            self.state = 2
        elif self.state = 2:
            self.state = 0

    def step(self):
        self.changeState()

class PersonAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.in_car = False
        self.car = None




