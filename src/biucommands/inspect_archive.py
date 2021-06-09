import os
import subprocess
import sys
import re

import pprint
import shutil
from pyunpack import Archive
from bidentify.fileobject import myFileObject
# extractpbodos -P -F=config.bin miroslavl_signs.pbo D:\#BIUniverse


#    %TEMP%

class InspectArchive:

    def __init__(self, fileObject, workingDir):
        #print("(InspectArchive) init()")
        self.fileObject = fileObject
        self.workingDir = workingDir
        self.optionVerbose = False

    def list(self):
        #print("(InspectArchive) list")
        self.inspectArchive(os.path.join(self.fileObject.get("filePath"),self.fileObject.get("fileName") ) )

    def extract(self):
        a=1

    def inspectArchive(self, thefile ):
        print("(InspectArchive) inspectArchive("+thefile+")")

        if os.path.isfile(thefile):
            if self.optionVerbose : print( "inspecting "+thefile)
        else:
            print ("(inspectArchive) ERROR! File not exist (" +thefile+ ")")
            sys.exit()

        fullpath = os.path.abspath(thefile)
        #print(fullpath)
        fileExtension = os.path.splitext(thefile)[1].lower()


        #print(" ")
        extensions = [".zip",".exe",".gz",".rar",".7z"]
        if fileExtension not in extensions :
            print('Extension is not allowed.')



        #fileObject = myFileObject(fullpath)
        #fileObject.print()

        tempFolder = "~"+fileExtension.replace(".","")+self.fileObject.get('fileHash')
        tempFolder = os.path.join(self.workingDir, tempFolder)
        print("----------------->>>>>>>>>>>>>>>" + tempFolder)


        if os.path.exists(tempFolder):
            shutil.rmtree(tempFolder)
        if not os.path.exists(tempFolder):
            os.mkdir(tempFolder)




        # Unpack if the file is a known archive.
        if fileExtension in [".zip",".rar",".7z"]:
            print("(InspectArchive) Extracting from "+fileExtension+"!")

            # Create the object for this archive.
            ArchiveInformation = myFileObject(fullpath)


            Archive(fullpath).extractall(tempFolder)

            os.chdir(tempFolder)
            thecontents = []
            allcontents = []
            # Walk through all dirs and subdirectories.
            for root, dirs, files in os.walk(".", topdown = False):
               for name in files:
                   #print(os.path.splitext(name)[1])
                   if os.path.splitext(name)[1] == ".pbo":
                       #print(os.path.join(root, name))
                       allcontents.append(  myFileObject( os.path.abspath(os.path.join(root, name)) ) )
                       #allcontents.append(os.path.abspath(os.path.join(root, name)) )
                   #fileObject = myFileObject( os.path.join(root, name) )
                   #if fileObject.get("fileType")==".pbo":
                   #thecontents.append(fileObject)

            print("(InspectArchive) Iterating.... ")

            #
            #for item in allcontents:
            #print()
            #print(allcontents[0])
            #print("(InspectArchive) ..")
            #fileObject = myFileObject( allcontents[0] )
            #print("(InspectArchive) ... print(fileObject.getAll())")
            ##print( fileObject.getAll() )
            #print("(InspectArchive) ....")
            #fileObject.print()
            #thecontents.append(fileObject)

            ArchiveInformation.setFileContentsList(allcontents)
            pprint.pprint(ArchiveInformation.getAll())
            #fileObject.print()
            #for item in allcontents:
            #    print()
            #    print(item)
            #    fileObject = myFileObject( item )
            #    thecontents.append(fileObject)
            #
            #    #fileObject.print()

            return thecontents


