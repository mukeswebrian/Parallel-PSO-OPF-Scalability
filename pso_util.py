import random
import pandas as pd
import pandapower as pp
from pandapower import networks
import pandapower.converter as pc
from pandapower.plotting import to_html
import network_component_updates as up
import os
import random as rd

def loadPowerSys(case):
    # if case is not in case list, use built in case
    if case in os.listdir(os.path.join(os.getcwd(), 'case_files')):
        net = pc.from_mpc(os.path.join(os.getcwd(), 'case_files', case),
                      casename_mpc_file='ans')
    else:
        net = networks.case14()

    return net


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

def initVelocities(paramTypes, n):
    # intialize stationary particles
    velocities = {}

    for i in range(n):
        velocities[i] = [0 for i in paramTypes.index]

    return pd.DataFrame(velocities)

def calcFitness(net, param_data):

    '''
    Fitness Evaluation: calculate total real power losses
    '''

    # write particle data to network
    up.updateControlParams(net, param_data)

    # solve case
    pp.runpp(net)

    # calculate total real power losses
    loss = net.res_line.pl_mw.sum() + net.res_trafo.pl_mw.sum() + net.res_trafo3w.pl_mw.sum()

    return loss

def saveBestCase(net, gBestPos, paramTypes, run_name):
    '''
    Save the case data for the global best solution
    '''
    gBestPos.name = 'params'
    param_data = pd.concat([gBestPos, paramTypes.paramType, paramTypes['index']], axis=1)

    # write particle data to network and solve case
    up.updateControlParams(net, param_data)
    pp.runpp(net)

    to_html(net, os.path.join(os.getcwd(), 'run_results',run_name+'.html')) # save solved case


def updateVelocities(velocities, positions, pBestPos, gBestPos, omega, alpha1, alpha2):
    '''
    Execute PSO velocity update step
    '''
    term1 = (omega * velocities)
    term2 = (alpha1 * rd.random() * (pBestPos-positions))
    term3 = (alpha2 * rd.random() * (gBestPos-positions.T).T)

    velocities = term1 + term2 + term3
    return velocities

def updatePositions(positions, velocities, paramTypes):
    '''
    Update the particle positions while handilng special cases i.e.
      1. handling discrete dimentions
      2. handling min and max limits
    '''

    def checkLimits(x, minVal, maxVal):
        if minVal<=x and x<=maxVal:
            return x
        elif x<minVal:
            return minVal
        else:# then x is greater than maxVal
            return maxVal

    # Handle discrete dimensions
    filt = lambda x: x=='discrete'
    discrete = list(paramTypes[paramTypes.numType.apply(filt)].index)

    if discrete == []:# no discrete dimensions
        newPos = positions + velocities

    else:# handle discrete dimensions
        newPos = positions + velocities
        to_discrete = lambda x: round(x)
        dVals = newPos.loc[discrete].apply(to_discrete)
        newPos.update(dVals)

    # Handle max min limits
    for i in paramTypes.index:
        maxVal = paramTypes.loc[i].maxVal
        minVal = paramTypes.loc[i].minVal

        dimData = newPos.loc[i].apply(checkLimits, args=(minVal, maxVal))
        newPos.T.update(dimData)

    return newPos
