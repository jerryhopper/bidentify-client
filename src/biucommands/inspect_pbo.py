import os
import subprocess
import sys
import re
from bidentify.pbo import PBOFile

from matching.configcpp import configCpp
from matching.descriptionext import descriptionExt
from matching.missionsqf import missionSqf


import pprint
from subprocess import check_output
import shutil
# extractpbodos -P -F=config.bin miroslavl_signs.pbo D:\#BIUniverse


#    %TEMP%

class InspectPbo:

    def __init__(self, fileObject, workingDir):
        #print("(InspectPbo) init()")
        self.fileObject = fileObject
        self.workingDir = workingDir
        self.optionVerbose = False

    def list(self):
        print("(InspectPbo) list()")

        path = os.path.join(self.fileObject.get("filePath"),self.fileObject.get("fileName") )
        path2 = os.path.join(self.workingDir,path.replace('.\\',''))
        print("List contents of pbo: "+ path2 )
        print(self.workingDir)

        try:
            output = check_output("ExtractPboDos.exe -P -LB \""+path2+"\"", shell=True)
        except FileNotFoundError:
            # handle file not found error.
            a=1
        theContents = []
        number =0
        for line in output.splitlines():
            # we have found a config file!
            if number >=2:
                theContents.append( line.decode() )
            number=number+1
        #print(theContents)
        return theContents

    def matchDescriptionExt(self,theFile):
        #
        d = descriptionExt(theFile)
        d.getAll()


    def matchMissionSqf(self, theMission):
        # https://pythex.org/
        m = missionSqf(theMission)
        m.getAll()


    def matchConfigCpp(self,theConfig):
        #
        c = configCpp(theConfig)
        c.getAll()


    def matchPboPrefix(self,thePrefix):
        #
        p = pboPrefix(thePrefix)
        p.getAll()


    def extractCfg(self,configFile):
        #configFile="config.cpp"
        print("(InspectPbo) extractCfg()")
        #print("Current dir: ", os.getcwdb() )
        curdir = os.getcwdb()
        if self.optionVerbose : print("extractCfg "+configFile)

        # relative path to the pbo file.
        path = os.path.join(self.fileObject.get("filePath"),self.fileObject.get("fileName") )
        #print("path="+path)

        # absolute path to the pbo file
        path2 = os.path.join(self.workingDir,path.replace('.\\',''))
        #print("path2="+path2)

        #
        pboFolderName= self.fileObject.get("fileName").replace(".pbo","")
        #print("pboExtractFolderName="+pboFolderName)

        self.fileObject.get("fileHash")


        xtractDirectory = os.path.join(self.workingDir,"~pbo"+self.fileObject.get("fileHash"))
        #print("xtractDirectory " +xtractDirectory)
        if os.path.exists(xtractDirectory) :
            shutil.rmtree( xtractDirectory )


        xtractConfigDir = os.path.join(xtractDirectory,pboFolderName)


        #xtractConfigDir = os.path.join(self.workingDir,os.path.join("_PboContents",pboFolderName))
        #print("xtractConfigDir="+xtractConfigDir)


        #os.path.mkdir( xtractConfigDir )
        #os.path.mkdir( xtractConfigDir )
        #sys.exit()
        #print("PATH TO PBO : "+path2)
        if os.path.exists( path2 ):
            if self.optionVerbose : print("__________________________________________________")
            #print(["extractpbodos", "-P","-F=config.cpp", path2 , xtractConfigDir])


            # extract config from pbo
            #command = "ExtractPboDos.exe -P "+path2+" "+xtractDirectory
            command = "ExtractPboDos.exe -P -F=\""+configFile+"\" \""+path2+"\" \""+xtractDirectory+"\""
            if self.optionVerbose : print(command)
            #sys.exit()
            output = check_output(command, shell=False)
            #for line in output.splitlines():
            #    print(line.decode())
            #sys.exit()

            #configFile="config.cpp"
            #print( os.path.join( xtractConfigDir , configFile )  )
            theConfig = None
            thePrefix = None
            MissionData = None
            DescriptionExt = None
            #########################################################################
            os.chdir(xtractDirectory)
            for root, dirs, files in os.walk(".", topdown = False):
               for name in files:
                  if name == "config.cpp":
                     theConfig=os.path.join(root,name)
                     if self.optionVerbose : print("Found "+name +" "+theConfig)
                     #print(root)
                  if name == "$PBOPREFIX$.txt":
                     thePrefix=os.path.join(root,name)
                     if self.optionVerbose : print("Found "+name +" "+thePrefix)
                     #print(root)
                  if name == "mission.sqm":
                     print(os.path.abspath(os.path.join(root,name)) )
                     MissionData = self.matchMissionSqf(os.path.abspath(os.path.join(root,name)))
                     #print(MissionData)
                     #return "mission"
                  if name == "description.ext":
                     print(os.path.abspath(os.path.join(root,name)) )
                     DescriptionExt = self.matchDescriptionExt(os.path.abspath(os.path.join(root,name)))
                     #print(MissionData)
                     #return "mission"



            #theConfig = os.path.join( xtractConfigDir ,configFile )
            if self.optionVerbose : print("__________________________________________________")
            pboConfig = {}
            if theConfig is not None:
                pboConfig = self.matchConfigCpp(theConfig)




            #config['config.cpp'] =TheconfigPatches
            #p = re.compile("class (CfgPatches)[\s,\S]{([\s,\S]*?\}[\s,\S]*?\}[\s,\S]*?\}[\s,\S]*?\}[\s,\S]*?)\};")

            #x= p.match(config['config.cpp'])
            #print(p.group())
            #print(p.groups())
            #print(p.groups()[0])

            #print(p.groups()[1])
            #r = p.match(config['config.cpp'])

            #config['config.cpp'] = p.group()
            #sys.exit()
            if MissionData is not None:
                pboConfig['mission']=MissionData

            #
            # read the PBOPRFIX
            #
            if thePrefix is not None:
                pboConfig['prefix'] = self.matchPboPrefix(thePrefix)


            #if os.path.exists(xtractDirectory) :
            #shutil.rmtree( xtractDirectory )
            os.chdir(curdir)
            #########################################################################
            #print("(InspectPbo) extractCfg()")
            #pprint.pprint(config)
            #return config

            #
            #
            #
            #
            #
            #  pboConfig['prefix'] = Prefix-data.
            #
            #print("xtractDirectory " +xtractDirectory)
            if os.path.exists(xtractDirectory) :
                shutil.rmtree( xtractDirectory )
            return pboConfig



#d = InspectPbo('bogus.pbo')
#e = InspectPbo('Buddy')
#d.add_trick('roll over')
#e.add_trick('play dead')
#d.tricks

