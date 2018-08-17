import numpy as np

def phi_changed(newActions, originalActions):
    if(len(newActions) != len(originalActions)):
        return [1,0]

    for i in range(len(newActions)):
        if newActions[i] != originalActions[i]:
            return [1,0]

    return [0,1]

# percentage of actions that agree
# def phi_percent_changed(newActions, originalActions):
#     newSet = Counter(newActions)
#     originalSet = Counter(originalActions)
#     intersect = newSet & originalSet

#     same = 0.0
#     for uniq in intersect:
#         same += intersect[uniq] * 2

#     ans = same / (len(newActions) + len(originalActions))
#     return [1 - ans , ans]

def phi_percent_changed(newActions, originalActions):
    nNew = len(newActions)
    nOld = len(originalActions)

    same = 0.0
    for i in range(min(nNew,nOld)):
        if newActions[i] == originalActions[i]:
            same += 1

    ans = 2.0 * same / (nNew + nOld)
    return [1 - ans , ans]

# compares how
def phi_block_moved(newActions, originalActions):

    originalSet = set()
    newSet = set()

    for ac in originalActions:
        if ac == "Stop":
            continue
        block, direction = ac.strip().split()
        originalSet.add(block)

    for ac in newActions:
        if ac == "Stop":
            continue
        block, direction = ac.strip().split()
        newSet.add(block)

    if originalSet == newSet and len(newSet) == 1:
        return [0, 1]
    else:
        return [1, 0]
    
def phi_destination(newActions, originalActions):
    from collections import defaultdict
    from functools import partial

    dirMap = {}
    dirMap["south"] = np.array( [0, -1] )
    dirMap["north"] = np.array( [0, +1] )
    dirMap["east"] = np.array( [+1, 0] )
    dirMap["west"] = np.array( [-1, 0] )

    init = np.zeros(2)
    dNew =  defaultdict(partial(np.zeros, 2))
    dOrig = defaultdict(partial(np.zeros, 2))

    for ac in originalActions:
        if ac == "Stop":
            continue
        block, direction = ac.strip().split()
        dOrig[block] += dirMap[direction]


    for ac in newActions:
        if ac == "Stop":
            continue
        block, direction = ac.strip().split()
        dNew[block] += dirMap[direction]


    #blocks = set(dNew.keys() + dOrig.keys())
    blocks = set(dOrig.keys())

    distance = 0.0
    for b in blocks:
        distance += abs(dNew[b][0] - dOrig[b][0]) + abs(dNew[b][1] - dOrig[b][1])
    
    if distance >= 2:
        return [1, 0]
    else:
        return [0, 1]


# returns 1 if both list of commands have stop or both don't have stop
def phi_stop(newActions, originalActions):

    newStop = False
    orignalStop = False

    if len(newActions) > 0 and newActions[-1] == "Stop":
        newStop = True
    if len(originalActions) > 0 and originalActions[-1] == "Stop":
        orignalStop = True

    if newStop == orignalStop:
        return [0, 1]
    else:
        return [1, 0]


def phi_num_moves (newActions, originalActions):

    newL = len(newActions)
    newR = len(originalActions)

    sim = abs(newL - newR) / (0.0 + newL + newR)
    return [sim, 1 - sim]

def phi_comp_distance (newActions, originalActions):

    from collections import defaultdict
    from functools import partial

    dirMap = {}
    dirMap["south"] = np.array( [0, -1] )
    dirMap["north"] = np.array( [0, +1] )
    dirMap["east"] = np.array( [+1, 0] )
    dirMap["west"] = np.array( [-1, 0] )

    init = np.zeros(2)
    dNew =  defaultdict(partial(np.zeros, 2))
    dOrig = defaultdict(partial(np.zeros, 2))

    for ac in originalActions:
        if ac == "Stop":
            continue
        block, direction = ac.strip().split()
        dOrig[block] += dirMap[direction]


    for ac in newActions:
        if ac == "Stop":
            continue
        block, direction = ac.strip().split()
        dNew[block] += dirMap[direction]


    blocks = set(dNew.keys() + dOrig.keys())

    distance = 0.0
    total = 0.0
    for b in blocks:
        distance += abs(dNew[b][0] - dOrig[b][0]) + abs(dNew[b][1] - dOrig[b][1])
        total += abs(dNew[b][0]) + abs(dOrig[b][0]) + abs(dNew[b][1]) + abs(dOrig[b][1])
    
    
    if distance > 2:
        return [1, 0]
    else:
        return [0, 1]


def phi_len(newActions, originalActions):
    return [ 40-len(newActions), len(newActions) ]

def phi_constant(newActions, originalActions):
    return [1,0]

def phi_random (newActions, originalActions):
    first = np.random.randint(2)
    return [first, 1 - first]

