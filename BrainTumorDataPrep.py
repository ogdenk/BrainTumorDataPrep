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
for root, dirs, files in os.walk(pathName, topdown=True):
    files = [file for file in files if file.endswith('.tsv')]  # only grab .tsv files (all we need)
    files = [file for file in files if file.startswith('e')]  # only grab edited files
    dirs[:] = [d for d in dirs if d.startswith('PAT')]  # only look in folders that start with PAT
    listOfFiles += [os.path.join(root, file) for file in files]
    listOfFNames += files  # create list of .tsv files from all PAT folders
    listOfPAT += dirs  # only gives one instance each instead of listing the folder name for each file

# remove pathName and 'filename from root list
j = 0
listLength = len(listOfFiles)
numberOfPatientsTotal = len(listOfPAT)
while j < listLength:
    listOfFiles[j] = listOfFiles[j].replace(pathName + '/', '')
    listOfFiles[j] = listOfFiles[j][0:8]  # remove the file name by keeping only the first 8 char
    j = j + 1
i = 0
while i < listLength:
    listOfFNames[i] = listOfFNames[i].replace('.tsv', '')
    i = i + 1

# sort list into alphabetical order to ensure correct assignment of tumor type and data
listOfPAT.sort()
# read in the excel file containing patient #, tumor type, and number of slices
# the excel file has been edited to just include relevant data, this is located on sheet 2
excel_df = pd.read_excel(pathName + '/SliceData.xls', sheet_name='Sheet2', header=0)

# use slice number to determine number of columns ie the number of augmented data sets, 4 slices = 256 etc
slices = excel_df['Slice_Num'].tolist()
x = 0
for sliceNumber in slices:
    slices[x] = pow(4, sliceNumber)
    x = x + 1
col_num = sum(slices)
total_pats = len(listOfPAT)
# there are 841 different attributes calculated by slicer that we are interested in
# use dtype object to ensure there are no errors including both string and float data
dataSet = np.empty([841, col_num], dtype=object)

# import .tsv file as panda data frame for manipulation, use one as a template to generate attribute list
tsv_df = pd.read_csv(pathName + "/PAT00010/eFlair.tsv", index_col=0, parse_dates=True, sep=',', header=0)

# find total # of rows in .tsv file ie: number of attributes, repeats per slice so only grab the first instance?
total_rows = tsv_df.shape[0]

# set attribute names to first column
# not in while loop as we only want to do this once at the beginning
info_entries = tsv_df['Feature Name'].tolist()
info_entries = info_entries[0:841]
attributes = np.array(info_entries)
# trim attributes to the first instance (ie: 841)
dataSet = np.insert(dataSet, 0, attributes, axis=1)

# create a list of patient names, there should be approx 256 entries of each name and set to first row of dataSet
# number of name repeats will depend on number of slices
count = 0
pat = 0
i = 1
patNum = np.empty([1, col_num + 1], dtype=object)
current = listOfPAT[0]
patNum[0, 0] = ''
while i <= col_num:
    patNum[0, i] = current
    if count == slices[pat]:
        count = 0
        pat = pat + 1
        if pat < total_pats:
            current = listOfPAT[pat]
    i = i + 1
    count = count + 1
dataSet = np.insert(dataSet, 0, patNum, axis=0)

# create a list of tumor types, 256 entries for each patient then add tumorType row to dataSet matrix
tumor_Type = excel_df['Type'].tolist()
tumorType = np.empty([1, col_num + 1], dtype=object)
i = 1

count = 0
tumor = 0
current = tumor_Type[0]
tumorType[0, 0] = ''
while i <= col_num:
    tumorType[0, i] = current
    if count == slices[tumor]:
        count = 0
        tumor = tumor + 1
        if tumor < total_pats:
            current = tumor_Type[tumor]
    i = i + 1
    count = count + 1
dataSet = np.insert(dataSet, 1, tumorType, axis=0)

# set headers for first two rows
dataSet[0, 0] = 'Patient Number'
dataSet[1, 0] = 'Tumor Type'  # 0: Medulloblastoma, 1: Pilocytic Astrocytoma, 2: Ependymoma

patient_Num = 0  # count number of patients completed
while patient_Num < numberOfPatientsTotal:
    patientNum = listOfPAT[patient_Num]
    # generate locations for input file
    location = pathName + "/" + patientNum

    # import .tsv file as panda data frame for manipulation
    if os.path.exists(location + "/eFlair.tsv") is True:
        tsvFlair_df = pd.read_csv(location + "/eFlair.tsv", index_col=0, parse_dates=True, sep=',', header=0)
    if os.path.exists(location + "/eT1.tsv") is True:
        tsvT1_df = pd.read_csv(location + "/eT1.tsv", index_col=0, parse_dates=True, sep=',', header=0)
    if os.path.exists(location + "/eT2.tsv") is True:
        tsvT2_df = pd.read_csv(location + "/eT2.tsv", index_col=0, parse_dates=True, sep=',', header=0)
    if os.path.exists(location + "/eDWI.tsv") is True:
        tsvADC_df = pd.read_csv(location + "/eDWI.tsv", index_col=0, parse_dates=True, sep=',', header=0)
    if os.path.exists(location + "/eADC.tsv") is True:
        tsvADC_df = pd.read_csv(location + "/eADC.tsv", index_col=0, parse_dates=True, sep=',', header=0)

    # determine number of slices for each patient
    slice_num = 0  # initialize
    # use pandas to find 293-296, if exists add 1 to slice_num: MAX = 4, MIN = 1
    if tsvT1_df.index.str.contains('293').any():  # check the index of T1df to see if it contains the slice #s anywhere
        slice_num = slice_num + 1
    if tsvT1_df.index.str.contains('294').any():
        slice_num = slice_num + 1
    if tsvT1_df.index.str.contains('295').any():
        slice_num = slice_num + 1
    if tsvT1_df.index.str.contains('296').any():
        slice_num = slice_num + 1

    # create data augmentation vectors
    i = 0
    j = 0
    k = 0
    m = 0
    row = 0
    column = 0
    T1_value = 0
    T2_value = 0
    Flair_value = 0
    ADC_value = 0
    valueVector = [] * 4  # initialize a vector that will hold 4 values
    column_num = pow(4, slice_num)
    tempArray = np.empty([841, column_num], dtype=object)  # 841 = number of attributes

    # iterate through the rows
    valuesT1 = tsvT1_df['Value']
    valuesT2 = tsvT2_df['Value']
    valuesFlair = tsvFlair_df['Value']
    valuesADC = tsvADC_df['Value']  # may be DWI, ADC is being used as a catchall for both for simplicity's sake

    # create augmented data by stepping through the slices, start by iterating through ADC then work backwards
    # ie: [1,1,1,1],[1,1,1,2],[1,1,1,3],[1,1,1,4],[1,1,2,1],[1,1,2,2] ... [4,4,4,1], [4,4,4,2], [4,4,4,3], [4,4,4,4]
    while row < 841:
        # iterate through the columns
        while column < column_num:
            # walk through T1
            while i < slice_num:
                index = i * 841 + row
                T1_value = valuesT1.iloc[index]
                i = i + 1
                # walk through T2
                while j < slice_num:
                    index = j * 841 + row
                    T2_value = valuesT2.iloc[index]
                    j = j + 1
                    # walk through Flair
                    while k < slice_num:
                        index = k * 841 + row
                        Flair_value = valuesFlair.iloc[index]
                        k = k + 1
                        # walk through ADC (or DWI listed as ADC for convenience)
                        while m < slice_num:
                            index = m * 841 + row
                            ADC_value = valuesADC.iloc[index]
                            m = m + 1
                            valueVector = [T1_value, T2_value, Flair_value, ADC_value]
                            tempArray[row, column] = valueVector
                            dataColumn = column + 1 + patient_Num * pow(4, slice_num)
                            dataSet[2 + row, dataColumn] = valueVector
                            if column < column_num:
                                column = column + 1
                            if column > (column_num - 1):  # iterate to next row?
                                i = slice_num
                                j = slice_num
                                k = slice_num
                                m = slice_num
                        m = 0
                    k = 0
                j = 0
            i = 0
        column = 0
        row = row + 1  # move to next attribute
    patient_Num = patient_Num + 1  # move to next patient and start the process over
print("Done!")  # check that while loop has completed for testing purposes
# convert numpy array to a data frame and then save df as a tsv file
dt = pd.DataFrame(dataSet)
pd.DataFrame.to_csv(dt, pathName + '/dataSet.tsv', sep=',', header = False, index = False)
