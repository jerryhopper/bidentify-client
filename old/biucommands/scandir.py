import sys, getopt
import os
import re
import csv
from bidentify.hashfile import hashfile








class BIdentifyScanCommand:

    def __init__(self, config):
        self.config = config
        self.optionDirectory = None
        self.optionVerbose = False


    def setDirectory(self,dir):
        self.optionDirectory=dir

    def setVerbosity(self,verbose):
        #print('(BIdentifyScanCommand) setVerbosity: '+str(verbose))
        self.optionVerbose = verbose

    def showUsage(self):
        #
        print("Usage:")
        print(" "+self.config.get('EXENAME')+" scan [-d --directory= ] [-h --help] [-v]")


    def scandir(self):
        print("- scandir ")
        #self.scandirStart(self.optionDirectory)


    def scandirStart(self,directory):
        # setx path "D:\#BiUniverse_git\biuniverse;%path%;"
        # pathman /au D:\#BiUniverse_git\biuniverse
        #global output
        #print(output)


        if self.optionVerbose : print()
        print("Scanning... "+directory)
        print("------------------------------")
        print(os.getcwd() )



        csvFile = open(os.path.join(directory,'fileList.bifl'), 'w', encoding='utf8')
        FileListWriterFieldNames = ['exactName', 'fileSize','filePath','fileName','fileExtension']
        FileListWriter = csv.DictWriter(csvFile, fieldnames=FileListWriterFieldNames)
        FileListWriter.writeheader()

        csvFile = open('fileList.bidl', 'w', encoding='utf8')
        DirListWriterFieldNames = ['exactName','filePath']
        DirListWriter = csv.DictWriter(csvFile, fieldnames=DirListWriterFieldNames)
        DirListWriter.writeheader()

        extensions = [".zip",".exe",".gz",".rar",".7z"]


        os.chdir(directory)
        for root, dirs, files in os.walk(".", topdown = False):
           for name in files:
               if os.path.splitext(name)[1].lower() in extensions :
                   exactName=name
                   filePath=root
                   fileName=os.path.splitext(name)[0]
                   #fileHash=hashfile(os.path.join(root, name))
                   fileSize=str(os.path.getsize(os.path.join(root, name)))
                   fileExtension=os.path.splitext(name)[1].lower()
                   #print( exactName+","+str(fileSize)+","+root+","+fileName+","+fileExtension )
                   FileListWriter.writerow({'exactName': exactName, 'fileSize': fileSize,'filePath': filePath, 'fileName': fileName, 'fileExtension': fileExtension})
               #print(os.path.join(root, name))

           for name in dirs:
               filePath=root
               exactName=name
               #print( exactName+","+filePath )
               #print(os.path.join(root, name))
               DirListWriter.writerow({'exactName': exactName,'filePath': filePath})
        #
        #print("------------------------------")
        #if self.optionVerbose : print("output written to: ")
        #if self.optionVerbose : print("fileList.bifl")
        #if self.optionVerbose : print("fileList.bidl")
        print("Scanning complete, index created.")
