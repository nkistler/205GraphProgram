#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import matplotlib.transforms as mtransforms
import matplotlib.text as mtext
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

#Defines line graph
class MyLine(lines.Line2D):
   def __init__(self, *args, **kwargs):
      # we'll update the position when the line data is set
      self.text = mtext.Text(0, 0, '')
      lines.Line2D.__init__(self, *args, **kwargs)

      # we can't access the label attr until *after* the line is initialized
      self.text.set_text(self.get_label())

   def set_figure(self, figure):
      self.text.set_figure(figure)
      lines.Line2D.set_figure(self, figure)

   def set_axes(self, axes):
      self.text.set_axes(axes)
      lines.Line2D.set_axes(self, axes)

   def set_transform(self, transform):
      # 2 pixel offset
      texttrans = transform + mtransforms.Affine2D().translate(2, 2)
      self.text.set_transform(texttrans)
      lines.Line2D.set_transform(self, transform)


   def set_data(self, x, y):
      if len(x):
         self.text.set_position((x[-1], y[-1]))

      lines.Line2D.set_data(self, x, y)

   def draw(self, renderer):
      # draw my label at the end of the line with 2 pixel offset
      lines.Line2D.draw(self, renderer)
      self.text.draw(renderer)

def graphBySearchTerm():
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

def main():

    fig, ax = plt.subplots()
    x, y = ([0,1,2], [0,1,2])
    line = MyLine(x, y)
    #line.text.set_text('line label')

    ax.set_title('Frequency of Search Term Over Time')
    ax.add_line(line)

    plt.show()

main()
