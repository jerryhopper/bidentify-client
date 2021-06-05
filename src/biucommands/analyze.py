import sys, getopt
import os
import re
import csv
from biucommands.findinlist import findinlist


def showUsage():
    #print("BI Universe - the definitive tool for identifying Arma-files")
    print("Usage:")
    print(" "+sys.argv[0]+" analyze [-h --help] [-d --directory] [-i --input]")






def analyzeFiles(name):
    #
    results = []
    # Open the bidentify file-list ()
    with open(name+'.bifl', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #print(row['exactName'], row['fileSize'], row['filePath'], row['fileName'], row['fileExtension'])
            # Attempt to find the record in the bidentify-database.
            foundFiles=findinlist(row['exactName'])
            for foundFile in foundFiles:
                #print (row)
                if len(foundFile) != 0:
                    test = {'localFile': row, 'foundFiles':foundFiles }
                    results.append(test)
    return results;
    #print(results)


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

def writeAnalyzeResults(results):

    csvFile = open('found.txt', 'w', encoding='utf8')
    FileListWriterFieldNames = ['localFile']
    FileListWriter = csv.DictWriter(csvFile, fieldnames=FileListWriterFieldNames)
    FileListWriter.writeheader()

    print('The following files matched the bidentify lists')
    for line in results:
        print(line['localFile']['filePath']+"\\"+line['localFile']['exactName'])
        #print(line['localFile']['filePath'])
        #line['exists']
        FileListWriter.writerow({'localFile': line['localFile']['filePath']+"\\"+line['localFile']['exactName'] })



def analyzeStart(output,directory,verbose):
    # setx path "D:\#BiUniverse_git\biuniverse;%path%;"
    # pathman /au D:\#BiUniverse_git\biuniverse
    #global output
    #print(output)

    if output is None:
        if verbose: print("Missing option -o -output, using default 'fileList'")
        output="fileList"
    if directory is None:
        if verbose: print("Missing option -d -directory, using current directory")
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

    results = analyzeFiles(output)
    #print(results)
    writeAnalyzeResults(results)
    #analyzeDir(output)





