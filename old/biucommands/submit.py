
import os,sys
import csv
import requests
from pathlib import Path
from requests_toolbelt.multipart import encoder

class BIdentifySubmitCommand:

    def __init__(self, config):
        self.config = config
        self.optionDirectory = None
        self.optionVerbose = False
        self.tricks = []    # creates a new empty list for each dog


    def setDirectory(self,dir):
        print( "setDirectory("+dir+")" )
        self.optionDirectory=dir

    def setVerbosity(self,verbose):
        #print('(BIdentifyScanCommand) setVerbosity: '+str(verbose))
        self.optionVerbose = verbose

    def sizeof_fmt(self,num, suffix='B'):
        for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)

    def showUsage(self):
        print("Usage:")
        #print(" "+self.config.get('EXENAME')+" scan (-h --help)")
        #print(" "+self.config.get('EXENAME')+" update (-h --help)")
        #print(" "+self.config.get('EXENAME')+" analyze (-h --help)")
        #print(" "+self.config.get('EXENAME')+" inspect (-h --help)")

    def submitItem(self,file,row):


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
            form = encoder.MultipartEncoder({
                "theFile": (fileName , a_file, "application/octet-stream"),
                "fileName": fileName,
                "fileSize": str(os.path.getsize(file)),
                "armaholicid": row['armaholicid'],
                "section": row['section'],
                "game": row['game']
            })
            headers = {"Prefer": "respond-async", "Content-Type": form.content_type }

            response = session.post("http://bidentify.jerryhopper.com/missingfile/"+row['armaholicid'], headers=headers, data=form)
            # http://bidentify.jerryhopper.com
            if response.status_code == 503:
                print("Server full!")
                sys.exit()

            print(response.text)
            print(response.status_code )
            #file_dict = {fileName: a_file}
            #try:
            #    response = requests.post("http://bidentify.jerryhopper.com/missingfile/"+row['armaholicid'], files=file_dict)
            #except:
            #    print("response error")
            #    print(response.text)
        #except:
        #    print("open-file error!")
        #    pass
        return os.path.getsize(file)




    def submit(self):
        print("------------------")
        if os.path.exists(os.path.join(self.optionDirectory,"found.txt") )  :
            # update needed
            print("found.txt")
            #csvFile = open('found.txt', 'w', encoding='utf8')
            #FileListWriterFieldNames = ['localFile']
        theFile = open(os.path.join(self.optionDirectory,"found.txt"), encoding='utf8')
        totalsize=0
        with theFile as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                #print(row)
                #sys.exit()
                THEpath = os.path.join(self.optionDirectory,row['localFile'])
                if os.path.exists(  THEpath ) :
                    totalsize = totalsize+self.submitItem(THEpath,row)
                #print(row['exactName'], row['fileSize'], row['filePath'], row['fileName'], row['fileExtension'])
                # Attempt to find the record in the bidentify-database.
                #foundFiles=findinlist(row['exactName'])
                #for foundFile in foundFiles:
                #    #print (row)
                #    if len(foundFile) != 0:
                #        test = {'localFile': row, 'foundFiles':foundFiles }
                #        results.append(test)
        print(self.sizeof_fmt(totalsize))
