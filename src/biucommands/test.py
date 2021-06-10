
import os
from biucommands.hashfile import hashfile
from biucommands.findinlist import findinlist

from biucommands.inspect_pbo import InspectPbo
from biucommands.inspect_archive import InspectArchive

from bidentify.fileobject import myFileObject


from bidentify.update import BIdentifyUpdateCommand

from biucommands.scandir import BIdentifyScanCommand
from biucommands.analyze import BIdentifyAnalyzeCommand

from biucommands.inspect import BIdentifyInspectCommand



import pprint






class BIdentifyTestCommand :

    def __init__(self,config):
        print("(BIdentifyTestCommand) init()")
        self.config = config
        self.optionVerbose = False
        self.contentPath = "example"+os.path.sep+"contentdirectory"+os.path.sep
        print( os.getcwd() )


        self.inspectAddonPbo()
        self.inspectAddonArchive()

        self.inspectMissionPbo()




    def testresult(self, what,result):
        print("Test `"+what+"` : "+str(result))


    def inspectMissionPbo(self):
        path = self.contentPath+"Assassination.Stratis.rar"
        InspectCommand = BIdentifyInspectCommand(self.config)
        InspectCommand.setVerbosity(self.optionVerbose)

        InspectCommand.setDirectory(os.getcwd())
        InspectCommand.setSelectedFile(path)

        data = InspectCommand.inspect()
        #pprint.pprint(data)

        print("=============================================")
        print ("Testing "+path)
        self.testresult( 'contains', data['contains'] == "mission" )
        self.testresult( 'fileHash', data['fileHash'] == "ee66bbfa6773226319a37ea06bc7b1f4" )
        self.testresult( 'fileName', data['fileName'] == "Assassination.Stratis.rar" )
        self.testresult( 'fileContentsList', len(data['fileContentsList']) == 1 )
        self.testresult( 'fileContentsList-filename', data['fileContentsList'][0]['fileName'] == "mission.sqm")
        self.testresult( 'fileContentsList-filetype', data['fileContentsList'][0]['fileType'] == ".sqm")
        self.testresult( 'fileContentsList-missionconfig', len (data['fileContentsList'][0]['missionconfig']) == 3)















    def inspectAddonArchive(self):
        path = self.contentPath+"test_addons.zip"

        print("bidentify -f "+path )

        InspectCommand = BIdentifyInspectCommand(self.config)
        InspectCommand.setVerbosity(self.optionVerbose)

        InspectCommand.setDirectory(os.getcwd())
        InspectCommand.setSelectedFile(path)

        data = InspectCommand.inspect()

        #pprint.pprint(data)
        print("=============================================")
        print ("Testing "+path)
        self.testresult( 'contains', data['contains'] == "addon" )
        self.testresult( 'fileHash', data['fileHash'] == "485eb3a0eaa92b2f248595b279884dda" )

        self.testresult( 'fileContentsList', len(data['fileContentsList']) == 4 )
        test = False
        for item in data['fileContentsList']:
            if item['fileHash']=="ce28c6b31c6fddf93ab2b5d217441916":
                test == True
        self.testresult( 'fileContentsListItem', test )
        print("=============================================")




    def inspectAddonPbo( self ):

        path = self.contentPath+"bogus.pbo"

        print("bidentify -f "+path )

        InspectCommand = BIdentifyInspectCommand(self.config)
        InspectCommand.setVerbosity(self.optionVerbose)

        InspectCommand.setDirectory(os.getcwd())
        InspectCommand.setSelectedFile(path)

        data = InspectCommand.inspect()

        print("=============================================")
        print ("Testing "+path)
        self.testresult( 'author', data['pboconfig']['author'] == "Jerry Hopper" )
        self.testresult( 'author', data['pboconfig']['className'] == "nul_nonsense" )
        self.testresult( 'filename', data['pboconfig']['filename'] is None )
        self.testresult( 'prefix-addons', data['pboconfig']['prefix'] ['addons']== None )
        self.testresult( 'prefix-intel', data['pboconfig']['prefix'] ['intel']== None )
        self.testresult( 'prefix-version', data['pboconfig']['prefix'] ['version']== None )

        self.testresult( 'requiredAddons', ('cwr3_Core' in data['pboconfig']['requiredAddons']) == ('cwr3_Core' in data['pboconfig']['requiredAddons']) == True )

        self.testresult( 'requiredVersion', data['pboconfig']['requiredVersion'] == "0.1" )
        self.testresult( 'url', data['pboconfig']['url'] == "http : //cwr3.arma2.fr" )
        self.testresult( 'version', data['pboconfig']['version'] == "0.1" )
        print("=============================================")
