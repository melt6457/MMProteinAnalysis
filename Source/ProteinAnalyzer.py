#################################################################################
# File Name:    ProteinAnalyzer
# Author:       Kory Melton
# Date:         6/28/17
# Project:      ProteinAnalysis
# Purpose:      This file is used to create a module that will be used to run
#               Protein Analyzer
#################################################################################

#################################################################################
# Imports
#################################################################################
import simulation as sim
import fileManager as files
import sys

#################################################################################
# CONSTANTS
#################################################################################
LOW_START = 0
HIGH_START = 3
QUIT = 0
PRINT_RESOURCES = 1
RUN_ANALYSIS = 2
COMBINE_SIMULATIONS = 3
RESOURCE_PATH = "../Resources"
NUM_ANALYSIS_CHOICES = 6

#################################################################################
# User Interface Functions
#################################################################################
def quit():
    #################################################################################
    # Function:     quit
    #
    # Description:  quits the program
    #
    # Parameters:   none
    #
    # Returned:     none
    #################################################################################

    print("Thank you for using Protein Analyzer!")
    sys.exit()

def printHeader():
    #################################################################################
    # Function:     printHeader
    #
    # Description:  prints the header to the program
    #
    # Parameters:   none
    #
    # Returned:     none
    #################################################################################
    print("***********************************")
    print("*** Welcome to Protein Analyzer ***")
    print("***********************************\n")

def printStartMenu():
    #################################################################################
    # Function:     printStartMenu
    #
    # Description:  Prints the start menu in the form
    #               Please select from the following
    #               0) Quit
    #               1) Display Resource Files
    #               2) Run Analysis on a single Simulation
    #               3) Combine Simulation (extended by checkpoint files) for Analysis
    #
    # Parameters:   none
    #
    # Returned:     none
    #################################################################################
    print("Please select from the following")
    print("0) Quit")
    print("1) Display Resource Files")
    print("2) Run Analysis on a single Simulation")
    print("3) Combine Simulations (extended by checkpoint files) for Analysis\n")

def getSelection(low_val, high_val):
    #################################################################################
    # Function:     getSelection
    #
    # Description:  Gets an integer selection from the user after a menu is printed.
    #               This function will have input validation from testSelection to
    #               ensure the selection occurs between a lower bound and an upper bound.
    #
    # Parameters:   low_val     -   the lower bound for the selection
    #               high_val    -   the upper bound for the selection
    #
    # Returned:     an integer representing the users selection
    #################################################################################

    selection = -1  # use this to jump into the loop

    # get the selection with input validation from testSelection
    while testSelection(selection, low_val, high_val) is False:
        choice = input("Enter your choice here (integer): ")
        selection = int(choice)

    return selection

def testSelection(choice, low_val, high_val):
    #################################################################################
    # Function:     testSelection
    #
    # Description:  Tests for user input validation by ensuring the selection is
    #               from the list of integers in the menu. This is done generically
    #               with a lower bound and an upper bound for easy use in the future.
    #
    # Parameters:   choice      -   the choice from the user
    #               low_val     -   the lower bound for the choice
    #               high_val    -   the upper bound for the choice
    #
    # Returned:     TRUE    -   if the selection is valid
    #               FALSE   -   if the selection is invalid
    #################################################################################

    bIsValid = False  # used to store the boolean variable (default false)
    test = int(choice)  # we need to have an integer to test below

    # tests the choice to see if it falls within the boundaries
    # if the choice does then change the returned boolean to true
    if (choice >= low_val and choice <= high_val):
        bIsValid = True

    return bIsValid

def performSelection(selection):
    #################################################################################
    # Function:     performSelection
    #
    # Description:  performs the users selection using if...else if statements
    #
    # Parameters:   selection   -   the users selection
    #
    # Returned:     none
    #################################################################################

    if selection is QUIT:
        quit()
    elif selection is PRINT_RESOURCES:
        files.printResourceFiles()
    elif selection is RUN_ANALYSIS:
        runAnalysis()
    elif selection is COMBINE_SIMULATIONS:
        combineSims()

def analysisMenu():
    #################################################################################
    # Function:     analysisMenu
    #
    # Description:  prints the analysis menu for the user
    #
    # Parameters:   none
    #
    # Returned:     none
    #################################################################################

    print("Please select from the following")
    print("0) Quit")
    print("1) Graph RMSD")
    print("2) Graph RMSD vs. Temp")
    print("3) Graph Potential Energy vs. Time")
    print("4) Graph Potential Energy vs. Temp")
    print("5) Graph Kinetic Energy vs. Temp")
    print("6) Report Potential Energy Data")

def selectSimulation():
    #################################################################################
    # Function:     selectSimulation
    #
    # Description:  Provides functionality to have the user select which simulation
    #               (previously loaded into the Resources directory) they would like
    #               to run an analysis on.
    #
    # Parameters:   none
    #
    # Returned:     the selected simulation
    #################################################################################

    print("Please select a simulation")

    index = 0  # start numbering for print out
    sims = files.findSimulations()  # get a list of the simulations

    print(index, ") Quit", sep='') # print quit out choice

    # print choices for each sim
    for sim in sims:
        index += 1
        print(index, ") ", sim, sep='')

    # get the simulation selection from the user
    selection = getSelection(0, len(sims))

    # perform the selection
    if selection is QUIT:
        quit()
    else:
        return sims[(selection - 1)] # return -1 because the list starts numbering at 0

def selectMultipleSimulations():
    #################################################################################
    # Function:     selectSMultipleSimulations
    #
    # Description:  Allows the user to select multiple simulations
    #
    # Parameters:   none
    #
    # Returned:     A list of the selected simulations
    #################################################################################

    index = 0  # start numbering for print out
    sims = files.findSimulations()  # get a list of the simulations
    simulations = [] # a list of the simulations to combine

    proceed = 'y'

    while proceed is 'y':
        print("Please select a simulation")

        print(index, ") Quit", sep='') # print quit out choice

        # print choices for each sim
        for sim in sims:
            index += 1
            print(index, ") ", sim, sep='')

        # get the simulation selection from the user
        selection = getSelection(0, len(sims))

        # perform the selection
        if selection is QUIT:
            quit()
        else:
            simulations.append(sims[(selection - 1)]) # return -1 because the list starts numbering at 0

        proceed = input("Do you want to choose another simulation to combine? (y or n): ")
        index = 0

    return simulations

#################################################################################
# Performance Functions
#################################################################################
def createSimAnalysis(fileSet):
    #################################################################################
    # Function:     createSimAnalysis
    #
    # Description:  Creates a simulation for analysis. This uses functionality from
    #               file manager to open files correctly, as well as the initializer
    #               from the simulation class.
    #
    # Parameters:   fileSet -   the set of files that contain simulation information
    #
    # Returned:     none
    #################################################################################

    if files.isRMSD(fileSet) is True:
        rmsdFile = files.openFile(fileSet[0])
        logFile = files.openFile(fileSet[1])
        simulation = sim.simulation(log_file=logFile, rmsd_file=rmsdFile)
    else:
        logFile = files.openFile(fileSet[0])
        simulation = sim.simulation(log_file = logFile)

    return simulation

def performAnalysis(selection, simulation):
    #################################################################################
    # Function:     performAnalysis
    #
    # Description:  Performs the analysis the user selects. Provides errors if the
    #               specified analysis can't be run.
    #
    # Parameters:   selection   -   the selection from the user
    #               simulation  -   the simulation object created
    #
    # Returned:     none
    #################################################################################

    if selection is QUIT:
        quit()
    elif selection is 1:
        if simulation.rmsd is "None":
            print("There is no .dat for RMSD graphing.")
        else:
            simulation.graphRMSD()

            avg = simulation.calcAveDAT()
            print("The Average is: ", avg)
    elif selection is 2:
        if simulation.rmsd is "None":
            print("There is no .dat for RMSD graphing.")
        else:
            simulation.graphRMSDvsTemp()
    elif selection is 3:
        if simulation.log is "None":
            print("There is no .log to use for graphing.")
        else:
            simulation.graphPotentialEnergy()

            avePotEnergy = simulation.calcAvePotentialEnergy()
            print("The Average Potential Energy is: ", avePotEnergy)
    elif selection is 4:
        if simulation.log is "None":
            print("There is no .log to use for graphing.")
        else:
            simulation.graphPotentialEnergyTemp()
    elif selection is 5:
        if simulation.log is "None":
            print("There is no .log to use for graphing.")
        else:
            simulation.graphKineticEnergyTemp()
    elif selection is 6:
        if simulation.log is "None":
            print("There is not .log info to use for graphing.")
        else:
            avePE = simulation.calcAvePotentialEnergy()
            stdDevPE = simulation.calcStdDevPotentialEnergy()

            print("The Average Potential Energy is: ", avePE)
            print("The Standard Deviation of Potential Energy is: ", stdDevPE)

            simulation.graphErrorBars(avePE, stdDevPE)

def runAnalysis():
    #################################################################################
    # Function:     runAnalysis
    #
    # Description:  Runs analysis functionality:
    #                   Prints out Current Simulation
    #                   Retrieves set of simulation files
    #                   Creates a simulation object
    #                   Gets the users selection
    #                   Performs the analysis
    #
    # Parameters:   none
    #
    # Returned:     none
    #################################################################################
    simName = selectSimulation()
    print("Your Simulation: ", simName)
    fileSet = files.getSimulationFiles(simName)
    simulation = createSimAnalysis(fileSet)
    simulation.loadLog()
    simulation.loadRMSD()

    proceed = 'y'
    while proceed is 'y':
        analysisMenu()
        selection = getSelection(0, NUM_ANALYSIS_CHOICES)
        performAnalysis(selection, simulation)
        proceed = input("Keep analyzing this simulation? (y or n): ")

def combineSims():
    #################################################################################
    # Function:     combineSims
    #
    # Description:  Allows to user to select two simulations and it combines the
    #               the information of these two simulations into the first simulation.
    #
    # Parameters:   none
    #
    # Returned:     none
    #################################################################################
    print("Select Sims to Combine")
    simNames = selectMultipleSimulations()
    sims = []

    for count in range(0, len(simNames)):
        fileSet = files.getSimulationFiles(simNames[count])
        sim = createSimAnalysis(fileSet)
        sim.loadLog()
        sim.loadRMSD()
        sims.append(sim)

    for count in range(1, len(simNames)):
        sims[0].combine(sims[count])


    proceed = 'y'
    while proceed is 'y':
        analysisMenu()
        selection = getSelection(0, NUM_ANALYSIS_CHOICES)
        performAnalysis(selection, sims[0])
        proceed = input("Keep analyzing this simulation? (y or n): ")