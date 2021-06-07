import sys
import os
import os.path


class myFileObject:

    def __init__(self, fileObject=None ):

        if isinstance(fileObject, myFileObject ):

            self.object = {}
            self.object['fileHash'] = fileObject.get('fileHash')
            self.object['filePath'] = fileObject.get('filePath')
            self.object['fileName'] = fileObject.get('fileName')
            self.object['fileSize'] = fileObject.get('fileSize')
            self.object['fileType'] = fileObject.get('fileType')
            self.object['fileContentsList'] = fileObject.get('fileContentsList')
        elif fileObject is None:
            self.object = {}
            self.object['fileHash'] = None
            self.object['filePath'] = None
            self.object['fileName'] = None
            self.object['fileSize'] = None
            self.object['fileType'] = None
            self.object['fileContentsList'] = None
        else:
            raise RuntimeError("incorrect Type " + str( type(fileObject) ))
            #print( type(fileObject) )
            #print( isinstance(fileObject, myFileObject ) )

    def getAll(self):
        return self.object

    def get(self,property):
        return self.object[property]

    def print(self):
        #print(self.object['fileHash'],self.object['filePath'],self.object['fileName'],self.object['fileSize'],self.object['fileType'])

        if self.object['fileContentsList'] is None:
            print(self.object['fileHash'],self.object['filePath'],self.object['fileName'],self.object['fileSize'],self.object['fileType'])
        else:
            print(self.object['fileHash'],self.object['filePath'],self.object['fileName'],self.object['fileSize'],self.object['fileType'])
            for item in self.object['fileContentsList']:
                print(item)


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


