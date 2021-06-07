# !/usr/bin/python3
import os
import sys, getopt



from bidentify.bidentify import BIdentify
from bidentify.config import BIdentifyConfig


#from biucommands.scandir import scandir
#from biucommands.analyze import analyze
#from biucommands.update import update
#from biucommands.inspect import inspect
#from biucommands.hashfile import hashfile
#from biucommands.findinlist import findinlist

#def showUsage():
#    print("Usage:")
#    print(" "+sys.argv[0].split("\\")[-1]+" scan (-h --help)")
#    print(" "+sys.argv[0].split("\\")[-1]+" update (-h --help)")
#    print(" "+sys.argv[0].split("\\")[-1]+" analyze (-h --help)")
#    print(" "+sys.argv[0].split("\\")[-1]+" inspect (-h --help)")




def main():
    # Init config
    config = BIdentifyConfig()
    # Init instance
    Instance = BIdentify(config)

    #identify.update()

    # if no arguments, show usage.
    if len(sys.argv)==1:
        Instance.showUsage()
        sys.exit()
    Instance.start()
    sys.exit()




if __name__ == "__main__":
    main()


