'''
CMIP5 hist runs from 1850 to 2005 included hence:
total time = (2006 - 1850) * 12 = 56 * 12 = 1872
A 1980 to 2000 average is therefore:
start time = (1981 - 1850) * 12 = 131 * 12 = 1572
finish time = (2001 - 1850) * 12 - 1 = 151 * 12 - 1 = 1811

WARNING: for the time dimension in ncra, python numbering standards are using
ie. start from 0

HIST:
experiment = 'historical'
year_start = 1981
year_finish = 2001

RCP:
experiment = 'rcp85'
year_start = 2081
year_finish = 2101
'''

import os

def listdir_nohidden(path):
    f_list = [f for f in os.listdir(path) if not f.startswith('.')]
    return f_list
            
data_dir = '/g/data/e14/erd561/CMIP5/anthurium'

my_dir = '/g/data/e14/erd561/CMIP5/bromeliad'

# rcp85 or historical
experiment = raw_input('experiment? e.g. rcp85, historical: ')

if experiment == 'rcp85':
    year_start = 2080
    year_finish = 2100
elif experiment == 'historical':
    year_start = 1980
    year_finish = 2000

frequency = 'mon'

medium = raw_input('medium? e.g. ocean, atmos: ')

# tos or tauuo
var = raw_input('var? e.g. thetao, tauu: ')

version = 'latest'

data_path = data_dir + '/' + experiment + '/' + frequency + '/' + \
medium + '/' +  var + '/' +  version

my_path = my_dir + '/' + experiment + '/' + frequency + '/' + \
medium + '/' +  var + '/' +  version

data_ls = sorted(listdir_nohidden(data_path))

my_ls = listdir_nohidden(my_path)

for model_now in data_ls:
    model = model_now[:-24]
    input_data_path = data_path + '/' +  model_now
    
    first_year = model_now[-16:-10]
    if first_year[4:6] != '01':
        print(first_year[4:6])
        print(model[:-24] + " doesn't start in January! Rejected. \n")
        continue
    start_time = (year_start - int(first_year[0:4])) * 12
    finish_time = (year_finish - int(first_year[0:4])) * 12 - 1
    
    print(model + ' first year: ' + first_year)
    print(model + ' start time: ' + str(start_time))
    print(model + ' finish time: ' + str(finish_time))
    months_n = finish_time - start_time
    assert(months_n == 239)
    print(model + ' number of months: ' + str(months_n) + 
          '. Must be 239!')
    #print(model + ' first year: ' + first_year)
    
    output_name = model + '_' + model_now[-23:-17] + '_' + str(year_start) + '-' + str(year_finish-1) + 'mean.nc'
    
    my_data_path = my_path + '/' +  output_name
    
    print(model + " averaged over " + str(year_start) + '-' + str(year_finish-1) +  "...")
    if output_name in my_ls:
        print("it's already there! \n")
        
    else:
        os.system('ncra -d time,' + str(start_time) + ',' + str(finish_time) + ' ' + 
                  input_data_path + ' ' + my_data_path)
        print("Done. \n")
    
    
    
    
    
    
    