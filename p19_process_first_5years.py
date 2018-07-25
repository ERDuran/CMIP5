import os
import pickle
import numpy as np

input_path = '/short/e14/erd561/mom/archive/gfdl_nyf_1080_hist_8099/'
output_path = '/g/data/e14/erd561/R8exp/gfdl_nyf_1080_hist_8099/first_5years/'

if not os.path.exists(output_path):
    print("Creating " + output_path + " ...")
    os.makedirs(output_path)
    print("Done. \n")

file_names = ['ice_month', 'ocean_month', 'ocean_month', 'ocean_month', 'ocean_month', 'ocean_month', 'ocean_month']
var_names = ['SST', 'net_sfc_heating', 'tau_x', 'tau_y', 'tau_curl', 'ekman_we', 'ekman_heat']
data_names = ['SST', 'nsh', 'tau_x', 'tau_y', 'tau_curl', 'ekman_we', 'ekman_heat']

# tau_curl: Ekman vertical velocity averaged to wt-point in m/s
# ekman_we: Ekman Component to heat transport in Watts

pls_out = os.listdir(output_path)
for f,v,d in zip(file_names, var_names, data_names):
    data_name = f + '_' + d
    output_data_path_all = ''
    for yr in range(502, 506):
        data_name_yr = data_name + '_'+ str(yr)
        input_data_path = input_path + 'output' + str(yr) + '/' + f + '.nc'
        output_data_path = output_path + data_name_yr + '.nc'
        if data_name_yr + '.nc' not in pls_out:
            print('Creating ' + data_name_yr)
            os.system('ncra -v ' + v + ' ' + input_data_path + ' ' + output_data_path)
            print('Done. \n')
        output_data_path_all += output_data_path + ' '
    if data_name + '.nc' not in pls_out:
        os.system('ncrcat ' + output_data_path_all + ' ' + output_path + data_name + '.nc')
print("All done! \n")        
