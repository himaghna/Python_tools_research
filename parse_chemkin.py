import plotly
import xlsxwriter as xw
import os
import argparse

def parse_gasmass(chemkin_folder, out_folder):
    gas_mass_file = chemkin_folder + '/tube_gasmass_ss.out'
    if not os.path.isfile(gas_mass_file):
        print('Error. tube_gasmass_ss.out not found. Exiting')
        os._exit(-1)
    if not out_folder == None:
        out_file = out_folder +'/tube_gassmass_parsed.xlsx'
    else:
        out_file = chemkin_folder + '/tube_gassmass_parsed.xlsx'
    with open(gas_mass_file, "r") as fp:
        count = 1
        print('Opening file {}'.format(gas_mass_file))
        try:
            workbook = xw.Workbook(out_file)
        except:
            print("Error creating output file. Exiting")
            os._exit(-1)
        column_num = 0
        for line in fp:
            row_to_be_written = []
            if "Experimental condition" in line:
                worksheet = workbook.add_worksheet(name='Run {}'.format(count))
                count +=1
                row_num = 0
            for word in line.split():
                row_to_be_written.append(word)
            if 'Vol' in line:
                row_temp = row_to_be_written
                row_to_be_written = []
                row_to_be_written.append(row_temp[0] + row_temp[1])
                for entry in row_temp[2:-4]:
                    row_to_be_written.append(entry)
                row_to_be_written.append(("Temperature in K"))
                row_to_be_written.append("Pressure in atm")
            worksheet.write_row(row=row_num, col= column_num, data=row_to_be_written)
            row_num +=1
    workbook.close()

def parse_tubecov(chemkin_folder, out_folder):
    tube_cov_file = chemkin_folder + '/tube_cov_ss.out'
    if not os.path.isfile(tube_cov_file):
        print('Error. tube_cove_ss.out not found. Exiting')
        os._exit(-1)
    if not out_folder == None:
        out_file = out_folder + '/tube_cov_ss_parsed.xlsx'
    else:
        out_file = chemkin_folder + '/tube_cov_ss_parsed.xlsx'
    with open(tube_cov_file, "r") as fp:
        count = 1
        print('Opening file {}'.format(tube_cov_file))
        try:
            workbook = xw.Workbook(out_file)
        except:
            print("Error creating output file. Exiting")
            os._exit(-1)
        column_num = 0
        for line in fp:
            row_to_be_written = []
            if "Experimental condition" in line:
                worksheet = workbook.add_worksheet(name='Run {}'.format(count))
                count += 1
                row_num = 0
            for word in line.split():
                row_to_be_written.append(word)
            if 'Vol' in line:
                row_temp = row_to_be_written
                row_to_be_written = []
                row_to_be_written.append(row_temp[0] + row_temp[1])
                for entry in row_temp[2:-2]:
                    row_to_be_written.append(entry)
                row_to_be_written.append(("Temperature in K"))
            worksheet.write_row(row=row_num, col=column_num, data=row_to_be_written)
            row_num += 1
    workbook.close()




def __main__():
    parser = argparse.ArgumentParser(description='Enter path')
    parser.add_argument('chemkin_folder', type = str, default=None, help= 'Enter folder containing tube_gasmass_ss.out without trailing /' )
    parser.add_argument('-o', '--out_folder', type= str, default = None, help= 'Enter name of folder where you would want your output file to be stored without trailing /')
    command_args = parser.parse_args()
    chemkin_folder = command_args.chemkin_folder
    out_folder = command_args.out_folder
    if out_folder:
        #check done only when the rgument is supplies
        if not os.path.isdir(out_folder):
            print("Error, {} does not exist".format(out_folder))
            exit(-1)
    parse_gasmass(chemkin_folder=chemkin_folder, out_folder=out_folder)
    parse_tubecov(chemkin_folder=chemkin_folder, out_folder=out_folder)


if __name__ == "__main__":
    __main__()

#parse_gasmass('/Users/Ne0/Documents/Prof/Research/MkM/Chemkin/Full_model_IPA_dehydration_Q1/q1_IPA_dehydration_out', None)







