import sys, getopt
import os
import re
import csv


def showUsage():
    #print("BI Universe - the definitive tool for identifying Arma-files")
    print("Usage:")
    print(" "+sys.argv[0]+" analyze [-h --help] [-d --directory] [-i --input]")






def analyzeFile(name):
    #
    with open(name+'.bifl', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row['exactName'], row['fileSize'], row['filePath'], row['fileName'], row['fileExtension'])

def analyzeDir(name):
    #
    with open(name+'.bidl', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row['exactName'], row['filePath'])

def analyze():
    try:
        opts, args = getopt.getopt(sys.argv[2:], "hdi:v", ["help","directory","input"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        showUsage()
        sys.exit(2)
    global output
    output = None
    verbose = False
    directory = None
    #print(args)
    for o, a in opts:

        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            showUsage()
            sys.exit()
        elif o in ("-d", "--directory"):
            directory = a
        elif o in ("-i", "--input"):
            output = a
        else:
            assert False, "unhandled option"
    # ...

    analyzeStart(output,directory,verbose)

def analyzeStart(output,directory,verbose):
    # setx path "D:\#BiUniverse_git\biuniverse;%path%;"
    # pathman /au D:\#BiUniverse_git\biuniverse
    #global output
    #print(output)

    if output is None:
        print("Missing option -o -output, using default 'fileList'")
        output="fileList"
    if directory is None:
        print("Missing option -d -directory, using current directory")
        CURRENT_DIR=os.getcwd()
    else:
        CURRENT_DIR=directory


    if verbose: print("Using input files: ")
    if verbose: print(" "+output+".bifl")
    if verbose: print(" "+output+".bidl")


    print("Analyzing... "+CURRENT_DIR )
    print("------------------------------")

    #os.chdir(os.path.dirname(__file__))
    #print(CURRENT_DIR)

    extensions = [".zip",".exe",".gz",".rar",".7z"]

    gamename = ["ofp","arma","arma2","arma2oa","arma2_oa","arma3"]

    #analyzeFile(output)
    analyzeDir(output)





