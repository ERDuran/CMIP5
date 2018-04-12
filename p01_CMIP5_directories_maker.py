import os
import pickle

CMIP5_dir = '/g/data1/ua6/DRSv2/CMIP5'

erd561_dir = '/g/data/e14/erd561/CMIP5'

output_dir = raw_input('output directory? e.g. anthurium, bromeliad: ')

my_dir = erd561_dir + '/' + output_dir

# models_list = sorted(os.listdir(CMIP5_dir))

# if var in ['tos', 'tauuo']:
#     models_list = sorted(os.listdir(CMIP5_dir))
# elif var in ['uas', 'vas']:
#     with open('p05_index_and_pools.pkl', 'rb') as f:
#         lat_warmN, lat_warmS, lon_warmW, lon_warmE, \
#         SAM_index_sorted_cleaned, warm_pool_sorted_cleaned, wind_pool_sorted_cleaned = \
#         pickle.load(f)
#         models_list = sorted(SAM_index_sorted_cleaned)

# print(models_list)

experiment = raw_input('experiment? e.g. rcp85, historical: ')

frequency = 'mon'

medium = raw_input('medium? e.g. ocean, atmos: ')

initial_cond = 'r1i1p1'

var = raw_input('var? e.g. thetao, tauuo, uas, vas: ')

version = 'latest'

my_path = my_dir + '/' + experiment + '/' + frequency + '/' + medium + '/' +  var  + '/' +  version

print("Creating " + my_path + " ...")
if not os.path.exists(my_path):
    os.makedirs(my_path)
    print("Done. \n")
    
else:
    print("it's already there! \n")
