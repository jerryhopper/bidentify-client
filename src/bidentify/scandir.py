import sys, getopt
import os
import re
import csv
import requests
from requests_toolbelt.multipart import encoder
import time
from bidentify.hashfile import hashfile



def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)








class BIdentifyScanCommand:

    def __init__(self, config):
        self.config = config
        self.optionDirectory = None
        self.optionVerbose = False


    def setDirectory(self,dir):
        self.optionDirectory=dir

    def setVerbosity(self,verbose):
        #print('(BIdentifyScanCommand) setVerbosity: '+str(verbose))
        self.optionVerbose = verbose

    def showUsage(self):
        #
        print("Usage:")
        print(" "+self.config.get('EXENAME')+" scan [-d --directory= ] [-h --help] [-v]")

    def sizeof_fmt(self,num, suffix='B'):
        for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)

    def scandir(self):
        print("- scandir ")
        import json,urllib.request
        data = urllib.request.urlopen("http://bidentify.jerryhopper.com/api/missing").read()

        self.theMissingList = json.loads(data)
        #print (output)
        filenameList = []
        for item in self.theMissingList:
            filenameList.append(item['filename'])

        self.filenameList = filenameList

        self.scandirStart(self.optionDirectory)

        self.submitFiles()


    def matchMatch(self,match):
        for item in self.theMissingList :
            if item['filename'] == match['exactName']:
                match['id']=item['id']
                match['section']=item['section']
                return match

    def scandirStart(self,directory):
        if self.optionVerbose : print()
        print("Scanning... "+directory)
        print("------------------------------")

        extensions = [".zip",".exe",".gz",".rar",".7z"]


        os.chdir(directory)
        foundList = []
        foundSize = 0
        for root, dirs, files in os.walk(".", topdown = False):
           for name in files:
               if os.path.splitext(name)[1].lower() in extensions :
                   exactName=name
                   filePath=os.path.abspath(root)
                   fileName=os.path.splitext(name)[0]
                   #fileHash=hashfile(os.path.join(root, name))
                   fileSize=str(os.path.getsize(os.path.join(root, name)))
                   fileExtension=os.path.splitext(name)[1].lower()
                   if exactName in self.filenameList :
                       print( exactName +"  "+ sizeof_fmt(int(fileSize)))
                       foundSize = foundSize + int(fileSize)
                       foundList.append(self.matchMatch({'exactName': exactName, 'fileSize': fileSize,'filePath': filePath}) )

        #
        print("")
        print("Scanning complete.")
        self.foundList = foundList
        print("Found "+self.sizeof_fmt(foundSize)+" of missing files.")
        #print(foundSize)

    def checkFreeSpace(self):
        #print("Check free space")
        try:
            response = requests.get("http://bidentify.jerryhopper.com/api/client/uploadspace")
        except:
            print("response error")
            return response.status_code
        #print("response code "+str(response.status_code))

        return response.status_code

    def submitFiles(self):
        print("Submitting....")

        for item in self.foundList:
            #print(item)
            #item['exactName']
            #item['filePath']
            #item['id']
            while self.checkFreeSpace()  != 200:
                print("Server full, please wait 15s.")
                time.sleep(15)

            if os.path.getsize( os.path.join(item['filePath'] , item['exactName'])  ) < 573000000 :
                self.submitItem( item['exactName'], os.path.join(item['filePath'] , item['exactName']) , item['id']  )
            else:
                print("Skipping large file: "+ item['exactName'])
            #print(h)
            time.sleep(1)
            #sys.exit()


    def submitItem(self,fileName,file,id):
        hash = hashfile( file  )
        size = self.sizeof_fmt(os.path.getsize(file))
        print("submitItem : "+ size +" "+file)
        #print(self.optionDirectory)

        #parts = os.path.splitext(file)
        fileName = os.path.split(file)[1]
        #print(fileName)
        #print(row)
        #sys.exit()

        #try:
        session = requests.Session()
        with open(file, "rb") as a_file:
            #
            form = encoder.MultipartEncoder({
                "theFile": (fileName , a_file, "application/octet-stream"),
                "fileName": fileName,
                "fileHash": hashfile(file),
                "fileSize": str(os.path.getsize(file)),
                "id": id
            })
            #
            headers = {"Prefer": "respond-async", "Content-Type": form.content_type }

            response = session.post("http://bidentify.jerryhopper.com/api/client/upload/"+id, headers=headers, data=form)
            # http://bidentify.jerryhopper.com


            print(response.text)
            print(response.status_code )

            if response.status_code == 503:
                print("Server full!")
                return 503


            print("Done!!")
            time.sleep(1)
            #sys.exit()


            #file_dict = {fileName: a_file}
            #try:
            #    response = requests.post("http://bidentify.jerryhopper.com/api/client/upload/"+id, files=file_dict)
            #except:
            #    print("response error")
            #    print(response.text)
        #except:
        #    print("open-file error!")
        #    pass
        return os.path.getsize(file)
