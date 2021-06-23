
import os
import io
import sys
import csv
import builtins
import traceback
from functools import wraps
from pathlib import Path
import hashlib
import requests
import time

from io import StringIO
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()








class ImportCommand:

    def __init__(self, config):
        self.config = config
        self.optionDirectory = None
        self.optionFile = None

        self.optionVerbose = False


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


    def Import(self):
        print("(BIdentifyInspectCommand) inspect")
        print("-----------------------------------------------------")
        print("| Directory: "+ str(self.optionDirectory))
        print("| File: "+ str(self.optionFile))
        print("-----------------------------------------------------")
        self.scanBidb("arma")
        self.scanBidb("arma2")
        self.scanBidb("arma2_oa")

    def strip_tags(self,html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()

    def scanBidb(self,name):
            print("scanlist")

            os.chdir(self.optionDirectory)
            print(self.optionDirectory)
            thedir = os.getcwd()
            FoundList = []
            MissingList = []
            #name="arma"
            print(name)
            totalSize = 0
            path = str(Path.home())
            with open( name+'.bidb', encoding='utf8') as csvfile:
                exactName = ""
                reader = csv.DictReader(csvfile,fieldnames=['game','exists','armaholicid','section','name','filename','armaholicpath'])
                #
                # parse each line
                #
                for row in reader:
                    #
                    # object
                    #
                    object = {}
                    p = os.path.join(thedir,row['game'],row['game']+"_"+row['section'],row['filename'])
                    pi = os.path.join(thedir,row['game'],row['game']+"_"+row['section'],row['armaholicid']+"-"+row['filename']+".html")
                    #
                    # if htmlfile exists.
                    #
                    if os.path.exists(pi):
                        with open(pi, encoding='utf8') as f:
                            contents = f.readlines()
                            info_dict = self.extractFromHtml(contents)
                            for key in info_dict:
                                object[key]=info_dict[key]
                            #print(info)
                    #
                    # if file exists.
                    #
                    if os.path.exists(p):
                        if os.path.isfile(p):


                            md5 = hashlib.md5()
                            sha1 = hashlib.sha1()
                            BUF_SIZE = 65536
                            with open(p, 'rb') as f:
                                while True:
                                    data = f.read(BUF_SIZE)
                                    if not data:
                                        break
                                    md5.update(data)
                                    sha1.update(data)
                            #fileObj = {}
                            object['filehash'] = md5.hexdigest()

                            #fileObj['md5'] = md5.hexdigest()

                            #fileObj['sha1'] = sha1.hexdigest()
                            object['filesize'] = os.path.getsize(p)
                            #fileObj['size'] = os.path.getsize(p)
                            # set the object
                            #object['fileinfo']=fileObj

                    object['game']=row['game'].replace("_","")
                    object['armaholicid']=int(row['armaholicid'])
                    object['section']= object['game']+"_"+row['section']
                    object['name']=row['name']
                    object['filename']=row['filename']
                    object['armaholicpath']=row['armaholicpath']

                    #print(object)
                    try:
                        r = requests.post('http://bidentify.jerryhopper.com/helper/import', json=object )
                        print(r.status_code,r.text)
                    except:
                        time.sleep(8)
                        r = requests.post('http://bidentify.jerryhopper.com/helper/import', json=object )
                        print(r.status_code,r.text)
                        pass
                    time.sleep(0.1)
                    FoundList.append(object)
            #print( "Missing: "+str(len(MissingList)) )
            #print("Found: "+str(len(FoundList))+" "+str(convert_size(totalSize) ) )
            return FoundList

    def extractFromHtml(self,contents):
        #
        htmlinfo = {}
        for line in contents:
            test = False

            line = line.strip("<font class=\"fontcolordark\">")
            line = line.replace("<br/>","")
            line = line.replace("</font>","")
            if "Author:" in line:
                test = True
            if "Requirements:" in line:
                test = True
            if "Island(s):" in line:
                test = True
            if "Island(s):" in line:
                test = True
            if "Playable options:" in line:
                test = True
            if "Author Website:" in line:
                test = True
            if "Version:" in line:
                test = True
            if "Date:" in line:
                test = True
            if "Signed:" in line:
                test = True
            #print(contents)
            if test :
                dta = line.split(":")
                htmlinfo[ dta[0].replace(" ","_").replace("(","").replace(")","").lower()    ] =  self.strip_tags(dta[1].strip()).strip()
        return htmlinfo
