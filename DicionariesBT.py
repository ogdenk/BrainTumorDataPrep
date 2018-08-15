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
# print(listOfPAT, listOfFiles)
total_pats = len(listOfPAT)

# Get ref file
RefDs = dicom.read_file(listOfFiles[0])

# Load dimensions based on the number of rows, columns, and slices (along the Z axis)
ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(listOfFiles))

# Load spacing values (in mm)
ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), float(RefDs.SliceThickness))

dataSet = np.empty([ConstPixelDims, 4, 4], dtype = RefDs.pixel_array.dtype)

i = 0
while i < total_pats:
    j = 0
    while j < numOfSlices[i]:
        k = 0
        while k < 4:

            k = k + 1
        j = j + 1
    i = i + 1

