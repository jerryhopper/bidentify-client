import sys, getopt
import os
import re
import csv
import urllib.request
from pathlib import Path



class BIdentifyUpdateCommand:

    def __init__(self, config):
        self.config = config
        self.tricks = []    # creates a new empty list for each dog



    def setVerbosity(self,verbose):
        #print('(BIdentifyScanCommand) setVerbosity: '+str(verbose))
        self.optionVerbose = verbose

    def showUsage(self):
        #
        print("Usage:")
        print(" "+self.config.get('EXENAME')+" scan [-d --directory= ] [-h --help] [-v]")


    def update(self):
        # setx path "D:\#BiUniverse_git\biuniverse;%path%;"
        # pathman /au D:\#BiUniverse_git\biuniverse
        #print(output)
        # http://ftp.armedassault.info/armaholic/arma.armaholic.txt
        # http://ftp.armedassault.info/armaholic/arma2.armaholic.txt
        # http://ftp.armedassault.info/armaholic/arma2_os.armaholic.txt
        home = self.config.get("LOCALAPPDATA") #str(Path.home())
        #home+"/armaholic/ofp.bidb"
        #home+"/armaholic/arma.bidb"
        #home+"/armaholic/arma2.bidb"
        #home+"/armaholic/arma2_oa.bidb"
        self.config.get("ROOTSERVER")

        output = self.config.get("ROOTSERVER")

        if self.optionVerbose : print("Connecting to bidentify server at " +output)

        #sys.exit()
        #print("Updating Arma file index (ofp.bidb)")
        #try:
        #    urllib.request.urlretrieve(output+"/armaholic/ofp.bidb",home+"/ofp.bidb")
        #except ( urllib.error.URLError,urllib.error.HTTPError) as e:
        #    print (e)

        if self.optionVerbose : print("Updating Arma file index (arma.bidb)")
        try:
            urllib.request.urlretrieve(output+"/armaholic/arma.bidb",home+"/arma.bidb")
        except ( urllib.error.URLError,urllib.error.HTTPError) as e:
            print (e)

        if self.optionVerbose : print("Updating Arma2 file index. (arma2.bidb)")
        try:
            urllib.request.urlretrieve(output+"/armaholic/arma2.bidb",home+"/arma2.bidb")
        except ( urllib.error.URLError,urllib.error.HTTPError) as e:
            print (e)

        if self.optionVerbose : print("Updating Arma2_OA file index. (arma2_oa.bidb)")
        try:
            urllib.request.urlretrieve(output+"/armaholic/arma2_oa.bidb",home+"/arma2_oa.bidb")
        except ( urllib.error.URLError,urllib.error.HTTPError) as e:
            print (e)
        print("updates downloaded to: "+home)




    def getRootservers():
        print("getRootservers()")
        print(self.config)


#print(sys.version)











