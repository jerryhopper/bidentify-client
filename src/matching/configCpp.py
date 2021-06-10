import re
import os
import pprint

class configCpp:

    def __init__(self, fileLocation, verbose = False ):
        # set verbosity
        self.optionVerbose = verbose
        if self.optionVerbose : print("(matching\configCpp) init()")

        # open file.
        f = open(os.path.abspath(fileLocation), "r") # ,encoding='utf-8'
        self.textString   = f.read()
        f.close()

        #########################################
        # Object definition
        #########################################
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
        #########################################

        self.matchConfigCpp()

    def getAll(self):
        return self.configObject

    def matchConfigCpp(self):
        if self.optionVerbose : print("(configCpp) matchConfigCpp")
        if self.optionVerbose : print(self.textString)

        #p = re.compile("/^class ([A-z].*)[\s,\S]{([\s,\S]{,}?^\});/")
        #p = re.search("class (CfgPatches)[\s,\S]({[\s,\S]*?\}[\s,\S]*?\}[\s,\S]*?\}[\s,\S]*?\}[\s,\S]*?\});",config['config.cpp'])
        #print(rawConfig)
        p = re.findall("class CfgPatches[\s,\S]{([\s,\S]*?\}[\s,\S]*?\}[\s,\S]*?\}[\s,\S]*?\}[\s,\S]*?)\};",self.textString)
        if p is None:
            if self.optionVerbose : print("(configCpp) matchConfigCpp : Nothing found in config.cpp")
            return None
        configPatches = p[0].replace("\t","")


        p = re.search("class ([A-z,0-9,\_].*)",configPatches)
        if p : self.configObject['className'] = p.groups()[0]



        p = re.search("requiredVersion\s=\s(.*);",configPatches)
        if p : self.configObject['requiredVersion'] = p.groups()[0]

        p = re.search("requiredAddons\[\]\s=\s(.*);",configPatches)
        if p : self.configObject['requiredAddons'] = p.groups()[0].replace('"',"").replace("{","").replace("}","").split(",")

        p = re.search("version\s=\s(.*);",configPatches)
        if p : self.configObject['version'] = p.groups()[0]

        p = re.search("name\s=\s(.*);",configPatches)
        if p : self.configObject['name'] = p.groups()[0].replace('"',"")

        p = re.search("fileName\s=\s(.*);",configPatches)
        if p : self.configObject['filename'] = p.groups()[0].replace('"',"")

        p = re.search("author\s=\s(.*);",configPatches)
        if p : self.configObject['author'] = p.groups()[0].replace('"',"")

        p = re.search("mail\s=\s(.*);",configPatches)
        if p : self.configObject['mail'] = p.groups()[0].replace('"',"")

        p = re.search("url\s=\s(.*);",configPatches)
        if p : self.configObject['url'] = p.groups()[0].replace('"',"")


