#!/bin/bash --login

# This is a Slurm script for the Tier2 system Cirrus

# Slurm job options (name, compute nodes, job time)
#SBATCH --job-name=pso_opf
#SBATCH --time=0:02:0
#SBATCH --exclusive
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=36

#SBATCH --account=dc116-s1895870
#SBATCH --partition=standard
#SBATCH --qos=standard


# configure environment
eval "$(/lustre/home/dc116/s1895870/miniconda3/bin/conda shell.bash hook)"
conda activate dissertation

# Change to the directory that the job was submitted from
cd $SLURM_SUBMIT_DIR

# execute parallel pso opf code
srun  --cpu-bind=cores python parallel_pso_algorithm.py "" 50 20 0.25 0.2 0.7 parallel20run1_4T 4
srun  --cpu-bind=cores python parallel_pso_algorithm.py "" 50 20 0.25 0.2 0.7 parallel20run1_8T 8
srun  --cpu-bind=cores python parallel_pso_algorithm.py "" 50 20 0.25 0.2 0.7 parallel20run1_12T 12
srun  --cpu-bind=cores python parallel_pso_algorithm.py "" 50 20 0.25 0.2 0.7 parallel20run1_16T 16
srun  --cpu-bind=cores python parallel_pso_algorithm.py "" 50 20 0.25 0.2 0.7 parallel20run1_20T 20
