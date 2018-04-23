import os
import pickle

CMIP5_dir = '/g/data1/ua6/DRSv2/CMIP5'

erd561_dir = '/g/data/e14/erd561/CMIP5'

output_dir = raw_input('output directory? e.g. anthurium, bromeliad: ')

my_dir = erd561_dir + '/' + output_dir

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
