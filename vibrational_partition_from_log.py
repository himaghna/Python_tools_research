


'''@Author: Himaghna
   Date: March 17th 2018
   Description: this file takes in a Gaussian log file and calculates vibrational partition function
   Call type: vibrational_partition_from_log.py "logfilename".log "outputfilename (optional)" '''

import Gaussian_tools as gt
import constants
import sys
import math

T_Kelvin = 393.15
frequencies = gt.get_frequencies_inv_cm(sys.argv[1])
denominator = 1.0
for wavenumber_inverse_centimeter in frequencies:
    #Gaussian gives frequencies as wavenumbers in inverse centimeters. We have to convert to Hz
    frequency = wavenumber_inverse_centimeter * constants.SPEED_OF_LIGHT_CENTIMETER_PER_SECOND
    exponent = -(constants.PLANK_CONSTANT_JOULE_SECOND * frequency) / (constants.kBOLTZMANN_JOULE_PER_KELVIN * T_Kelvin)
    denominator = denominator * (1-math.exp(exponent))

q_vibration = 1/denominator
print('Vibrational Partition Function is {}'.format(q_vibration))





