import os
import re
import pprint

class missionSqf :

    def __init__(self, fileLocation ,verbose = False ):
        # set verbosity
        self.optionVerbose = verbose
        if self.optionVerbose : print("(matching\missionSqf) init()")

        # open file.
        f = open(os.path.abspath(fileLocation), "r") # ,encoding='utf-8'
        self.textString =  f.read()
        f.close()

        #########################################
        # Object definition
        #########################################
        self.missionObject = {}
        self.missionObject['version'] = None
        self.missionObject['addons'] = None
        self.missionObject['intel'] = None
        #########################################

        self.matchMissionSqf()

    def getAll(self):
        return self.missionObject


    def matchMissionSqf(self):
        # https://pythex.org/

        p = re.search("version=(.*);",self.textString)
        if p is not None:
            print("(missionSqf) matchMissionSqf - Version found!")
            self.missionObject['version'] = p.groups()[0]


        p = re.search('addons\[\]=[\n,\n,\t]{([\n,\t,\",A-z,0-9,]*)};',self.textString)
        if p is not None:
            if self.optionVerbose : print("(missionSqf) matchMissionSqf - Addons found!")
            self.missionObject['addons']  = p.groups()[0].strip().replace("\t","").replace("\n","").replace('"',"").split(",")
            if self.optionVerbose : pprint.pprint(addons )
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




        p = re.search("(class (Intel)[\s,\S]*?})",self.textString)
        if p is not None:
            if self.optionVerbose : print("(missionSqf) matchMissionSqf - Intel found!")
            configPatches = p.groups()[0]
            intelObject = {}
            lijstje = p.groups()[0].replace("\t","").replace("}","").replace("{","").replace("class Intel","").replace("\n","").split(";")
            for item in lijstje:
                if item != "":
                    theItem = item.split("=")
                    intelObject[theItem[0]] = theItem[1].strip("\"")


            self.missionObject['intel']  = intelObject #p.groups()[0].replace("\t","").replace("}","").replace("{","").replace("class Intel","").replace("\n","").split(";")


