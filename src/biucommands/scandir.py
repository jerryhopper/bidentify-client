import sys, getopt
import os
import re
import csv
from biucommands.hashfile import hashfile
       
def showUsage():
    #print("BI Universe - the definitive tool for identifying Arma-files")
    print("Usage:")
    print(" "+sys.argv[0]+" scan [-h --help] [-o outputfilename ]")


def scandir():
    try:
        opts, args = getopt.getopt(sys.argv[2:], "sho:v", ["scan","help", "output="])
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
            scandirStart()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unhandled option"
    # ...
    
    scandirStart()


def scandirStart():
    # setx path "D:\#BiUniverse_git\biuniverse;%path%;"
    # pathman /au D:\#BiUniverse_git\biuniverse
    global output
    #print(output)

    
    if output is None:
        output="fileList"
    
    CURRENT_DIR=os.getcwd()
    print("Scanning directory: "+CURRENT_DIR)
    print("------------------------------")
    
    #os.chdir(os.path.dirname(__file__))
    #print(CURRENT_DIR)




       
    csvFile = open(output+'.bifl', 'w', encoding='utf8')
    FileListWriterFieldNames = ['exactName', 'fileSize','filePath','fileName','fileExtension']
    FileListWriter = csv.DictWriter(csvFile, fieldnames=FileListWriterFieldNames)
    FileListWriter.writeheader()

    csvFile = open(output+'.bidl', 'w', encoding='utf8')
    DirListWriterFieldNames = ['exactName','filePath']
    DirListWriter = csv.DictWriter(csvFile, fieldnames=DirListWriterFieldNames)
    DirListWriter.writeheader()




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
    print("output written to: ")
    print(" "+output+".bifl")
    print(" "+output+".bidl")
    
