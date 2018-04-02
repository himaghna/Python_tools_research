
import xlsxwriter

''' Author: Himaghna Bhattacharjee
    Date: March 2018
    Description: This code take in an input Gaussian log file and exports an Excel file with all vibrational frequencies listed as a single column '''

column = 1
filename = input("\nEnter filename: ")

output_filename = filename.split('.')[0]+'frequencies.xlsx'
try:
    workbook = xlsxwriter.Workbook(output_filename)
    worksheet = workbook.add_worksheet()

except:
    print('Error with opening output file. Exiting')
    exit()
frequencies = []
try:
    with open(filename) as fp:
        for line in fp:
            if "Frequencies" in line.strip("\n"):
                for cell in line.split():
                    if not cell == "Frequencies" and not cell == '--':
                        frequencies.append(float(cell))
except:
    print("no Filename passed")
    exit()
worksheet.write_row('A1', frequencies)


