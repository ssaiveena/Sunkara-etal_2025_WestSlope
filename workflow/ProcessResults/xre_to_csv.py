
import csv
import sys

def xre_to_csv(inputfile, hmm, realization, basin, structure_name, structure_ID):
    """
    Writes the data for a single reservoir from a raw .xre file to a csv file

    :param inputfile: the name of the xre file to be read
    :param basin: basin name (Gunnison, SanJuan_Dolores, Upper_CO, White or Yampa)
    :param structure_name: Name of the reservoir
    :param structure_ID: structure ID of the reservoir

    :example:

    .. code-block::python

        # Example with Granby Reservoir on the Upper Colorado River

        # input reservoir information
        xre_file = 'cm2015B.xre' # path the the xre file
        structure_ID = '5104055' # structure ID for reservoir of interest
        structure_name = 'Granby' # name of the reservoir

        xre_to_csv(xre_file, 'Upper_CO', structure_name, structure_ID)

    """

    # input reservoir information
    xre_file = inputfile  # path the the xre file

    # Open the .res file and grab the contents of the file
    with open(xre_file, 'r') as f:
        all_data_xre = [x for x in f.readlines()]
    f.close()

    with open(xre_file, 'r') as f:
        all_split_data_xre = [x.split('.') for x in f.readlines()]
    f.close()

    out_data = [['Res ID', 'ACC', 'Year', 'MO', 'Init. Storage', 'From River By Priority', 'From River By Storage',
                 'From River By Other', 'From River By Loss', 'From Carrier By Priority',
                 'From Carrier By Other', 'From Carrier By Loss', 'Total Supply', 'From Storage to River For Use',
                 'From Storage to River for Exc', 'From Storage to Carrier for use', 'Total Release', 'Evap',
                 'Seep and Spill', 'EOM Content', 'Target Stor', 'Decree Lim', 'River Inflow', 'River Release',
                 'River Divert',
                 'River by Well', 'River Outflow']]

    # loop through each line and identify the structure of interest
    for i in range(len(all_data_xre)):
        row_id_data = []  # this will store the structure ID, account num, year, month and init storage
        row_id_data.extend(all_split_data_xre[i][0].split())  # loading the data described above
        if row_id_data and row_id_data[0] == structure_ID:  # if the structure is the one we're looking for
            row_detail_data = all_split_data_xre[i][1:]  # first grab the initial data
            out_data.append(
                row_id_data + row_detail_data)  # combine it with the rest of the data and append to out_data

    # write the output data
    out_file = open('ReservoirResults/' + basin + '/'  +  structure_name + '_S' + str(hmm) + '_' + str(realization) + '_xre_data_wodemand.csv', 'a+', newline='')
    with out_file:
        write = csv.writer(out_file)
        write.writerows(out_data)

# basin = 'wm'#sys.argv[1]
# structure_name = 'WC' #lake granby
# structure_ID = '4404313'#'5104055'for granby (UC) #BM blue mesa 6203532 (gunnison), Mcphee MR 7103614 (sanjuan)

# for hmm in range(1000):
#     for realization in range(20):
#         xre_file =  '../ReservoirData/withoutdemand/' + basin + '2015B_S' + str(hmm) + '_' + str(realization) + '.xre'
#         xre_to_csv(xre_file, hmm, realization, basin, structure_name, structure_ID)

def xre_to_csv_hist(inputfile,basin, structure_name, structure_ID):
    """
    Writes the data for a single reservoir from a raw .xre file to a csv file

    :param inputfile: the name of the xre file to be read
    :param basin: basin name (Gunnison, SanJuan_Dolores, Upper_CO, White or Yampa)
    :param structure_name: Name of the reservoir
    :param structure_ID: structure ID of the reservoir

    :example:

    .. code-block::python

        # Example with Granby Reservoir on the Upper Colorado River

        # input reservoir information
        xre_file = 'cm2015B.xre' # path the the xre file
        structure_ID = '5104055' # structure ID for reservoir of interest
        structure_name = 'Granby' # name of the reservoir

        xre_to_csv(xre_file, 'Upper_CO', structure_name, structure_ID)

    """

    # input reservoir information
    xre_file = inputfile  # path the the xre file

    # Open the .res file and grab the contents of the file
    with open(xre_file, 'r') as f:
        all_data_xre = [x for x in f.readlines()]
    f.close()

    with open(xre_file, 'r') as f:
        all_split_data_xre = [x.split('.') for x in f.readlines()]
    f.close()

    out_data = [['Res ID', 'ACC', 'Year', 'MO', 'Init. Storage', 'From River By Priority', 'From River By Storage',
                 'From River By Other', 'From River By Loss', 'From Carrier By Priority',
                 'From Carrier By Other', 'From Carrier By Loss', 'Total Supply', 'From Storage to River For Use',
                 'From Storage to River for Exc', 'From Storage to Carrier for use', 'Total Release', 'Evap',
                 'Seep and Spill', 'EOM Content', 'Target Stor', 'Decree Lim', 'River Inflow', 'River Release',
                 'River Divert',
                 'River by Well', 'River Outflow']]

    # loop through each line and identify the structure of interest
    for i in range(len(all_data_xre)):
        row_id_data = []  # this will store the structure ID, account num, year, month and init storage
        row_id_data.extend(all_split_data_xre[i][0].split())  # loading the data described above
        if row_id_data and row_id_data[0] == structure_ID:  # if the structure is the one we're looking for
            row_detail_data = all_split_data_xre[i][1:]  # first grab the initial data
            out_data.append(
                row_id_data + row_detail_data)  # combine it with the rest of the data and append to out_data

    # write the output data
    out_file = open('ReservoirResults/' + basin + '/'  +  structure_name + '_xre_data_hist.csv', 'a+', newline='')
    with out_file:
        write = csv.writer(out_file)
        write.writerows(out_data)

basin = 'sj'#sys.argv[1]
structure_name = 'MR' #lake granby
structure_ID = '7103614'#'5104055'for granby (UC) #BM blue mesa 6203532 (gunnison), Mcphee MR 7103614 (sanjuan)

xre_file =  '../../sj2015_StateMod_modified/StateMod/' + 'sj2015B.xre'
xre_to_csv_hist(xre_file, basin, structure_name, structure_ID)