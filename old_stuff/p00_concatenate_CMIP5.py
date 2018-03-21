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

my_dir = '/g/data/e14/erd561/CMIP5'

#os.chdir(CMIP5_dir)
#models_list = str(os.system('ls'))
models_list = sorted(os.listdir(CMIP5_dir))

#print(models_list)

experiment = 'historical'

frequency = 'mon'

medium = 'ocean'

initial_cond = 'r1i1p1'

SST = 'tos'

#tau = 'tos'

version = 'latest'

for model in models_list:
	pls = os.listdir(CMIP5_dir + '/' + model)
	if experiment in pls:
		pls = os.listdir(CMIP5_dir + '/' + model + '/' + experiment)
	else:
		print model + " doesn't have a " + experiment + " experiment"
		continue

	if frequency in pls:
		pls = os.listdir(CMIP5_dir + '/' + model + '/' + experiment + '/' + frequency)
	else:
		print model + " doesn't have a " + frequency + " frequency"
		continue

	if medium in pls:
		pls = os.listdir(CMIP5_dir + '/' + model + '/' + experiment + '/' + frequency + '/' + 
			medium)
	else:
		print model + " doesn't have a " + medium + " medium"
		continue

	if initial_cond in pls:
		pls = os.listdir(CMIP5_dir + '/' + model + '/' + experiment + '/' + frequency + '/' + 
			medium + '/' + initial_cond)
	else:
		print model + " doesn't have " + initial_cond + " initial conditions"
		continue

	if SST in pls:
		pls = os.listdir(CMIP5_dir + '/' + model + '/' + experiment + '/' + frequency + '/' + 
			medium + '/' + initial_cond  + '/' +  SST)
	else:
		print model + " doesn't have the " + SST + " variable"
		continue

	if version in pls:
		pls = sorted(os.listdir(CMIP5_dir + '/' + model + '/' + experiment + '/' + frequency + '/' + 
			medium + '/' + initial_cond  + '/' +  SST  + '/' +  version))
	else:
		print model + " doesn't have a " + version + " version"
		continue

	# Because SST is 2D, the data should be in one file
	if len(pls) == 1:
		pass
	else:
		print model + " has " + str(len(pls)) + " chunks of data and not one"
		print "concatenating into " + my_dir + "..."

		if os.path.isdir(my_dir + '/' + model + '/' + experiment + '/' + frequency + '/' + 
			medium + '/' + initial_cond  + '/' +  SST  + '/' +  version):
			pass
		else:
			



		continue

	# The CMIP5 Historical runs should start on January 1850 and finish in December 2005
	if '185001' in pls[0]:
		pass
	else:
		print model + " starts in " + pls[0][-16:-10] + " and not in January 1850"
		continue

	# And finish in December 2005
	if '200512' in pls[0]:
		pass
	else:
		print model + " finishes in " + pls[0][-9:-3] + " and not in December 2005"
		continue


	print model + " is all good :)"

	

	#print pls






