# Parallel-PSO-OPF-Scalability

>Note: All code snipets assume that the project's parent directory is the current active directory.

## Work Undertaken
In this MSc Dissertation project, we implemented a parallelized version of the PSO algorithm that was applied to a power loss minimization problem and executed on the [Cirrus Supercomputing System](https://www.cirrus.ac.uk/). We also explored how our implementation of the parallel PSO algorithm exploits the additional computational resources availed by the Cirrus system to minimize the computation time required to achieve an acceptable solution for the problem of minimizing power loss in the [IEEE 14 Bus benchmark power system](https://labs.ece.uw.edu/pstca/pf14/pg_tca14bus.htm). 

#### Particle Swarm Optimization (PSO)
PSO is an evolutionary heuristic search algorithm that was first described by a social psychologist and an electrical engineer in 1995 to model the behavior of bird flock (Kennedy and Eberhart, 1995). The algorithm involves directly searching the problem hyperspace over several iterations using a population of candidate solutions that are referred to as “particles” to find an optimal solution.

#### Optimal Power Flow (OPF)
An electrical power system refers to the set of components involved in the generation, transmission, and distribution of electricity. Supplying electricity to the loads on an electrical power system typically entails satisfying several constraints (e.g., safety and physical operation constraints) and solving optimization problems like power loss minimization. Generally, the OPF problem involves choosing the set of control parameters of the power system that optimizes a given metric e.g., financial cost of electricity generation, power loss, emissions etc. or a set of metrics (multi-objective optimization).

## Installing Dependencies 
>> <code>pip install -f requirements.txt</code>

## Visualization of Results
As part of the project, a custom browser-based interactive viewer was implemented using [Streamlit](https://www.streamlit.io/) to facilitate analysis of experimetal data. The viewer can be started using the following command:
>> <code>streamlit run run_viewer.py</code>

Here is a snapshot of the viewer
> ![viewer](archives/image.png)


## Project Work Plan
> ![viewer](archives/work_plan.png)
