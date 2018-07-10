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
    dirs[:] = [d for d in dirs if d.startswith('PAT')]  # only look in folders that start with PAT?
    listOfFiles += [os.path.join(root, file) for file in files]  # not really needed, redundant to be removed later
    listOfFNames += files  # create list of .tsv files from all PAT folders
    listOfPAT += dirs  # incorrect, only gives one instance each instead of listing the folder name for each file

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

# make a matrix combining listOfFiles and listOfPAT, column 0 = patient number, column 1 = file name
fileMatrix = np.column_stack((listOfFiles, listOfFNames))

excel_df = pd.read_excel(pathName + '/SliceData.xls', sheet_name='Sheet2', header=0)

slices = excel_df['Slice_Num'].tolist()
x = 0
for sliceNumber in slices:
    slices[x] = pow(4, sliceNumber)
    x = x + 1
col_num = sum(slices)
total_pats = len(listOfPAT)
dataSet = np.empty([841, col_num], dtype=object)
# dataSetTest = pd.DataFrame(data=dataSet)  # rows, columns
# dataSet[:, 0] = listOfFNames
# dataSet[:, 0] = listOfAttributes
# dataSet[] = tumorType

# import .tsv file as panda data frame for manipulation
# need to automate & move to later in the code **make sure to leave one to use for early calculations
tsv_df = pd.read_csv(pathName + "/PAT00010/eFlair.tsv", index_col=0, parse_dates=True, sep=',', header=0)
# tsvADC = pd.read_csv(pathName + "/PAT00010/eADC.tsv", index_col=0, parse_dates=True, sep=',', header=0)

# find total # of rows in .tsv file ie: number of attributes, repeats per slice so only grab the first instance?
total_rows = tsv_df.shape[0]

# set attribute names to first column
# not in while loop as we only want to do this once at the beginning
info_entries = tsv_df['Feature Name'].tolist()
info_entries = info_entries[0:841]
attributes = np.array(info_entries)
# trim attributes to the first instance (ie: 841)
# pd.cut(attributes, bins = )  # not working atm
dataSet = np.insert(dataSet, 0, attributes, axis=1)


# create a list of patient names, there should be 256 entries of each name and set to first row of dataSet
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
# noinspection PyRedeclaration
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
dataSet[1, 0] = 'Tumor Type'  # 0:Medulloblastoma, 1: Pilocytic Astrocytoma, 2: Ependymoma

patient_Num = 0  # count number of patients completed
while patient_Num < numberOfPatientsTotal:
    patientNum = listOfPAT[patient_Num]
    # generate locations for input file
    location = pathName + "/" + patientNum

    # import .tsv file as panda data frame for manipulation
    tsvFlair_df = pd.read_csv(location + "/eFlair.tsv", index_col=0, parse_dates=True, sep=',', header=0)
    tsvT1_df = pd.read_csv(location + "/eT1.tsv", index_col=0, parse_dates=True, sep=',', header=0)
    tsvT2_df = pd.read_csv(location + "/eT2.tsv", index_col=0, parse_dates=True, sep=',', header=0)
    tsvDWI_df = pd.read_csv(location + "/eDWI.tsv", index_col=0, parse_dates=True, sep=',', header=0)

    # determine number of slices for each patient
    slice_num = 0

    # use pandas to find 293-296, if exists add 1 to slice_num: MAX = 4, MIN = 1
    # change to ADC in the future
    x = '201: F AX T2-label_label_293' in tsvT2_df.index
    y = '201: F AX T2-label_label_294' in tsvT2_df.index
    z = '201: F AX T2-label_label_295' in tsvT2_df.index
    w = '201: F AX T2-label_label_296' in tsvT2_df.index
    if x:
        slice_num = slice_num + 1
    if y:
        slice_num = slice_num + 1
    if z:
        slice_num = slice_num + 1
    if w:
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
    valuesADC = tsvDWI_df['Value']  # change to ADC later, currently using DWI files in the test folder

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
                        # walk through ADC
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
                            if column > (column_num - 1):
                                i = slice_num
                                j = slice_num
                                k = slice_num
                                m = slice_num
                        m = 0
                    k = 0
                j = 0
            i = 0
        column = 0
        row = row + 1
    patient_Num = patient_Num + 1
print("Done!")
# save df as a tsv file? **dataset is not a dataframe atm, fix that
# pd.read_csv(location + "/eFlair.tsv", index_col=0, parse_dates=True, sep=',', header=0)
dt = pd.DataFrame(dataSet)
pd.DataFrame.to_csv(dt, pathName + '/dataSet.tsv', sep=',', header = False)
# np.savetxt('dataSet.tsv', dataSet, delimiter=',')
