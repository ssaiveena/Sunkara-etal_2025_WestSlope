SLURM="#!/bin/bash\n\
#SBATCH --nodes=1\n\
#SBATCH --ntasks-per-node=40\n\
#SBATCH --export=ALL\n\
#SBATCH -t 3-2:00:00\n\
#SBATCH --exclusive\n\
#SBATCH --output=gm_with.out\n\
#SBATCH --error=gm_with.err\n\
#SBATCH --job-name=gm_with\n\

source /home/fs02/pmr82_0001/ss4285/myvenv/bin/activate\n\

mpirun python Step1a_extractCUshortage_parallel_cm.py"

echo -e $SLURM | sbatch
sleep 0.5 
