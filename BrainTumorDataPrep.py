# Program to auto-populate matrix of data spreadsheets and identify data with separate key matrix

import os
import numpy as np

pathName = "/Volumes/Public/Test"

# make sure that the Drobo is mounted and findable
os.getcwd()
# if the path does not exist the program will end early and give an error message
if os.path.exists(pathName) is False:
    print("ERROR: The path does not exist.")
    exit()

# display all tsv files in project folder

listOfFiles = list()
listOfPAT = list()
listOfFNames = list()

# use os.walk() to walk through directory and grab files that we're interested in
for root, dirs, files in os.walk(pathName, topdown = True):
    files = [file for file in files if file.endswith('.tsv')]  # only grab .tsv files (all we need)
    dirs[:] = [d for d in dirs if d.startswith('PAT')]  # only look in folders that start with PAT?
    listOfFiles += [os.path.join(root, file) for file in files]  # not really needed, redundant to be removed later
    listOfFNames += files  # create list of .tsv files from all PAT folders
    listOfPAT += dirs  # incorrect, only gives one instance each instead of listing the folder name for each file within

# remove pathName and 'filename from root list
j = 0
listLength = len(listOfFiles)
while j < listLength:
    listOfFiles[j] = listOfFiles[j].replace(pathName + '/', '')
    listOfFiles[j] = listOfFiles[j][0:8]  # remove the file name by keeping only the first 8 char
    j = j + 1
i = 0
while i < listLength:
    listOfFNames[i] = listOfFNames[i].replace('.tsv', '')
    i = i + 1

# make a matrix combining listOfFiles and listOfPAT, column 0 = patient number, column 1 = file name
fileMatrix = np.column_stack((listOfFiles, listOfFNames))
print(fileMatrix)

k = 0
while k < listLength:
    patientNum = fileMatrix[k, 0]
    fileName = fileMatrix[k, 1]
    fileNameEdit = fileName + 'E'
    k = k + 1