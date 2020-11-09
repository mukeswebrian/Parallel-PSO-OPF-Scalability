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
    parameter default values

    n = 100 # number of particles
    alpha1 = 0.2 # attraction to personal best
    alpha2 = 0.2 # attraction to globa; best
    omega = 0.5 # intertia
    iterations = 100 # maximum number of iterations
    case = 'pglib_opf_case57_ieee.mat' # specify the power system to use
    '''

    print('Initializing case ...')

    # read problem parameters
    # net = util.loadPowerSys(case)
    net = networks.case14()
    paramTypes = rd.get1DparameterArray(net)

    nParticles = int(sys.argv[3])

    # initialize particles
    # - positions
    # - velociities
    positions = util.initPositions(paramTypes, nParticles)
    velocities = util.initVelocities(paramTypes, nParticles)

    fitness = pd.Series([-1 for pos in positions.columns], index=positions.columns)
    pBestFitness = copy.deepcopy(fitness)
    pBestPos = copy.deepcopy(positions)
    gBestFitness = -1
    gBestPos = pd.Series(dtype=float)

    case = sys.argv[1]
    iterations = int(sys.argv[2])

    alpha1 = float(sys.argv[4])
    alpha2 = float(sys.argv[5])
    omega = float(sys.argv[6])
    run_name = sys.argv[7]


    # log inputs
    inputs = [case, iterations, nParticles, alpha1, alpha2, omega]
    names = ['case', 'iterations', 'nParticles', 'alpha1', 'alpha2', 'omega']
    log_util.logInputs(inputs, names, run_name)

    # initalize data logger
    log = log_util.createIterLog(run_name)

    # start iteration loop
    i = 0

    # init subprocesses
    subprocesses = Pool(3).map

    # show progress bar
    bar = Bar('Running iterations:', max=iterations)

    # start timer
    tStart = time.perf_counter()

    while i<iterations:
        particles = positions.columns
        nets = [copy.deepcopy(net) for particle in particles]
        pTypes = [paramTypes for particle in particles]
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
        log_util.logIter(log, i, gBestFitness, tIter-tStart)

    bar.finish()
    del(log)

    # save network file with best solution
    util.saveBestCase(net, gBestPos, paramTypes, run_name)

    print('\ndone!')
