
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










class BIdentifyTestCommand :

    def __init__(self,config):
        print("(BIdentifyTestCommand) init()")
        self.config = config
        self.optionVerbose = False
        contentPath = "example"+os.path.sep+"contentdirectory"+os.path.sep
        print( os.getcwd() )

        self.inspectTest(contentPath+"bogus.pbo")


    def inspectTest(self , path):
        print("bidentify -f "+path )

        InspectCommand = BIdentifyInspectCommand(self.config)
        InspectCommand.setVerbosity(self.optionVerbose)

        InspectCommand.setDirectory(os.getcwd())
        InspectCommand.setSelectedFile(path)

        InspectCommand.inspect()
