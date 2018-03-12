import xlsxwriter
import os
import sys
import glob
import constants

'''Author: Himaghna Date: 3/2018
 This script takes in a folder 'folder_name' and searches for all instances of zero point and e
electronic energy and writes to a single output file with format Original Filename: ZPE Electronic ZPE+Electronic'''

folder_name = input('\nEnter folder name: ')

if not os.path.isdir(folder_name):
    print('\nNot valid path name. Exiting')
    sys.exit(-1)

out_file = input('\nEnter output file name: ')

workbook = xlsxwriter.Workbook(out_file)
worksheet = workbook.add_worksheet()

# data[[]] will be written to excel
data = [['Name of species', 'ZPE(eV)', 'Electronic Energy(eV)', 'Sum of electronic and ZPE']]
for filename in glob.glob(os.path.join(folder_name, '*.log')):

    with open(filename) as fp:

        for line in fp:
            if 'Zero-point vibrational energy' in line:
                #ZPE in J/mol
                zpe_joules_per_mole = float(line.split()[-2])
                #storing units for verification
                units = line.split()[-1]

            if 'Sum of electronic and zero-point Energies' in line:
                # sum of electronic and zpe in Hartrees
                electronic_plus_zpe_hartrees = float(line.split()[-1])


        #converting to eV
        try:
            electronic_plus_zpe_eV = electronic_plus_zpe_hartrees * constants.HARTREES_TO_eV
            zpe_eV = zpe_joules_per_mole * constants.JOULES_PER_MOLE_TO_eV
            electronic_eV = electronic_plus_zpe_eV - zpe_eV
        except:
            electronic_plus_zpe_eV = 'Nan'
            zpe_eV = 'Nan'
            electronic_eV = 'Nan'

        #add the row entry to data
        data.append([(filename.split('.')[0].split('/')[-1]), zpe_eV, electronic_eV, electronic_plus_zpe_eV])

row = 0
col = 0
# Iterate over the data and write it out row by row.
for species, zpe, electronic, sum in data:
    worksheet.write(row, col, species)
    worksheet.write(row, col + 1, zpe)
    worksheet.write(row, col + 2, electronic)
    worksheet.write(row, col + 3, sum)
    row += 1

workbook.close()






