import re
import os
import pprint

class pboPrefix :

    def __init__(self, fileLocation ,verbose = False ):
        # set verbosity
        self.optionVerbose = verbose
        self.optionVerbose : print("(matching\pboPrefix) init()")

        # open file.
        #f = open(os.path.abspath(fileLocation), "r") # ,encoding='utf-8'
        #self.textString = f.read()
        #f.close()
        f = open(fileLocation, "r")
        #return f.read()
        self.Lines = f.readlines()
        f.close()

        #########################################
        # Object definition
        #########################################
        self.prefixObject = {}
        self.prefixObject['version'] = None
        self.prefixObject['addons'] = None
        self.prefixObject['intel'] = None
        #########################################

        self.matchPboPrefix()

    def getAll(self):
        return self.prefixObject


    def matchPboPrefix(self):
        if self.optionVerbose : print("(pboPrefix) matchPboPrefix")
        lijstje = []
        prefix = False
        for line in self.Lines:
            cleanLine = line.strip()
            if cleanLine[:6] == "prefix":
                if self.optionVerbose : print("found prefix")
                #config['prefix']=cleanLine.split("=")[1]
                #lijstje['prefix']=cleanLine.split("=")[1]
                prefix = cleanLine.split("=")[1]

                #lijstje.append(line.strip())
        if prefix is not False : return prefix
        return lijstje
