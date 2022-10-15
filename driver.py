from BehaviorNodes import *
import numpy as np

xInd = 0
yInd = 1

def randXY(dimension):
    xCoord = np.random.randint(0, dimension)
    yCoord = np.random.randint(0, dimension)

    randCoords = [xCoord, yCoord]
    return randCoords

class Environment():
    def __init__(self, dimension = 10, obstacleNum = 10) -> None:
        self.dimension = dimension
        self.obstacleNum = obstacleNum
        self.notableCoords = [[]]
        self.genObstacles()
    
    def genObstacles(self):
        for i in range(self.obstacleNum):
            randCoords = randXY(self.dimension) # Init rand coords aren't possible
            while randCoords in self.notableCoords:
                randCoords = randXY(self.dimension)
            
            self.notableCoords.append(randCoords)
    
    def printEnv(self):
        for y in range(self.dimension):
            for x in range(self.dimension):
                if [x, y] in self.notableCoords: print("*", end =" ")
                else: print(".", end =" ")
            print("\n")

class Agent():
    def __init__(self, environment: Environment) -> None:
        self.loc = self.findStart()
        self.e = environment
    
    def findStart(self):
        randStart = randXY(self.e.dimension)
        while (randStart in self.e.notableCoords):
            randStart = randXY(self.e.dimension)
        return randStart
    
    def move(self, action):
        def canMove(newState):
            if newState in self.e.notableCoords: return False
            else: return True

        if action == "Up": 
            newState = [self.loc[xInd], self.loc[yInd] + 1] 
            self.loc = newState if canMove(newState) else self.loc
        if action == "Down": 
            newState = [self.loc[xInd], self.loc[yInd] - 1] 
            self.loc = newState if canMove(newState) else self.loc
        if action == "Left": 
            newState = [self.loc[xInd] - 1, self.loc[yInd]] 
            self.loc = newState if canMove(newState) else self.loc
        if action == "Right": 
            newState = [self.loc[xInd] + 1, self.loc[yInd]] 
            self.loc = newState if canMove(newState) else self.loc
        


testenv = Environment()
testenv.printEnv()

# testTree = BehaviorTree()
