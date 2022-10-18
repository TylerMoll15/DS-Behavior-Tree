from enum import Enum, unique
from abc import ABC, abstractmethod

verbose = False

@unique
class s(Enum):
    SUCCESS = 1
    RUNNING = 2
    FAILURE = 3
    STANDBY = 4 # in none of the other states, hasn't been ticked

class Node(ABC):
    def __init__(self, children):
        self.state: s = s.STANDBY
        self.children: list[Node] = children
    
    def tick(self) -> s:
        pass

class BehaviorTree(): # BTree itself has implied root node
    def __init__(self, child: Node = None):
        self.child: Node = child
        self.state: s = s.STANDBY
    
    def tick(self): 
        self.state = s.RUNNING
        cState = self.child.tick()
        if verbose: print(f"Behavior tree returned {cState}!")
        return cState

# LEAF NODES
class Condition(Node):
    def __init__(self, func, args= []):
        self.state = s.STANDBY
        self.condition = func # Higher order function to check T/F condition
        self.args = args

    def tick(self):
        self.state = s.RUNNING
        if self.condition(self.args): 
            if verbose: print("Condition True!")
            return s.SUCCESS
        else: 
            if verbose: print("Condition false! :(")
            return s.FAILURE

class Action(Node):
    def __init__(self, func, args= []):
        self.state = s.STANDBY
        self.do = func # Higher order function to do action
        self.args = args # List of args for action

    def tick(self):
        self.state = s.RUNNING
        # breakpoint()
        if self.args and self.do(self.args): return s.SUCCESS
        elif self.do(): return s.SUCCESS
        else: return s.FAILURE

# OTHER NODES
class Sequence(Node):
    def __init__(self, children):
        super().__init__(children)
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

                if verbose: print("Oh no, there was a failure. Terminating...")
                return s.FAILURE

        if verbose: print("Sequence was successful!")
        self.cIdx = 0 # Reset node counter upon success
        return s.SUCCESS

class SequenceStar(Node):
    def __init__(self, children):
        super().__init__(children)
        self.cIdx = 0 #Keeps track of which child is being ticked

    def tick(self):
        self.state = s.RUNNING

        while self.cIdx < len(self.children):
            cStatus = self.children[self.cIdx].tick()
            if(cStatus == s.SUCCESS): self.cIdx+=1
            else: return cStatus

        if verbose: print("Sequence was successful!")
        self.cIdx = 0 # Reset node counter upon success
        return s.SUCCESS

class Fallback(Node):
    def __init__(self, children):
        super().__init__(children)
    
    def tick(self):
        self.state = s.RUNNING

        for child in self.children:
            cStatus = child.tick()
            if cStatus == s.RUNNING:
                return s.RUNNING
            elif cStatus == s.SUCCESS:
                return s.SUCCESS
        return s.FAILURE

class Decorator(Node):
    def __init__(self, child: Node = None):
        super().__init__(child)
        self.children: Node = child # Only 1 child allowed

class InverterNode(Decorator):
    def __init__(self, child: Node = None):
        super().__init__(child)
    
    def tick(self):
        self.state = s.RUNNING

        cState = self.children.tick()
        if cState == s.RUNNING: return s.RUNNING
        elif cState == s.FAILURE: return s.SUCCESS
        elif cState == s.SUCCESS: return s.FAILURE

class ForceSuccessNode(Decorator):
    def __init__(self, child: Node = None):
        super().__init__(child)

    def tick(self):
        self.state = s.RUNNING

        cState = self.children.tick()
        if cState == s.RUNNING: return s.RUNNING
        else: return s.SUCCESS

class ForceFailureNode(Decorator):
    def __init__(self, child: Node = None):
        super().__init__(child)
    
    def tick(self):
        self.state = s.RUNNING

        cState = self.children.tick()
        if cState == s.RUNNING: return s.RUNNING
        else: return s.FAILURE

class RepeatNode(Decorator):
    def __init__(self, child, n): # I think child should be a requred parameter for decorator nodes. No reason to ever have a decorator node with no child.
        super().__init__(child)
        self.n = n

    def tick(self):
        self.state = s.RUNNING

        for i in range(self.n):
            cState = self.children.tick()
            if cState == s.FAILURE: return s.FAILURE
            elif cState == s.RUNNING: return s.RUNNING

        return s.SUCCESS

class RetryNode(Decorator):
    def __init__(self, child, n): 
        super().__init__(child)
        self.n = n

    def tick(self):
        self.state = s.RUNNING

        for i in range(self.n):
            cState = self.children.tick()
            if cState == s.SUCCESS: return s.SUCCESS
            elif cState == s.RUNNING: return s.RUNNING

        return s.FAILURE

# SEQUENCE STAR TEST

# x = 1

# def goto1():
#     return 1 if x >= 1 else 0

# def goto2():
#     return 1 if x >= 2 else 0

# def goto3():
#     return 1 if x >= 3 else 0

# seqStar = SequenceStar([Action(goto1), Action(goto2), Action(goto3)])
# for i in range(3):
#     print(seqStar.tick())
#     x += 1

# RETRY NODE TEST

# def conditionXGreaterThan3(x):
#     return x[0] > 3


# cond = Condition(conditionXGreaterThan3, [0])
# def incX():
#     global cond
#     cond.args[0] += 1
#     return 1

# action = Action(incX)
# seq = Sequence([action, cond])
# retry = RetryNode(seq, 3)
# print(retry.tick())

# REPEAT NODE TEST

# def conditionXLessThan3(x):
#     return x[0] < 3


# cond = Condition(conditionXLessThan3, [0])
# def incX():
#     global cond
#     cond.args[0] += 1
#     return 1

# action = Action(incX)
# seq = Sequence([action, cond])
# repeat = RepeatNode(seq, 2)
# print(repeat.tick())

# TEST FOR SEQUENCE, CONDITION, AND ACTION NODES

# x = 0
# y = 0

# def conditionXGreaterThan3(x):
#     return x[0] > 3
# def actionSetYto1():
#     global y
#     y = 1
#     return 1

# seq = Sequence()
# cond = Condition(conditionXGreaterThan3, [x])
# cond2 = Condition(lambda a: 1 == 2) #False
# cond3 = Condition(lambda a: 1 > 2) #False
# cond4 = Condition(lambda a: 10 > 9) #True

# action1 = Action(lambda: print("Hello I'm the first!") or True) # First action works
# action2 = Action(lambda: print("Hello I'm the second!") or False) # Second action fails, but is successful through inverter node

# fallB = Fallback()
# invert = InverterNode()
# forceS = ForceSuccessNode()
# forceF = ForceFailureNode()

# invert.children = action2
# seq.children = [fallB, action1, invert]
# fallB.children = [cond2, cond3, cond4, cond2] # Second instance of cond2 is ignored since cond4 is successful
# BTree = BehaviorTree(seq)

# BTree.tick()

# for i in range(5):
#     seq.tick()
#     cond.args[0] += 1

# print(x, y)



