from mesa import Agent

class LightAgent(Agent):
    """
    States: 
    0 - green light
    1 - yellow light
    2 - red light
    """
    def __init__(self, unique_id, model, x, y, road):
        super().__init__(unique_id, model)
        self.state = 1
        self.x = x
        self.y = y
        self.road = road

    def check(self):
        x, y = self.pos
        if self.road == 1:
            neighbor = (x-1, y)
            neighbor2 = (x+4, y+1)
        elif self.road == 3:
            neighbor = (x, y+1)
            neighbor2 = (x+1, y-4)
        cellmates = self.model.grid.get_cell_list_contents([neighbor])
        cellmates2 = self.model.grid.get_cell_list_contents([neighbor2])
        if len(cellmates) > 1 or len(cellmates2) > 1:
            return True
        else:
            return False

    def changeState(self):
        if self.road == 1:
            if self.unique_id == 'light 0':
                partner = self.model.schedule.agents[1]
            else:
                partner = self.model.schedule.agents[0]
            other = self.model.schedule.agents[2]
            other2 = self.model.schedule.agents[3]
            if self.model.found == 0:
                self.state = 0
                partner.state = 0
                other.state = 2
                other2.state = 2
            elif self.state == 1:
                self.state = 2
                partner.state = 2
                other.state = 0
                other2.state = 0
            elif self.state == 0:
                self.state = 1
                partner.state = 1
                other.state = 2
                other2.state = 2
            else:
                if other.state == 1:
                    self.state = 0
                    partner.state = 0
                    other.state = 2
                    other2.state = 2
                else:
                    other.state = 1
                    other2.state = 1
        elif self.road == 3:
            if self.unique_id == 'light 2':
                partner = self.model.schedule.agents[3]
            else:
                partner = self.model.schedule.agents[2]
            other = self.model.schedule.agents[0]
            other2 = self.model.schedule.agents[1]
            if self.model.found == 0:
                self.state = 0
                partner.state = 0
                other.state = 2
                other2.state = 2
    def step(self):
        if self.model.found == 0:
            if self.unique_id == 'light 0' or self.unique_id == 'light 2':
                if self.check():
                    self.changeState()
                    self.model.found = 1
                    self.model.count = 0
                    print("FOUND")
        else:
            if self.unique_id == 'light 0':
                if self.state == 2 and self.model.count == 5:
                    self.changeState()
                    self.model.count = 0
                elif self.state == 2 and self.model.count == 3:
                    self.changeState()
                elif self.state == 1 and self.model.count == 5:
                    print("yellow 1")
                    self.changeState()
                    self.model.count = 0
                elif self.state == 0 and self.model.count == 3:
                    self.changeState()