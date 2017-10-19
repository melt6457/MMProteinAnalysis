#################################################################################
# File Name:    ProteinAnalysis.py
# Author:       Kory Melton
# Date:         6/28/17
# Project:      ProteinAnalysis
# Purpose:      To run the ProteinAnalysis Program
#################################################################################

#################################################################################
# Imports
#################################################################################
from ProteinAnalyzer import *
import os

clear = lambda: os.system('cls')
proceed = 'y'
printHeader()

while proceed is 'y':
    printStartMenu()
    selection = getSelection(LOW_START, HIGH_START)
    performSelection(selection)
    proceed = input("Proceed? (y or n): ")
    clear()

print("Thank you for using MMProteinAnalysis!")