#!/usr/bin/env python
# a bar plot with errorbars
import numpy as np
import matplotlib.pyplot as plt
import os, re, time
from datetime import datetime

#global variables
homeDir = "/home/nathan/gmail-archive/"
homeDirList = list()
listOfMatchingFiles = list()

#initialize needed modules
os.system("getmail -r /home/nathan/.getmail/getmailrc")

#This allows us to recursively search our "home" directory. Places all possible audio file paths in homeDirList.
def getAllHomeFolder(x, dir_name, files): 
    for item in files:
	fullPath = dir_name + "/" + item
        if (os.path.isdir(fullPath)):
            pass
	else:
            homeDirList.append(fullPath)
os.path.walk(homeDir, getAllHomeFolder, 0)

#get user input
search = raw_input("Enter search term: ")
search_term = re.compile(search)

#This searches our list of email files for the expression which the user entered
for entry in homeDirList:
    #variables needed to handle every file
    date = re.compile("Date: ")
    fileList = list()
    dateFound = False

    #open file
    fileObject = open(entry, "r")

    #search every line in the file 
    for line in fileObject:
        #Finds first line in the file containing date
        if(date.findall(line) and dateFound == False):
            subline = line[6:31]
            if (subline[6]==" "):
                subline = subline[0:24]
            #timeValue = time.strptime(subline, '%a, %d %b %Y %H:%M:%S')
            date_object = datetime.strptime(subline, '%a, %d %b %Y %H:%M:%S')
            fileList.append(date_object)
            dateFound = True

        #logs file name and date if the search term is found
        if (search_term.findall(line)):
            fileList.append(entry)
            listOfMatchingFiles.append(fileList)
            break

for entry in listOfMatchingFiles:
    for item in entry:
        print item
    
def barGraph(title):
    N = 5
    menMeans = (20, 35, 30, 35, 27)
    menStd =   (2, 3, 4, 1, 2)

    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, menMeans, width, color='r', yerr=menStd)

    womenMeans = (25, 32, 34, 20, 25)
    womenStd =   (3, 5, 2, 3, 3)
    rects2 = ax.bar(ind+width, womenMeans, width, color='y', yerr=womenStd)

    # add some
    ax.set_ylabel('Scores')
    ax.set_title(title)
    ax.set_xticks(ind+width)
    ax.set_xticklabels( ('G1', 'G2', 'G3', 'G4', 'G5') )

    ax.legend( (rects1[0], rects2[0]), ('Men', 'Women') )

    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                    ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    plt.show()

barGraph("Frequency of Search Term")
