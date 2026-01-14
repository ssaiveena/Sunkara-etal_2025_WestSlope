import os
import numpy as np
from mpi4py import MPI
import sys
import subprocess
from mpi_run_parquet import XddConverter
# projectdirectory = '/home/fs02/pmr82_0001/ss4285/West_Slope_Exp/Statemod_input/'
projectdirectory = '/pscratch/sd/s/saiveena/West_Slope_Exp/Statemod_input/'

start_realization = np.arange(0,1000,1)#(0,100,10)

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

scenarios_per_rank = len(start_realization)//size
assigned_scenario = start_realization[rank*scenarios_per_rank : (rank+1)*scenarios_per_rank]
for scenario_loop in assigned_scenario:
    for i in range(20):
        scenario = 'S{}_{}'.format(scenario_loop, i)
        os.chdir(projectdirectory + 'Experiment_files/wodemand/' + 'S_{}'.format(scenario_loop) + '/')
        try:
            subprocess.run(['./statemod-17.0.3-gfortran-lin-64bit-o3', f'gm2015B_{scenario}', '-simulate'], check=True)
        except subprocess.CalledProcessError:
            pass

        # os.system('./statemod-17.0.3-gfortran-lin-64bit-o3 gm2015B_{} -simulate'.format(scenario))
        if os.path.getsize('gm2015B_{}'.format(scenario)+'.xdd')>100000000:
            os.remove('gm2015B_{}'.format(scenario)+'.xss')
            os.remove('gm2015B_{}'.format(scenario)+'.b43')
            os.remove('gm2015B_{}'.format(scenario)+'.b67')
            os.remove('gm2015B_{}'.format(scenario)+'.b39')
            os.remove('gm2015B_{}'.format(scenario) + '.b44')
            converter = XddConverter(
                output_path='./',
                allow_overwrite=True,
                xdd_files= 'gm2015B_{}'.format(scenario)+'.xdd',
                id_subset=None,
                parallel_jobs=1,
            )
            converter.convert()
            os.remove('gm2015B_{}'.format(scenario) + '.xdd')
        else:
            print('failed runs')
            print(scenario)
        # subprocess.run(['./statemod-17.0.3-gfortran-lin-64bit-o3', f'ym2015B_{scenario}', '-simulate'], check=True)
        try:
            subprocess.run(['./statemod-17.0.3-gfortran-lin-64bit-o3', f'ym2015B_{scenario}', '-simulate'], check=True)
        except subprocess.CalledProcessError:
            pass  # Ignore the error and continue with the next line
        # os.system('./statemod-17.0.3-gfortran-lin-64bit-o3 ym2015B_{} -simulate'.format(scenario))
        if os.path.getsize('ym2015B_{}'.format(scenario)+'.xdd')>100000000:
            os.remove('ym2015B_{}'.format(scenario)+'.xss')
            os.remove('ym2015B_{}'.format(scenario)+'.b43')
            os.remove('ym2015B_{}'.format(scenario)+'.b67')
            os.remove('ym2015B_{}'.format(scenario)+'.b39')
            os.remove('ym2015B_{}'.format(scenario)+'.b44')
            converter = XddConverter(
                output_path='./',
                allow_overwrite=True,
                xdd_files='ym2015B_{}'.format(scenario) + '.xdd',
                id_subset=None,
                parallel_jobs=1,
            )
            converter.convert()
            os.remove('ym2015B_{}'.format(scenario) + '.xdd')
        else:
            print('failed runs')
            print(scenario)
        try:
            subprocess.run(['./statemod-17.0.3-gfortran-lin-64bit-o3', f'wm2015B_{scenario}', '-simulate'], check=True)
        except subprocess.CalledProcessError:
            pass
        # os.system('./statemod-17.0.3-gfortran-lin-64bit-o3 wm2015B_{} -simulate'.format(scenario))
        if os.path.getsize('wm2015B_{}'.format(scenario)+'.xdd')>100000000:
            os.remove('wm2015B_{}'.format(scenario)+'.xss')
            os.remove('wm2015B_{}'.format(scenario)+'.b43')
            os.remove('wm2015B_{}'.format(scenario)+'.b67')
            os.remove('wm2015B_{}'.format(scenario)+'.b39')
            os.remove('wm2015B_{}'.format(scenario)+'.b44')
            converter = XddConverter(
                output_path='./',
                allow_overwrite=True,
                xdd_files='wm2015B_{}'.format(scenario) + '.xdd',
                id_subset=None,
                parallel_jobs=1,
            )
            converter.convert()
            os.remove('wm2015B_{}'.format(scenario) + '.xdd')
        else:
            print('failed runs')
            print(scenario)
        try:
            subprocess.run(['./statemod-17.0.3-gfortran-lin-64bit-o3', f'sj2015B_{scenario}', '-simulate'], check=True)
        except subprocess.CalledProcessError:
            pass
        # os.system('./statemod-17.0.3-gfortran-lin-64bit-o3 sj2015B_{} -simulate'.format(scenario))
        if os.path.getsize('sj2015B_{}'.format(scenario)+'.xdd')>100000000:
            os.remove('sj2015B_{}'.format(scenario)+'.xss')
            os.remove('sj2015B_{}'.format(scenario)+'.b43')
            os.remove('sj2015B_{}'.format(scenario)+'.b67')
            os.remove('sj2015B_{}'.format(scenario)+'.b39')
            os.remove('sj2015B_{}'.format(scenario)+'.b44')
            converter = XddConverter(
                output_path='./',
                allow_overwrite=True,
                xdd_files='sj2015B_{}'.format(scenario) + '.xdd',
                id_subset=None,
                parallel_jobs=1,
            )
            converter.convert()
            os.remove('sj2015B_{}'.format(scenario) + '.xdd')
        else:
            print('failed runs')
            print(scenario)

        # os.system('./statemod cm2015B_{} -simulate'.format(scenario))
        try:
            subprocess.run(['./statemod', f'cm2015B_{scenario}', '-simulate'], check=True)
        except subprocess.CalledProcessError:
            pass

        if os.path.getsize('cm2015B_{}'.format(scenario)+'.xdd')>100000000:
            os.remove('cm2015B_{}'.format(scenario)+'.xss')
            os.remove('cm2015B_{}'.format(scenario)+'.b43')
            os.remove('cm2015B_{}'.format(scenario)+'.b67')
            #os.remove('cm2015B_{}'.format(scenario)+'.b39')
            os.remove('cm2015B_{}'.format(scenario)+'.b44')
            converter = XddConverter(
                output_path='./',
                allow_overwrite=True,
                xdd_files='cm2015B_{}'.format(scenario) + '.xdd',
                id_subset=None,
                parallel_jobs=1,
            )
            converter.convert()
            os.remove('cm2015B_{}'.format(scenario) + '.xdd')
        else:
            print('failed runs')
            print(scenario)

comm.Barrier()
