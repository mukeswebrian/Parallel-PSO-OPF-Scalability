'''
Author: Brian Mukeswe
Date: Novemebr 9, 2020
Email: b.mukeswe@sms.ed.ac.uk


Purpose: This is a Python based implemetnation of the canonical
         particle swarm optimization algorithm for optimal power flow.
'''
import pso_util as util
import read_control_parameters as rd
import copy
import pandas as pd
import sys
import os
from progress.bar import Bar
import log_util
import time
from pandapower import networks

def runPSO(case='', iterations=100, n=100, alpha1=0.25, alpha2=0.2, omega=0.65, run_name='example'):
    '''
    parameter default values

    n = 100 # number of particles
    alpha1 = 0.2 # attraction to personal best
    alpha2 = 0.2 # attraction to globa; best
    omega = 0.5 # intertia
    iterations = 100 # maximum number of iterations
    case =  None # path to the MATPOWER power system to use (.mat file)
    '''

    # log inputs
    log_destination = 'file' # either "file" or "database"
    inputs = [case, iterations, n, alpha1, alpha2, omega]
    names = ['case', 'iterations', 'nParticles', 'alpha1', 'alpha2', 'omega']
    log_util.logInputs(inputs, names, run_name, log_destination)

    # initalize data logger
    log = log_util.createIterLog(run_name, log_destination)

    # load case data
    if case == '':
        net = networks.case14() # use built in IEEE 14 bus case by default
    else:
        net = util.loadPowerSys(case)

    paramTypes = rd.get1DparameterArray(net)

    # initialize particles
    # - positions
    # - velociities
    positions = util.initPositions(paramTypes, n)
    velocities = util.initVelocities(paramTypes, n)


    # intialize iteration variables
    i = 0
    fitness = pd.Series([-1 for pos in positions.columns], index=positions.columns)
    pBestFitness = copy.deepcopy(fitness)
    pBestPos = copy.deepcopy(positions)
    gBestFitness = -1
    gBestPos = pd.Series(dtype=float)

    # show progress bar
    bar = Bar('Running iterations:', max=iterations)

    # start timer
    tStart = time.perf_counter()

    # start iteration loop
    while i<iterations:

        # calculate fitness of each particle
        for particle in positions.columns:
            param_data = pd.concat([positions[particle], paramTypes.paramType, paramTypes['index']], axis=1)
            param_data.rename(columns={particle:'params'}, inplace=True)

            fitnessVal = util.calcFitness(net, param_data)
            fitness.update(pd.Series([fitnessVal], index=[particle]))

            # update personal best (minimization)
            if fitnessVal < pBestFitness.loc[particle] or pBestFitness.loc[particle] == -1:
                pBestFitness.update(pd.Series([fitnessVal], index=[particle]))
                pBestPos.update(copy.deepcopy(positions[particle]))

            # update global best (use best ever)
            if fitness.loc[particle] < gBestFitness or gBestFitness==-1:
                gBestFitness = fitness.loc[particle]
                gBestPos = copy.deepcopy(positions[particle])

        # update velocities
        velocities = util.updateVelocities(velocities, positions, pBestPos, gBestPos, omega, alpha1, alpha2)

        # update positions - integer dimentisons are truncated to the nearest int
        positions = util.updatePositions(positions, velocities, paramTypes)

        i += 1
        bar.next()
        tIter = time.perf_counter()
        log_util.logIter(log, i, gBestFitness, tIter-tStart, log_destination)

    bar.finish() # terminate progress bar
    log_util.endLog(log, run_name, log_destination) # terminate data logger

    # save network file with best solution
    util.saveBestCase(net, gBestPos, paramTypes, run_name)

    print('\ndone!')


if __name__ == '__main__':

    print('Initializing case ...')
    case = sys.argv[1]
    iterations = int(sys.argv[2])
    nParticles = int(sys.argv[3])
    alpha1 = float(sys.argv[4])
    alpha2 = float(sys.argv[5])
    omega = float(sys.argv[6])
    run_name = sys.argv[7]

    runPSO(case=case,
           iterations=iterations,
           n=nParticles,
           alpha1=alpha1,
           alpha2=alpha2,
           omega=omega,
           run_name=run_name)
