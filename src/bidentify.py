# !/usr/bin/python3

import sys, getopt

from biucommands.scandir import scandir
from biucommands.analyze import analyze
from biucommands.update import update
from biucommands.inspect import inspect
from biucommands.hashfile import hashfile
from biucommands.findinlist import findinlist

def showUsage():
    print("Usage:")
    print(" "+sys.argv[0].split("\\")[-1]+" scan (-h --help)")
    print(" "+sys.argv[0].split("\\")[-1]+" update (-h --help)")
    print(" "+sys.argv[0].split("\\")[-1]+" analyze (-h --help)")
    print(" "+sys.argv[0].split("\\")[-1]+" inspect (-h --help)")



def main():
    if len(sys.argv)==1:
        showUsage()
        sys.exit()

    if sys.argv[1] == "scan":
        scandir()
        analyze()
        sys.exit()
    if sys.argv[1] == "analyze":
        analyze()
        sys.exit()
    if sys.argv[1] == "update":
        update()
        sys.exit()
    if sys.argv[1] == "inspect":
        inspect()
        sys.exit()
    showUsage()
    sys.exit()



if __name__ == "__main__":
    main()


