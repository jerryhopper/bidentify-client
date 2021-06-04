import sys, getopt
import os
import re
import csv
import urllib.request
from pathlib import Path


print(sys.version)

def showUsage():
    #print("BI Universe - the definitive tool for identifying Arma-files")
    print("Usage:")
    print(" "+sys.argv[0]+" update [-h --help]")



def update():
    try:
        opts, args = getopt.getopt(sys.argv[2:], "h:v", ["help"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        showUsage()
        sys.exit(2)
    global output
    output = 'http://bidentify.jerryhopper.com'
    verbose = False
    #print(args)
    for o, a in opts:

        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            showUsage()
            sys.exit()
        elif o in ("-i", "--input"):
            output = a
        else:
            assert False, "unhandled option"
    # ...

    updateStart()





def updateStart():
    # setx path "D:\#BiUniverse_git\biuniverse;%path%;"
    # pathman /au D:\#BiUniverse_git\biuniverse
    global output
    #print(output)
    # http://ftp.armedassault.info/armaholic/arma.armaholic.txt
    # http://ftp.armedassault.info/armaholic/arma2.armaholic.txt
    # http://ftp.armedassault.info/armaholic/arma2_os.armaholic.txt
    home = str(Path.home())

    
    print("Updating Arma file index, using bidentify server at " +output)
    try:
        urllib.request.urlretrieve(output+"/armaholic/arma.bidb",home+"/arma.bidb")
    except ( urllib.error.URLError,urllib.error.HTTPError) as e:
        print (e)
        
    print("Updating Arma2 file index.")
    try:
        urllib.request.urlretrieve(output+"/armaholic/arma.bidb",home+"/arma2.bidb")
    except ( urllib.error.URLError,urllib.error.HTTPError) as e:
        print (e)

    print("Updating Arma2_OA file index.")
    try:
        urllib.request.urlretrieve(output+"/armaholic/arma2_oa.bidb",home+"/arma2_oa.bidb")
    except ( urllib.error.URLError,urllib.error.HTTPError) as e:
        print (e)
    print("updates downloaded to: "+home)












