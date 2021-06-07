import sys, getopt
import os
import os.path
import re
import rarfile
import csv
import shutil
from pyunpack import Archive

from biucommands.hashfile import hashfile
from biucommands.findinlist import findinlist

from biucommands.inspect_pbo import InspectPbo

from bidentify.fileobject import myFileObject

import subprocess
import sys




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
        print("Directory: "+ str(self.optionDirectory))
        print("File: "+ str(self.optionFile))

        self.inspectStart( self.optionFile )

    def inspectStart(self, thefile ):

        if os.path.isfile(thefile):
            print("-------------------------------------------------------")
            print( "inspecting "+thefile)
        else:
            print ("ERROR! File not exist (" +thefile+ ")")
            sys.exit()

        print(" ")
        extensions = [".zip",".exe",".gz",".rar",".7z"]

        gamename = ["ofp","arma","arma2","arma2oa","arma2_oa","arma3"]


        #print(os.path.splitext(output))
        #print(os.path.abspath(output))
        #print(os.path.basename(output))
        #print(os.path.dirname(output))
        #print(os.path.getsize(output))
        #os.path.getctime(output)
        #os.path.getmtime(output)
        #CURRENT_DIR=os.getcwd()
        #os.chdir(CURRENT_DIR)

        fullpath = os.path.abspath(thefile)
        #print(fullpath)
        fileExtension = os.path.splitext(thefile)[1]




        if os.path.splitext(fullpath)[1].lower() in extensions :
            #print("fileUri: "+fullpath)

            #print("filePath: "+os.path.dirname(fullpath))
            filePath=os.path.dirname(fullpath)


            #print("parentDirname: "+os.path.basename(filePath))

            #print("exactName: "+os.path.basename(fullpath))
            exactName=os.path.basename(fullpath)

            fileName = os.path.splitext(exactName)[0]
            #print("fileName: "+fileName)


            #print("fileExtension: "+fileExtension)

            fileSize=str(os.path.getsize(fullpath))
            #print("fileSize: "+fileSize)


            #fileName=os.path.splitext(fullpath)[0].split("\\")[-1]
            #print(fileName)
            fileHash=hashfile(fullpath)
            print("fileHash: "+fileHash)
            #print(os.path.split(fullpath)[0])



            print('exactName: '+ exactName+ ', fileSize:'+ fileSize+', filePath:'+ filePath+',fileName:'+ fileName + ', fileExtension: '+ fileExtension)
            #fileExtension=os.path.splitext(name)[1].lower()
            #print( exactName+","+str(fileSize)+","+root+","+fileName+","+fileExtension )
            #FileListWriter.writerow({'exactName': exactName, 'fileSize': fileSize,'filePath': filePath, 'fileName': fileName, 'fileExtension': fileExtension})
            #print(os.path.join(root, name))

            #if fileExtension == ".rar":
            #    rar(fullpath)
            #findinlist(exactName)


            object = myFileObject()

            object.setFileHash(fileHash)
            object.setFileName(exactName)
            object.setFileSize(fileSize)
            object.setFileType(fileExtension)

            object.print()


            #object.setFileContentsList(list)


            #print(self.optionDirectory )

            tempFolder = "~"+fileHash
            tempFolder = os.path.join(self.optionDirectory, tempFolder)

            if not os.path.exists(tempFolder):
                os.mkdir(tempFolder)



            # Unpack if the file is a known archive.
            if fileExtension in [".zip",".rar",".7z"]:
                print("Extracting from "+fileExtension+"!")

                Archive(fullpath).extractall(tempFolder)

                os.chdir(tempFolder)
                thecontents = []
                allcontents = []
                # Walk through all dirs and subdirectories.
                for root, dirs, files in os.walk(".", topdown = False):
                   for name in files:
                       fileObject = myFileObject()
                       fileObject.setFileHash(hashfile(os.path.join(root, name)))
                       fileObject.setFilePath(root)
                       fileObject.setFileName(name)
                       fileObject.setFileSize(str(os.path.getsize(os.path.join(root, name))))
                       fileObject.setFileType(os.path.splitext(name)[1].lower())

                       if os.path.splitext(name)[1].lower() == ".pbo":
                           print("**")
                           print("InspectPbo!")
                           print(tempFolder)
                           pboInspector = InspectPbo( fileObject,tempFolder )
                           contents = pboInspector.list()
                           fileObject.setFileContentsList(contents)
                           if "config.cpp" in contents:
                               print("******CONFIG FOUND")
                               pboInspector.extractCfg()


                       #print(root)

                       #fileObject.print()
                       #sys.exit()

                       #myFileObject()
                       #allcontents.append(fileObject)
                       #if fileExtension == ".pbo":
                       #     thecontents.append(fileObject)
                       #print( exactName+","+str(fileSize)+","+root+","+fileName+","+fileExtension )
                       #FileListWriter.writerow({'exactName': exactName, 'fileSize': fileSize,'filePath': filePath, 'fileName': fileName, 'fileExtension': fileExtension})
                       #print(os.path.join(root, name))

            sys.exit()
            if fileExtension == ".pbo":
                print("File is a PBO! ")
                fileObject = {}
                #fileObject["exactName"]=name
                #fileObject["filePath"]=root
                #fileObject["abspath"]= os.path.abspath(root)
                #fileObject["fileName"]=os.path.splitext(name)[0]
                #fileObject["fileHash"]=hashfile(os.path.join(root, name))
                #fileObject["fileSize"]=str(os.path.getsize(os.path.join(root, name)))
                #fileObject["fileExtension"]=os.path.splitext(name)[1].lower()

            #
            # allcontents  contain all files in the archive.
            #print(allcontents)
            # thecontens contain all pbo's in the archive.
            #print(thecontents)



            os.chdir(self.optionDirectory)

            # iterate through the contents of the archive.
            for item in thecontents:
                #print("Hash :"+  )
                #print(os.path.join(root, name))
                print(os.path.join(item['abspath'],item['exactName']))
                print(item)
                sys.exit()


                # before unpacking pbo, delete any previous unpack folder
                unpackFolder = os.path.join(item['abspath'],item['fileName'])
                if os.path.exists( unpackFolder):
                    shutil.rmtree(unpackFolder )




                # List files in the pbo.
                from subprocess import check_output
                output = check_output("ExtractPboDos.exe -P -LB "+os.path.join(item['abspath'],item['exactName']), shell=True)

                for line in output.splitlines():
                    # we have found a config file!
                    if line.decode() in ["config.cpp","config.bin"] :
                        #print(line.decode().strip())

                        # extract config from pbo
                        command = "ExtractPboDos.exe -P -F="+line.decode().strip()+" "+os.path.join(item['abspath'],item['exactName'])
                        output = check_output(command, shell=True)
                        for line in output.splitlines():
                            print(line.decode())


                        print(item)
                        print("unpackFolder: "+ unpackFolder)


                        os.chdir(unpackFolder)
                        for root, dirs, files in os.walk(".", topdown = False):
                           for name in files:
                               if name == "config.cpp":
                                   #print(name)
                                   #print(root)
                                   exactName=name
                                   filePath=root
                                   fileName=os.path.splitext(name)[0]
                                   #fileHash=hashfile(os.path.join(root, name))
                                   fileSize=str(os.path.getsize(os.path.join(root, name)))
                                   fileExtension=os.path.splitext(name)[1].lower()
                                   #print( exactName+","+str(fileSize)+","+root+","+fileName+","+fileExtension )
                                   #FileListWriter.writerow({'exactName': exactName, 'fileSize': fileSize,'filePath': filePath, 'fileName': fileName, 'fileExtension': fileExtension})

                                   tagFolder = root.split("\\")[-2]
                                   nameFolder = root.split("\\")[-1]
                                   theFile = name
                                   theRoot = root
                                   print("Found: "+name+' in '+ root)
                                   print("Tag: "+ tagFolder)
                                   print("name: "+ nameFolder)
                                   break
                                   #print(tagFolder,nameFolder)
                                   #print(os.path.join(root, name))
                        print(os.path.join(theRoot, theFile))
                        f = open(os.path.join(theRoot, theFile), "r")
                        print(f.read())
                        sys.exit()




                        dirs = os.listdir( unpackFolder )

                        # This would print all the files and directories
                        #for file[] in dirs:
                        #print ("unpackFolder2: "+ dirs[0].strip)
                        pbocontentsfolder = os.path.join(unpackFolder,dirs[0].strip())
                        print("pbocontentsfolder :"+pbocontentsfolder)

                        dirs = os.listdir( pbocontentsfolder )

                        finalfolder = dirs[0].strip()
                        #print("finalfolder :"+finalfolder)

                        final = os.path.join(pbocontentsfolder,finalfolder)
                        print("finalfolder :"+final)

                        cpp = os.path.join(final,"config.cpp")

                        #print(pbocontentsfolder)
                        f = open(cpp, "r")
                        print(f.read())




            #print(str(x))
            #result = subprocess.run(
            #    [ExtractPboDos.exe, "-c", "ExtractPboDos.exe"], capture_output=True, text=True
            #)
            #print("stdout:", result.stdout)
            #print("stderr:", result.stderr)

            #ExtractPboDos.exe
            # ExtractPboDos.exe -P bogus.pbo

            #shutil.rmtree(tempFolder)










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










