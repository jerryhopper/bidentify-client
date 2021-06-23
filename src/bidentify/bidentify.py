import os
import sys, getopt

from bidentify.update import BIdentifyUpdateCommand

from bidentify.scandir import BIdentifyScanCommand




class BIdentify:

    # bidentify -h
    # bidentify scan -d c:\directory  -h
    # bidentify analyze -d c:\directory -h
    # bidentify update -s http://bidentify.jerryhopper.com -h


    def __init__(self, config):
        self.config = config

        self.optionVerbose = self.config.get('optionVerbose')
        if self.optionVerbose : print("Initial verbosity is "+str(self.optionVerbose))

        self.optionDirectory = os.getcwd()
        self.optionFile = None
        self.optionHelp= False

        #print("BIdentify->init")

        #print("optionDirectory:"+self.optionDirectory)

        self.type="dirCommand"
        #self.type="fileCommand"


    def start(self):
        # File-specific commands.
        if sys.argv[1] == "update":
            self.NoArguments()
            self.doUpdate()
            sys.exit()
        if sys.argv[1] == "scan":
            self.type="dirCommand"
            self.DirectoryArguments()
            self.doScan()
            #self.doAnalyze()
            sys.exit()
        self.showUsage()







    def showUsage(self):
        print("Usage:")
        print(" "+self.config.get('EXENAME')+" scan (-h --help)")

    def doTest(self):
        testCommand = BIdentifyTestCommand(self.config)
        #testCommand.setVerbosity(self.optionVerbose)


    def doUpdate(self):
        # update
        UpdateCommand = BIdentifyUpdateCommand(self.config)
        UpdateCommand.setVerbosity(self.optionVerbose)
        if self.optionHelp:
            UpdateCommand.showUsage()
            sys.exit()
        UpdateCommand.update()


    def doScan(self):
        # initialisation.
        ScanCommand = BIdentifyScanCommand(self.config)
        # set Verbosity
        ScanCommand.setVerbosity(self.optionVerbose)

        # check if help is requested.
        if self.optionHelp:
            ScanCommand.showUsage()
            sys.exit()

        # check if directory exists
        if not os.path.exists(self.optionDirectory):
            print("FATAL: directory '"+self.optionDirectory+"'does not exist.")
            sys.exit()

        # set the directory.
        ScanCommand.setDirectory(self.optionDirectory)

        # scan
        ScanCommand.scandir()

        # analyze
        #self.doAnalyze()



    # bidentify update -h --help -v --verbose
    #
    # bidentify scan -d --directory -h --help -v --verbose
    # bidentify analyze -d --directory -h --help -v
    #
    # bidentify inspect -f --file -h --help -v --verbose
    # bidentify submit -f --file -h --help -v --verbose

    def DirectoryArguments(self):
        try:
            opts, args = getopt.getopt(sys.argv[2:], "d:hv", ["directory=","help","verbose"])
        except getopt.GetoptError as err:
            # print help information and exit:
            print(err)  # will print something like "option -a not recognized"
            #self.showUsage()
            sys.exit(2)
        for o, a in opts:

            if o in ("-d", "--directory"):
                self.optionDirectory = a
            elif o in ("-h", "--help"):
                self.optionHelp = True
                #sys.exit()
            elif o == "-v":
                print("verbose was set to : True")
                self.optionVerbose = True
            else:
                assert False, "unhandled option"
        #sys.exit()
        # ...

    def FileArguments(self):
        try:
            opts, args = getopt.getopt(sys.argv[2:], "f:hv", ["file=","help","verbose"])
        except getopt.GetoptError as err:
            # print help information and exit:
            print(err)  # will print something like "option -a not recognized"
            #self.showUsage()
            sys.exit(2)

        verbose = False
        #print(args)
        for o, a in opts:

            if o == "-v":
                self.optionVerbose = True
            elif o in ("-h", "--help"):
                self.optionHelp = True
            elif o in ("-f", "--file"):
                self.optionFile = a
            else:
                assert False, "unhandled option"
        # ...

    def NoArguments(self):
        try:
            opts, args = getopt.getopt(sys.argv[2:], "hv", ["help","verbose"])
        except getopt.GetoptError as err:
            # print help information and exit:
            print(err)  # will print something like "option -a not recognized"
            #self.showUsage()
            sys.exit(2)

        verbose = False
        #print(args)
        for o, a in opts:
            if o == "-v":
                self.optionVerbose = True
            elif o in ("-h", "--help"):
                self.optionHelp = True
            else:
                assert False, "unhandled option"
        # ...









