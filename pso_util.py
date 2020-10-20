import random
import pandas as pd

def makeRandomElement(numType, minVal, maxVal):
    '''
    Utitlity method for generating random elements
    '''
    def min_max_projection(x, minVal, maxVal):
        if minVal != maxVal:
            return minVal + x*(maxVal-minVal)
        else:
            return minVal

    if numType == 'continuous':
        return min_max_projection(random.random(),
                              minVal,
                              maxVal)

    elif numType == 'discrete':
        return random.choice(range(int(minVal), int(maxVal)+1))

def initPositions(paramTypes, n):
    positions = {}

    for i in range(n):
        positions[i] = map(makeRandomElement,
                           paramTypes.numType, paramTypes.minVal, paramTypes.maxVal)

    return pd.DataFrame(positions)
