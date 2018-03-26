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

data_dir = '/g/data/e14/erd561/CMIP5/bromeliad'

my_dir = '/g/data/e14/erd561/CMIP5/bromeliad'

# rcp85 or historical
experiment = raw_input('experiment? e.g. rcp85, historical: ')

frequency = 'mon'

medium = 'ocean'

initial_cond = 'r1i1p1'

# tos or tauuo
var = raw_input('var? e.g. tos, tauuo: ')

version = 'latest'

data_path = data_dir + '/' + experiment + '/' + frequency + '/' + \
medium + '/' + initial_cond  + '/' +  var + '/' +  version

my_path = my_dir + '/' + experiment + '/' + frequency + '/' + \
medium + '/' + initial_cond  + '/' +  var + '/' +  version

data_ls = sorted(listdir_nohidden(data_path))

my_ls = sorted(listdir_nohidden(my_path))

thefile = open('p04_models_list.txt', 'r')
lines = thefile.readlines()
#print(lines)
#print(lines[0][:-1])






















