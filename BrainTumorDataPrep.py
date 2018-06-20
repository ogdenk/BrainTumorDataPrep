# Program to autopopulate matrix of data spreadsheets and identify data with seperate key matrix

import os

# make sure that the Drobo is mounted and findable
os.getcwd()
print(os.path.exists("/Volumes/Public/PosteriorFossaTumors"))

# display all folders in Posterior Fossa Tumors

for root, name, dirs in os.walk("/Volumes/Public/PosteriorFossaTumors", topdown=True):
    print(root, name)
