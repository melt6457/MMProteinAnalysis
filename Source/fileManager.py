#################################################################################
# File Name:    fileManager.py
# Author:       Kory Melton
# Date:         6/28/17
# Project:      ProteinAnalysis
# Purpose:      This file contains functionality to manage the files in the
#               Resources folder to allow the easy vieiwing and use of these
#               file
#################################################################################

#################################################################################
# Imports
#################################################################################
import glob
import os

#################################################################################
# Functions
#################################################################################
def printResourceFiles():
    #################################################################################
    # Function:     printResourcesFiles
    #
    # Description:  Prints a list of all the files in the resource folder
    #
    # Parameters:   none
    #
    # Returned:     returns all of the files as well (for convenience)
    #################################################################################
    print("These are the files in the Resources Folder:\n")
    os.chdir("../Resources")
    files = glob.glob("*.*")
    for f in files:
        print("File:", f)

    os.chdir("../Source") # return to the source directory
    return files

def getSimulationFiles(simName):
    #################################################################################
    # Function:     getSimulationFiles
    #
    # Description:  gathers a list of the simulation files in Resources
    #
    # Parameters:   simName - the name of the simulation
    #
    # Returned:     A list of the files for the simulation
    #################################################################################

    os.chdir("../Resources")
    file = simName + ".*"
    files = glob.glob(file)

    os.chdir("../Source") # return to the source directory
    return files

def findSimulations():
    #################################################################################
    # Function:     findSimulations
    #
    # Description:  Finds the simulations in the Resources Folder of ProteinAnalysis
    #
    # Parameters:   None
    #
    # Returned:     A list with the names of the simulations in Resources
    #################################################################################

    NAME_INDEX = 0 # the index of name in info
    simulations = [] # a list to store the simulations
    os.chdir("../Resources") # move into the resource folder
    files = glob.glob("*.*") # grab the files in the directory

    # append the simulations with the name (if original) of the file
    for f in files:
        info = f.split(".") # split the file by name and extension

        # test if the simulation name is already in simulations
        if info[NAME_INDEX] not in simulations:
            simulations.append(info[NAME_INDEX])

    os.chdir("../Source") # return to the source folder
    return simulations

def openFile(file_path):
    #################################################################################
    # Function:     openFile
    #
    # Description:  moves into resources opens a file and then moves back into the
    #               highest source folder
    #
    # Parameters:   file_path - the name of the file and its path from the level of
    #               the resource folder
    #
    # Returned:     A list of the files for the simulation
    #################################################################################
    os.chdir("../Resources")
    file = open(file_path)
    os.chdir("../Source")
    return file

def isRMSD(fileSet):
    #################################################################################
    # Function:     isRMSD
    #
    # Description:  tests to see if we can run RMSD analysis by checking if there is
    #               a .dat file from VMD
    #
    # Parameters:   fileSet - the set of files in the simulation
    #
    # Returned:     A list of the files for the simulation
    #################################################################################
    if any(".dat" in f for f in fileSet):
        return True
    else:
        return False