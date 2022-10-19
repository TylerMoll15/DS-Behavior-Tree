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
    def __init__(self, dimension = 5, obstacleNum = 2) -> None:
        self.dimension = dimension
        self.rewardLoc = [self.dimension - 1, self.dimension - 1]
        self.obstacleNum = obstacleNum
        self.obstacleCoords = [[]]
        self.genObstacles()
        self.validCoords = self.allCoords()
    
    def genObstacles(self):
        for i in range(self.obstacleNum):
            randCoords = randXY(self.dimension) # Init rand coords aren't possible
            while randCoords in self.obstacleCoords or randCoords == self.rewardLoc:
                randCoords = randXY(self.dimension)
            
            self.obstacleCoords.append(randCoords)
    
    def allCoords(self):
        allCoords = [[]]
        for x in range(self.dimension):
            for y in range(self.dimension):
                allCoords.append([x, y])
        
        return allCoords
    
    def placeWall(self, length, type, wallStart = None):
        if not wallStart: wallStart = randXY(self.dimension)
        self.obstacleCoords.append(wallStart)

        if type != ("h" or "v"): print("not a valid wall type")

        for i in range(1, length):
            if type == "h": self.obstacleCoords.append([wallStart[xInd] + i, wallStart[yInd]])
            elif type == "v": self.obstacleCoords.append([wallStart[xInd], wallStart[yInd] + i])

class Agent():
    def __init__(self, environment: Environment, start) -> None:
        self.e = environment
        self.loc = self.findStart(start)
        self.atEnd = False
        self.visitedLocations = [[]]
        self.actions = ["Up", "Down", "Left", "Right"]
    
    def findStart(self, start = None):
        # breakpoint()

        if start: return start

        randStart = randXY(self.e.dimension)
        while (randStart in self.e.obstacleCoords or randStart[yInd] > (self.e.dimension / 2)):
            randStart = randXY(self.e.dimension)
        return randStart
    
    def canMove(self, newState, force = False):
        visitedForce = not force if force else newState in self.visitedLocations

        if newState in self.e.obstacleCoords or newState not in self.e.validCoords or visitedForce: return False
        else: return True
    
    def move(self, actionForce = []):
        action, force = actionForce

        if action == "Up": newState = [self.loc[xInd], self.loc[yInd] - 1] 
        elif action == "Down": newState = [self.loc[xInd], self.loc[yInd] + 1] 
        elif action == "Left": newState = [self.loc[xInd] - 1, self.loc[yInd]] 
        elif action == "Right": newState = [self.loc[xInd] + 1, self.loc[yInd]] 

        canMoveBool = self.canMove(newState, force)
        self.loc = newState if canMoveBool else self.loc
        self.visitedLocations.append(self.loc)

        if self.loc == self.e.rewardLoc: self.atEnd = True
        return canMoveBool
    
    def result(self, action):
        if action == "Up": newState = [self.loc[xInd], self.loc[yInd] - 1] 
        elif action == "Down": newState = [self.loc[xInd], self.loc[yInd] + 1] 
        elif action == "Left": newState = [self.loc[xInd] - 1, self.loc[yInd]] 
        elif action == "Right": newState = [self.loc[xInd] + 1, self.loc[yInd]] 
        return newState
    
    def fewestVisitsAction(self): 
        leastTimes = 1000000
        leastAction = "Not an Action"
        for a in self.actions:
            if (self.visitedLocations.count(self.result(a)) < leastTimes) and self.result(a) not in self.e.obstacleCoords and self.result(a) in self.e.validCoords:
                leastAction = a
                leastTimes = self.visitedLocations.count(self.result(a))
        
        return leastAction

        


    def printEnv(self):
        for y in range(self.e.dimension):
            for x in range(self.e.dimension):
                if [x, y] in self.e.obstacleCoords: print("*", end = " ")
                elif [x, y] == self.loc: print("X", end = " ")
                elif [x,y] == self.e.rewardLoc: print("$", end = " ")
                else: print(".", end =" ")
            print("\n")
        print("\n\n")
        
    def wallLeft(self):
        if [self.loc[xInd] - 1, self.loc[yInd]] in self.e.obstacleCoords: return True
        else: return False
    def wallRight(self):
        if [self.loc[xInd] + 1, self.loc[yInd]] in self.e.obstacleCoords: return True
        else: return False
    def wallBelow(self):
        if [self.loc[xInd], self.loc[yInd] + 1] in self.e.obstacleCoords: return True
        else: return False
    def wallBelowLeft(self):
        if [self.loc[xInd] - 1, self.loc[yInd] + 1] in self.e.obstacleCoords: return True
        else: return False
    def wallBelowRight(self):
        if [self.loc[xInd] + 1, self.loc[yInd] + 1] in self.e.obstacleCoords: return True
        else: return False
    
    def multipleVisits(self, coords = None):
        if self.visitedLocations.count(coords) > 5:
            #  breakpoint()
             return True
        return False

    def randAction(self):
        rand = np.random.randint(0, len(testagent.actions))
        return self.actions[rand]

testenv = Environment(5, 0)
testenv.placeWall(3, "h", [2,2])
testenv.placeWall(1, "h", [2,4])
testenv.placeWall(1, "h", [3,1])
testenv.placeWall(1, "h", [0,4])

testagent = Agent(testenv, [4,1])
backup = Action(testagent.move, [testagent.fewestVisitsAction(), True])
mainFallback = Fallback([Action(testagent.move, ["Down", False]), Action(testagent.move, ["Right", False]), Action(testagent.move, ["Left", False]), Action(testagent.move, ["Up", False]), backup])
bt = BehaviorTree(mainFallback)

while testagent.loc != testenv.rewardLoc:
    testagent.printEnv()
    bt.tick()
testagent.printEnv()
