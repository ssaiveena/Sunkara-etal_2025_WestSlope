
for i in {0..999}
do
    mkdir S${i}_1/parquet/
done

mkdir parquet

START_REL=0
NUM_REL=10
BASIN_NAME=sj

for i in $(seq $START_REL $NUM_REL 999)
do 
    SLURM="#!/bin/bash\n\
#SBATCH --nodes=1\n\
#SBATCH --ntasks-per-node=1\n\
#SBATCH --export=ALL\n\
#SBATCH -t 10:00:00\n\
#SBATCH --job-name=${BASIN_NAME}_${i}_parquet\n\
#SBATCH --output=output/${BASIN_NAME}_${i}_parquet.out\n\
#SBATCH --error=error/parquet_${BASIN_NAME}_${i}_parquet.err\n\


source /home/fs02/pmr82_0001/dfg42/statemod_training/cdss-app-statemod-fortran/src/main/fortran/sj2015_StateMod_modified/sj2015_StateMod_modified/StateMod/StateModPy/bin/activate\n\

time python updated_xdd_to_parquet.py $i $NUM_REL $BASIN_NAME"

    echo -e $SLURM | sbatch
    sleep 0.5 
done
