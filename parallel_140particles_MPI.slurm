#!/bin/bash --login

# This is a Slurm script for the Tier2 system Cirrus

# Slurm job options (name, compute nodes, job time)
#SBATCH --job-name=pso_opf
#SBATCH --time=0:40:0
#SBATCH --exclusive
#SBATCH --nodes=4
#SBATCH --tasks-per-node=36
#SBATCH --cpus-per-task=1

#SBATCH --account=dc116-s1895870
#SBATCH --partition=standard
#SBATCH --qos=standard


# configure environment
eval "$(/lustre/home/dc116/s1895870/miniconda3/bin/conda shell.bash hook)"
conda activate dissertation

# configure MPI compiler
module load mpt
module load intel-compilers-19
export MPICC_CC=icc
export OMP_NUM_THREADS=1

# Change to the directory that the job was submitted from
cd $SLURM_SUBMIT_DIR

# execute parallel pso opf code
srun python parallel_mpi_pso_algorithm.py "" 50 140 0.25 0.2 0.7 parallel_particles140_processes28_run1 28
srun python parallel_mpi_pso_algorithm.py "" 50 140 0.25 0.2 0.7 parallel_particles140_processes56_run1 56
srun python parallel_mpi_pso_algorithm.py "" 50 140 0.25 0.2 0.7 parallel_particles140_processes84_run1 84
srun python parallel_mpi_pso_algorithm.py "" 50 140 0.25 0.2 0.7 parallel_particles140_processes112_run1 112
srun python parallel_mpi_pso_algorithm.py "" 50 140 0.25 0.2 0.7 parallel_particles140_processes140_run1 140
