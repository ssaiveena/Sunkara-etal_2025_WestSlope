#!/bin/bash
#SBATCH --account=m2702
#SBATCH -C cpu
#SBATCH --nodes=5
#SBATCH --ntasks-per-node=32
#SBATCH -t 30:00
#SBATCH --output=output/MPI_batch.out
#SBATCH --error=error/MPI_batch.err

module load python
conda activate my_mpi4py_env

srun python Step2a_generate_iwr_cm.py
