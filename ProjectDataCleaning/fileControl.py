import os
import csv
import random

# Finds full path of a given file in a given folder, was having trouble with it not reading the correct path, ended up with a slightly different method than I normally use.
# I might rewrite this, I am unsure if it is better like this or not
def selectFile(folders,fileName):
   folderPath = format(os.getcwd())
   for folder in folders:
      folderPath = os.path.join(folderPath,folder)
   filePath = os.path.join(folderPath,fileName)
   return filePath


# Opens and reads a given file, so that the data can be manipulated
def readFile(filePath,delim):
   with open(filePath, "r") as csvFile:
        csvReader = csv.reader(csvFile,delimiter = delim)
        fileLines = list(csvReader)
        csvFile.close()
        return fileLines


# Writes new lines to the correct file
def writeFile(filePath,fileLines):
   with open(filePath, "w", newline = "") as csvFile:
        csvWriter = csv.writer(csvFile,delimiter = ",")
        csvWriter.writerows(fileLines)
        csvFile.close()




