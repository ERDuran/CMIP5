'''
CMIP5 get SST using ncks.
plev = 0
'''

import os

def listdir_nohidden(path):
    f_list = [f for f in os.listdir(path) if not f.startswith('.')]
    return f_list
            
data_dir = '/g/data/e14/erd561/CMIP5/bromeliad'

my_dir = '/g/data/e14/erd561/CMIP5/camelia'

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
var = raw_input('var? e.g. thetao: ')

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
    
    output_name = model_now[:-3] + '_10.nc'
    
    my_data_path = my_path + '/' +  output_name
    
    if output_name in my_ls:
        print(model + " is already there!")
        os.system('ncks -P -m -v plev ' + my_data_path)
        
    else:
        plev = 1
        print(model + " subset at plev = " + str(plev) +  "...")
        os.system('ncks -d plev,' + str(plev) + ' ' + 
                  input_data_path + ' ' + my_data_path)
        os.system('ncks -P -m -v plev ' + my_data_path)









