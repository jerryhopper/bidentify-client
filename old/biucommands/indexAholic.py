import sys, getopt
import os
import re
import csv
import time
import urllib.request
from pathlib import Path
from biucommands.inspect import BIdentifyInspectCommand
from biucommands.inspect_archive import InspectArchive
import pprint
from biucommands.hashfile import hashfile
import math
import requests
from torf import Torrent
import base64

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def cb(torrent, filepath, pieces_done, pieces_total):
    print(f'{pieces_done/pieces_total*100:3.0f} % done')



class indexAholicCommand:

    def __init__(self,config):
        self.config = config
        self.optionVerbose=False

    def setVerbosity(self,x):
        self.optionVerbose=True

    def setDirectory(self,dir):
        self.workingdir = dir

    def inspect(self,thefile):
        path = thefile
        InspectCommand = BIdentifyInspectCommand(self.config)
        InspectCommand.setVerbosity(self.optionVerbose)
        if thefile is None:
            print("ERROR INSPECTING")
            return
        InspectCommand.setDirectory(os.getcwd())
        InspectCommand.setSelectedFile(path)

        #data = InspectCommand.inspect()
        data = InspectCommand.inspectArchive(thefile)
        #try:
        #    data = InspectCommand.inspectArchive(thefile)
        #    print(data)
        #except:
        #    print("(indexAholicCommand) inspect : InspectCommand.inspectArchive(thefile) Unexpected error:", sys.exc_info()[0])


        #sys.exit()
    def scanGameLists(self):
        print("scanGameLists")



        #self.scanBidb("arma")
        #self.scanBidb("arma2")
        self.scanBidb("arma2_oa")

        #self.scanList("arma")
        #self.scanlist("arma2")
        #self.scanlist("arma2_oa")

    def scanBidb(self,name):
        print("scanlist")

        os.chdir(self.workingdir)
        print(self.workingdir)
        thedir = os.getcwd()
        FoundList = []
        MissingList = []
        #name="arma"
        print(name)
        totalSize = 0
        path = str(Path.home())
        with open(path+"\\"+name+'.bidb', encoding='utf8') as csvfile:
            exactName = ""
            reader = csv.DictReader(csvfile,fieldnames=['game','exists','armaholicid','section','name','filename','armaholicpath'])
            for row in reader:
                p = os.path.join(thedir,row['game'],row['game']+"_"+row['section'],row['filename'])

                if row['exists'] == "ERR":
                    #print(row['game']+" ", )
                    #print(row)
                    r = requests.post('http://bidentify.jerryhopper.com/api/hash/p3/'+row['armaholicid'], json=row )
                    print(r.status_code,r.text)
                    #sys.exit()


                #redisKey = row['game']+":"+row['section'].replace("_",":")
                #print(redisKey+" "+row['game']+"\\"+row['game']+"\\"+row['section']+"\\"+row['filename'])


                #time.sleep(20)

                #FoundList.append(row)
        print( "Missing: "+str(len(MissingList)) )
        print("Found: "+str(len(FoundList))+" "+str(convert_size(totalSize) ) )
        return FoundList


    def resolvePath(self,rediskey):
        rediskey.split(":")

    def scanlist(self,name):
        print("scanlist")
        return
        os.chdir(self.workingdir)
        print(self.workingdir)
        thedir = os.getcwd()
        FoundList = []
        MissingList = []
        #name="arma"
        print(name)
        totalSize = 0
        path = str(Path.home())
        with open(path+"\\"+name+'.bidb', encoding='utf8') as csvfile:
            exactName = ""
            reader = csv.DictReader(csvfile,fieldnames=['game','exists','armaholicid','section','name','filename','armaholicpath'])
            for row in reader:
                p = os.path.join(thedir,row['game'],row['game']+"_"+row['section'],row['filename'])
                #print(p)
                redisKey = row['game']+":"+row['section'].replace("_",":")
                #print(redisKey+" "+row['game']+"\\"+row['game']+"\\"+row['section']+"\\"+row['filename'])
                if os.path.exists( p ) :
                    if not os.path.isdir(p) :
                        #pprint.pprint( { hashfile(p) : { "aid":row['armaholicid'],"key": redisKey, "fname":row['filename'] } })
                        #print( hashfile(p) )
                        #print({"aid":row['armaholicid'],"key": redisKey,"fname":row['filename'] } )
                        #print(redisKey+" "+row['game']+"\\"+row['game']+"\\"+row['section']+"\\"+row['filename'])
                        #print(row)
                        jsonObject= {}
                        jsonObject['fileHash']=hashfile(p)
                        jsonObject['fileName']=row['filename']
                        jsonObject['fileSize']=os.path.getsize(p)
                        jsonObject['fileSection']=redisKey
                        jsonObject['filePath']= os.path.join(row['game'],row['game']+"_"+row['section'])
                        jsonObject['commonName']=row['name']
                        totalSize = totalSize+jsonObject['fileSize']
                        #if row['exists'] == "OK" :
                        #    jsonObject['AHmissing']=False
                        #else:
                        #    jsonObject['AHmissing']=True

                        jsonObject['AHid']=int(row['armaholicid'])
                        #pprint.pprint(jsonObject)
                        #sys.exit()

                        if not os.path.exists(jsonObject['fileHash']+'.torrent') :
                            #
                            #torrent = Torrent(p, trackers=['udp://tracker.openbittorrent.com:6969','udp://tracker.opentrackr.org:1337/announce','http://tracker.gbitt.info/announce','udp://explodie.org:6969'])
                            #torrent.comment = "Armhaholic section: "+redisKey.replace(":"," - ")+" "+row['filename']
                            #torrent.private = False
                            #success = torrent.generate(callback=cb, interval=1)
                            #jsonObject['magnet']= str(torrent.magnet())
                            #torrent.write( jsonObject['fileHash']+'.torrent')
                            #self.inspect(p)
                            a=1
                            r = requests.post('http://bidentify.jerryhopper.com/api/hash/p2/'+jsonObject['fileHash'], json=jsonObject )
                            print(r.status_code,r.text)



                        FoundList.append(jsonObject)
                else:
                    MissingList.append(row)
                #time.sleep(20)

                #FoundList.append(row)
        print( "Missing: "+str(len(MissingList)) )
        print("Found: "+str(len(FoundList))+" "+str(convert_size(totalSize) ) )
        return FoundList

    def scandir(self):

        extensions = [".zip",".exe",".gz",".rar",".7z"]
        print("scanlist")
        return
        os.chdir(self.workingdir)
        for root, dirs, files in os.walk(".", topdown = False):
           for name in files:
               if os.path.splitext(name)[1].lower() in extensions :
                   exactName=name
                   filePath=root
                   fileName=os.path.splitext(name)[0]
                   fileHash=hashfile(os.path.join(root, name))
                   fileSize=str(os.path.getsize(os.path.join(root, name)))
                   fileExtension=os.path.splitext(name)[1].lower()

                   pathParts = root.split("\\")
                   if pathParts[1] not in ['arma','arma2','arma2_oa']:
                       print("corrupt directory structure.")
                       sys.exit()
                   section = pathParts[2]

                   #print(root.split("\\") )

                   print( section+" "+fileHash+" "+exactName+","+str(fileSize)+","+fileName )
                   #FileListWriter.writerow({'exactName': exactName, 'fileSize': fileSize,'filePath': filePath, 'fileName': fileName, 'fileExtension': fileExtension})
               #print(os.path.join(root, name))


