# -*- coding: utf-8 -*-
'''
@author: Himaghna
date: 18th April 2018
description: run with a foldername to get thermochemistry of all log files in the folder
call syntax python3 ./get_thermo_gaussian.py <input folder name> -t <temperature Default 120'C> -p <pressure. Default 1 atmosphere>
'''

import glob
from Gaussian_tools import Thermochemistry
import constants as c
import datetime
import argparse
import xlsxwriter
import os

def build_argument(is_gas, pressure = None):
    if is_gas:
        if not pressure:
            # no pressure defined for gas
            print('Enter pressure')
            return 'NaN'
        argument = {
            'apply_qrrho': True,
            'rotation': True,
            'translation': 3,
            'translation_parameter': pressure
        }
        mass_mobile_species = 'get'
    else:
        # if not gas consider only vibrational
        argument = {
            'apply_qrrho': True,
            'rotation': False,
            'translation': 0,
            'translation_parameter': ''
        }
        mass_mobile_species = []
    return argument, mass_mobile_species


def write_to_excel(out_file  = '', data = ()):
    workbook = xlsxwriter.Workbook(filename=out_file)
    worksheet = workbook.add_worksheet()
    for index,row in enumerate(data):
        worksheet.write_row(index, 0, tuple(row))

def __main__(path, temperature, pressure = 101325):

    if os.path.isdir(path):
        #folder supplied as argument
        time_stamp = datetime.datetime.now()
        output_folder_kcal = path + '/thermochemistry_in_kcal'
        output_folder_SI = path + '/thermochemistry_in_SI'
        if not os.path.isdir(output_folder_kcal):
            os.system("mkdir " + output_folder_kcal)
        if not os.path.isdir(output_folder_SI):
            os.system("mkdir " + output_folder_SI)
        out_file_SI = output_folder_SI + '/thermochemistry_all_species_SI-units_' + str(time_stamp.date()) + '.xlsx'
        out_file_kcal = output_folder_kcal + '/' + 'thermo_' + str(temperature) + '_' + str(time_stamp.date()) + '.xlsx'
        out_list_SI =[['Species', 'Gibbs (J/mol)', 'Enthalpy(J/mol)', 'Entropy(J/mol/K)', 'Electronic(J/mol)', 'ZPE(J/mol)']]
        out_list_kcal = [['Species', 'Gibbs (kcal/mol)', 'Enthalpy(kcal/mol)', 'Entropy(kcal/mol/K)', 'Electronic(kcal/mol)', 'ZPE(kcal/mol)']]
        for file in glob.glob(os.path.join(path, '*.log')):
            print(file)
            #check if logfile represents a species adsorbed on surface
            if file.split('/')[-1].split('-')[0] == 'surf':
                is_gas = False
                print('Treating species as adsorbed with only vibrational degrees of freedom...')
            else:
                is_gas = True
                print('Treating species as ideal gas...')

            #build argument for calling get_entropy_and_thermal_corrections method and also define mass_mobile_species
            argument, mass_mobile_species= build_argument(is_gas = is_gas, pressure= pressure)

            #instantiate Thermochemistry class
            thermo_object = Thermochemistry(log_file=file, temperature=temperature, mass_mobile_species=mass_mobile_species)
            entropy, energy_corrections = thermo_object.get_entropy_and_thermal_corrections(**argument)
            energies = thermo_object.get_energies(entropy, energy_corrections)

            #tabulate outputs
            G_SI = energies['gibbs_free_energy']
            G_kcal = G_SI * c.JOULES_TO_KCAL

            H_SI = energies['enthalpy']
            H_kcal = H_SI * c.JOULES_TO_KCAL

            S_SI = sum([entropy[key] for key in entropy])
            S_kcal = S_SI * c.JOULES_TO_KCAL

            Electronic_SI = energies['electronic_energy']
            Electronic_kcal = Electronic_SI * c.JOULES_TO_KCAL

            ZPE_SI = thermo_object.get_zero_point_energy()
            ZPE_kcal = ZPE_SI * c.JOULES_TO_KCAL

            out_list_SI.append([file.split('.')[0].split('/')[-1], G_SI, H_SI, S_SI, Electronic_SI, ZPE_SI])
            out_list_kcal.append([file.split('.')[0].split('/')[-1], G_kcal, H_kcal, S_kcal, Electronic_kcal, ZPE_kcal])
        out_list_SI.append(['Temperature:', temperature])
        out_list_SI.append(['Pressure:', pressure])
        out_list_kcal.append(['Temperature:', temperature])
        out_list_kcal.append(['Pressure:', pressure])


        write_to_excel(out_file=out_file_SI, data=out_list_SI)
        write_to_excel(out_file=out_file_kcal, data=out_list_kcal)



parser = argparse.ArgumentParser(description = 'Enter')

parser.add_argument('path', type=str, default=None,
                    help='Name of folder with log files from Gaussian')
parser.add_argument('-t', '--temperature', type =float, default = 120.0,
                    help = 'Temperature is degree Celsius for applying thermal corrections')
parser.add_argument('-p', '--pressure',type = float, default = 1.0,
                    help = 'Pressure in atmospheres')
command_args = parser.parse_args()
path = command_args.path
temperature = command_args.temperature + 273.15 #convert to Kelvin
pressure = command_args.pressure *c.ATM_TO_PASCAL #convert to Pascal
__main__(path = path, temperature= temperature, pressure=pressure)















