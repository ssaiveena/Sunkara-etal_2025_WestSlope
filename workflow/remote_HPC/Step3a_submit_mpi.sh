#!/bin/bash
#SBATCH --nodes=10
#SBATCH --ntasks-per-node=100
#SBATCH --cpus-per-task=1
#SBATCH --account=m2702
#SBATCH -C cpu
#SBATCH --export=ALL
#SBATCH -t 20:29:00
#SBATCH --exclusive
#SBATCH --output=output/MPI_batch_wodemand.out
#SBATCH --error=error/MPI_batch.err
#SBATCH --job-name=wodemand
#SBATCH --qos=regular

module load python
module load conda
conda activate my_mpi4py_env

srun python mpi_batch_jobs.py
