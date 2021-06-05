import sys, getopt
import os
import re
import csv
from biucommands.hashfile import hashfile

def showUsage():
    print("Usage:")
    print(" "+sys.argv[0]+" scan [-h --help] [-o outputfilename ] [-d directory ] [-v]")


def scandir():
    try:
        opts, args = getopt.getopt(sys.argv[2:], "shod:v", ["scan","help", "output=","directory="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        showUsage()
        sys.exit(2)
    output = None
    directory = None
    verbose = False
    #print(args)
    for o, a in opts:

        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            scanUsage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
        elif o in ("-d", "--directory"):
            directory = a
        else:
            assert False, "unhandled option"
    # ...

    scandirStart(output,directory,verbose)


def scandirStart(output,directory,verbose):
    # setx path "D:\#BiUniverse_git\biuniverse;%path%;"
    # pathman /au D:\#BiUniverse_git\biuniverse
    #global output
    #print(output)


    if output is None:
        if verbose: print("Missing option -o -output, using default 'fileList'")
        output="fileList"
    if directory is None:
        CURRENT_DIR=os.getcwd()
        if verbose: print("Missing option -d -directory, using current directory")
    else:
        CURRENT_DIR=directory
    print()
    print("Scanning... "+CURRENT_DIR)
    print("------------------------------")




    csvFile = open(output+'.bifl', 'w', encoding='utf8')
    FileListWriterFieldNames = ['exactName', 'fileSize','filePath','fileName','fileExtension']
    FileListWriter = csv.DictWriter(csvFile, fieldnames=FileListWriterFieldNames)
    FileListWriter.writeheader()

    csvFile = open(output+'.bidl', 'w', encoding='utf8')
    DirListWriterFieldNames = ['exactName','filePath']
    DirListWriter = csv.DictWriter(csvFile, fieldnames=DirListWriterFieldNames)
    DirListWriter.writeheader()

    extensions = [".zip",".exe",".gz",".rar",".7z"]


    os.chdir(CURRENT_DIR)
    for root, dirs, files in os.walk(".", topdown = False):
       for name in files:
           if os.path.splitext(name)[1].lower() in extensions :
               exactName=name
               filePath=root
               fileName=os.path.splitext(name)[0]
               #fileHash=hashfile(os.path.join(root, name))
               fileSize=str(os.path.getsize(os.path.join(root, name)))
               fileExtension=os.path.splitext(name)[1].lower()
               #print( exactName+","+str(fileSize)+","+root+","+fileName+","+fileExtension )
               FileListWriter.writerow({'exactName': exactName, 'fileSize': fileSize,'filePath': filePath, 'fileName': fileName, 'fileExtension': fileExtension})
           #print(os.path.join(root, name))

       for name in dirs:
           filePath=root
           exactName=name
           #print( exactName+","+filePath )
           #print(os.path.join(root, name))
           DirListWriter.writerow({'exactName': exactName,'filePath': filePath})
    #
    #print("------------------------------")
    if verbose : print("output written to: ")
    if verbose : print(" "+output+".bifl")
    if verbose : print(" "+output+".bidl")

