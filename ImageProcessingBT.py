# Program to add image data to a matrix for use in machine learning

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
print(listOfPAT, listOfFiles)
total_pats = len(listOfPAT)

dataSet = np.empty([5, total_pats], dtype = object)
dataSet[0, :] = listOfPAT
internalDataSet = np.empty([1, 4], dtype = object)

i = 0
while i < total_pats:
    j = 0
    while j < numOfSlices[i]:
        k = 0
        while k < 4:
            internalDataSet[0, k] = dicom.dcmread(listOfFiles[k])
            k = k + 1
        dataSet[j+1, i] = internalDataSet
        j = j + 1
    i = i + 1
df = pd.DataFrame(dataSet)
print(listOfPAT, listOfFiles)