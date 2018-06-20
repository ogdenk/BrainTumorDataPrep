# Program to remove info category from data spreadsheets, add DWI as an additional prompt?
from typing import List, Union

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import os

# make sure that the Drobo is mounted and findable
os.getcwd()
print(os.path.exists("/Volumes/Public/PosteriorFossaTumors/PAT00010"))

continueYN = "y"

while continueYN == "y":
    # ask user which patient to update files for
    # patientNum = input("What patient's spreadsheets would you like to update? ")
    patientNum = "00010"  # for troubleshooting purposes

    # use user input to generate locations for input and output files
    locationT1 = "/Volumes/Public/PosteriorFossaTumors/PAT" + patientNum + "/T1.tsv"
    locationT2 = "/Volumes/Public/PosteriorFossaTumors/PAT" + patientNum + "/T2.tsv"
    locationflux = "/Volumes/Public/PosteriorFossaTumors/PAT" + patientNum + "/flux.tsv"
    locationDWI = "/Volumes/Public/PosteriorFossaTumors/PAT" + patientNum + "/DWI.tsv"
    locationT1e = "/Volumes/Public/PosteriorFossaTumors/PAT" + patientNum + "/T1e.tsv"
    locationT2e = "/Volumes/Public/PosteriorFossaTumors/PAT" + patientNum + "/T2e.tsv"
    locationfluxe = "/Volumes/Public/PosteriorFossaTumors/PAT" + patientNum + "/fluxe.tsv"
    locationDWIe = "/Volumes/Public/PosteriorFossaTumors/PAT" + patientNum + "/DWIe.tsv"

    # import .tsv file as panda dataframe for manipulation
    dfT1 = pd.DataFrame.from_csv(locationT1, sep='\t', header=0)
    dfT2 = pd.DataFrame.from_csv(locationT2, sep='\t', header=0)
    # dfflux = pd.DataFrame.from_csv(locationflux, sep='\t', header=0)
    # dfDWI = pd.DataFrame.from_csv(locationDWI, sep='\t', header=0)

    # find all entries with Feature Class: info
    info_entriesT1 = dfT1[dfT1['Feature Class'] == 'info']
    info_entriesT2 = dfT2[dfT2['Feature Class'] == 'info']
    # info_entriesflux = dfflux[dfflux['Feature Class'] == 'info']
    # info_entriesDWI = dfDWI[dfDWI['Feature Class'] == 'info']

    # remove all entries with Feature Class: info
    editdfT1 = dfT1[dfT1['Feature Class'] != 'info']
    editdfT2 = dfT2[dfT2['Feature Class'] != 'info']
    # editdfflux = dfflux[dfflux['Feature Class'] != 'info']
    # editdfDWI = dfDWI[dfDWI['Feature Class'] != 'info']

    # check
    # print(editdf[:])

    # Add column with patient number
    total_rows = editdfT1.shape[0]
    i = 0
    #make a 2D array with total_rows # of rows and one column
    PatNum = [None] * total_rows

    for total_rows in PatNum:
        PatNum[i] = patientNum
        i = i + 1
    editdfT1.insert(0, 'PatNum', PatNum)

    #remove Image Type and Feature Class columns
    # editdfT1.drop(columns = ['Image Type', 'Feature Class']) #doesn't currently work as the version of pandas is too old
    editdfT1.drop(['Image type', 'Feature Class'], axis=1)

    # Save edited data frame to a new tsv file--ends up comma delineated, ok?
    editdfT1.to_csv(locationT1e)
    # editdfT2.to_csv(locationT2e)
    # editdfflux.to_csv(locationflux)
    # editdfDWI.to_csv(locationDWI)

    # Ask for next patient
    # continueYN = input("Would you like to edit another patient? y/n ")
    continueYN = 'n'  # for troubleshooting purposes
    print(pd.__version__)