#################################################################################
# File Name:    rmsdAnalysis.py
# Author:       Kory Melton
# Date:         6/28/17
# Project:      ProteinAnalysis
# Purpose:      This file will define and implement the rmsdAnalysis class
#               to allow the easy use of analyzing information for
#               root mean square deviation (a measure of molecular movement)
#################################################################################

import math

class rmsdAnalysis:

    #################################################################################
    # Initializer
    #################################################################################
    def __init__(self, rmsd_file):
        #################################################################################
        # Function:     __init__
        #
        # Description:  Initializes the variables for the rmsdAnalysis class
        #
        # Parameters:   rmsd_file    -   the log_file with the simulation data stored
        #
        # Returned:     none
        #################################################################################

        #################################################################################
        # File Variables
        #################################################################################
        self.rmsd_file = rmsd_file  # this is a .dat file created from VMD to analyze RMSD of the simulation
        self.rmsd_lines = self.rmsd_file.readlines()  # the lines from the RMSD file

        #################################################################################
        # Data Variables
        # Each variable is a list of a different column from the dat file. The specific
        # measurement will be listed to the right
        #################################################################################
        self.frames = []    # this is a list of the frames from the VMD output
        self.RMSDs = []     # this is a list of the RMSDs from the VMD output
        self.times = []     # this is a list of the time for each corresponding frame
        self.temps = []     # this is a list of the temperatures for each corresponding frame

        #################################################################################
        # Index variables
        # Each variable represents the index for each variable in the log file
        #################################################################################
        self.FRAME_INDEX = 0  # the index of the frame when separating the lines from the file
        self.RMSD_INDEX = 1  # the index of the RMSD when seperating the lines from the file

    #################################################################################
    # Functions
    #################################################################################
    def extractRMSD(self):
        #################################################################################
        # Function:     extractRMSD
        #
        # Description:  Extracts the RMSD information in two lists that can be used later
        #
        # Parameters:   none
        #
        # Returned:     none
        #################################################################################

        self.cleanRMSD()

        for line in self.rmsd_lines: # step through the lines
            vars = line.split() # split the line by spaces to get the two variables

            # retrieve the two variables from vars
            frame = int(vars[self.FRAME_INDEX])
            RMSD = float(vars[self.RMSD_INDEX])

            # store them in each list
            self.frames.append(frame)
            self.RMSDs.append(RMSD)

    def combineSims(self, newSim):
        #################################################################################
        # Function:     combineSims
        #
        # Description:  combines the log information and the rmsd for a simulation
        #
        # Parameters:   newSim      -   the new simulation object
        #
        # Returned:     the new simulation object
        #################################################################################

        start = len(self.frames) + 1
        end = start + len(newSim.rmsd.frames)

        newSim.rmsd.frames.clear()
        for count in range (start, end):
            newSim.rmsd.frames.append(count)

        self.frames.extend(newSim.rmsd.frames)
        self.RMSDs.extend(newSim.rmsd.RMSDs)
        self.times.extend(newSim.rmsd.times)

    def cleanRMSD(self):

        if self.rmsd_lines[0] == '0 0\n':
            del self.rmsd_lines[0]
            del self.rmsd_lines[0]
            del self.rmsd_lines[0]
            self.rmsd_lines.pop()

    def calculateFrameTimes(self, simTimeStart, simTimeEnd):
        #################################################################################
        # Function:     calculateFrameTimes
        #
        # Description:  This will calculate the time for each frame and add it to a list
        #               of times. First, it will look to see how many frames there are
        #               and how long the simulation ran. Then, it will simply divide the
        #               the simulation time by the number of frames to get the time for
        #               each frame.
        #
        # Parameters:   simTimeStart    -   the start of the sim in picoseconds
        #               simTimeEnd      -   the end of the sim in picoseconds
        #
        # Returned:     none
        #################################################################################

        numFrames = len(self.frames)
        simTime = simTimeEnd - simTimeStart
        timePerFrame = simTime / numFrames

        start = 0
        end = numFrames

        for frame in range(start, end):
            time = simTimeStart + frame * timePerFrame
            self.times.append(time)

    def calculateFrameTemps(self, simFrames, temps):
        #################################################################################
        # Function:     calculateFrameTemps
        #
        # Description:
        #
        # Parameters:
        #
        # Returned:     none
        #################################################################################

        # a stride is the how often the frames from the original file are used
        #   so a stride of 3 means every 3rd frame from the original simulation was used
        stride = simFrames / len(self.frames)   # find the stride of the .dat file
        step = math.floor(stride)
        start = self.frames[0]
        end = len(self.frames) + start

        # use the stride and the frame in the .dat file to find the temperature
        for frame in range(start, end):
            tempIndex = frame * step # the index(or frame) from the original simulation
            self.temps.append(temps[tempIndex - 1]) # append temps with the temperature from that index