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
'''

import os

CMIP5_dir = '/g/data1/ua6/DRSv2/CMIP5'

my_dir = '/g/data/e14/erd561/CMIP5/process-land'

models_list = sorted(os.listdir(CMIP5_dir))

experiment = 'rcp85'

frequency = 'mon'

medium = 'ocean'

initial_cond = 'r1i1p1'

var = 'tos'

version = 'latest'

start_time = 200601

finish_time = 210012

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
        pls = os.listdir(input_path)
    else:
        print(model + " doesn't have a " + medium + " medium...")
        print('rejected. \n')
        continue

    if initial_cond in pls:
        input_path = CMIP5_dir + '/' + model + '/' + experiment + '/' + frequency + '/' + \
            medium + '/' + initial_cond
        pls = os.listdir(input_path)
    else:
        print(model + " doesn't have " + initial_cond + " initial conditions...")
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
    
    
    # The CMIP5 Historical runs should start on January 1850
    if str(start_time) in pls[0]:
        pass
    else:
        print(model + " starts in " + pls[0][-16:-10] + " and not in " + str(start_time) + "...")
        
        if int(pls[0][-16:-10]) <= start_time:
            print("start time is on or before " + str(start_time) + "...")
            print('rejected. \n')
            continue
        else:
            print('rejected. \n')
            continue        
    # And finish in December 2005
    if str(finish_time) in pls[-1]:
        pass
    else:
        print(model + " finishes in " + pls[-1][-9:-3] + " and not in " + str(finish_time) + "...")
        
        if int(pls[0][-9:-3]) > finish_time:
            print("finish time is after " + str(finish_time) + "...")
            print('rejected. \n')
            continue
        else:
            print('rejected. \n')
            continue
    
    
    
    ########################################        
    output_path = my_dir + '/' + experiment + '/' + frequency + '/' + \
            medium + '/' + initial_cond  + '/' +  var  + '/' +  version
    output_name = model + '_' + pls[0][-16:-10] + '-' + pls[-1][-9:-3] + '.nc'
    output_data_path = output_path + '/' +  output_name
    ########################################
    
    # Because surface properties are 2D, the data should be in one file
    if len(pls) == 1:
        print(model + " is all good :) ...")
        print("copying into " + my_dir + "...")
        ########################################
        input_data_path = input_path + '/' +  pls[0]
        ########################################
        
        pls_out = os.listdir(output_path)
        if output_name in pls_out:
            print("it's already there!")
        else:
            os.system('cp ' + input_data_path + ' ' + output_data_path)
            print('Done. \n')
    
    else:
        print(model + " has " + str(len(pls)) + " chunks of data and not one...")
        print("concatenating into " + my_dir + "...")
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
            
            
            
            
            
            
            
            
            

