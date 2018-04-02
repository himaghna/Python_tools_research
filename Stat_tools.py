
'''@Author: Himaghna
   Date: March 18th 2018
   Description: collection of statistical tools '''

import numpy as np
import xlsxwriter
import os
import sys

#takes in a text file containing many columns and converts into XL file with the format of each cell as cell_format int/str/float (default is float)
def create_xl(input_filename, output_filename, cell_format = 'float'):
    try:
        input_fp = open(input_filename, 'r')
    except:
        print('Error opening input file. Exiting')
        sys.exit(-1)

    try:
        workbook = xlsxwriter.Workbook(output_filename)
        worksheet = workbook.add_worksheet()

    except:
        print('Error with opening output file. Exiting')
        exit()
    #index of row being written
    row_number = 0
    for line in input_fp:
        row = []
        for word in line.split(' '):

            if(cell_format == 'str'):
                row.append(str(word))
            elif(cell_format == 'int'):
                row.append(int(word))
            else:
                row.append(float(word))

        #writing to file
        worksheet.write_row(row = row_number, col = 0, data = row)
        #update row_number to start writing from next row
        row_number = row_number + 1
    workbook.close()
    input_fp.close()


create_xl('/Users/Ne0/Documents/Prof/Acads/1-2/Math/HW/HW3_Stats/14_37.txt', '/Users/Ne0/Documents/Prof/Acads/1-2/Math/HW/HW3_Stats/14_37.xlsx')


