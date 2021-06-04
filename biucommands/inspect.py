import sys, getopt
import os
import os.path
import re
import rarfile
import csv
from biucommands.hashfile import hashfile
from biucommands.findinlist import findinlist

def showUsage():
    #print("BI Universe - the definitive tool for identifying Arma-files")
    print("Usage:")
    print(" "+sys.argv[0]+" inspect [-i inputfilename] [-h --help]")


#def detectType(fileName):



def inspect():
    try:
        opts, args = getopt.getopt(sys.argv[2:], "hi:v", ["help", "input="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        showUsage()
        sys.exit(2)
    global output
    output = None
    verbose = False
    #print(args)
    for o, a in opts:

        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            inspectStart()
            sys.exit()
        elif o in ("-i", "--input"):
            output = a
        else:
            assert False, "unhandled option"
    # ...
    if output == None:
        showUsage()
        sys.exit()

    inspectStart()


def rar(fileLocation):
    rf = rarfile.RarFile(fileLocation)
    for f in rf.infolist():
        print(f.filename, f.file_size)
        if f.filename == "README":
            print(rf.read(f))


def inspectStart():
    global output
    if os.path.isfile(output):
        print( "inspecting "+output)
    else:
        print ("ERROR! File not exist (" +output+ ")")
        sys.exit()
    print(" ")
    extensions = [".zip",".exe",".gz",".rar",".7z"]

    gamename = ["ofp","arma","arma2","arma2oa","arma2_oa","arma3"]


    #print(os.path.splitext(output))
    #print(os.path.abspath(output))
    #print(os.path.basename(output))
    #print(os.path.dirname(output))
    #print(os.path.getsize(output))
    #os.path.getctime(output)
    #os.path.getmtime(output)
    #CURRENT_DIR=os.getcwd()
    #os.chdir(CURRENT_DIR)

    fullpath = os.path.abspath(output)
    #print(fullpath)
    fileExtension = os.path.splitext(fullpath)[1]




    if os.path.splitext(fullpath)[1].lower() in extensions :

        #print("fileUri: "+fullpath)

        #print("filePath: "+os.path.dirname(fullpath))
        filePath=os.path.dirname(fullpath)


        #print("parentDirname: "+os.path.basename(filePath))

        #print("exactName: "+os.path.basename(fullpath))
        exactName=os.path.basename(fullpath)

        fileName = os.path.splitext(exactName)[0]
        #print("fileName: "+fileName)


        #print("fileExtension: "+fileExtension)

        fileSize=str(os.path.getsize(fullpath))
        #print("fileSize: "+fileSize)


        #fileName=os.path.splitext(fullpath)[0].split("\\")[-1]
        #print(fileName)
        fileHash=hashfile(fullpath)
        #print("fileHash: "+fileHash)
        #print(os.path.split(fullpath)[0])



        print('exactName: '+ exactName+ ', fileSize:'+ fileSize+', filePath:'+ filePath+',fileName:'+ fileName + ', fileExtension: '+ fileExtension)
        #fileExtension=os.path.splitext(name)[1].lower()
        #print( exactName+","+str(fileSize)+","+root+","+fileName+","+fileExtension )
        #FileListWriter.writerow({'exactName': exactName, 'fileSize': fileSize,'filePath': filePath, 'fileName': fileName, 'fileExtension': fileExtension})
        #print(os.path.join(root, name))

        #if fileExtension == ".rar":
        #    rar(fullpath)
        findinlist(exactName)


















