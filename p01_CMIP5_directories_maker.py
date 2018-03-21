import os

CMIP5_dir = '/g/data1/ua6/DRSv2/CMIP5'

erd561_dir = '/g/data/e14/erd561/CMIP5'

output_dir = '/bromeliad'

my_dir = erd561_dir + output_dir

models_list = sorted(os.listdir(CMIP5_dir))

experiment = 'historical'

frequency = 'mon'

medium = 'ocean'

initial_cond = 'r1i1p1'

var = 'tos'

version = 'latest'

my_path = my_dir + '/' + experiment + '/' + frequency + '/' + \
medium + '/' + initial_cond  + '/' +  var  + '/' +  version

print("Creating " + my_path + " ...")
if not os.path.exists(my_path):
    os.makedirs(my_path)
    print("Done. \n")
    
else:
    print("it's already there! \n")
