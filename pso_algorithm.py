import pso_util as util


n = 10 # number of particles
alpha1 = 0.2 # attraction to personal best
alpha2 = 0.2 # attraction to globa; best
omega = 0.5 # intertia

# initialize particles
# - positions
# - velociities

positions = util.initPositions(paramTypes, n)



# start iteration loop

# calculate fitness of each particle

# update personal best for each particle
# update global best (to use best ever)

# update velociities
# update positions

# check loop termination criteria
