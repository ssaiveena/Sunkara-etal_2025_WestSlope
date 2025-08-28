BASIN_NAME=sj2015
SOW=1

mkdir error
mkdir output
for i in {0..999}
do 
    mkdir  S${i}_1
    ln -s ../../../../../../statemod-17.0.3-gfortran-lin-64bit-o3 S${i}_1/
done

source /home/fs02/pmr82_0001/dfg42/statemod_training/cdss-app-statemod-fortran/src/main/fortran/sj2015_StateMod_modified/sj2015_StateMod_modified/StateMod/StateModPy/bin/activate

python gen_rsp.py BASIN_NAME SOW