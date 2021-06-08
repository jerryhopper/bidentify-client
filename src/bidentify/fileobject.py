import sys
import os
import os.path
from biucommands.hashfile import hashfile

from biucommands.inspect_pbo import InspectPbo


class myFileObject:

    def __init__(self, fileObject=None ):
        print("(myFileObject) init()")
        self.optionVerbose = False
        extensions = [".zip",".exe",".gz",".rar",".7z",".pbo"]

        if isinstance(fileObject, myFileObject ):
            # import object
            self.object = {}
            self.object['fileHash'] = fileObject.get('fileHash')
            self.object['filePath'] = fileObject.get('filePath')
            self.object['fileName'] = fileObject.get('fileName')
            self.object['fileSize'] = fileObject.get('fileSize')
            self.object['fileType'] = fileObject.get('fileType')
            self.object['fileContentsList'] = fileObject.get('fileContentsList')
            self.object['pboconfig'] = fileObject.get('pboconfig')
        elif isinstance(fileObject, str):
            # import from string.
            fullPath = os.path.abspath(fileObject)
            print("(myFileObject) init("+fullPath+")")
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
            self.object['fileContentsList'] = self.getFileContentsList()


        elif fileObject is None:
            self.object = {}
            self.object['fileHash'] = None
            self.object['filePath'] = None
            self.object['fileName'] = None
            self.object['fileSize'] = None
            self.object['fileType'] = None
            self.object['fileContentsList'] = []
            self.object['pboconfig'] = None

        else:
            raise RuntimeError("incorrect Type " + str( type(fileObject) ))
            #print( type(fileObject) )
            #print( isinstance(fileObject, myFileObject ) )

    def getFileContentsList(self):
        print("Current dir: ", os.getcwdb() )
        print("(myFileObject) getFileContentsList")
        extensions = [".zip",".exe",".gz",".rar",".7z"]
        fullPath = os.path.join(self.object['filePath'],self.object['fileName'])
        if self.object['fileType']==".pbo":
            # Return the contents of the PBO
            X = InspectPbo(self, self.get('filePath') )
            # set the pbo-config.
            self.object['pboconfig']= X.extractCfg("")
            return X.list()
        #if self.object['fileType'] in extensions:
        #    #
        return []


    def getAll(self):
        return self.object

    def get(self,property):
        return self.object[property]

    def print(self):
        #print(self.object['fileHash'],self.object['filePath'],self.object['fileName'],self.object['fileSize'],self.object['fileType'])

        if self.object['fileContentsList'] is None:
            print("-----------------------------------------------")
            print("| fileHash: "+str(self.object['fileHash']))
            print("| filePath: "+str(self.object['filePath']))
            print("| fileName: "+str(self.object['fileName']))
            print("| fileSize: "+str(self.object['fileSize']))
            print("| fileType: "+str(self.object['fileType']))
            print("-----------------------------------------------")

        else:
            print("-----------------------------------------------")
            print("| fileHash: "+str(self.object['fileHash']))
            print("| filePath: "+str(self.object['filePath']))
            print("| fileName: "+str(self.object['fileName']))
            print("| fileSize: "+str(self.object['fileSize']))
            print("| fileType: "+str(self.object['fileType']))
            print("-----------------------------------------------")


            for item in self.object['fileContentsList']:
                if self.optionVerbose : print("| "+item)
            #print("-----------------------------------------------")
            if self.object['pboconfig'] is not None:
                for item in self.object['pboconfig']:
                    print("| "+item, self.object['pboconfig'][item])



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
        if self.object['fileContentsList'] is None:
            self.object['fileContentsList'] = contents
        else:
            raise RuntimeError("fileContentsList was already set")


