#################################################################################
# File Name:    
# Author:       Kory Melton
# Date:         6/28/17
# Project:      ProteinAnalysis
# Purpose:
#################################################################################

#################################################################################
# Imports
#################################################################################
import matplotlib.pyplot as plt; plt.rcdefaults()
import logAnalysis as log
import rmsdAnalysis as rmsd
import numpy as np

class simulation:

    #################################################################################
    # Initializer
    #################################################################################
    def __init__(self, log_file = "None", rmsd_file = "None"):
        #################################################################################
        # Function:     __init__
        #
        # Description:  Initializes the variables for the simulation class. Both file
        #               types are default to "None" and this will be used to test if a
        #               a given file is specified and if a chosen analysis can be run
        #
        # Parameters:   log_file    -   the log_file with the simulation data stored
        #               rmsd_file   -   the rmsd_file with simulation data
        #
        # Returned:     none
        #################################################################################

        # Loads the log_file if one has been given
        if(log_file is not "None"):
            self.log = log.logAnalysis(log_file)
        else:
            self.log = "None"

        # Loads the rmsd_file is one has been given
        if(rmsd_file is not "None"):
            self.rmsd = rmsd.rmsdAnalysis(rmsd_file)
        else:
            self.rmsd = "None"

    #################################################################################
    # Functions
    #################################################################################
    def plot(self, x, y):
        #################################################################################
        # Function:     plot
        #
        # Description:  Plots a graph using two vectors (lists) using matplotlib.pyplot
        #
        # Parameters:   x   -   a vector of the independent variable to graph
        #               y   -   a vector of the dependent variable to graph
        #
        # Returned:     none
        #################################################################################
        plt.plot(x, y, 'ro')
        plt.show()

    def combine(self, newSim):
        #################################################################################
        # Function:     combine
        #
        # Description:
        #
        # Parameters:   new_sim -   the sim class object to combine to the current
        #                           simulation object
        #
        # Returned:     none
        #################################################################################

        self.log.combineLogInfo(newSim)

        if (self.rmsd is not "None" and newSim.rmsd is not "None"):
            self.rmsd.combineSims(newSim)

    def graphPotentialEnergy(self):
        #################################################################################
        # Function:    graphPotentialEnergy
        #
        # Description:  a function to graph time (dependent) vs. potential energy (independent)
        #
        # Parameters:   none
        #
        # Returned:     none
        #################################################################################

        self.plot(self.log.times, self.log.pot_energy)

    def calcAvePotentialEnergy(self):
        #################################################################################
        # Function:     calcAvePotentialEnergy
        #
        # Description:  calculates the average potential energy for a simulation
        #
        # Parameters:   none
        #
        # Returned:     the average potential energy for the simulation
        #################################################################################

        return np.mean(self.log.pot_energy)

    def calcStdDevPotentialEnergy(self):
        #################################################################################
        # Function:     calcAvePotentialEnergy
        #
        # Description:  calculates the average potential energy for a simulation
        #
        # Parameters:   none
        #
        # Returned:     the average potential energy for the simulation
        #################################################################################

        return np.std(self.log.pot_energy)

    def graphRMSD(self):
        #################################################################################
        # Function:     graphRMSD
        #
        # Description:  a function to graph frame (dependent) vs. RMSD(independent)
        #
        # Parameters:   none
        #
        # Returned:     none
        #################################################################################

        self.rmsd.calculateFrameTimes(self.log.getStartTime(), self.log.getEndTime())
        self.plot(self.rmsd.times, self.rmsd.RMSDs)

    def calcAveDAT(self):
        #################################################################################
        # Function:     calcAveDAT
        #
        # Description:  calculates the average of the data in the DAT file
        #
        # Parameters:   none
        #
        # Returned:     the average of thedata in the DAT file
        #################################################################################

        return np.mean(self.rmsd.RMSDs)

    def calcStdDevDAT(self):
        #################################################################################
        # Function:     calcStdDevDAT
        #
        # Description:  calculates the standard deviation of the data in the DAT file
        #
        # Parameters:   none
        #
        # Returned:     the standard deviation of the data in the DAT file
        #################################################################################
        return np.std(self.rmsd.RMSDs)

    def graphRMSDvsTemp(self):
        #################################################################################
        # Function:     graphRMSDvsTemp
        #
        # Description:  a function to graph temp (dependent) vs. RMSD(independent)
        #
        # Parameters:   none
        #
        # Returned:     none
        #################################################################################

        self.rmsd.calculateFrameTemps(len(self.log.times), self.log.temp)
        self.plot(self.rmsd.temps, self.rmsd.RMSDs)

    def graphPotentialEnergyTemp(self):
        #################################################################################
        # Function:    graphPotentialEnergyTemp
        #
        # Description:  a function to graph temp (dependent) vs. potential energy (independent)
        #
        # Parameters:   none
        #
        # Returned:     none
        #################################################################################

        self.log.extractLogInfo()
        self.plot(self.log.temp, self.log.pot_energy)

    def graphKineticEnergyTemp(self):
        #################################################################################
        # Function:    graphKineticEnergyTemp
        #
        # Description:  a function to graph temp (dependent) vs. kinetic energy (independent)
        #
        # Parameters:   none
        #
        # Returned:     none
        #################################################################################

        self.log.extractLogInfo()
        self.plot(self.log.temp, self.log.kin_energy)

    def loadRMSD(self):
        if (self.rmsd == "None"):
            print ("No RMSD for this simulation\n")
        else:
            self.rmsd.extractRMSD()

    def loadLog(self):
        if (self.log == "None"):
            print ("No Logs for this simulation\n")
        else:
            self.log.extractLogInfo()

    def graphErrorBars(self, objects, values, errors):

        y_pos = np.arange(len(objects))

        plt.bar(y_pos, values, align='center', alpha=0.5, yerr=errors)
        plt.xticks(y_pos, objects)
        # plt.xticklabels('First', 'Second')
        plt.ylabel('Value')
        plt.title('Cool Data')

        plt.show()





