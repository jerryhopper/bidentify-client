import re,os
import pprint
import pprint
import time

class descriptionExt :

    def __init__(self, fileLocation , verbose = False):
        # set verbosity
        self.optionVerbose = verbose
        if self.optionVerbose : print("(matching\descriptionExt) init()")

        # open file.
        f = open(os.path.abspath(fileLocation), "r") # ,encoding='utf-8'
        self.textString =  f.read()
        f.close()

        #########################################
        # Object definition
        #########################################
        self.descriptionObject = {}
        self.matchDescriptionExt()
        #########################################

    def getAll(self):
        return self.descriptionObject


    def matchDescriptionExt(self):

        print("(descriptionExt) matchDescriptionExt")
        print(self.textString)

        extOptions = {}
        p = re.search("class header([A-z,0-9,\_].*)",self.textString)
        #if p : self.configObject['className'] = p.groups()[0]
        if p:
            print("class header([A-z,0-9,\_].*)" )
            print( p.groups() )
            time.sleep(10)

        p = re.findall('onLoadMission\=(.*);',self.textString)
        if p:
            print('onLoadMission\=(.*);')
            extOptions['onLoadMission']=p[0].replace("\"","")
            print( p[0])
            time.sleep(1)

        #p = re.search('onLoadMission\=(.*);',self.textString)
        #if p:
        #    print('onLoadMission\=(.*);')
        #    print( p.groups() )
        #    time.sleep(10)

        p = re.search("respawn=([0-9].*);",self.textString)
        if p:
            print("respawn=([0-9].*);")
            extOptions['respawn']=p[0].replace("\"","")
            #print( p.groups() )
            #time.sleep(10)

        p = re.search("respawndelay=([0-9].*);",self.textString)
        if p:
            print("respawndelay=([0-9].*);")
            extOptions['respawndelay']=p[0].replace("\"","")
            #print( p.groups() )
            #time.sleep(10)




        p = re.search("gameType[\s,]*=(.*);",self.textString)
        if p:
            print("gameType=([0-9].*);")
            extOptions['gameType']=p[0].replace("\"","")
            print( p.groups() )
            time.sleep(10)

        p = re.search("minPlayers[\s,]*=[\s]?([0-9].*);",self.textString)
        if p:
            print("minPlayers[\s,]*=[\s]?([0-9].*);")
            extOptions['minPlayers']=p[0].replace("\"","")
            print( p.groups() )
            time.sleep(10)

        p = re.search("maxPlayers[\s,]*=[\s]?([0-9].*);",self.textString)
        if p:
            print("maxPlayers[\s,]*=[\s]?([0-9].*);")
            extOptions['maxPlayers']=p[0].replace("\"","")
            print( p.groups() )
            time.sleep(10)

        #p = re.search("respawn=([0-9].*);",self.textString)


        #p = re.search("version=(.*);",rawConfig)
        #if p is not None:
        #    print("(InspectPbo) matchMissionSqf - Version found!")
        #    version = p.groups()[0]




        #sys.exit()

