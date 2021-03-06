from model import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

def agent_portrayal(agent):
    portrayal = {"Shape": "rect",
            "w": 1,
            "h": 1,
            "Filled": "true",
            "Layer": 0,
            "Color": "blue",
            }
    if type(agent) == Road:
        portrayal = {"Shape": "rect",
            "w": 1,
            "h": 1,
            "Filled": "true",
            "Layer": 0,
            "Color": "grey"}
    if type(agent) == PersonAgent:
        portrayal = {"Shape": "rect",
            "w": 0.5,
            "h": 0.5,
            "Filled": "true",
            "Layer": 1,
            "Color": "red"}
    if type(agent) == Stop:
        portrayal = {"Shape": "rect",
            "w": 1,
            "h": 1,
            "Filled": "true",
            "Layer": 0,
            "Color": "black"}
    if type(agent) == CarAgent:
        portrayal = {"Shape": "rect",
            "w": 0.5,
            "h": 0.5,
            "Filled": "true",
            "Layer": 2,
            "Color": "blue"}
    if type(agent) == LightAgent:
        portrayal = {"Shape": "rect",
                "w": 1,
                "h": 1,
                "Filled": "true",
                "Layer": 1,
                "Color": "green"}
        if agent.state == 0:
            portrayal["Color"] = "green"
        elif agent.state == 1:
            portrayal["Color"] = "yellow"
        else:
            portrayal["Color"] = "red"
    return portrayal


grid = CanvasGrid(agent_portrayal, 30, 30, 500, 500)
server = ModularServer(TrafficModel,
                       [grid],
                       "Traffic Model",
                       {"N":20, "width":30, "height":30, "M": 20})
server.port = 8000 # The default
server.launch()