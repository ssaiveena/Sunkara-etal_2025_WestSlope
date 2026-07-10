[![DOI](https://zenodo.org/badge/481033714.svg)](https://doi.org/10.5281/zenodo.21294774)


# Sunkara-etal_2025_WestSlope

**Clarifying How the Drivers of Future Water Shortages Change across Regional to User-level Scales in Colorado’s West Slope River Basins**

Sai Veena, Sunkara <sup>1\*</sup>, David F. Gold<sup>2</sup>, and Patrick M. Reed <sup>1</sup>

<sup>1 </sup> School of Civil and Environmental Engineering, Cornell University, Ithaca, NY
<sup>2 </sup> Department of Physical Geography, Faculty of Geosciences, Utrecht University, Utrecht, Netherlands

\* corresponding author:  ss4285@cornell.edu

## Abstract
Colorado’s West Slope Basins are a critical source of water for the Colorado River, contributing approximately 70% of the inflows to Lake Powell in a typical year. Whether these basins will face intensifying water shortages by mid-century remains highly debated due to deep uncertainties in future climate conditions, including the possibility of wetter or drier futures, persistence of severe drought, population growth, and evolving multisectoral water demands. Identifying the primary drivers of plausible mid-century water shortages is particularly challenging given the region’s high internal climate variabil ity, changing hydrology, and complex institutional framework governing water rights for thousands of users. This study integrates large-scale exploratory modeling with diagnostic sensitivity analysis to clarify the relative influence of uncertain natural and human drivers of water shortages in the West Slope basins. A multi-site Hidden Markov Model (HMM) is used to generate a wide range of synthetic streamflow scenarios representing plausible mid-century changes relative to the historical baseline. These stochastic hydrologic scenarios span both wetter and drier futures and are combined with projected demand changes across sectors. The resulting scenarios are simulated within Colorado’s StateMod water allocation model to estimate water shortages at basin, district, and sectoral scales. Diagnostic sensitivity analysis reveals that the dominant drivers of shortages vary markedly by basin, district, major reservoir and sector. These findings provide actionable, scale-specific insights into the most influential factors shaping future water stress in Colorado’s West Slope basins.


## Journal reference
Sunkara, S.V., Gold, D. and Reed, P. Unraveling the Drivers of Water Shortage across Spatial Scales and Sectors in Colorado’s West Slope River Basins. Earth's Future
## Code reference
Sunkara, S.V., Gold, D. and Reed, P. Unraveling the Drivers of Water Shortage across Spatial Scales and Sectors in Colorado’s West Slope River Basins. Earth's Future (v1.0). Zenodo. https://doi.org/10.5281/zenodo.8388003

## Data reference
Sunkara, S.V., Gold, D. and Reed, P. (2026). Data for Unraveling the Drivers of Water Shortage across Spatial Scales and Sectors in Colorado's West Slope River Basins (Version v1) [Data set]. MSD-LIVE Data Repository. https://doi.org/10.57931/3012850

### Input data
Colorado Decision Support Systems: [https://cdss.colorado.gov/modeling-data/surface-water-statemod](https://cdss.colorado.gov/modeling-data/surface-water-statemod)

### Output data


## Contributing modeling software
| Model | Version | Repository Link | DOI |
|-------|---------|-----------------|-----|
| StateMod | 15.0 | [https://github.com/OpenCDSS/cdss-app-statemod-fortran](https://github.com/OpenCDSS/cdss-app-statemod-fortran) | - |

## Reproduce my experiment
This experiment has three main phases. First, the multi-site HMM is fit to the historical record of streamflows in the West Slope Basins. This can be done locally on a laptop or desktop. Second, the streamflow ensembles are genersted and run through StateMod, and output is collected and compressed. This step must be done on an HPC resource. This experiment was conducted on [NERSC Perlmutter](https://www.nersc.gov/what-we-do/computing-for-science/perlmutter) clusters. Finally, the StateMod output is post-processed, and figures are generated. This step can be done on a laptop, but is recommended to be completed on a HPC resource. 

### 1. Fit the multi-site HMM and generate synthetic streamflow ensembles for hydroclimatic and demand projections
| Script Name | Description | How to Run |
| --- | --- | --- |
| `Step0_fit_hmm.py` | Fits the HMM to 75 years of historical record and saves parameters to text files| `python3 fit_hmm.py` |
| `Step1_sample_parameters.sh` | uses the HMM parameters and demand factors to generate a  ensemble of annual streamflow records for each basin | `sh Step1_sample_parameters.sh` |
| `Step2_create_synthetic_records_num_realization.py` | applies adjustements the HMM parameters and generates an adjusted ensemble of annual streamflow records for each basin | `python3 Step2_create_synthetic_records_num_realization.py` |
| `Step3_annual_records_to_xbm_lhs.py` | disaggregates baseline synthetic records across space and time and creates StateMod input files (xbm) | `python3 Step3_annual_records_to_xbm_lhs.py` |

### 2. Run the ensemble through StateMod and compress the data output

1. Download and install StateMod from [Contributing modeling software](#contributing-modeling-software)
2. Navigate to the "fortran" directory, located within the directory you just downloaded (cdss-app-statemod-fortran/src/main/fortran)
3. Open the file called "makefile" and remove the term "-static" from lines 164 and 171
4. Compile the StateMod executable by typing: `make statemod` 
5. Download and install the StateMod input data for each West Slope basin (Upper Colorado, Gunnison, Yampa, White, and San Juan/Dolores) from CDSS [Input data](#input-data) and unzip the files
6. For each basin
   - Navigate to the "StateMod" directory. For example, for the Gunnison basin, navigate to "gm2015_StateMod_modified/      StateMod".
   - Create new directory "Experiment_Files"
   - Navigate to "Experiment_Files" and upload the 20000 xbm files generated by the HMM to the directory
   - Run the scripts in the table below
 7. Repeat step 6 for each basin
   - Note: it is highly recommended to remove raw StateMod output after completing each set of runs as it generates a few TB of data that are not needed for further analysis

| Script Name | Description | How to Run |
| --- | --- | --- |
| `Step0_rsp_demand.py` | Creates 20000 rsp files that determines the input file directories and output directories | `python3 Step0_rsp_demand.py` |
| `Step1_Extract_Structure_files.py` | Extracts the information of nodes that is later used for calculation of shortages and classification into different sectors | `python3 Step1_Extract_Structure_files.py` |
|`Step2_input_statemod_cm.py`| runs the python script to generate input files and store them in the desired folder | `python3 Step2_input_statemod_cm.py`|
|`Step2a_submit_mpi.sh` | runs the python script `Step2a_generate_iwr_cm.py` to generate .iwr files applyin demands changes sampled| `./Step2a_submit_mpi.sh`|
|`Step3a_submit_mpi.sh` | runs the python script `mpi_batch_jobs.py` to simulate StateMod for all scenarios | `./Step3a_submit_mpi.sh`|
|`Step4_mpi_submit_parquet.sh` | runs the python script `mpi_run_parquet.py` to compress .xdd files into parquet format | `./Step4_mpi_submit_parquet.sh`|

8. Run the following scripts in the `workflow/ProcessResults` directory to compare outputs to those from the publication

| Script Name | Description | How to Run |
| --- | --- | --- |
| `Step0_processoutflows.sh` | Extracts the total annual deliveries to Lake Powell for each realization using `ProcessPowellOutflows.py` | `./Step0_processoutflows.sh` |
|`Step1_submit_shortage_cm.sh` | Extracts the total annual consumptive use shortage from each basin for each realization using `Step1a_extractCUshortage_parallel_cm.py` This should be run 5 times for each of the West Slope basins| `Step1_submit_shortage_cm.sh` |
| `Step2_res_percentiles.py` | Extracts storage data from a reservoir of interest from .xre files to csv files | `python3 Step2_res_percentiles.py` |
| `Step2a_Reservoir_Storage_Sensitivity.py` | Extracts delta index by performing delta moment independent sensitivity analysis of reservoir storage to the sampled uncertain factors | `python3 Step2a_Reservoir_Storage_Sensitivity.py` |
| `Step3_Sensitivity_analysis_basin.py` | Extracts delta index by performing delta moment independent sensitivity analysis of shortages at basin scale to the sampled uncertain factors | `python3 Step3_Sensitivity_analysis_basin.py` |
| `Step3a_Sensitivity_analysis_district.py` | Extracts delta index by performing delta moment independent sensitivity analysis of shortages at district scale to the sampled uncertain factors | `python3 Step3a_Sensitivity_analysis_district.py` |
| `Step3b_Sensitivity_analysis_sector.py` | Extracts delta index by performing delta moment independent sensitivity analysis of shortages at sector scale to the sampled uncertain factors | `python3 Step3b_Sensitivity_analysis_sector.py` |

### 3. Reproduce figures
Use the scripts found in the `figures` directory to reproduce the figures used in this publication.

| Script Name | Description | How to Run |
| --- | --- | --- |
| `Figure4_Powell_Outflow_ANOVA.py` | Generates Figure 4 | `python3 Figure4_Powell_Outflow_ANOVA.py`|
| `Figure5_reservoir_percentile_plot_time.py` | Generates Figure 5 | `python3 Figure5_reservoir_percentile_plot_time.py`|
| `Figure6_CDF_shortage.py` | Generates Figure 6 | `python3 Figure6_CDF_shortage.py`|
| `Figure7_Shortage_duration_curves_basin.py` | Generates Figure 7 | `python3 Figure7_Shortage_duration_curves_basin.py` |
| `Figure8_Shortage_duration_curves_district.py` | Generates Figure 8 | `python3 Figure8_Shortage_duration_curves_district.py` |
| `Figure9_Shortage_duration_curves_sector.py` | Generates Figure 9 | `python3 Figure9_Shortage_duration_curves_sector.py` |
