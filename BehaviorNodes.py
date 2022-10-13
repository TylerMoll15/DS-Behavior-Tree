from enum import Enum, unique

@unique
class s(Enum):
    SUCCESS = 1
    RUNNING = 2
    FAILURE = 3
    STANDBY = 4 # in none of the other states, hasn't been ticked

class BehaviorTree():
    def __init__(self):
        self.root = Node()

class Node():
    def __init__(self):
        self.state: s = s.STANDBY
        self.children: list[Node] = []
    
    def tick(self) -> s:
        self.state = s.RUNNING

        print("Node was ticked!")
        return s.FAILURE
        # Then do more stuff, (will be specified in child nodes)

        # Not sure I understand this, may be important but im ignoring it for now
        # "Tick again" means that the next time the sequence is ticked, the same child is 
        # ticked again. Previous sibling, which returned SUCCESS already, are not ticked again.

class Condition(Node):
    def __init__(self, func):
        self.state = s.STANDBY
        self.condition = func # Higher order function to check T/F condition

    def tick(self):
        self.state = s.RUNNING
        if self.condition(): return s.SUCCESS
        else: return s.FAILURE

class Action(Node):
    def __init__(self, func, args):
        self.state = s.STANDBY
        self.do = func # Higher order function to do action
        self.args = args # List of args for action

    def tick(self):
        self.state = s.RUNNING
        if self.do(self.args): return s.SUCCESS
        else: return s.FAILURE

class Sequence(Node):
    def __init__(self):
        self.cIdx = 0 #Keeps track of which child is being ticked

    def tick(self):
        self.state = s.RUNNING

        while self.cIdx < len(self.children):
            cStatus = self.children[self.cIdx].tick()
            
            if(cStatus == s.SUCCESS): self.cIdx+=1
            elif (cStatus == s.RUNNING): return s.RUNNING
            elif cStatus == s.FAILURE:
                # HaltAllChildren() ????
                self.cIdx = 0

                print("Oh no, there was a failure. Terminating...")
                return s.FAILURE

        print("Sequnce was ticked!")
        return s.SUCCESS

testNode = Node()
testSequence = Sequence()
anotherSequence = Sequence()
testSequence.children = [testNode, testNode, testNode, anotherSequence]

testSequence.tick()




