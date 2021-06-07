import sys, getopt
import os
import re
import csv
from pathlib import Path

from bidentify.update import BIdentifyUpdateCommand

from biucommands.findinlist import findinlist







class BIdentifyAnalyzeCommand:

    def __init__(self, config):
        self.config = config
        self.optionDirectory = None
        self.optionVerbose = False
        self.tricks = []    # creates a new empty list for each dog


    def setDirectory(self,dir):
        self.optionDirectory=dir

    def setVerbosity(self,verbose):
        #print('(BIdentifyScanCommand) setVerbosity: '+str(verbose))
        self.optionVerbose = verbose

    def showUsage(self):
        #print("BI Universe - the definitive tool for identifying Arma-files")
        print("Usage:")
        print(" "+sys.argv[0]+" analyze [-h --help] [-d --directory] [-i --input]")

    def analyzeDir(self):
        #
        print("analyzeDir")
        self.analyzeStart(self.optionDirectory,self.optionVerbose)

    def doUpdate(self):
        # update
        UpdateCommand = BIdentifyUpdateCommand(self.config)
        UpdateCommand.setVerbosity(self.optionVerbose)
        UpdateCommand.update()

    def analyzeStart(self,directory,verbose):
        # setx path "D:\#BiUniverse_git\biuniverse;%path%;"
        # pathman /au D:\#BiUniverse_git\biuniverse
        #global output
        #print(output)

        output="fileList"

        if verbose: print("Using input files: ")
        if verbose: print(" "+output+".bifl")
        if verbose: print(" "+output+".bidl")


        print("Analyzing... "+directory )
        print("------------------------------")

        #os.chdir(os.path.dirname(__file__))
        #print(CURRENT_DIR)

        extensions = [".zip",".exe",".gz",".rar",".7z"]

        gamename = ["ofp","arma","arma2","arma2oa","arma2_oa","arma3"]


        # check if bidentify lists are available.
        home = self.config.get("LOCALAPPDATA")

        NeedsUpdate = False
        if os.path.exists(home+"/ofp.bidb") != True:
            # update needed
            NeedsUpdate = True
        if os.path.exists(home+"/arma.bidb") != True:
            #
            NeedsUpdate = True
        if os.path.exists(home+"/arma2.bidb") != True:
            #
            NeedsUpdate = True
        if os.path.exists(home+"/arma2_oa.bidb") != True:
            #
            NeedsUpdate = True

        if NeedsUpdate == True:
            self.doUpdate()

        results = self.analyzeFiles(output)
        #print(results)
        self.writeAnalyzeResults(results)
        #analyzeDir(output)


    def analyzeFiles(self,name):
        #
        results = []
        # Open the bidentify file-list ()
        with open(name+'.bifl', encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                #print(row['exactName'], row['fileSize'], row['filePath'], row['fileName'], row['fileExtension'])
                # Attempt to find the record in the bidentify-database.
                foundFiles=findinlist(row['exactName'])
                for foundFile in foundFiles:
                    #print (row)
                    if len(foundFile) != 0:
                        test = {'localFile': row, 'foundFiles':foundFiles }
                        results.append(test)
        return results
        return results
    #print(results)

    def writeAnalyzeResults(self,results):

        csvFile = open('found.txt', 'w', encoding='utf8')
        FileListWriterFieldNames = ['localFile']
        FileListWriter = csv.DictWriter(csvFile, fieldnames=FileListWriterFieldNames)
        FileListWriter.writeheader()

        print('The following files matched the bidentify lists')
        for line in results:
            print(line['localFile']['filePath']+"\\"+line['localFile']['exactName'])
            #print(line['localFile']['filePath'])
            #line['exists']
            FileListWriter.writerow({'localFile': line['localFile']['filePath']+"\\"+line['localFile']['exactName'] })




    def analyzeDir(self,directory):
        a=1
        self.analyzeStart(directory,self.optionVerbose)
        #
        #with open(name+'.bidl', encoding='utf8') as csvfile:
        #    reader = csv.DictReader(csvfile)
        #    for row in reader:
        #        print(row['exactName'], row['filePath'])











