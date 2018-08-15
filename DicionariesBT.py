# Program to add image data to a matrix for use in machine learning
# Matrix will be populated by dictionary entries corresponding to each Patient
# Dictionary entries will hold data matrices containing all time slices for each channel of data

import os
import numpy as np
import pandas as pd
import pydicom as dicom


pathName = "/Volumes/Public/Test"

# make sure that the Drobo is mounted and findable
os.getcwd()
# if the path does not exist the program will end early and give an error message
if os.path.exists(pathName) is False:
    print("ERROR: The path does not exist.")
    exit()

listOfFiles = list()
listOfPAT = list()
fileName = list()
listOfDirs = list()
numOfSlices = list()

excel_df = pd.read_excel(pathName + '/SliceData.xls', sheet_name='Sheet2', header=0)
tumorType = excel_df['Type'].tolist()

# use os.walk() to walk through directory and grab files that we're interested in
for root, dirs, files in os.walk(pathName, topdown=True):
    dirs = [d for d in dirs if d.startswith('PAT')]  # only look in folders that start with PAT
    listOfPAT += dirs  # only gives one instance each instead of listing the folder name for each file
listOfPAT.sort()

for allPatients in listOfPAT:
    pathNameNew = pathName + '/' + allPatients + '/Slices'
    for root, dirs, files in os.walk(pathNameNew, topdown = True):
        files = [file for file in files if file.endswith('.dcm')]
        fileName += files
        listOfFiles += [os.path.join(root, file) for file in files]
    numOfSlices.append(len(files))
listOfFiles.sort()
total_pats = len(listOfPAT)

i = 0
y = 0
data = {}
patient = {}
dataSet = {}

while i < total_pats:
    j = 0
    while j < numOfSlices[i]:
        k = 0
        while k < 4:
            if k == 0:
                name = 'ADC'
            if k == 1:
                name = 'Flair'
            if k == 2:
                name = 'T1'
            if k == 3:
                name = 'T2'
            ds = dicom.dcmread(listOfFiles[y])
            number = str(j + 1)
            data[name + '.' + number] = ds.pixel_array
            k = k + 1
            y = y + 1
        j = j + 1
    patient['type'] = (tumorType[i])
    patient['Data'] = data
    dataSet[listOfPAT[i]] = patient
    i = i + 1
print(len(dataSet))
print('Donezo')
