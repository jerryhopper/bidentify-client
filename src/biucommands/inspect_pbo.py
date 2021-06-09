import os
import subprocess
import sys
import re
from bidentify.pbo import PBOFile

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
        print("(InspectPbo) matchMissionSqf")
        f = open(theFile, "r") # ,encoding='utf-8'
        #result = chardet.detect(f.read())
        #charenc = result['encoding']
        #f.close()
        #f = open(theConfig, "r", charenc)
        #return f.read()
        rawConfig = f.read()
        f.close()


        p = re.search('class Header\[\]=[\n,\n,\t]{([\n,\t,\",A-z,0-9,]*)};',rawConfig)


        #p = re.search("version=(.*);",rawConfig)
        #if p is not None:
        #    print("(InspectPbo) matchMissionSqf - Version found!")
        #    version = p.groups()[0]




        sys.exit()



    def matchMissionSqf(self, theMission):
        # https://pythex.org/

        #theMission="D:\\#BiUniverse_git\\bidentify-client\\example\\contentdirectory\\sethhosll_arma3-missions-master\\arma3-missions-master\\ARTS.Altis\\mission.sqm"
        print("(InspectPbo) matchMissionSqf")
        f = open(theMission, "r") # ,encoding='utf-8'
        #result = chardet.detect(f.read())
        #charenc = result['encoding']
        #f.close()
        #f = open(theConfig, "r", charenc)
        #return f.read()
        rawConfig = f.read()
        f.close()


        p = re.search("version=(.*);",rawConfig)
        if p is not None:
            print("(InspectPbo) matchMissionSqf - Version found!")
            version = p.groups()[0]


        p = re.search('addons\[\]=[\n,\n,\t]{([\n,\t,\",A-z,0-9,]*)};',rawConfig)
        if p is not None:
            print("(InspectPbo) matchMissionSqf - Addons found!")
            addons = p.groups()[0].strip().replace("\t","").replace("\n","").replace('"',"").split(",")
            pprint.pprint(addons )
        else :
            addons = []


        #p = re.findall('class\sItem[0-9]\n\t\t{\n\t\t\t([A-z,0-9,=,\",;,\n,\t,\s,\-,\:,\/\.]*)};',rawConfig)
        #if p is not None:
        #    addonsmeta = p
        #    #pprint.pprint("addonsmetas")
        #    for meta in addonsmeta:
        #        print(meta.strip("\t").strip(" "))
        #    #pprint.pprint(addonsmeta)

        #sys.exit()

        ## class\sItem[0-9]\n\t\t({\n\t\t\t[A-z,0-9,=,",;,\n,\t,\s,\-,\:,\/\.]*)};




        p = re.search("(class (Intel)[\s,\S]*?})",rawConfig)
        if p is not None:
            print("(InspectPbo) matchMissionSqf - Intel found!")
            configPatches = p.groups()[0]
            intel =p.groups()[0].replace("\t","").replace("}","").replace("{","").replace("class Intel","").replace("\n","").split(";")

        #print(p)

        missionInfo = {}
        missionInfo['intel']=intel
        missionInfo['addons']=addons
        missionInfo['version']=version

        return missionInfo
        #sys.exit()



    def matchConfigCpp(self,theConfig):
        a=1
        #
        # read the config.cpp
        #

        #print( theConfig )
        f = open(theConfig, "r") # ,encoding='utf-8'
        #result = chardet.detect(f.read())
        #charenc = result['encoding']
        #f.close()
        #f = open(theConfig, "r", charenc)
        #return f.read()
        rawConfig = f.read()
        f.close()

        #p = re.compile("/^class ([A-z].*)[\s,\S]{([\s,\S]{,}?^\});/")
        #p = re.search("class (CfgPatches)[\s,\S]({[\s,\S]*?\}[\s,\S]*?\}[\s,\S]*?\}[\s,\S]*?\}[\s,\S]*?\});",config['config.cpp'])
        #print(rawConfig)
        p = re.findall("class CfgPatches[\s,\S]{([\s,\S]*?\}[\s,\S]*?\}[\s,\S]*?\}[\s,\S]*?\}[\s,\S]*?)\};",rawConfig)
        if p is None:
            #print("nothing found in config.cpp")
            return None
        configPatches = p[0].replace("\t","")

        #sys.exit()
        #configPatches = p.group()
        #print(configPatches)

        TheconfigPatches = {}

        p = re.search("class ([A-z,0-9,\_].*)",configPatches)
        TheconfigPatches['className'] = p.groups()[0]
        #print(p.groups()[0])



        p = re.search("requiredVersion\s=\s(.*);",configPatches)
        if p :TheconfigPatches['requiredVersion'] = p.groups()[0]

        p = re.search("requiredAddons\[\]\s=\s(.*);",configPatches)
        if p : TheconfigPatches['requiredAddons'] = p.groups()[0].replace('"',"").replace("{","").replace("}","").split(",")

        p = re.search("version\s=\s(.*);",configPatches)
        if p :
            TheconfigPatches['version'] = p.groups()[0]

        p = re.search("name\s=\s(.*);",configPatches)
        if p :
            TheconfigPatches['name'] = p.groups()[0].replace('"',"")

        p = re.search("fileName\s=\s(.*);",configPatches)
        if p :
            TheconfigPatches['filename'] = p.groups()[0].replace('"',"")

        p = re.search("author\s=\s(.*);",configPatches)
        if p :
            TheconfigPatches['author'] = p.groups()[0].replace('"',"")

        p = re.search("mail\s=\s(.*);",configPatches)
        if p :
            TheconfigPatches['mail'] = p.groups()[0].replace('"',"")

        p = re.search("url\s=\s(.*);",configPatches)
        if p :
            TheconfigPatches['url'] = p.groups()[0].replace('"',"")

        return TheconfigPatches

    def matchPboPrefix(self,thePrefix):
        #
        # read the PBOPRFIX
        #
        f = open(thePrefix, "r")
        #return f.read()
        Lines = f.readlines()
        #print(Lines)
        lijstje = []
        prefix = False
        for line in Lines:
            cleanLine = line.strip()
            if cleanLine[:6] == "prefix":
                print("found prefix")
                #config['prefix']=cleanLine.split("=")[1]
                #lijstje['prefix']=cleanLine.split("=")[1]
                prefix = cleanLine.split("=")[1]

                #lijstje.append(line.strip())
        f.close()
        if prefix is not False : return prefix
        return lijstje

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

