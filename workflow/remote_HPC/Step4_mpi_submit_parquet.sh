#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=100
#SBATCH --cpus-per-task=1
#SBATCH --account=m2702
#SBATCH -C cpu
#SBATCH --export=ALL
#SBATCH -t 29:00
#SBATCH --exclusive
#SBATCH --output=output/MPI_parquet.out
#SBATCH --error=error/MPI_parquet.err
#SBATCH --job-name=parquet_mpi


module load python
module load conda
conda activate my_mpi4py_env

srun python mpi_run_parquet.py
