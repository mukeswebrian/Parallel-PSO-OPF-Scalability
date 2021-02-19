#!/bin/bash --login

# This is a Slurm script for the Tier2 system Cirrus

# Slurm job options (name, compute nodes, job time)
#SBATCH --job-name=pso_opf
#SBATCH --time=0:50:0
#SBATCH --exclusive
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
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
# srun python parallel_mpi_pso_algorithm.py "" 50 1 0.25 0.2 0.7 parallel_particles1_processes1_run1 1
# srun python parallel_mpi_pso_algorithm.py "" 50 2 0.25 0.2 0.7 parallel_particles2_processes1_run1 1
# srun python parallel_mpi_pso_algorithm.py "" 50 3 0.25 0.2 0.7 parallel_particles3_processes1_run1 1
# srun python parallel_mpi_pso_algorithm.py "" 50 4 0.25 0.2 0.7 parallel_particles4_processes1_run1 1
# srun python parallel_mpi_pso_algorithm.py "" 50 5 0.25 0.2 0.7 parallel_particles5_processes1_run1 1

# srun python parallel_mpi_pso_algorithm.py "" 50 1 0.25 0.2 0.7 parallel_particles1_processes1_run2 1
# srun python parallel_mpi_pso_algorithm.py "" 50 2 0.25 0.2 0.7 parallel_particles2_processes1_run2 1
# srun python parallel_mpi_pso_algorithm.py "" 50 3 0.25 0.2 0.7 parallel_particles3_processes1_run2 1
# srun python parallel_mpi_pso_algorithm.py "" 50 4 0.25 0.2 0.7 parallel_particles4_processes1_run2 1
# srun python parallel_mpi_pso_algorithm.py "" 50 5 0.25 0.2 0.7 parallel_particles5_processes1_run2 1

# srun python parallel_mpi_pso_algorithm.py "" 50 1 0.25 0.2 0.7 parallel_particles1_processes1_run3 1
# srun python parallel_mpi_pso_algorithm.py "" 50 2 0.25 0.2 0.7 parallel_particles2_processes1_run3 1
# srun python parallel_mpi_pso_algorithm.py "" 50 3 0.25 0.2 0.7 parallel_particles3_processes1_run3 1
# srun python parallel_mpi_pso_algorithm.py "" 50 4 0.25 0.2 0.7 parallel_particles4_processes1_run3 1
# srun python parallel_mpi_pso_algorithm.py "" 50 5 0.25 0.2 0.7 parallel_particles5_processes1_run3 1

# srun python parallel_mpi_pso_algorithm.py "" 50 1 0.25 0.2 0.7 parallel_particles1_processes1_run4 1
# srun python parallel_mpi_pso_algorithm.py "" 50 2 0.25 0.2 0.7 parallel_particles2_processes1_run4 1
# srun python parallel_mpi_pso_algorithm.py "" 50 3 0.25 0.2 0.7 parallel_particles3_processes1_run4 1
# srun python parallel_mpi_pso_algorithm.py "" 50 4 0.25 0.2 0.7 parallel_particles4_processes1_run4 1
# srun python parallel_mpi_pso_algorithm.py "" 50 5 0.25 0.2 0.7 parallel_particles5_processes1_run4 1

# srun python parallel_mpi_pso_algorithm.py "" 50 1 0.25 0.2 0.7 parallel_particles1_processes1_run5 1
# srun python parallel_mpi_pso_algorithm.py "" 50 2 0.25 0.2 0.7 parallel_particles2_processes1_run5 1
# srun python parallel_mpi_pso_algorithm.py "" 50 3 0.25 0.2 0.7 parallel_particles3_processes1_run5 1
# srun python parallel_mpi_pso_algorithm.py "" 50 4 0.25 0.2 0.7 parallel_particles4_processes1_run5 1
# srun python parallel_mpi_pso_algorithm.py "" 50 5 0.25 0.2 0.7 parallel_particles5_processes1_run5 1

# srun python parallel_mpi_pso_algorithm.py "" 50 48 0.25 0.2 0.7 parallel_particles48_processes1_run1 1
# srun python parallel_mpi_pso_algorithm.py "" 50 48 0.25 0.2 0.7 parallel_particles48_processes1_run2 1
# srun python parallel_mpi_pso_algorithm.py "" 50 48 0.25 0.2 0.7 parallel_particles48_processes1_run3 1
# srun python parallel_mpi_pso_algorithm.py "" 50 48 0.25 0.2 0.7 parallel_particles48_processes1_run4 1
# srun python parallel_mpi_pso_algorithm.py "" 50 48 0.25 0.2 0.7 parallel_particles48_processes1_run5 1

# srun python parallel_mpi_pso_algorithm.py "" 50 96 0.25 0.2 0.7 parallel_particles96_processes1_run1 1
# srun python parallel_mpi_pso_algorithm.py "" 50 96 0.25 0.2 0.7 parallel_particles96_processes1_run2 1
# srun python parallel_mpi_pso_algorithm.py "" 50 96 0.25 0.2 0.7 parallel_particles96_processes1_run3 1
# srun python parallel_mpi_pso_algorithm.py "" 50 96 0.25 0.2 0.7 parallel_particles96_processes1_run4 1
# srun python parallel_mpi_pso_algorithm.py "" 50 96 0.25 0.2 0.7 parallel_particles96_processes1_run5 1


srun python parallel_mpi_pso_algorithm.py "case30" 50 1 0.25 0.2 0.7 parallel_particles1_processes1_run1_case30 1
srun python parallel_mpi_pso_algorithm.py "case30" 50 1 0.25 0.2 0.7 parallel_particles1_processes1_run2_case30 1

srun python parallel_mpi_pso_algorithm.py "case30" 50 2 0.25 0.2 0.7 parallel_particles2_processes1_run1_case30 1
srun python parallel_mpi_pso_algorithm.py "case30" 50 2 0.25 0.2 0.7 parallel_particles2_processes1_run3_case30 1

srun python parallel_mpi_pso_algorithm.py "case30" 50 3 0.25 0.2 0.7 parallel_particles3_processes1_run1_case30 1
srun python parallel_mpi_pso_algorithm.py "case30" 50 3 0.25 0.2 0.7 parallel_particles3_processes1_run2_case30 1

srun python parallel_mpi_pso_algorithm.py "case30" 50 4 0.25 0.2 0.7 parallel_particles4_processes1_run1_case30 1
srun python parallel_mpi_pso_algorithm.py "case30" 50 4 0.25 0.2 0.7 parallel_particles4_processes1_run2_case30 1

srun python parallel_mpi_pso_algorithm.py "case30" 50 5 0.25 0.2 0.7 parallel_particles5_processes1_run1_case30 1
srun python parallel_mpi_pso_algorithm.py "case30" 50 5 0.25 0.2 0.7 parallel_particles5_processes1_run2_case30 1
