from BehaviorNodes import *
import random

shedDoor = 0 # Closed
hasShovel = 0 # does not have shovel

def isBusy():
    r = random.random()
    if r > 0.5:
        print('not busy! Let\'s go plant a tree!')
        return 0
    else:
        print('too busy. I\'ll plant a tree later.')
        return 1

def openShedDoorFunc():
    global shedDoor
    if not shedDoor:
        shedDoor = 1 # Open shed door
        print('opening shed door...') 
        return 1
    else:
        return 0

def closeShedDoorFunc():
    global shedDoor
    if shedDoor:
        shedDoor = 0 # Close shed door
        print('closing shed door...')
        return 1
    else:
        return 0

def lookForShovelFunc():
    global hasShovel
    r = random.randint(0, 1)
    if r == 1:
        hasShovel = 1
        print('shovel found!')
    elif r == 0:
        hasShovel = 0
        print('can\'t find shovel...')
    return r

def goToBackyardFunc():
    # Move to backyard
    print('moving to backyard...')
    return 1

def digFunc():
    r = random.random()
    if r > 0.1:
        print('dig...')
        return 1
    else:
        print('not good soil, can\'t plant here...')
        return 0

def moveFunc():
    # Move to different spot in backyard
    print('moving to a different spot...')
    return 1

def plantTreeFunc():
    # Plant tree
    print('tree successfully planted!')
    return 1

busy = Condition(isBusy)
openShedDoor = Action(openShedDoorFunc)
lookForShovel = Action(lookForShovelFunc)
closeShedDoor = Action(closeShedDoorFunc)
hasShovelCond = Condition(lambda: hasShovel)
goToBackyard = Action(goToBackyardFunc)
dig = Action(digFunc)
move = Action(moveFunc)
plantTree = Action(plantTreeFunc)

getShovel = Sequence([InverterNode(busy), openShedDoor, ForceSuccessNode(RetryNode(lookForShovel, 2)), closeShedDoor, hasShovelCond])
digHole = Fallback([RepeatNode(dig, 5), ForceFailureNode(move)])

bt = BehaviorTree(SequenceStar([getShovel, goToBackyard, digHole, plantTree]))

trial = bt.tick()
while trial == s.FAILURE:
    trial = bt.tick()