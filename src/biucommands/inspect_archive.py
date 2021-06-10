import os
import subprocess
import sys
import re
import time
import json
import pprint
import shutil
from pyunpack import Archive
from bidentify.fileobject import myFileObject


from matching.missionSqf import missionSqf

# extractpbodos -P -F=config.bin miroslavl_signs.pbo D:\#BIUniverse


#    %TEMP%

class InspectArchive:

    def __init__(self, fileObject, workingDir):
        self.fileObject = fileObject
        self.workingDir = workingDir
        self.optionVerbose = False
        if self.optionVerbose : print("(InspectArchive) init()")


        #pprint.pprint(fileObject.getAll() )
        #sys.exit()


        self.unpackedFolderName = os.path.join(fileObject.get( "filePath" ), os.path.splitext(self.fileObject.get("fileName"))[0] )

        #if not os.path.exists( self.unpackedFolderName ) :
        #    print("FATAL: directory does not exist "+self.unpackedFolderName)
        #    sys.exit()
        ######################################print(self.unpackedFolderName)
        #sys.exit()

    def list(self):
        if self.optionVerbose : print("(InspectArchive) list")
        thefile = os.path.join(self.fileObject.get("filePath"),self.fileObject.get("fileName") )

        self.ArchiveInformation = self.inspectArchive(thefile )


        fullpath = os.path.abspath(thefile)
        #print(fullpath)
        fileExtension = os.path.splitext(thefile)[1].lower()

        fileExtension = os.path.splitext(thefile)[1].lower()

        tempFolder = "~"+fileExtension.replace(".","")+self.fileObject.get('fileHash')
        tempFolder = os.path.join(self.workingDir, tempFolder)
        return tempFolder

    def get(self):
        return self.ArchiveInformation

    def inspectArchive(self, thefile ):
        if self.optionVerbose : print("(InspectArchive) inspectArchive("+thefile+")")

        # check if the file actually exists.
        if os.path.isfile(thefile):
            if self.optionVerbose : print( "inspecting "+thefile)
        else:
            print ("(inspectArchive) ERROR! File not exist (" +thefile+ ")")
            sys.exit()

        fullpath = os.path.abspath(thefile)
        # print(fullpath)
        # fileObject.get("fileType")
        fileExtension = self.fileObject.get("fileType") #os.path.splitext(thefile)[1].lower()


        #print(" ")
        extensions = [".zip",".exe",".gz",".rar",".7z"]
        if fileExtension not in extensions :
            print('Extension is not allowed.')



        #fileObject = myFileObject(fullpath)
        #fileObject.print()

        tempFolder = "~"+fileExtension.replace(".","")+self.fileObject.get('fileHash')
        tempFolder = os.path.join(self.workingDir, tempFolder)
        #print("----------------->>>>>>>>>>>>>>>" + tempFolder)

        # remove  tempfolder :  ~raree66bbfa6773226319a37ea06bc7b1f4
        if os.path.exists(tempFolder):
            shutil.rmtree(tempFolder)
        if not os.path.exists(tempFolder):
            os.mkdir(tempFolder)




        # Unpack if the file is a known archive.
        if fileExtension in [".zip",".rar",".7z"]:
            print("(InspectArchive) Extracting from "+self.fileObject.get('fileName')+"")

            # Create the object for this archive.
            ArchiveInformation = myFileObject(fullpath)


            Archive(fullpath).extractall(tempFolder)

            os.chdir(tempFolder)

            archiveContents = []
            archiveContentsPbo = []
            archiveContentsMissionSqm = []
            archiveContentsDescriptionExt = []
            archiveContentsOtherFiles = []

            thecontents = []
            allcontents = []
            listing = []
            missionInZip = False
            pboInZip = False

            # Walk through all dirs and subdirectories.
            print("(InspectArchive) InspectArchive : Iterating.... ")
            for root, dirs, files in os.walk(".", topdown = False):
               for name in files:
                   archiveContents.append( os.path.join(root,name) )
                   #print(os.path.join(root,name))
                   if os.path.splitext(name)[1] == ".pbo":
                       #print(">> (InspectArchive) InspectArchive : PBO :"+os.path.join(root,name) )
                       #print(os.path.join(root, name))
                       archiveContentsPbo.append( os.path.abspath(os.path.join(root, name)) )
                       #allcontents.append(  myFileObject( os.path.abspath(os.path.join(root, name)) ) )
                       #allcontents.append(os.path.abspath(os.path.join(root, name)) )
                   elif name == "description.ext":
                       archiveContentsDescriptionExt.append(os.path.join(root,name) )
                   elif name == "mission.sqm":
                       archiveContentsMissionSqm.append(os.path.join(root,name) )
                   #if os.path.splitext(name)[1] == ".sqm":
                   #    print("(>> InspectArchive) InspectArchive : SQM :"+os.path.join(root,name) )
                   #    missionInZip = True
                   #    print("(>> InspectArchive) detected Archived mission!" )
                   else:
                        archiveContentsOtherFiles.append(os.path.join(root,name))
                   #listing.append(os.path.join(root,name))
                   #print() listing
                   #fileObject = myFileObject( os.path.join(root, name) )
                   #if fileObject.get("fileType")==".pbo":
                   #thecontents.append(fileObject)

            print("Archive contains "+str(len(archiveContents))+" files" )
            print("Archive contains "+str(len(archiveContentsPbo))+" .pbo files" )
            print("Archive contains "+str(len(archiveContentsMissionSqm))+" mission.sqm files" )
            print("Archive contains "+str(len(archiveContentsDescriptionExt))+" description.ext files" )
            print("Archive contains "+str(len(archiveContentsOtherFiles))+" other files.")

            if len(archiveContentsMissionSqm) >1 or len(archiveContentsMissionSqm) >1 :
                print("UNSUPPORTED!  - Multiple missions found in archive.")
                sys.exit()

            #if
            #print("Decisions")

            if len(archiveContentsMissionSqm) == 1 :
                print("(InspectArchive) InspectArchive() : Mission found in Archive!" )
                print(archiveContentsMissionSqm[0])

                missionFileObject = myFileObject(archiveContentsMissionSqm[0])
                #pprint.pprint(missionFileObject.getAll())
                #sys.exit()

                #missionData = missionSqf(archiveContentsMissionSqm[0] )
                #pprint.pprint( missionData.getAll() )
                #MissionData = self.matchMissionSqf()
                ArchiveInformation.setContains("mission")
                ArchiveInformation.setFileContentsList( [missionFileObject.getAll()] )

            elif len(archiveContentsPbo) > 1 :
                print("(InspectArchive) InspectArchive() : Pbo's found in Archive" )
                ll = []
                for item in archiveContentsPbo:
                    myFileObject(item).getAll()
                    ll.append( myFileObject(item).getAll()  )
                ArchiveInformation.setContains("addon")
                ArchiveInformation.setFileContentsList(ll)


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


            #pprint.pprint(ArchiveInformation.getAll())
            #x = json.dumps(ArchiveInformation.getAll())
            #print(x)
            #sys.exit()
            #fileObject.print()
            #for item in allcontents:
            #    print()
            #    print(item)
            #    fileObject = myFileObject( item )
            #    thecontents.append(fileObject)
            #
            #    #fileObject.print()
            if self.optionVerbose : print("(InspectArchive) inspectArchive  FINISHED!")
            return ArchiveInformation


