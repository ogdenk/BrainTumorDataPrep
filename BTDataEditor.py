# Program to remove info category from data spreadsheets

import pandas as pd
import csv

with open("X:/PosteriorFossaTumors/PAT00010/T1.tsv") as tsvfile:
    reader = cv.DictReader(tsvfile, dialect='excel-tab')
    for row in reader:
        print(row)
