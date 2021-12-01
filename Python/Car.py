from mesa import Agent
from Light import LightAgent

class CarAgent(Agent):
    def __init__(self, unique_id, model, road, seats):
        super().__init__(unique_id, model)
        self.road = road
        self.seats = seats
        self.available = seats - 1

    def move(self):
        x, y = self.pos
        if self.road == 1:
            if x+3 < self.model.width:
                new_position = (x+3, y)
                pos1 = (x+2,y)
                pos2 = (x+1,y)
                if self.checkPos(new_position) and self.checkPos(pos1) and self.checkPos(pos2):
                    self.model.grid.move_agent(self, new_position)
            else:
                new_position = (self.model.width-1, y-1)
                if self.checkPos(new_position):
                    self.model.grid.move_agent(self, new_position)
                    self.road = 4
            if x == round(self.model.width/2) - 2 and y == self.model.height - 1:
                new_position = (x+1, y-1)
                if self.checkPos(new_position):
                    self.model.grid.move_agent(self, new_position)
                    self.road = 4
        elif self.road == 2:
            if x-3 >= 0:
                new_position = (x-3, y)
                pos1 = (x-2,y)
                pos2 = (x-1,y)
                if self.checkPos(new_position) and self.checkPos(pos1) and self.checkPos(pos2):
                    self.model.grid.move_agent(self, new_position)
            else:
                new_position = (0, y+1)
                if self.checkPos(new_position):
                    self.model.grid.move_agent(self, new_position)
                    self.road = 3
            if x == round(self.model.width/2) + 1 and y == 0:
                new_position = (x-1, y+1)
                if self.checkPos(new_position):
                    self.model.grid.move_agent(self, new_position)
                    self.road = 3
        elif self.road == 3:
            if y+3 < self.model.height:
                new_position = (x, y+3)
                pos1 = (x,y+2)
                pos2 = (x,y+1)
                if self.checkPos(new_position) and self.checkPos(pos1) and self.checkPos(pos2):
                    self.model.grid.move_agent(self, new_position)
            else:
                new_position = (x+1, self.model.height-1)
                if self.checkPos(new_position):
                    self.model.grid.move_agent(self, new_position)
                    self.road = 1
            if y == round(self.model.height/2) - 2 and x == 0:
                new_position = (x+1, y+1)
                if self.checkPos(new_position):
                    self.model.grid.move_agent(self, new_position)
                    self.road = 1
        elif self.road == 4:
            if y-3 >= 0:
                new_position = (x, y-3)
                pos1 = (x,y-2)
                pos2 = (x,y-1)
                if self.checkPos(new_position) and self.checkPos(pos1) and self.checkPos(pos2):
                    self.model.grid.move_agent(self, new_position)
            else:
                new_position = (x-1, 0)
                if self.checkPos(new_position):
                    self.model.grid.move_agent(self, new_position)
                    self.road = 2
            if y == round(self.model.height/2)+1 and x == self.model.width - 1:
                new_position = (x-1, y-1)
                if self.checkPos(new_position):
                    self.model.grid.move_agent(self, new_position)
                    self.road = 2
        else:
            return

    def checkPos(self, ps):
        cellmates = self.model.grid.get_cell_list_contents([ps])
        if len(cellmates) == 1:
            return True
        else:
            if len(cellmates) > 1:
                move = True
                for i in range(len(cellmates)):
                    if type(cellmates[i]) == CarAgent:
                        move =  False
                    if type(cellmates[i]) == LightAgent:
                        if cellmates[i].state != 0:
                            move = False
                if move == False:
                    return False
                return True

    
    # Check if the car has space and there is people waiting in the station
    def lookPass(self):
        road = self.road
        x, y = self.pos
        if road == 1:
            if (x == round((self.model.width/2)/2) - 1 or x == round((self.model.width/2)/2) or x == round((self.model.width/2)/2) - 2) and self.available > 0 and self.model.stops[0].tot > 0 and y == round(self.model.height/2) - 1:
                while self.available > 0 and self.model.stops[0].tot > 0:
                    person = self.model.stops[0].persons.pop()
                    self.model.grid.move_agent(person, (-300, -300))
                    self.model.stops[0].tot -= 1
                    self.available -= 1
                return True
        elif road == 2:
            if (x == self.model.width - round((self.model.width/2)/2) or x == self.model.width - round((self.model.width/2)/2) - 1 or x == self.model.width - round((self.model.width/2)/2) + 1) and self.available > 0 and self.model.stops[1].tot > 0 and y == round(self.model.height/2):
                while self.available > 0 and self.model.stops[1].tot > 0:
                    person = self.model.stops[1].persons.pop()
                    self.model.grid.move_agent(person, (-300, -300))
                    self.model.stops[1].tot -= 1
                    self.available -= 1
                return True
        elif road == 3:
            if (y == round((self.model.height/2)/2) - 1 or y == round((self.model.height/2)/2) or y == round((self.model.height/2)/2) - 2) and self.available > 0 and self.model.stops[2].tot > 0 and x == round(self.model.width/2):
                while self.available > 0 and self.model.stops[2].tot > 0:
                    person = self.model.stops[2].persons.pop()
                    self.model.grid.move_agent(person, (-300, -300))
                    self.model.stops[2].tot -= 1
                    self.available -= 1
                return True
        elif road == 4:
            if (y == self.model.height - round((self.model.height/2)/2) or y == self.model.height - round((self.model.height/2)/2) - 1 or y == self.model.height - round((self.model.height/2)/2) + 1) and self.available > 0 and self.model.stops[3].tot > 0 and x == round(self.model.width/2) - 1:
                while self.available > 0 and self.model.stops[3].tot > 0:
                    person = self.model.stops[3].persons.pop()
                    self.model.grid.move_agent(person, (-300, -300))
                    self.model.stops[3].tot -= 1
                    self.available -= 1
                return True
        return False

    def checkIfPass(self):
        total = 0
        for i in range (len(self.model.stops)):
            total += self.model.stops[i].tot
        if total == 0:
            return False
        return True


    def deleteEmpty(self):
        if self.available == self.seats - 1:
            self.model.grid.move_agent(self, (-300, -300))
            self.road = 5
            print("delete ", str(self.unique_id))

    def step(self):
        if self.checkIfPass() == True:
            if self.lookPass() == False:
                self.move()
        else:
            self.move()
            self.deleteEmpty()

