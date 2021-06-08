
import os,sys,getopt
import urllib.request
import time
from random import shuffle
from random import choice
from urllib.error import HTTPError
from urllib.error import URLError
import urllib.request

from bidentify.update import BIdentifyUpdateCommand


#%Appdata%/Local/BIdentity   %LOCALAPPDATA%/BIdentity

#import os
# print os.getenv('LOCALAPPDATA')


class BIdentifyConfig:


    def __init__(self):
        #print("(BIdentifyConfig) init: set verbosity to: False")
        self.optionVerbose = False
        try:
            opts, args = getopt.getopt(sys.argv[2:], "f:d:hv", ["file=","directory=","help","verbose"])
        except getopt.GetoptError as err:
            # print help information and exit:
            print(err)  # will print something like "option -a not recognized"
            #self.showUsage()
            pass

        for o, a in opts:
            if o in ["-v","--verbose"]:
                print("(BIdentifyConfig) init: set verbosity to: True")
                self.optionVerbose = True


        self.EXENAME= sys.argv[0].split("\\")[-1]
        self.LOCALAPPDATA = os.path.join( os.getenv('LOCALAPPDATA'),"BIdentify")
        self.TMP = os.getenv('%TEMP%')
        self.ROOTSERVERLIST = "https://raw.githubusercontent.com/jerryhopper/bidentify-definitions/master/data/servers.list"


        FiveDays = (3600*24)*5
        OneDay = 3600*24
        OneHour = 3600
        current_time = time.time()

        #
        # Check if bidentify-data folder exists.
        #
        if not os.path.exists( self.LOCALAPPDATA  ):
            if self.optionVerbose : print("BIdentify appdatafolder does not exist!")
            # Create the bidentify-data folder.
            os.mkdir( self.LOCALAPPDATA )


        #
        # Check if bidentify serverlist exists.
        #
        if not os.path.exists( os.path.join( self.LOCALAPPDATA,"servers.list")):
            if self.optionVerbose : print("servers.list does not exist!")
            # Grab the initial serverlist from github!
            self.getInitialRootservers()



        #
        # If serverlist is too old, update it from github!
        #
        modTimesinceEpoc = os.path.getmtime(os.path.join( self.LOCALAPPDATA,"servers.list"))
        modificationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modTimesinceEpoc))
        #print("servers.list modificationTime: "+modificationTime)
        if (current_time-modTimesinceEpoc) > FiveDays :
            if self.optionVerbose : print("Servers.list was older than five days : ", modificationTime )
            self.getInitialRootservers()



        #
        # get the available bidentify rootservers
        #

        self.ROOTSERVERS = self.readServers()

        #
        # Select the bidentify rootserver
        #
        self.ROOTSERVER = choice(self.ROOTSERVERS)
        teller = 0
        while not self.getServerStatus(self.ROOTSERVER):
            self.ROOTSERVER = choice(self.ROOTSERVERS)
            if self.optionVerbose : print("Finding optimal server... (Trying: "+self.ROOTSERVER+")")
            teller=teller+1
            if teller>3:
                time.sleep(1.4)

        if self.optionVerbose : print("Initial Rootservers set!")
        if self.optionVerbose : print(self.ROOTSERVER)


        #
        # Select the bidentify rootserver
        #

        # If serverlist is too old, update it from a communityserver!
        if (current_time-modTimesinceEpoc) > OneHour :
            if self.optionVerbose : print("Servers.list was older than 1 Hour: ", modificationTime )
            self.ROOTSERVERS = self.getServers()


        #
        # Select the bidentify rootserver
        #
        self.ROOTSERVER = choice(self.ROOTSERVERS)
        teller = 0
        while not self.getServerStatus(self.ROOTSERVER):
            self.ROOTSERVER = choice(self.ROOTSERVERS)
            if self.optionVerbose : print("Finding optimal server... (Trying: "+self.ROOTSERVER+")")
            teller=teller+1
            if teller>3:
                time.sleep(2.4)


        if self.optionVerbose : print( "self.EXENAME: "+self.EXENAME  )
        if self.optionVerbose : print( "self.LOCALAPPDATA: "+self.LOCALAPPDATA  )
        if self.optionVerbose : print( "self.ROOTSERVERLIST: "+self.ROOTSERVERLIST  )
        if self.optionVerbose : print( "self.ROOTSERVERS: "+str(self.ROOTSERVERS)  )
        if self.optionVerbose : print( "self.ROOTSERVER: "+self.ROOTSERVER  )
        #sys.exit()



    # bidentify -h
    # bidentify scan -d c:\directory  -h
    # bidentify analyze -d c:\directory -h
    # bidentify update -s http://bidentify.jerryhopper.com -h
    def getServerStatus(self,rootServer):
        try:
            response = urllib.request.urlopen( rootServer +"/api/status")
            response_status = response.status # 200, 301, etc
        except HTTPError as error:
            response_status = error.code # 404, 500, etc
            if self.optionVerbose : print("Error: "+self.ROOTSERVER+" returned "+str(response_status))
            return False
        except URLError as error:
            if self.optionVerbose : print("Error: "+self.ROOTSERVER+" "+str(error))
            return False
            sys.exit()
        return True



    def getServers(self):
        if self.optionVerbose : print("Getservers "+ self.LOCALAPPDATA  +", "+ self.ROOTSERVER )


        path=os.path.join( self.LOCALAPPDATA,"servers.list")
        #print(self.ROOTSERVER+"/api/servers.list" )
        #print(path)

        try:
            urllib.request.urlretrieve( self.ROOTSERVER+"/api/servers.list" , path)
        except ( urllib.error.URLError,urllib.error.HTTPError) as e:
            if self.optionVerbose : print (e)
            sys.exit()

        #if os.path.exists(os.path.join( self.LOCALAPPDATA,"servers.list")):
        #  os.remove(os.path.join( self.LOCALAPPDATA,"servers.list"))
        #else:
        #  print("The file 'servers.list' does not exist")

        #print("getServers()")
        # Grab the initial serverlist from the rootserver(s)
        serversFile = open(os.path.join( self.LOCALAPPDATA,"servers.list"), 'r')
        serverList = []
        count = 0
        while True:
            count += 1
            # Get next line from file
            server = serversFile.readline()
            # if line is empty
            # end of file is reached
            if not server:
                break
            #print("Server{}: {}".format(count, server.strip()))
            serverList.append( server.strip() )
        serversFile.close()
        return serverList


    def getInitialRootservers(self):
        print("getInitialRootservers()")
        try:
            urllib.request.urlretrieve( self.ROOTSERVERLIST ,os.path.join( self.LOCALAPPDATA,"servers.list"))
        except ( urllib.error.URLError,urllib.error.HTTPError) as e:
            print (e)
            sys.exit()

        # Grab the initial serverlist from the rootserver(s)
        serversFile = open(os.path.join( self.LOCALAPPDATA,"servers.list"), 'r')
        serverList = []
        count = 0
        while True:
            count += 1
            # Get next line from file
            server = serversFile.readline()
            # if line is empty
            # end of file is reached
            if not server:
                break
            #print("Server{}: {}".format(count, server.strip()))
            serverList.append( server.strip() )
        serversFile.close()


    def readServers(self):
        #print("readServers")
        # Grab the initial serverlist from the rootserver(s)
        serversFile = open(os.path.join( self.LOCALAPPDATA,"servers.list"), 'r')
        serverList = []
        count = 0
        while True:
            count += 1
            # Get next line from file
            server = serversFile.readline()
            # if line is empty
            # end of file is reached
            if not server:
                break
            #print("Server{}: {}".format(count, server.strip()))
            serverList.append( server.strip() )
        serversFile.close()
        # Set variable
        return serverList



    def get(self,what):
        try:
            func = getattr(self, what)
        except  (AttributeError) as e :
            print(e)
            sys.exit()
        return func
