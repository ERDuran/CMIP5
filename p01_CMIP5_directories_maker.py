import os

CMIP5_dir = '/g/data1/ua6/DRSv2/CMIP5'

my_dir = '/g/data/e14/erd561/CMIP5/process-land'

models_list = sorted(os.listdir(CMIP5_dir))

experiment = 'historical'

frequency = 'mon'

medium = 'ocean'

initial_cond = 'r1i1p1'

var = 'tos'

version = 'latest'

if not os.path.exists(my_dir + '/' + experiment + '/' + frequency + '/' + 
                      medium + '/' + initial_cond  + '/' +  var  + '/' +  version):
    os.makedirs(my_dir + '/' + '/' + experiment + '/' + frequency + '/' + 
                medium + '/' + initial_cond  + '/' +  var  + '/' +  version)