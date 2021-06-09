


import re
import pprint

class configCpp {

    def __init__(self, textString, verbose = False ):
        self.optionVerbose = verbose
        self.optionVerbose : self.optionVerbose : print("(matching\configCpp) init()")

        self.textString = textString

        self.configObject = {}
        self.configObject['className'] = None
        self.configObject['requiredVersion'] = None
        self.configObject['requiredAddons'] = None
        self.configObject['version'] = None
        self.configObject['name'] = None
        self.configObject['filename'] = None
        self.configObject['author'] = None
        self.configObject['mail'] = None
        self.configObject['url'] = None

        self.matchConfigCpp()
        
    def getAll(self):
        return self.configObject

    def matchConfigCpp(self):


        #p = re.compile("/^class ([A-z].*)[\s,\S]{([\s,\S]{,}?^\});/")
        #p = re.search("class (CfgPatches)[\s,\S]({[\s,\S]*?\}[\s,\S]*?\}[\s,\S]*?\}[\s,\S]*?\}[\s,\S]*?\});",config['config.cpp'])
        #print(rawConfig)
        p = re.findall("class CfgPatches[\s,\S]{([\s,\S]*?\}[\s,\S]*?\}[\s,\S]*?\}[\s,\S]*?\}[\s,\S]*?)\};",self.textString)
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

        return
}
