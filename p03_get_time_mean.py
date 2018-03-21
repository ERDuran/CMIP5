'''
CMIP5 hist runs from 1850 to 2005 included hence:
total time = (2006 - 1850) * 12 = 56 * 12 = 1872.
A 1980 to 2000 average is therefore:
start time = (1980 - 1850) * 12 = 130 * 12 = 1560
finish time = (2000 - 1850) * 12 - 1 = 150 * 12 -1 = 1799

WARNING: for the time dimension in ncra, python numbering standards are using
ie. start from 0

HIST:
experiment = 'historical'
year_min_exp = 1850
year_start = 1980
year_finish = 2000

RCP:
experiment = 'rcp85'
year_min_exp = 2006
year_start = 2080
year_finish = 2100
'''

import os

def listdir_nohidden(path):
    f_list = [f for f in os.listdir(path) if not f.startswith('.')]
    return f_list
            
data_dir = '/g/data/e14/erd561/CMIP5/process-land'

my_dir = '/g/data/e14/erd561/CMIP5/bromeliad'

experiment = 'historical'
year_min_exp = 1850
year_start = 1980
year_finish = 2000

frequency = 'mon'

medium = 'ocean'

initial_cond = 'r1i1p1'

var = 'tos'

version = 'latest'

start_time = (year_start - year_min_exp) * 12

finish_time = (year_finish - year_min_exp) * 12 - 1

data_path = data_dir + '/' + experiment + '/' + frequency + '/' + \
medium + '/' + initial_cond  + '/' +  var + '/' +  version

my_path = my_dir + '/' + experiment + '/' + frequency + '/' + \
medium + '/' + initial_cond  + '/' +  var + '/' +  version

data_ls = sorted(listdir_nohidden(data_path))

my_ls = listdir_nohidden(my_path)

for model in data_ls:
    input_data_path = data_path + '/' +  model
    
    output_name = model[:-17] + '_' + str(year_start) + '-' + str(year_finish) + 'mean.nc'
    
    my_data_path = my_path + '/' +  output_name
    
    print(model[:-17] + " averaged over " + str(year_start) + '-' + str(year_finish) +  "...")
    if output_name in my_ls:
        print("it's already there! \n")
        
    else:
        os.system('ncra -d time,' + str(start_time) + ',' + str(finish_time) + ' ' + 
                  input_data_path + ' ' + my_data_path)
        print("Done. \n")
    
    
    
    
    
    
    