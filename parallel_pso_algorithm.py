'''
Author: Brian Mukeswe
Date: Novemebr 9, 2020
Email: b.mukeswe@sms.ed.ac.uk


Purpose: This is a parallelized Python based implemetnation of the canonical
         particle swarm optimization algorithm for optimal power flow.

         Fitness evaluation of each particle can be distributed across multiple
         computing threads.
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
from multiprocessing import Pool


def updateParticles(info):
    particle, net, paramTypes, position = info
    param_data = pd.concat([position, paramTypes.paramType, paramTypes['index']], axis=1)
    param_data.rename(columns={particle:'params'}, inplace=True)

    fitnessVal = util.calcFitness(net, param_data)

    return particle, fitnessVal

def updateFitness(fitnessValues):
    particle = []
    values = []
    for particle, value in fitnessValues:
        particles.append(particles)
        values.append(value)

    fitness = pd.Series(values, index=particles)

    return fitness



if __name__ == '__main__':
    '''
    suggested parameter default values

    n = 100 # number of particles
    alpha1 = 0.2 # attraction to personal best
    alpha2 = 0.2 # attraction to globa; best
    omega = 0.5 # intertia
    iterations = 100 # maximum number of iterations
    case =  None # path to the MATPOWER power system to use (.mat file)
    '''

    print('Initializing case ...')


    # load case data
    case = sys.argv[1]
    if case == '':
        net = networks.case14() # use built in IEEE 14 bus case by default
    else:
        net = util.loadPowerSys(case)
    paramTypes = rd.get1DparameterArray(net)

    # load algorithm parameters
    nParticles = int(sys.argv[3])
    iterations = int(sys.argv[2])
    alpha1 = float(sys.argv[4])
    alpha2 = float(sys.argv[5])
    omega = float(sys.argv[6])
    run_name = sys.argv[7]
    nThreads = int(sys.argv[8])

    # log inputs
    log_destination = 'file' # either "file" or "database"
    inputs = [case, iterations, nParticles, alpha1, alpha2, omega]
    names = ['case', 'iterations', 'nParticles', 'alpha1', 'alpha2', 'omega']
    log_util.logInputs(inputs, names, run_name, log_destination)

    # initalize data logger
    log = log_util.createIterLog(run_name, log_destination)

    # initialize particles
    # - positions
    # - velociities
    positions = util.initPositions(paramTypes, nParticles)
    velocities = util.initVelocities(paramTypes, nParticles)

    # intialize iteration variables
    fitness = pd.Series([-1 for pos in positions.columns], index=positions.columns)
    pBestFitness = copy.deepcopy(fitness)
    pBestPos = copy.deepcopy(positions)
    gBestFitness = -1
    gBestPos = pd.Series(dtype=float)


    # init subprocesses
    subprocesses = Pool(nThreads).map

    # replicate network data for each particle
    particles = positions.columns
    nets = [copy.deepcopy(net) for particle in particles]
    pTypes = [paramTypes for particle in particles]

    # show progress bar
    bar = Bar('Running iterations:', max=iterations)

    # start timer
    tStart = time.perf_counter()

    # start iteration loop
    i = 0
    while i<iterations:
        # update particle fitness values using parallel threads
        pos = [positions[particle] for particle in particles]
        info = [(particle,net,pType,p) for particle,net,pType,p in zip(particles, nets, pTypes, pos)]
        fitnessValues = subprocesses(updateParticles, info)
        fitness = updateFitness(fitnessValues)

        for particle in fitness.index:

            fitnessVal = fitness.loc[particle]

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
