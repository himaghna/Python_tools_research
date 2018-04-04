'''@Author: Himaghna
   Date: March 17th 2018
   Description: file encapsulates the gaussian log file and defines operations for extracting information from it
   References: [1] S. Grimme, “Supramolecular binding thermodynamics by dispersion-corrected density functional theory,” Chem. - A Eur. J., vol. 18, no. 32, pp. 9955–9964, 2012.
               [2] Y. P. Li, J. Gomes, S. M. Sharada, A. T. Bell, and M. Head-Gordon, “Improved force-field parameters for QM/MM simulations of the energies of adsorption for molecules in zeolites and a free rotor correction to the rigid rotor harmonic oscillator model for adsorption enthalpies,” J. Phys. Chem. C, vol. 119, no. 4, pp. 1840–1850, 2015.'''
import sys
import os
import constants as c
import re
import math


class Thermochemistry:
    def __init__(self, log_file, temperature, mass_mobile_species = []):
        if mass_mobile_species == 'get':
            #if 'get' passed, get mass of species in amu units from log file. Usually for gas species
            mass_mobile_species = list(self.get_amu())
        self.number_of_mobile_species = len(mass_mobile_species)
        self.temperature = temperature
        if not os.path.isfile(log_file):
            print("Invalid log file. Exiting")
            exit(-1)
        else:
            self.log_file = log_file
            #convert adsorbate masses to kg (from AMU) and store as attribute
            self.mass_mobile_species = [c.AMU_TO_KG * atomic_mass for atomic_mass in mass_mobile_species]

    #get AMU from logfile
    def get_amu(self):
        amu = -1  # default initialization
        try:

            with open(self.log_file) as fp:
                for line in fp:
                    if re.search('Molecular mass:(.*)',line):
                        amu = (re.search('Molecular mass:(.*)',line) .groups()[0]).split()
                        amu = float(amu[0])
        except:
            print("Error opening log file.")
            exit(-1)
        return amu


    # returns the vibrational frequencies as an output list
    def get_frequencies_inv_cm(self):
        frequencies = []
        try:
            with open(self.log_file) as fp:
                for line in fp:
                    if "Frequencies" in line.strip("\n"):
                        for word in line.split():
                            if not word == "Frequencies" and not word == '--':
                                frequencies.append(float(word))
            return frequencies
        except:
            print("Error opening log file.")
            exit(-1)

    def get_rotational_temperatures(self):
        try:
            rotational_temperatures = ''
            with open(self.log_file) as fp:
                for line in fp:
                    if re.search('Rotational temperatures \(Kelvin\)(.*)', line):
                        rotational_temperatures = (
                        re.search('Rotational temperatures \(Kelvin\)(.*)', line).groups()[0]).split()
                        rotational_temperatures = [float(rotational_temperature) for rotational_temperature in
                                                       rotational_temperatures]
            return rotational_temperatures
        except:
            print("Error opening log file.")
            exit(-1)

    def get_symmetry_number(self):
        try:
            symmetry_number = ''
            with open(self.log_file) as fp:
                for line in fp:
                    if re.search('Rotational symmetry number(.*)', line):
                        symmetry_number = (re.search('Rotational symmetry number(.*)', line).groups()[0]).split()
                        symmetry_number = float(symmetry_number[0])
            return symmetry_number
        except:
            print("Error opening log file.")
            exit(-1)

    def get_vibrational_temperatures(self):
        return [vibrational_frequency_inv_cm * c.SPEED_OF_LIGHT_CENTIMETER_PER_SECOND * c.PLANK_CONSTANT_JOULE_SECOND/ c.kBOLTZMANN_JOULE_PER_KELVIN
                                             for vibrational_frequency_inv_cm in self.get_frequencies_inv_cm()]

    #get molecular partition function for translation considering 1 degree of freedom with L being length of the free dimension of translation
    def get_translational_q_1D(self, L = 0):
        translational_q_1D = 1
        #if translational degree of freedom (L not =0) or there is at least one mobile species ( or adsorbates)
        if not L == 0 and not self.number_of_mobile_species == 0:
            for mass_single_species in self.mass_mobile_species:
                translational_q_1D *= math.sqrt(2 * math.pi *mass_single_species * c.kBOLTZMANN_JOULE_PER_KELVIN *
                                                self.temperature /(c.PLANK_CONSTANT_JOULE_SECOND**2)) * L
        return translational_q_1D

    # get molecular partition function for translation considering 2 degree of freedom with A being the area of the product of the free dimensions of translation
    def get_translational_q_2D(self, A = 0):
        translational_q_2D = 1
        #if translational degree of freedom (A not =0) or there is at least one mobile species (adsorbates)
        if not A == 0 and not self.number_of_mobile_species == 0:
            for mass_single_species in self.mass_mobile_species:
                translational_q_2D *= 2 * math.pi * mass_single_species * c.kBOLTZMANN_JOULE_PER_KELVIN * \
                                      self.temperature /(c.PLANK_CONSTANT_JOULE_SECOND**2) * A
        return translational_q_2D

    #get molecular partition function for translation considering 3 degrees of freedom with P being pressure of the gas in Pa
    def get_translational_q_3D(self, P = 0):
        translational_q_3D = 1
        #if translational degree of freedom (P not =0) or there is at least one mobile species (adsorbates)
        if not P== 0 and not self.number_of_mobile_species == 0:
            for mass_single_species in self.mass_mobile_species:
                translational_q_3D *= (2 * math.pi *mass_single_species * c.kBOLTZMANN_JOULE_PER_KELVIN
                                                 / (c.PLANK_CONSTANT_JOULE_SECOND**2))**1.5 \
                                                                                     * (c.kBOLTZMANN_JOULE_PER_KELVIN/P) * self.temperature**2.5
        return translational_q_3D

    #get rotational partition function assuming a rigid rotor. if linear molecule, argument linear must be explicitly set to True
    def get_rotational_q(self, linear = False):
        if not isinstance(linear, bool):
            print('"linear" arguments must be boolean. Exiting')
            exit(-1)
        rotational_q = 1
        rotational_temperatures = self.get_rotational_temperatures()
        #if general polyatomic molecule with 3 rotational temeperature
        if not linear:
            rotational_q = (self.temperature**1.5/self.get_symmetry_number()) * math.sqrt(math.pi/(rotational_temperatures[0] *
                                                                                                   rotational_temperatures[1] * rotational_temperatures[2]))
        #if linear molecule with one rotational temperature
        else:
            rotational_q = self.temperature/rotational_temperatures[3] / self.get_symmetry_number()
        return rotational_q

    #set vibrational partition function assuming harmonic oscillator and with respect to bottom of potential well
    def get_vibrational_q(self):
        vibrational_q = 1
        for vibrational_temperature in self.get_vibrational_temperatures():
            vibrational_q *= math.exp(-vibrational_temperature/(2*self.temperature)) / (1 - math.exp(-vibrational_temperature/self.temperature))
        return vibrational_q

    #J/mol
    def get_zero_point_energy(self):
        zero_point_energy = 'NaN'
        with open(self.log_file) as fp:
            for line in fp:
                if re.search('Zero-point vibrational energy(.*?)\(', line):
                    zero_point_energy = float(re.search('Zero-point vibrational energy(.*?)\(', line).groups()[0])
        return zero_point_energy


    #J/mol
    def get_electronic_energy(self):
        electronic_energy_plus_zpe = 'NaN'
        with open(self.log_file) as fp:
            for line in fp:
                if re.search('Sum of electronic and zero-point Energies=(.*)', line):
                    #units Hartrees/particle
                    electronic_energy_plus_zpe = float(re.search('Sum of electronic and zero-point Energies=(.*)', line).groups()[0])
        #converting units to J/mol
        electronic_energy_plus_zpe *=c.HARTREES_TO_JOULES_PER_MOLE
        #electronic_energy = electronic_energy_plus_zpe - zpe
        return (electronic_energy_plus_zpe - self.get_zero_point_energy())

    # options for translation = 0 (Don't consider), 1 (1D degree of freedom translation _translation_parameter is the length)/
    # 2 (2D degrees of freedom translation_parameter is the area)
    # 3 (3D degrees of freedom translation_parameter is the pressure of the gas species in Pa)
    # return a dictionary of entropy contributions (J/mol/K) and a dictionary of thermal corrections to energy (J/mol)
    # as entropy, thermal_corrections
    def get_entropy_and_thermal_corrections(self, apply_qrrho = True, rotation = False, translation = 0, translation_parameter = 0):
        if translation not in [0, 1, 2, 3]:
            print('"translation" should be 0 (none), 1(1D), 2(2D) or 3(3D). Exiting')
            return 'NaN'
        entropy = dict()
        energy_thermal_corrections = dict()
        #translational entropy and thermal corrections
        if translation == 0:
            entropy['translational'] = 0
            energy_thermal_corrections['translational'] = 0
        elif translation ==1:
            entropy['translational'] = c.R['J/K/mol'] * (math.log(self.get_translational_q_1D(translation_parameter)) + (self.number_of_mobile_species * 0.5))
            energy_thermal_corrections['translational'] = c.R['J/K/mol'] * self.temperature * \
                                                          self.number_of_mobile_species * 0.5
        elif translation ==2:
            entropy['translational'] = c.R['J/K/mol'] * (math.log(self.get_translational_q_2D(translation_parameter)) + self.number_of_mobile_species)
            energy_thermal_corrections['translational'] = c.R['J/K/mol'] * self.temperature * self.number_of_mobile_species
        else:
            #3D translation (free ideal gas)
            entropy['translational'] = c.R['J/K/mol'] * (math.log(self.get_translational_q_3D(translation_parameter)) + self.number_of_mobile_species * 2.5)
            energy_thermal_corrections['translational'] = c.R['J/K/mol'] * self.temperature * \
                                                         self.number_of_mobile_species * 2.5


        #rotational entropy and thermal corrections
        if not rotation:
            #no rotation to be considered
            entropy['rotational'] = 0
            energy_thermal_corrections['rotational'] = 0
        else:
            entropy['rotational'] = c.R['J/K/mol'] * (math.log(self.get_rotational_q(linear = False)) + 1.5)
            energy_thermal_corrections['rotational'] = c.R['J/K/mol'] * self.temperature * 1.5


        #vibrational entropy and thermal corrections

        #considering the harmonic oscillator model only
        vibrational_entropies = [c.R['J/K/mol'] * (vibrational_temperature / (self.temperature * (math.exp(vibrational_temperature / self.temperature) - 1))
                                                    - math.log(1 - math.exp(-vibrational_temperature / self.temperature)))
                                                      for vibrational_temperature in self.get_vibrational_temperatures()]
        vibrational_energies = [c.R['J/K/mol'] * vibrational_temperature * (
        0.5 + 1 / (math.exp(vibrational_temperature / self.temperature) - 1))
                                for vibrational_temperature in self.get_vibrational_temperatures()]

        if apply_qrrho:
            # reference #1 entropy for QRRHO model
            frequencies_inv_cm = self.get_frequencies_inv_cm()
            frequencies_hertz = [frequency_inv_cm * c.SPEED_OF_LIGHT_CENTIMETER_PER_SECOND for frequency_inv_cm in frequencies_inv_cm]
            w_list = [1/(1+(100/frequency)**4) for frequency in frequencies_inv_cm ]
            B_av = 1e-44  # kg m^2 Average molecular moment of inertia as a limiting value for small moment of inertia
            # moment of inertia for a free rotor with the same frequency
            moments_inertia_free_rotor = [c.PLANK_CONSTANT_JOULE_SECOND/(8*math.pi**2*frequency) for frequency in frequencies_hertz]
            weighted_moments_inertia = [moment_inertia_free_rotor*B_av/(moment_inertia_free_rotor+B_av) for moment_inertia_free_rotor in moments_inertia_free_rotor]
            low_frequency_entropies = [c.R['J/K/mol'] *
                                     (0.5 + math.log(math.sqrt(8 * moment_inertia * c.kBOLTZMANN_JOULE_PER_KELVIN * self.temperature * math.pi**3/c.PLANK_CONSTANT_JOULE_SECOND**2)))
                                     for moment_inertia in weighted_moments_inertia]

            corrected_vibrational_entropies = [w * vibrational_entropy + (1-w) * low_frequency_entropy
                                     for w, vibrational_entropy, low_frequency_entropy in zip(w_list, vibrational_entropies, low_frequency_entropies)]
            corrected_vibrational_energies = [w * vibrational_energy + (1 - w) * 0.5 * c.R['J/K/mol'] * self.temperature
                                              for w, vibrational_energy in zip(w_list, vibrational_energies)]
        else:
            #entropy and thermal corrections for harmonic oscillator model
            corrected_vibrational_entropies = vibrational_entropies
            corrected_vibrational_energies = vibrational_energies


        entropy['vibrational'] = sum(corrected_vibrational_entropies)
        energy_thermal_corrections['vibrational'] = sum(corrected_vibrational_energies)


        #Correction term due to Sterling's approximation
        entropy['sterling additive constant'] = c.R['J/K/mol']


        return entropy, energy_thermal_corrections

    #all in J/mol
    def get_energies(self, entropy, energy_thermal_corrections):
        energies = dict()
        total_thermal_corrections_energy = sum([energy_thermal_corrections[key] for key in energy_thermal_corrections])
        energies['electronic_energy'] = self.get_electronic_energy()
        energies['internal_energy'] = energies['electronic_energy'] + total_thermal_corrections_energy + self.get_zero_point_energy()
        energies['enthalpy'] = energies['internal_energy'] + c.R['J/K/mol']*self.temperature
        energies['gibbs_free_energy'] = energies['enthalpy'] - self.temperature * sum([entropy[key] for key in entropy])
        return energies



































