'''
This file concatenates CMIP5 monthly chunks of data for the historical and RCP8.5 experiments located in 
/g/data1/ua6/DRSv2/CMIP5/
and places the concatenated complete runs in
/g/data/e14/erd561/CMIP5/

This code needs to be run in python 3 and uses the NCO toolkit
module load python3
module load nco

Earl Duran 
created: 23-Feb-18
e.duran@unsw.edu.au

HIST:
experiment = 'historical'
start_time = 198101
finish_time = 200012

RCP:
experiment = 'rcp85'
start_time = 208101
finish_time = 210012
'''

import os

CMIP5_dir = '/g/data1/ua6/DRSv2/CMIP5'

my_dir = '/g/data/e14/erd561/CMIP5/anthurium'

models_list = sorted(os.listdir(CMIP5_dir))

# rcp85 or historical
experiment = raw_input('experiment? e.g. rcp85, historical: ')

if experiment == 'rcp85':
    start_time = 208101
    finish_time = 210012
elif experiment == 'historical':
    start_time = 198101
    finish_time = 200012

frequency = 'mon'

medium = raw_input('medium? e.g. ocean, atmos: ')

# tos or tauuo
var = raw_input('var? e.g. thetao, tauuo, uas, vas: ')

version = 'latest'

print("Processing for " + var + " " + experiment + " ... \n")

for model in models_list:
    pls = os.listdir(CMIP5_dir + '/' + model)
    
    if experiment in pls:
        input_path = CMIP5_dir + '/' + model + '/' + experiment
        pls = os.listdir(input_path)
    else:
        print(model + " doesn't have a " + experiment + " experiment...")
        print('rejected. \n')
        continue

    if frequency in pls:
        input_path = CMIP5_dir + '/' + model + '/' + experiment + '/' + frequency
        pls = os.listdir(input_path)
    else:
        print(model + " doesn't have a " + frequency + " frequency...")
        print('rejected. \n')
        continue

    if medium in pls:
        input_path = CMIP5_dir + '/' + model + '/' + experiment + '/' + frequency + '/' + \
            medium
        pls = sorted(os.listdir(input_path))
    else:
        print(model + " doesn't have a " + medium + " medium...")
        print('rejected. \n')
        continue
        
    for initial_cond in pls:
        if initial_cond in ['r1i1p1', 'r2i1p1', 'r3i1p1']:
            input_path = CMIP5_dir + '/' + model + '/' + experiment + '/' + frequency + '/' + \
                medium + '/' + initial_cond
            pls = os.listdir(input_path)
        else:
            print(model + " doesn't have either r1i1p1 r2i1p1 r3i1p1 initial conditions...")
            print('rejected. \n')
            break

        if var in pls:
            input_path = CMIP5_dir + '/' + model + '/' + experiment + '/' + frequency + '/' + \
                medium + '/' + initial_cond  + '/' +  var
            pls = os.listdir(input_path)
        else:
            print(model + " doesn't have the " + var + " variable...")
            print('rejected. \n')
            continue

        if version in pls:
            input_path = CMIP5_dir + '/' + model + '/' + experiment + '/' + frequency + '/' + \
                medium + '/' + initial_cond  + '/' +  var  + '/' +  version
            pls = sorted(os.listdir(input_path))
        else:
            print(model + " doesn't have a " + version + " version...")
            print('rejected. \n')
            continue

        # If the CMIP5 Historical runs at least start before the start_time
        if int(pls[0][-16:-10]) <= start_time:
            print(model + " starts in " + pls[0][-16:-10] + " on or before " + str(start_time) + " so all good...")
        else:
            print(model + " starts in " + pls[0][-16:-10] + " after " + str(start_time) + " so that's rejected. \n")
            continue
        # And finish in December 2005
        if int(pls[-1][-9:-3]) >= finish_time:
            print(model + " finishes in " + pls[-1][-9:-3] + " on or after " + str(finish_time) + " so all good...")
        else:
            print(model + " finishes in " + pls[-1][-9:-3] + " before " + str(finish_time) + " so that's rejected. \n")
            continue


        ########################################        
        output_path = my_dir + '/' + experiment + '/' + frequency + '/' + \
                medium + '/' +  var  + '/' +  version
        output_name = model + '_' + initial_cond + '_' + pls[0][-16:-10] + '-' + pls[-1][-9:-3] + '.nc'
        output_data_path = output_path + '/' +  output_name
        ########################################

        # Because surface properties are 2D, the data should be in one file
        if len(pls) == 1:
            print("copying into " + output_data_path + "...")
            ########################################
            input_data_path = input_path + '/' +  pls[0]
            ########################################

            pls_out = os.listdir(output_path)
            if output_name in pls_out:
                print("it's already there! \n")
            else:
                os.system('cp ' + input_data_path + ' ' + output_data_path)
                print('Done. \n')
                break

        else:
            print(model + " has " + str(len(pls)) + " chunks of data and not one...")
            print("concatenating into " + output_data_path + "...")
            ########################################
            input_data_path = ''
            for n in range(len(pls)):
                input_data_path += input_path + '/' + pls[n] + ' '
            ########################################

            pls_out = os.listdir(output_path)
            if output_name in pls_out:
                print("it's already there! \n")
            else:
                os.system('ncrcat ' + input_data_path + ' ' + output_data_path)
                print('Done. \n')
                break

    continue
            
            
            
            
            
            
            
