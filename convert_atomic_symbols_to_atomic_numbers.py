'''Author" Himaghna Bh. 2/15/2018'''
'''This file is used to convert a column of a file ('filename') containing atomic symbols to corresponding atomic numbers'''

#input filename
filename = input('enter filename with complete path and extension: \n')
column = input('enter column you want processed. default is 1st column: \n') or 1
delem = input('enter delimiter in file. Default is space: \n') or ' '
column =- 1                       #converting column number to index

#generate a dictionary with key ==> atomic number and value ==> atomic number
atomic_dictionary = dict()


try:
    with open('/Users/Ne0/Documents/Prof/Research/Files/periodic_table.txt', 'r') as ptable:
        for line in ptable:
            key = (line.strip()).split(',')[1]
            value = line.strip().split(',')[0]
            atomic_dictionary[key] = value
except:
    print("File doesn't exist")


#load source file
try:
    source = open(filename,'r')

except:
    print("No such file")

#output file
try:
    outfile = open(filename.split('.')[0]+'_out.'+filename.split('.')[1], 'w')
except:
    print('ERROR: Could not create output file')




for line in source:
    for word in line.split():
        try:
            outfile.write(atomic_dictionary[word])     #If it is a symbol of an element
        except:
            #if not an atomic symbol
            outfile.write(word)
        outfile.write(delem)
    outfile.write('\n')


source.close()
outfile.close()



