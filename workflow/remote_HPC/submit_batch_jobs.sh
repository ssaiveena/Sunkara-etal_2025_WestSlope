BASIN_NAME=sj2015
RUN_TYPE=baseline_run

START_REL=0
NUM_REL=10
END_REL=990

SOW=1

for i in $(seq $START_REL $NUM_REL $END_REL)
do 
    SLURM="#!/bin/bash\n\
#SBATCH --nodes=1\n\
#SBATCH --ntasks-per-node=1\n\
#SBATCH --export=ALL\n\
#SBATCH -t 10:00:00\n\
#SBATCH --job-name=${i}_${BASIN_NAME}\n\
#SBATCH --output=output/${BASIN_NAME}_${i}.out\n\
#SBATCH --error=error/${BASIN_NAME}_${i}.err\n\

source /home/fs02/pmr82_0001/dfg42/statemod_training/cdss-app-statemod-fortran/src/main/fortran/sj2015_StateMod_modified/sj2015_StateMod_modified/StateMod/StateModPy/bin/activate\n\
time python run_batch_jobs.py $BASIN_NAME $RUN_TYPE $i $NUM_REL $SOW"

	echo -e $SLURM | sbatch
	sleep 0.5
done


