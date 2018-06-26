# Program to remove info category from data spreadsheets, add PAT# column and remove Image Type and Feature class
# columns, automated to do this for every .tsv file in a given directory
# Will NOT work if there are any already edited files in the path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
pathName = "/Volumes/Public/Test"

# make sure that the Drobo is mounted and findable
os.getcwd()
# if the path does not exist the program will end early and give an error message
if (os.path.exists(pathName) == False):
    print("ERROR: The path does not exist.")
    exit()

# display all tsv files in PosteriorFossaTumors folder

listOfFiles = list()
listOfPAT = list()
listOfFNames = list()

#use os.walk() to walk through directory and grab files that we're interested in
for root, dirs, files in os.walk(pathName, topdown = True):
    files = [file for file in files if file.endswith('.tsv')]  # only grab .tsv files (all we need)
    dirs[:] = [d for d in dirs if d.startswith('PAT')]  # only look in folders that start with PAT?
    listOfFiles += [os.path.join(root, file) for file in files]  # not really needed, redundant to be removed later
    listOfFNames += files  # create list of .tsv files from all PAT folders
    listOfPAT += dirs  # incorrect, only gives one instance each instead of listing the folder name for each file within

# end program early if there are any already edited files?, this doesn't work atm
if [f for f in files if f.startswith('e')] == True:
    print("Please delete the already edited files to avoid a crash.")
    exit()

#remove '/Volumes/Public/PosteriorFossaTumors/' and 'filename from root list
j = 0
listLength = len(listOfFiles)
while j < listLength:
    listOfFiles[j] = listOfFiles[j].replace(pathName + '/' ,'')
    listOfFiles[j] = listOfFiles[j][0:8]  # remove the file name by keeping only the first 8 char
    j= j + 1
i = 0
while i < listLength:
    listOfFNames[i] = listOfFNames[i].replace('.tsv', '')
    i = i + 1

# make a matrix combining listOfFiles and listOfPAT, column 0 = patient number, column 1 = file name
fileMatrix = np.column_stack((listOfFiles, listOfFNames))

# edit tsv file to desired specs
k = 0
while k < listLength:
    patientNum = fileMatrix[k,0]
    fileName = fileMatrix[k,1]
    fileNameEdit = 'e'+ fileName

    # generate locations for input and output files
    location = pathName + "/" + patientNum + "/" + fileName + ".tsv"
    locationE = pathName + "/" + patientNum + "/" + fileNameEdit + ".tsv"

    # import .tsv file as panda dataframe for manipulation, need to change .from_csv to .read_csv
    df = pd.read_csv(location, index_col = 0, parse_dates = True, sep = '\t', header = 0)

    # find all entries with Feature Class: info, not needed?
    info_entries = df[df['Feature Class'] == 'info']

    # remove all entries with Feature Class: info
    editdf = df[df['Feature Class'] != 'info']

    # Add column with patient number
    total_rows = editdf.shape[0]
    i = 0
    # make a 2D array with total_rows # of rows and one column
    PatNum = [None] * total_rows

    for total_rows in PatNum:
        PatNum[i] = patientNum
        i = i + 1
    editdf.insert(0, 'PatNum', PatNum)

    # remove Image Type and Feature Class columns
    del editdf['Image type']
    del editdf['Feature Class']

    #replace NAN and INF with 0 in values column, use DataFrame.fillna()
    editdf.replace('inf', 0, inplace = True)  # for some reason inf is not registering as a numpy expression
    editdf.fillna(0, inplace = True)  # inplace = True overwrites the original file, same as df = df.fillna()

    # Save edited data frame to a new tsv file--ends up comma delineated, ok?
    editdf.to_csv(locationE)

    k = k + 1
