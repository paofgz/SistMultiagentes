from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import BaseScheduler
import random
import numpy as np

class CarAgent(Agent):
    def __init__(self, unique_id, model, road):
        super().__init__(unique_id, model)
        self.road = road

    def move(self):
        move = True
        x, y = self.pos
        if self.road == 1:
            if x+3 <= self.model.width:
                new_position = (x+3, y)
        elif self.road == 2:
            if x-3 >= 0:
                new_position = (x-3, y)
        elif self.road == 3:
            if y+3 <= self.model.height:
                new_position = (x, y+3)
        elif self.road == 4:
            if y-3 >= 0:
                new_position = (x, y-3)
        cellmates = self.model.grid.get_cell_list_contents([new_position])
        if len(cellmates) == 0:
            self.model.grid.move_agent(self, new_position)
            print("move car")
        else:
            if len(cellmates) > 1:
                for i in range(len(cellmates)):
                    if type(cellmates[i]) == CarAgent:
                        move =  False
                    if type(cellmates[i]) == LightAgent:
                        if cellmates[i].state != 0:
                            move = False
                if move:
                    self.model.grid.move_agent(self, new_position)
            else:
                self.model.grid.move_agent(self, new_position)
        
    
    def step(self):
        self.move()

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
            neighbor = (x-2, y)
            neighbor2 = (x+5, y+1)
        elif self.road == 3:
            neighbor = (x, y+2)
            neighbor2 = (x+1, y-5)
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
                    print("tellow 1")
                    self.changeState()
                    self.model.count = 0
                elif self.state == 0 and self.model.count == 3:
                    self.changeState()
                
            

class Road(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class TrafficModel(Model):

    def __init__(self, 
        N = 50, 
        height = 100, 
        width = 100):
        self.num_cars = N
        self.num_lights = 4
        self.found = 0
        self.width = width
        self.height = height
        self.count = 0
    
        X = round(width/2)
        Y = round(height/2)
        cont = 0
        self.grid = MultiGrid(height, width, True)
        self.schedule = BaseScheduler(self)
        self.running = True
        roads = [1, 2, 3, 4]
        for a in range(self.width):
            c = Road(a, self)
            self.grid.place_agent(c, (a, Y-1))
            self.grid.place_agent(c, (a, Y))
        for b in range(self.height):
            d = Road(b, self)
            self.grid.place_agent(d, (X-1, b))
            self.grid.place_agent(d, (X, b))
        for j in range(self.num_lights):
            id = "light " + str(j)
            if cont == 0:
                b = LightAgent(id, self, X-2, Y-1, 1)
            elif cont == 1:
                b = LightAgent(id, self, X+1, Y, 2)
            elif cont == 2:
                b = LightAgent(id, self, X-1, Y+1, 3)
            else:
                b = LightAgent(id, self, X, Y-2, 4)
            self.schedule.add(b)
        # Add the agent to a random grid cell
            self.grid.place_agent(b, (b.x, b.y))
            cont += 1
        for i in range(self.num_cars):
            id = "car " + str(i)
            road = random.choice(roads)
            a = CarAgent(id, self, road)
            self.schedule.add(a)
            x = 0
            y = 0
            if road == 1:
                y = Y-1
            if road == 2:
                x = width - 1
                y = Y
            if road == 3:
                x = X 
            if road == 4:
                y = height - 1
                x = X - 1
            if i == 0:
                if road == 1:
                    x = 1
                elif road == 2:
                    x = width -2
                elif road == 3:
                    y = 1
                else:
                    y = height -2

            
            self.grid.place_agent(a, (x, y))
    
    def step(self):
        self.schedule.step()
        self.count += 1
        print("COUNT:", self.count)
        ps = []
        for i in range (self.num_lights, self.num_cars + self.num_lights):
            xy = self.schedule.agents[i].pos
            p = [xy[0], xy[1], 0] #XZY
            ps.append(p)
        return ps