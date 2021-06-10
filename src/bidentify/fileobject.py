import sys
import os
import os.path
from biucommands.hashfile import hashfile

from biucommands.inspect_pbo import InspectPbo

from matching.missionSqf import missionSqf

import pprint

class myFileObject:

    def __init__(self, fileObject=None ):
        self.optionVerbose = False
        if self.optionVerbose : print("(myFileObject) init()")
        extensions = [".zip",".exe",".gz",".rar",".7z",".pbo",".sqm"]

        if isinstance(fileObject, myFileObject ):
            # import object
            if self.optionVerbose : print("(myFileObject) init(MYFILEOBJECT)")
            self.object = {}
            self.object['fileHash'] = fileObject.get('fileHash')
            self.object['filePath'] = fileObject.get('filePath')
            self.object['fileName'] = fileObject.get('fileName')
            self.object['fileSize'] = fileObject.get('fileSize')
            self.object['fileType'] = fileObject.get('fileType')
            self.object['fileContentsList'] = fileObject.get('fileContentsList')
            self.object['pboconfig'] = fileObject.get('pboconfig')
            self.object['missionconfig'] = fileObject.get('missionconfig')
            self.object['contains'] = fileObject.get('contains')

        elif isinstance(fileObject, str):
            # import from string.
            fullPath = os.path.abspath(fileObject)
            if self.optionVerbose : print("(myFileObject) init(STRING)")
            #print("(myFileObject) init()")
            #print(fileObject)
            # Allow only our extensions.
            fileExtension = os.path.splitext(fullPath)[1].lower()
            if fileExtension not in extensions :
                print('Extension is not allowed!')
                sys.exit()

            # Check if file exists.
            if os.path.exists(fullPath) == False:
                # file doesnt exist.
                print('file doesnt exist')
                sys.exit()

            #dirName=os.path.dirname(fullPath)
            #print("dirName: "+dirName)
            #print("parentDirname: "+os.path.basename(filePath))

            self.object = {}
            self.object['fileHash'] = hashfile(fullPath)
            self.object['filePath'] = os.path.dirname(fullPath)
            self.object['fileName'] = os.path.basename(fullPath)
            #fileName
            self.object['fileSize'] = str( os.path.getsize(fullPath) )
            self.object['fileType'] = fileExtension
            self.object['pboconfig'] = None
            self.object['missionconfig'] = None
            self.object['contains'] = None
            self.object['fileContentsList'] = self.getFileContentsList()


        elif fileObject is None:
            if self.optionVerbose : print("(myFileObject) init(NONE)")
            self.object = {}
            self.object['fileHash'] = None
            self.object['filePath'] = None
            self.object['fileName'] = None
            self.object['fileSize'] = None
            self.object['fileType'] = None
            self.object['fileContentsList'] = []
            self.object['pboconfig'] = None
            self.object['missionconfig'] = None
            self.object['contains'] = None

        else:
            raise RuntimeError("incorrect Type " + str( type(fileObject) ))
            #print( type(fileObject) )
            #print( isinstance(fileObject, myFileObject ) )

    def getFileContentsList(self):
        if self.optionVerbose : print("(myFileObject) getFileContentsList")
        #print("Current dir: ", os.getcwdb() )
        #print("(myFileObject) getFileContentsList")
        extensions = [".zip",".exe",".gz",".rar",".7z"]
        fullPath = os.path.join(self.object['filePath'],self.object['fileName'])
        if self.object['fileType']==".pbo":
            # Return the contents of the PBO
            X = InspectPbo(self, self.get('filePath') )
            # set the pbo-config.
            self.object['pboconfig']= X.extractCfg("")
            #self.object['contains'] = "addon"
            return X.list()
        if self.object['fileType']==".sqm":
            print("(myFileObject) getFileContentsList : THIS IS A SQM FILE! "+fullPath)
            missionData = missionSqf(fullPath )
            self.object['missionconfig'] = missionData.getAll()
            self.object['contains'] = "mission"

            #pprint.pprint( missionData.getAll() )
            #pprint.pprint(self.object)
            return []
        #if self.object['fileType'] in extensions:
        #    #
        return None


    def getAll(self):
        #print("(myFileObject) getAll")
        return self.object

    def get(self,property):
        #print("(myFileObject) get")
        return self.object[property]

    def print(self):
        print("(myFileObject) print")
        print("-----------------------------------------------")

        pprint.pprint(self.object)
        print("-----------------------------------------------")
        sys.exit()




    def setContains(self,text):
        if self.object['contains'] is None:
            self.object['contains'] = text
        else:
            raise RuntimeError("contains was already set")

    def setFileHash(self,hash):
        if self.object['fileHash'] is None:
            self.object['fileHash'] = hash
        else:
            raise RuntimeError("fileHash was already set")

    def setFileName(self,fileName):
        if self.object['fileName'] is None:
            self.object['fileName'] = fileName
        else:
            raise RuntimeError("fileName was already set")

    def setFilePath(self,filePath):
        if self.object['filePath'] is None:
            self.object['filePath'] = filePath
        else:
            raise RuntimeError("filePath was already set")


    def setFileSize(self,size):
        if self.object['fileSize'] is None:
            self.object['fileSize'] = size
        else:
            raise RuntimeError("fileSize was already set")

    def setFileType(self,type):
        if self.object['fileType'] is None:
            self.object['fileType'] = type
        else:
            raise RuntimeError("fileType was already set")

    def setFileContentsList(self,contents):
        if self.optionVerbose : print("(myFileObject) setFileContentsList")
        if self.object['fileContentsList'] is None:
            self.object['fileContentsList'] = contents
        else:
            raise RuntimeError("fileContentsList was already set")


