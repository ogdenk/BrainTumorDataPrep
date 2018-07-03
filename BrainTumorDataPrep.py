# Program to auto-populate matrix of data spreadsheets and identify data with separate key matrix

import os
import numpy as np
import pandas as pd

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
    files = [file for file in files if file.startswith('e')]  # only grab edited files
    dirs[:] = [d for d in dirs if d.startswith('PAT')]  # only look in folders that start with PAT?
    listOfFiles += [os.path.join(root, file) for file in files]  # not really needed, redundant to be removed later
    listOfFNames += files  # create list of .tsv files from all PAT folders
    listOfPAT += dirs  # incorrect, only gives one instance each instead of listing the folder name for each file

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
# print(fileMatrix)

col_num = 256 * len(listOfPAT) + 1
total_pats = len(listOfPAT)
dataSet = np.empty([3364, col_num - 1], dtype = object)  # rows, columns
# dataSet[:, 0] = listOfFNames
# dataSet[:, 0] = listOfAttributes
# dataSet[] = tumorType

# import .tsv file as panda data frame for manipulation
tsv_df = pd.read_csv(pathName + "/PAT00010/eFlair.tsv", index_col=0, parse_dates=True, sep=',', header=0)
excel_df = pd.read_excel(pathName + '/SliceData.xls', sheet_name = 'Sheet2', header = 0)


# find total # of rows in .tsv file ie: number of attributes
total_rows = tsv_df.shape[0]

# not in while loop as we only want to do this once at the beginning
info_entries = tsv_df['Feature Name'].tolist()
attributes = np.array(info_entries)
dataSet = np.insert(dataSet, 0, attributes, axis = 1)

# create a list of patient names, there should be 256 entries of each name
count = 0
pat = 0
i = 1
patNum = np.empty([1, col_num], dtype = object)
current = listOfPAT[0]
patNum[0, 0] = ''
while i < col_num:
    patNum[0, i] = current
    if count == 256:
        count = 0
        pat = pat + 1
        if pat < total_pats:
            current = listOfPAT[pat]
    i = i + 1
    count = count + 1
dataSet = np.insert(dataSet, 0, patNum, axis = 0)

# create a list of tumor types, 256 entries for each patient then add tumorType row to dataSet matrix
tumor_Type = excel_df['Type'].tolist()
tumorType = np.empty([1, col_num], dtype = object)
i = 1
# noinspection PyRedeclaration
count = 0
tumor = 0
current = tumor_Type[0]
tumorType[0, 0] = ''
while i < col_num:
    tumorType[0, i] = current
    if count == 256:
        count = 0
        tumor = tumor + 1
        if tumor < total_pats:
            current = tumor_Type[tumor]
    i = i + 1
    count = count + 1
dataSet = np.insert(dataSet, 1, tumorType, axis = 0)

k = 0
while k < listLength:
    patientNum = fileMatrix[k, 0]
    fileName = fileMatrix[k, 1]

    # generate locations for input and output files
    location = pathName + "/" + patientNum + "/" + fileName + ".tsv"

    # import .tsv file as panda data frame for manipulation
    df = pd.read_csv(location, index_col= 0, parse_dates=True, sep=',', header=0)

    k = k + 1
# set headers for first two rows
dataSet[0, 0] = 'Patient Number'
dataSet[1, 0] = 'Tumor Type'  # 0:Medulloblastoma, 1: Pilocytic Astrocytoma, 2: Ependymoma

print("Done!")
