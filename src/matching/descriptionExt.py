import re
import pprint
import pprint

class descriptionExt {

    def __init__(self, fileLocation , verbose = False):
        # set verbosity
        self.optionVerbose = verbose
        if self.optionVerbose : print("(matching\descriptionExt) init()")

        # open file.
        f = open(os.path.abspath(fileLocation), "r") # ,encoding='utf-8'
        self.textString =  = f.read()
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



        p = re.search('class Header\[\]=[\n,\n,\t]{([\n,\t,\",A-z,0-9,]*)};',self.textString)


        #p = re.search("version=(.*);",rawConfig)
        #if p is not None:
        #    print("(InspectPbo) matchMissionSqf - Version found!")
        #    version = p.groups()[0]




        sys.exit()
}
