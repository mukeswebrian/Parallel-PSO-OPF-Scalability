import pso_util as util
import read_control_parameters as rd
import copy
import pandas as pd
import sys
import os
from progress.bar import Bar

def runPSO(n=10, alpha1=0.2, alpha2=0.2, omega=0.5, iterations=100, case='pglib_opf_case57_ieee.mat', log='example.log'):
    '''
    parameter default values

    n = 10 # number of particles
    alpha1 = 0.2 # attraction to personal best
    alpha2 = 0.2 # attraction to globa; best
    omega = 0.5 # intertia
    iterations = 100 # maximum number of iterations
    case = 'pglib_opf_case57_ieee.mat' # specify the power system to use
    '''

    # open log file - overites file if it exists
    logFile = open(os.path.join(os.getcwd(), 'run_logs', log), 'w')
    logFile.write('case: {}, iter: {}, n: {}, a1,a2: {},{} omega: {}\n'.format(case, iterations, n, alpha1, alpha2, omega))
    logFile.write('\niter, bestFitness\n')
    # read problem parameters
    net = util.loadPowerSys(case)
    paramTypes = rd.get1DparameterArray(net)

    # initialize particles
    # - positions
    # - velociities
    positions = util.initPositions(paramTypes, n)
    velocities = util.initVelocities(paramTypes, n)


    # start iteration loop
    i = 0
    fitness = pd.Series([-1 for pos in positions.columns], index=positions.columns)
    pBestFitness = copy.deepcopy(fitness)
    pBestPos = copy.deepcopy(positions)
    gBestFitness = -1
    gBestPos = pd.Series(dtype=float)

    # show progress bar
    bar = Bar('Running iterations:', max=iterations)

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

            # update global best (to use best ever)
            if fitness.loc[particle] < gBestFitness or gBestFitness==-1:
                gBestFitness = fitness.loc[particle]
                gBestPos = copy.deepcopy(positions[particle])

        logFile.write('{}, {}\n'.format(i, gBestFitness))


        # update velocities
        velocities = util.updateVelocities(velocities, positions, pBestPos, gBestPos, omega, alpha1, alpha2)

        # update positions - integer dimentisons are truncated to the nearest int
        positions = util.updatePositions(positions, velocities, paramTypes)

        i += 1
        bar.next()
    bar.finish()

    logFile.write('\n\n Best Position \n')
    logFile.write(str(gBestPos))

    return {'gBestPos':gBestPos, 'gBestFitness':gBestFitness}


if __name__ == '__main__':

    print('Initializing case ...')
    case = sys.argv[1]
    iterations = int(sys.argv[2])
    run_name = sys.argv[3]

    best = runPSO(case=case, iterations=iterations, log=run_name+'.log')
    #print(best['gBestFitness'])
    #print(best['gBestPos'])
