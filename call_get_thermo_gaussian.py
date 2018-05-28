import os


path = "'/Users/Ne0/Documents/Prof/Research/MkM/gaussian_log_files/ZSM5_all_files_Gaussian/log_files'"
pressure = '1'  #atm
cmd_skeleton = 'python3 ./get_thermo_gaussian.py ' + path + ' -p ' + pressure + ' -t '
for temperature in range(120, 500, 20):
    command = cmd_skeleton + str(temperature)
    os.system(command)


