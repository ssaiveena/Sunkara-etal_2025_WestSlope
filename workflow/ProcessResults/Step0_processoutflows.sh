SLURM="#!/bin/bash\n\
#SBATCH --nodes=1\n\
#SBATCH --ntasks-per-node=1\n\
#SBATCH --export=ALL\n\
#SBATCH -t 2-4:00:00\n\
#SBATCH --exclusive\n\
#SBATCH --output=MPI_batch_with.out\n\
#SBATCH --error=MPI_batch_with.err\n\
#SBATCH --job-name=outflows_with\n\

source /home/fs02/pmr82_0001/ss4285/myvenv/bin/activate\n\

mpirun python ProcessPowellOutflows.py"

echo -e $SLURM | sbatch
sleep 0.5 
