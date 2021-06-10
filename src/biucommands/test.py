
import os

class BIdentifyTestCommand :

    def __init__(self,config):
        print("(BIdentifyTestCommand) init()")
        self.config = config
        self.optionVerbose = False

        print( os.getcwd() )
