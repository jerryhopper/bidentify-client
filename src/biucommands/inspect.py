import sys, getopt
import os
import os.path
import re
import rarfile
import csv
import shutil
from pyunpack import Archive
import pprint

from biucommands.hashfile import hashfile
from biucommands.findinlist import findinlist

from biucommands.inspect_pbo import InspectPbo
from biucommands.inspect_archive import InspectArchive

from bidentify.fileobject import myFileObject

import subprocess
import sys


import io
import sys
import builtins
import traceback
from functools import wraps



class BIdentifyInspectCommand:

    def __init__(self, config):
        self.config = config
        self.optionDirectory = None
        self.optionFile = None

        self.optionVerbose = False
        self.tricks = []    # creates a new empty list for each dog

    def setSelectedFile(self,file):
        self.optionFile=file

    def setDirectory(self,dir):
        self.optionDirectory=dir

    def setVerbosity(self,verbose):
        print('(BIdentifyInspectCommand) setVerbosity: '+str(verbose))
        self.optionVerbose = verbose

    def showUsage(self):
        print("Usage:")
        print(" "+sys.argv[0]+" inspect [-f --file] [-h --help]")


    def inspect(self):
        print("(BIdentifyInspectCommand) inspect")
        print("-----------------------------------------------------")
        print("| Directory: "+ str(self.optionDirectory))
        print("| File: "+ str(self.optionFile))
        print("-----------------------------------------------------")

        if os.path.isdir(self.optionFile) :
            print('find scanresults. and scan them.')
            sys.exit()


        extensions = [".zip",".exe",".gz",".rar",".7z"]
        fileExtension = os.path.splitext(self.optionFile)[1].lower()
        # check if the file is a pbo.
        if fileExtension == ".pbo":
            result = self.inspectPbo(self.optionFile)
            print("--------------------")
            pprint.pprint(result)
            print("(BIdentifyInspectCommand) inspect FINISHED")
            sys.exit()
        # check if the file is a accepted archive.
        if fileExtension in extensions:
            result = self.inspectArchive( self.optionFile )
            print("--------------------")
            pprint.pprint(result)
            print("(BIdentifyInspectCommand) inspect FINISHED")
            sys.exit()



    def inspectArchive(self, thefile):
        print("(BIdentifyInspectCommand) inspectArchive()")
        fullpath = os.path.abspath(thefile)
        fileObject = myFileObject(fullpath)
        #print("(BIdentifyInspectCommand) inspectArchive(*) ")

        archive = InspectArchive(fileObject, self.optionDirectory )
        #print("(BIdentifyInspectCommand) inspectArchive() archive.list()")

        tempDir = archive.list()

        ArchiveInformation =  archive.get()
        #sys.exit()

        path_parent = os. path. dirname(os. getcwd())
        os. chdir(path_parent)

        if os.path.exists(tempDir):
            shutil.rmtree(tempDir)
        #archive.extract()
        return ArchiveInformation.getAll()


    def inspectPbo(self, thefile):
        print("(BIdentifyInspectCommand) inspectPbo("+thefile+")")
        if os.path.isfile(thefile):
            if self.optionVerbose : print( "inspecting "+thefile)
        else:
            print ("(inspectPbo) ERROR! File not exist (" +thefile+ ")")
            sys.exit()
        print("Current dir: ", os.getcwdb() )
        fullpath = os.path.abspath(thefile)
        fileExtension = os.path.splitext(thefile)[1].lower()

        if fileExtension == ".pbo" :
            if self.optionVerbose : print('Extension is allowed.')
        else:
            print("Not a .pbo!")
            sys.exit()

        fileObject = myFileObject(fullpath)

        #fileObject.print()
        print("(BIdentifyInspectCommand) FINISHED inspectPbo()")
        #sys.exit()
        return fileObject.getAll()
        #sys.exit()









def showUsage():
    #print("BI Universe - the definitive tool for identifying Arma-files")
    print("Usage:")
    print(" "+sys.argv[0]+" inspect [-i inputfilename] [-h --help]")


#def detectType(fileName):



def inspect():


    inspectStart()


def rar(fileLocation):
    rf = rarfile.RarFile(fileLocation)
    for f in rf.infolist():
        print(f.filename, f.file_size)
        if f.filename == "README":
            print(rf.read(f))










