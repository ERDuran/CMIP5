'''
This file concatenates CMIP5 monthly chunks of data for 
the historical and RCP8.5 experiments located in 
/g/data1/ua6/DRSv2/CMIP5/
and places the concatenated complete runs in
/g/data/e14/erd561/CMIP5/

This code needs to be run in python 2 and uses the NCO toolkit
module load python/2.x.x
module load nco

Earl Duran 
created: 23-Feb-18
e.duran@unsw.edu.au

HIST:
experiment = 'historical'
start_time = 198001
finish_time = 199912

RCP:
experiment = 'rcp85'
start_time = 208001
finish_time = 209912
'''

import os
import numpy as np

CMIP5_dir = '/g/data1/ua6/DRSv2/CMIP5'

my_dir = '/g/data/e14/erd561/CMIP5/anthurium'

models_list = sorted(os.listdir(CMIP5_dir))

# rcp85 or historical
experiment = raw_input('experiment? e.g. rcp85, historical: ')

if experiment == 'rcp85':
    start_time = 208001
    finish_time = 209912
elif experiment == 'historical':
    start_time = 198001
    finish_time = 199912

frequency = 'mon'

medium = raw_input('medium? e.g. ocean, atmos: ')

# tos or tauuo
var = raw_input('var? e.g. thetao, tauu, uas, vas: ')

version = 'latest'

print("Processing for " + var + " " + experiment + " ... \n")

for model in models_list:
    if model in ['CMCC-CESM']:
        print(model + " skipping as some data is missing...\n") 
        continue
    elif model in ['EC-EARTH']:
        if var in ['uas', 'vas']:
            print(model + " skipping as some data is missing...\n") 
            continue
    
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
    
    print(pls)
    for initial_cond in pls:
        print(initial_cond)
        if initial_cond in [
            'r1i1p1', 'r2i1p1', 'r3i1p1', 'r4i1p1', 'r5i1p1', 
            'r6i1p1', 'r7i1p1', 'r8i1p1', 'r9i1p1']:
            input_path = CMIP5_dir + '/' + model + '/' + experiment + '/' + frequency + '/' + \
                medium + '/' + initial_cond
            pls = os.listdir(input_path)
        else:
            print(model + " doesn't have initial conditions between r1i1p1 and r9i1p1...")
            print('rejected. \n')
            continue

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
            print(model + " starts in " + pls[0][-16:-10] + 
                  " on or before " + str(start_time) + " so all good...")
        else:
            print(model + " starts in " + pls[0][-16:-10] + 
                  " after " + str(start_time) + " so that's rejected. \n")
            continue
        # And finish in December 2005
        if int(pls[-1][-9:-3]) >= finish_time:
            print(model + " finishes in " + pls[-1][-9:-3] + 
                  " on or after " + str(finish_time) + " so all good...")
        else:
            print(model + " finishes in " + pls[-1][-9:-3] + 
                  " before " + str(finish_time) + " so that's rejected. \n")
            continue
        
        if len(pls) == 1:
            print(model + ' has only one file so no need to concatenate!...')
            ########################################        
            output_path = my_dir + '/' + experiment + '/' + frequency + '/' + \
                    medium + '/' +  var  + '/' +  version
            output_name = model + '_' + initial_cond + '_' + \
            pls[0][-16:-10] + '-' + pls[0][-9:-3] + '.nc'
            output_data_path = output_path + '/' +  output_name
            input_data_path = input_path + '/' + pls[0]
            ########################################
            print('copying in ' + output_data_path + '...')
            pls_out = os.listdir(output_path)
            if output_name in pls_out:
                print("it's already there! \n")
                break
            else:
                os.system('cp ' + input_data_path + ' ' + output_data_path)
                print('Done. \n')
                break
        
        # We concatenate desired time range
        pls_flipped = np.flipud(pls)
        
        start_idx_flipped, start_chunk = next((
            (idx,chunk) for idx,chunk in enumerate(pls_flipped) 
            if int(chunk[-16:-10]) <= start_time), None)
        start_idx = len(pls_flipped) - start_idx_flipped -1
        
        finish_idx, finish_chunk = next((
            (idx,chunk) for idx,chunk in enumerate(pls) 
            if int(chunk[-9:-3]) >= finish_time), None)
        
        print(model + 
              " concat starts in " + start_chunk[-16:-10] + 
              " and finishes in " + finish_chunk[-9:-3] + "...")
        
        idxes = list(range(start_idx,finish_idx+1))
        idxes_len = len(idxes)+1
        print(model + " has " + str(idxes_len) + " chunks of data...")
        
        if idxes_len == 1:
            print('which is only one file so no need to concatenate!...')
            print('copying in ' + output_data_path + '...')
            ########################################        
            output_path = my_dir + '/' + experiment + '/' + frequency + '/' + \
                    medium + '/' +  var  + '/' +  version
            output_name = model + '_' + initial_cond + '_' + \
            start_chunk[-16:-10] + '-' + start_chunk[-9:-3] + '.nc'
            output_data_path = output_path + '/' +  output_name
            input_data_path = input_path + '/' + start_chunk
            ########################################
            if output_name in pls_out:
                print("it's already there! \n")
                break
            else:
                os.system('cp ' + input_data_path + ' ' + output_data_path)
                print('Done. \n')
                break
                
                
        ########################################        
        output_path = my_dir + '/' + experiment + '/' + frequency + '/' + \
                medium + '/' +  var  + '/' +  version
        output_name = model + '_' + initial_cond + '_' + \
        start_chunk[-16:-10] + '-' + finish_chunk[-9:-3] + '.nc'
        output_data_path = output_path + '/' +  output_name
        ########################################

        print(model + " concatenating into " + output_data_path + "...")
        ########################################
        input_data_path = ''
        for n in idxes:
            input_data_path += input_path + '/' + pls[n] + ' '
        ########################################

        pls_out = os.listdir(output_path)
        if output_name in pls_out:
            print("it's already there! \n")
            break
        else:
            os.system('ncrcat ' + input_data_path + ' ' + output_data_path)
            print('Done. \n')
            break

    continue
            
            
            
            
            
            
            

