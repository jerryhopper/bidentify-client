import sys
import os
import re
import csv
from pathlib import Path

def findinlist(exactName):
    #print("Find: "+exactName)
    FoundList = []
    name="arma"
    path = str(Path.home())
    with open(path+"\\"+name+'.bidb', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile,fieldnames=['game','exists','armaholicid','section','name','filename','armaholicpath'])
        for row in reader:
            #print(row['filename'])
            if row['filename'] == exactName:
                #print("Exact Match by name!")
                row['game']=name
                #print(row)
                FoundList.append(row)

                #print(row['game'], row['exists'], row['armaholicid'], row['section'], row['name'], row['filename'], row['armaholicpath'])
            else:
                if str(row['filename']).lower() == str(exactName).lower():
                    #print("Case insensitive Match by name!")
                    row['game']=name
                    #print(row)
                    FoundList.append(row)
                    #print(row['game'], row['exists'], row['armaholicid'], row['section'], row['name'], row['filename'], row['armaholicpath'])
    name="arma2"
    with open(path+"\\"+name+'.bidb', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile,fieldnames=['game','exists','armaholicid','section','name','filename','armaholicpath'])
        for row in reader:
            #print(row)
            if row['filename'] == exactName:
                #print(row[0], row[1], row[2], row[3], row[4])
                #print("Exact Match by name!")
                row['game']=name
                #print(row)
                FoundList.append(row)
                #print(row['game'], row['exists'], row['armaholicid'], row['section'], row['name'], row['filename'], row['armaholicpath'])
            else:
                if str(row['filename']).lower() == str(exactName).lower():
                    #print("Case insensitive Match by name!")
                    row['game']=name
                    #print(row)
                    FoundList.append(row)
                    #print(row['game'], row['exists'], row['armaholicid'], row['section'], row['name'], row['filename'], row['armaholicpath'])
    name="arma2_oa"
    with open(path+"\\"+name+'.bidb', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile,fieldnames=['game','exists','armaholicid','section','name','filename','armaholicpath'])
        for row in reader:
            #print(row)
            if row['filename'] == exactName:
                #print(row[0], row[1], row[2], row[3], row[4])
                #print("Exact Match by name!")
                row['game']=name
                #print(row)
                FoundList.append(row)
                #print(row['game'], row['exists'], row['armaholicid'], row['section'], row['name'], row['filename'], row['armaholicpath'])
            else:
                if str(row['filename']).lower() == str(exactName).lower():
                    #print("Case insensitive Match by name!")
                    row['game']=name
                    #print(row)
                    FoundList.append(row)#print(row['game'], row['exists'], row['armaholicid'], row['section'], row['name'], row['filename'], row['armaholicpath'])
    return FoundList
