# Program to remove info category from data spreadsheets

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import os

#make sure that the Drobo is mounted and findable
os.getcwd()
print(os.path.exists("/Volumes/Public/PosteriorFossaTumors/PAT00010"))

#with open("/Volumes/Public/PosteriorFossaTumors/PAT00010/T1.tsv") as tsvfile:
    #reader = csv.DictReader(tsvfile, dialect='excel-tab')

#import .tsv file as panda dataframe for manipulation
df = pd.DataFrame.from_csv("/Volumes/Public/PosteriorFossaTumors/PAT00010/T1.tsv", sep='\t', header=0)


#find all entries with Feature Class: info
info_entries = df[df['Feature Class'] == 'info']

#remove all entries with Feature Class: info
editdf = df[df['Feature Class'] != 'info']
#print(editdf[:])


#Save edited data frame to a new tsv file--ends up comma delinated, ok?
editdf.to_csv('/Volumes/Public/PosteriorFossaTumors/PAT00010/T1e.tsv')

