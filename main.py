#!/usr/bin/env python
#Program to graph frequency of a term in user's email over time
#Requires getmail utility
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import matplotlib.transforms as mtransforms
import matplotlib.text as mtext
import os, re, time
from datetime import datetime
from datetime import timedelta

#global variables
homeDir = "/home/nathan/gmail-archive/"
homeDirList = list() #contains our set of email to search
listOfMatchingFiles = list() #contains emails that match our query
listOfXValues = list() #assigns number for each quarter
listOfXValuesAsDate = list() #contains list of three month intervals within date range
listOfYValues = list() #contains frequency of term with each index containing the frequency of one quarter
listOfFileDates = list() #contains list of dates, corrosponds to list of matching files

#initialize needed modules
os.system("getmail -r /home/nathan/.getmail/getmailrc")

#This allows us to recursively search our "home" directory. Places all possible email message file paths in homeDirList.
def getAllHomeFolder(x, dir_name, files): 
    for item in files:
	fullPath = dir_name + "/" + item
        if (os.path.isdir(fullPath)):
            pass
	else:
            homeDirList.append(fullPath)
os.path.walk(homeDir, getAllHomeFolder, 0)

def graphBySearchTerm():
    #initialize needed members
    start = ""
    end = ""
    interval = ""
    dateRE = re.compile(r'([0-9]*) ([A-z]{3}) ([0-9]{4})')
    date = re.compile("Date: ")

    #get user input
    search = raw_input("Enter search term: ")
    search_term = re.compile(search)
    while (not re.match(dateRE, start)):
        start = raw_input("Enter start date: (Ex. 2 Feb 2012)")
    start_date = datetime.strptime(start, '%d %b %Y')
    while (not re.match(dateRE, end)):
        end = raw_input("Enter end date: ")
    end_date = datetime.strptime(end, '%d %b %Y')
    while (not re.search(r'[MmQq]', interval)):
        interval = raw_input("Graph by quarter (Q) or month (M)?")
    
    #set interval
    if (re.search(r'[Qq]', interval)):
        interval = "Q"
        #get list of x values (every 3 months within range of start and end dates)
        three_months = timedelta(91, 26827, 2)
        while (start_date < end_date):
            listOfXValuesAsDate.append(start_date)
            start_date = start_date + three_months
        listOfXValuesAsDate.append(end_date)
    else:
        interval = "M"
        #get list of x values (every month within range of start and end dates)
        one_month = timedelta(30, 37739, 520000)
        while (start_date < end_date):
            listOfXValuesAsDate.append(start_date)
            start_date = start_date + one_month
        listOfXValuesAsDate.append(end_date)

    #This searches our list of email files for the expression which the user entered
    for entry in homeDirList:
        #variables needed to handle every file 
        dateFound = False
        date_object = None
        this_file_array = list()

        #open file
        fileObject = open(entry, "r")

        #search every line in the file 
        for line in fileObject:
            #Finds first line in the file containing date
            if(date.findall(line) and dateFound == False):
                subline = line[6:31]#this grabs the formatted date out of the line
                if (subline[6]==" "):#this handles case where day of the month is only one digit
                    subline = subline[0:24]
                date_object = datetime.strptime(subline, '%a, %d %b %Y %H:%M:%S')
                dateFound = True

            #logs file name and date if the search term is found
            if (search_term.findall(line)):
                listOfFileDates.append(date_object)
                this_file_array.append(date_object)
                this_file_array.append(entry)
                listOfMatchingFiles.append(this_file_array)
                break
        fileObject.close()
    
    #initialize plot values
    for x in xrange(len(listOfXValuesAsDate)-1):
        listOfYValues.append(0)
        listOfXValues.append(x)
   
    
    #Check dates of each file, check which date range they fit into, and add a +1 for frequency of term (our Y value)
    for x in xrange(len(listOfFileDates)-1):
        for y in xrange(len(listOfXValuesAsDate)-1):
            if (listOfFileDates[x] >= listOfXValuesAsDate[y] and listOfFileDates[x] < listOfXValuesAsDate[y+1]):
                listOfYValues[y] = listOfYValues[y]+1
                

    #This is just used to make sure we have the correct output
    for entry in listOfXValues:
        print entry
    for entry in listOfYValues:
        print entry
    for entry in listOfMatchingFiles:
        for item in entry:
            print item
    
    return interval

#Contains main program loop. New modules can be added here.
def main():
    loop = True
    while (loop == True):
        timeInterval = graphBySearchTerm()
    
        plt.plot(listOfXValues, listOfYValues)
    
        plt.xlabel('Time')
        plt.ylabel('Frequency')

        if (timeInterval == "Q"):
            plt.title('Search Term Frequency By Quarter')
        else:
            plt.title('Search Term Frequency By Month')

        plt.show()

        loopCmd = raw_input("Run again? (Y/N) ")
        if (re.match(r'[Yy]', loopCmd)):
            loop = True
        else:
            loop = False

#Execute
main()

