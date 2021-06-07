import os
import subprocess
import sys
from subprocess import check_output
import shutil
# extractpbodos -P -F=config.bin miroslavl_signs.pbo D:\#BIUniverse

class InspectPbo:

    def __init__(self, fileObject, workingDir):
        self.fileObject = fileObject
        self.workingDir = workingDir

    def list(self):
        path = os.path.join(self.fileObject.get("filePath"),self.fileObject.get("fileName") )
        path2 = os.path.join(self.workingDir,path.replace('.\\',''))
        print("List: "+ path2 )
        try:
            output = check_output("ExtractPboDos.exe -P -LB "+path2, shell=True)
        except FileNotFoundError:
            # handle file not found error.
            a=1
        theContents = []
        number =0
        for line in output.splitlines():
            # we have found a config file!
            if number >=2:
                theContents.append( line.decode() )
            number=number+1
        return theContents


    def extractCfg(self):
        path = os.path.join(self.fileObject.get("filePath"),self.fileObject.get("fileName") )
        path2 = os.path.join(self.workingDir,path.replace('.\\',''))

        pboExtractFolderName= self.fileObject.get("fileName").replace(".pbo","")

        xtractConfigDir = os.path.join(self.workingDir,"_PboContents")
        if os.path.exists(xtractConfigDir) :
            shutil.rmtree( xtractConfigDir )

        #os.path.mkdir( xtractConfigDir )
        #os.path.mkdir( xtractConfigDir )

        print("PATH TO PBO : "+path2)
        if os.path.exists( path2 ):
            print("__________________________________________________")
            print(["extractpbodos", "-P","-F=config.cpp", path2 , xtractConfigDir])

            # extract config from pbo
            command = "ExtractPboDos.exe -P -F=config.cpp"+" "+path2+" "+xtractConfigDir
            output = check_output(command, shell=True)
            for line in output.splitlines():
                print(line.decode())
            print( self.fileObject.get("fileName")  )

            theConfig = os.path.join( os.path.join(self.workingDir,pboExtractFolderName) , "config.cpp" )

            print( theConfig )
            f = open(theConfig, "r")
            print(f.read())





#d = InspectPbo('bogus.pbo')
#e = InspectPbo('Buddy')
#d.add_trick('roll over')
#e.add_trick('play dead')
#d.tricks

