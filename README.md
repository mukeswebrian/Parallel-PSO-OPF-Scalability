# Parallel-PSO-OPF-Scalability

## Background
MSc Dissertation project to study the scalability of the parallel Particle Swarm Optimization algorithm for solving the Optimal Power Flow problem.
In this project, we implement a parallelized version of the PSO algorithm that is applied to a power loss minimization problem using the IEE 20-bus benchmark system. The MPI implementation was executed on the Cirrus HPC system. 

### Particle Swarm Optimization (PSO)
PSO is an evolutionary heuristic search algorithm that was first described by a social psychologist and  an electrical engineer in 1995 to model the behavior of bird flock (Kennedy and Eberhart, 1995). The algorithm involves directly searching the problem hyperspace over several iterations using a population of candidate solutions that are referred to as “particles” to find an optimal solution.

### Optimal Power Flow (OPF)
An electrical power system refers to the set of components involved in the generation, transmission, and distribution of electricity. Supplying electricity to the loads on an electrical power system typically entails satisfying several constraints (e.g., safety and physical operation constraints) and solving optimization problems like power loss minimization. Generally, the OPF problem involves choosing the set of control parameters of the power system that optimizes a given metric e.g., financial cost of electricity generation, power loss, emissions etc. or a set of metrics (multi-objective optimization).

## Installing Dependencies 
<code>pip install -f requirements.txt</code>
