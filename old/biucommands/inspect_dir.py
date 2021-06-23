import os
import subprocess
import sys
import re

import shutil
# extractpbodos -P -F=config.bin miroslavl_signs.pbo D:\#BIUniverse


#    %TEMP%

class InspectDir:

    def __init__(self, fileObject, workingDir):
        print("(InspectDir) init()")
        self.fileObject = fileObject
        self.workingDir = workingDir
        self.optionVerbose = False


    def inspectDir(self, thefile):
        sys.exit()
        if os.path.isdir(self.optionFile) == False:
            print("Not a directory")
            sys.exit()
        os.chdir(thefile)
        thecontents = []
        allcontents = []
        extensions = [".zip",".exe",".gz",".rar",".7z"]
        print("Current dir: ", os.getcwdb() )
        # Walk through all dirs and subdirectories.
        for root, dirs, files in os.walk(".", topdown = False):
           for name in files:
               ext = os.path.splitext(name)[1]
               full = os.path.abspath(os.path.join(root,name))
               #print( full )
               if ext == ".pbo":
                   thecontents.append(full)
                   #self.inspectPbo(full)
               elif ext in extensions :
                   thecontents.append(full)
                   #self.inspectArchive(full)

        for file in thecontents:
           ext = os.path.splitext(file)[1]
           #full = os.path.abspath(os.path.join(root,name))
           print( file )
           if ext == ".pbo":
               self.inspectPbo(full)
           elif ext in extensions :
               self.inspectArchive(full)
