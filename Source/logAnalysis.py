#################################################################################
# File Name:    logAnalysis.py
# Author:       Kory Melton
# Date:         6/28/17
# Project:      ProteinAnalysis
# Purpose:      This file will define and implement the logAnalysis class
#               to allow the easy use of analyzing information from a log file
#################################################################################


class logAnalysis:

    #################################################################################
    # Initializer
    #################################################################################
    def __init__(self, log_file):
        #################################################################################
        # Function:     __init__
        #
        # Description:  Initializes the variables for the logAnalysis class
        #
        # Parameters:   log_file    -   the log_file with the simulation data stored
        #
        # Returned:     none
        #################################################################################

        #################################################################################
        # Log File Variables
        #################################################################################
        self.log_file = log_file  # this is the log file
        self.log_lines = self.log_file.readlines()  # the lines from the log file

        #################################################################################
        # Data Variables
        # Each variable is a list of a different column from the log file. The specific
        # measurement will be listed to the right
        #################################################################################
        self.times = []         # time
        self.pot_energy = []    # potential energy
        self.kin_energy = []    # kinetic energy
        self.tot_energy = []    # total energy
        self.temp = []          # temperature

        #################################################################################
        # Index variables
        # Each variable represents the index for each variable in the log file
        #
        # The way this program reads in data from the log file is by splitting the lines
        # in the file into lists (the log file is generically tab delimited) each time
        # there is whitespace. These variables store the location of each variable once
        # the line is split up into different strings using the getIndexFromLog function.
        #
        #################################################################################
        # Get the index for each variable from the log so we can read a line and access the informations location
        self.TIMES_INDEX = self.getIndexFromLog("\"Time (ps)\"")
        self.PE_INDEX = self.getIndexFromLog("\"Potential Energy (kJ/mole)\"")
        self.KE_INDEX = self.getIndexFromLog("\"Kinetic Energy (kJ/mole)\"")
        self.TE_INDEX = self.getIndexFromLog("\"Total Energy (kJ/mole)\"")
        self.K_INDEX = self.getIndexFromLog("\"Temperature (K)\"")

    #################################################################################
    # Functions
    #################################################################################
    def extractLogInfo(self):
        #################################################################################
        # Function:     extractLogInfo
        #
        # Description:  Extracts the information from the log file and stores them in
        #               the class variables. First, each line is split into a list of
        #               variables. Then, each variable is stored in a temporary variable
        #               as a float using the stored index value. Finally, each variable
        #               is appended to the end of the list for the variable type.
        #
        # Parameters:   none
        #
        # Returned:     none
        #################################################################################

        for line in self.log_lines:
            if line is not self.log_lines[0]:
                # split the line into a list of variables
                vars = line.split()

                # Store each variable
                time = float(vars[self.TIMES_INDEX])
                PE = float(vars[self.PE_INDEX])
                KE = float(vars[self.KE_INDEX])
                TE = float(vars[self.TE_INDEX])
                temp = float(vars[self.K_INDEX])

                # append each variable its corresponding list
                self.times.append(time)
                self.pot_energy.append(PE)
                self.kin_energy.append(KE)
                self.tot_energy.append(TE)
                self.temp.append(temp)

    def getIndexFromLog(self, string):
        #################################################################################
        # Function:     getIndexFromLog
        #
        # Description:  Finds the index of a string from the header line of a log file
        #               once the line is split up.
        #               for example
        #                   self.TIMES_INDEX = self.getIndexFromLog("\"Time (ps)\"")
        #
        # Parameters:   string  -   the string to find the index for
        #
        # Returned:     none
        #################################################################################

        header = self.log_lines[0]  # grab the header for the log file
        info = header.split('\t')   # split the header into different information
        return info.index(string)   # returns the index of the string

    def combineLogInfo(self, newSim):
        #################################################################################
        # Function:     combineLogInfo
        #
        # Description:
        #
        # Parameters:   newSim  -
        #
        # Returned:     none
        #################################################################################
        self.times.extend(newSim.log.times)
        self.pot_energy.extend(newSim.log.pot_energy)
        self.kin_energy.extend(newSim.log.kin_energy)
        self.tot_energy.extend(newSim.log.tot_energy)
        self.temp.extend(newSim.log.temp)

    def getStartTime(self):
        #################################################################################
        # Function:     getStartTime
        #
        # Description:  gets the start time of the simulation
        #
        # Parameters:   none
        #
        # Returned:     the start time of the sim
        #################################################################################
        return self.times[0]

    def getEndTime(self):
        #################################################################################
        # Function:     getEndTime
        #
        # Description:  gets the end time of the simulation
        #
        # Parameters:   none
        #
        # Returned:     the end time of the sim
        #################################################################################
        return self.times[len(self.times) - 1]