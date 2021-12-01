from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import BaseScheduler
from Car import CarAgent
from Person import PersonAgent
from Light import LightAgent
from Stop import Stop

import random
import numpy as np

class Road(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class TrafficModel(Model):

    def __init__(self, 
        N = 20, 
        height = 30, 
        width = 30,
        M = 40):
        self.num_cars = N
        self.num_lights = 4
        self.found = 0
        self.width = width
        self.height = height
        self.count = 0
        self.numPersons = M
    
        X = round(width/2)
        Y = round(height/2)
        cont = 0
        self.grid = MultiGrid(height, width, True)
        self.schedule = BaseScheduler(self)
        self.running = True
        roads = [1, 2, 3, 4]
        available = [2, 3, 4]
        self.stops = []
        self.people = []

        # Create stops
        for r in range(len(roads)):
            id = "stop " + str(r+1)
            if r == 0:
                y = Y - 2
                x = round(X/2)-1
            if r == 1:
                y = Y + 1
                x = width - round(X/2)
            if r == 2:
                x = X + 1
                y = round(Y/2)-1
            if r == 3:
                x = X - 2
                y = height - round(Y/2)
            stop = Stop(id, self, x, y)
            self.grid.place_agent(stop, (x, y))
            self.stops.append(stop)

        # Create Roads
        for a in range(self.width):
            c = Road(a, self)
            self.grid.place_agent(c, (a, Y-1))
            self.grid.place_agent(c, (a, Y))
            self.grid.place_agent(c, (a, height-1))
            self.grid.place_agent(c, (a, 0))
        for b in range(self.height):
            d = Road(b, self)
            self.grid.place_agent(d, (X-1, b))
            self.grid.place_agent(d, (X, b))
            self.grid.place_agent(d, (0, b))
            self.grid.place_agent(d, (width-1, b))

        # Add stop lights
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
            self.grid.place_agent(b, (b.x, b.y))
            cont += 1

        # Add people
        for i in range(self.numPersons):
            id = "person " + str(i)
            stop = random.choice(self.stops)
            if stop.unique_id == "stop 1":
                y = stop.y
                x = stop.x
            if stop.unique_id == "stop 2":
                y = stop.y
                x = stop.x
            if stop.unique_id == "stop 3":
                y = stop.y
                x = stop.x
            if stop.unique_id == "stop 4":
                y = stop.y
                x = stop.x
            p = PersonAgent(id, self, x, y)
            self.grid.place_agent(p, (x, y))
            stop.addPeople(p)
            self.people.append(p)
        
        # Add car
        for i in range(self.num_cars):
            id = "car " + str(i)
            road = random.choice(roads)
            seats = random.choice(available)
            a = CarAgent(id, self, road, seats)
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
                    x = 3
                elif road == 2:
                    x = width - 4
                elif road == 3:
                    y = 3
                else:
                    y = height - 4
            self.grid.place_agent(a, (x, y))
    
    def step(self):
        self.schedule.step()
        self.count += 1
        ps = []
        for i in range (self.num_lights, self.num_cars + self.num_lights):
            xy = self.schedule.agents[i].pos
            if (xy[0] == 0 and xy[1] == 0):
                p = [-300, -300, -300] #XZY
            else:
                p = [xy[0], xy[1], 0.3] #XZY
            ps.append(p)
        for i in range(self.numPersons):
            pxy = self.people[i].pos
            if (pxy[0] == 0 and pxy[1] == 0):
                p = [-300, -300, -300] #XZY
            else:
                p = [pxy[0], pxy[1], 0.3] #XZY
            ps.append(p)
        print(ps)
        return ps