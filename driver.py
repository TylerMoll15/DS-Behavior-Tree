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
    def __init__(self, environment: Environment) -> None:
        self.e = environment
        self.loc = self.findStart()
        self.atEnd = False
        self.visitedLocations = [[]]
        self.actions = ["Up", "Down", "Left", "Right"]
    
    def findStart(self):
        randStart = randXY(self.e.dimension)
        while (randStart in self.e.obstacleCoords or randStart[yInd] > (self.e.dimension / 2)):
            randStart = randXY(self.e.dimension)
        return randStart
    
    def canMove(self, newState):
            if newState in self.e.obstacleCoords or newState not in self.e.validCoords: return False
            else: return True
    
    def move(self, action):
        if action == "Up": newState = [self.loc[xInd], self.loc[yInd] - 1] 
        elif action == "Down": newState = [self.loc[xInd], self.loc[yInd] + 1] 
        elif action == "Left": newState = [self.loc[xInd] - 1, self.loc[yInd]] 
        elif action == "Right": newState = [self.loc[xInd] + 1, self.loc[yInd]] 
        
        canMoveBool = self.canMove(newState)
        self.loc = newState if canMoveBool else self.loc
        self.visitedLocations.append(self.loc)

        if self.loc == self.e.rewardLoc: self.atEnd = True
        return canMoveBool

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
             breakpoint()
             return True
        return False

    def randAction(self):
        rand = np.random.randint(0, len(testagent.actions))
        return self.actions[rand]
    
    


testenv = Environment()
testenv.placeWall(3, "h", [2,2])
testagent = Agent(testenv)
testagent.printEnv()
stuckInLoop = Sequence([Condition(testagent.multipleVisits, testagent.loc), Fallback([Sequence([Condition(testagent.wallBelowLeft), Action(testagent.move, "Left")]), Sequence([Condition(testagent.wallBelowRight), Action(testagent.move, "Right")])])])
obsBelow = Sequence([Condition(testagent.wallBelow), Action(testagent.move, "Left")])
obsLeft = Sequence([Condition(testagent.wallLeft), Sequence([InverterNode(Condition(testagent.wallRight)), Fallback([Action(testagent.move, "Down"), Action(testagent.move, "Up")])])])
obsRight = Sequence([Condition(testagent.wallRight), Fallback([Action(testagent.move, "Down"), Action(testagent.move, "Up")])])
obsActions = Fallback([obsBelow, obsLeft, obsRight])

# mainFallback = Fallback([RepeatNode(Action(testagent.move, "Down"), 2),RepeatNode(Action(testagent.move, "Right"), 2), RepeatNode(Action(testagent.move, "Up"), 2), RepeatNode(Action(testagent.move, "Left"), 2)])
mainFallback = Fallback([stuckInLoop, obsActions, Action(testagent.move, "Down"), Action(testagent.move, "Right")])
bt = BehaviorTree(mainFallback)

while testagent.loc != testenv.rewardLoc:
    # breakpoint()
    bt.tick()
    testagent.printEnv()



# testTree = BehaviorTree()
