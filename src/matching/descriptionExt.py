

import re
import pprint



class descriptionExt {

    def __init__(self, textString , verbose = False):
        self.optionVerbose = verbose
        self.optionVerbose : print("(matching\descriptionExt) init()")

        self.textString = textString
        self.descriptionObject = {}
        #self.descriptionObject = {}
        self.matchDescriptionExt()

    def getAll(self):
        return self.descriptionObject


    def matchDescriptionExt(self):



        p = re.search('class Header\[\]=[\n,\n,\t]{([\n,\t,\",A-z,0-9,]*)};',self.textString)


        #p = re.search("version=(.*);",rawConfig)
        #if p is not None:
        #    print("(InspectPbo) matchMissionSqf - Version found!")
        #    version = p.groups()[0]




        sys.exit()
}
