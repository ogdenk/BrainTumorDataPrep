# Program to add image data to a matrix for use in machine learning

import os
import numpy as np
import pandas as pd
import skimage
import pydicom

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

# use os.walk() to walk through directory and grab files that we're interested in
for root, dirs, files in os.walk(pathName, topdown=True):
    files = [file for file in files if file.endswith('.dcm')]  # only grab .dcm files (all we need)
    dirs[:] = [d for d in dirs if d.startswith('PAT')]  # only look in folders that start with PAT
    listOfFiles += [os.path.join(root, file) for file in files]
    listOfPAT += dirs  # only gives one instance each instead of listing the folder name for each file
    fileName += files
print(listOfFiles, listOfPAT, files)
