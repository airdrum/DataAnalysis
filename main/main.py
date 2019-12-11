import telnetlib
import sys,os
import time
import re 
from statistics import mean , stdev
from _winapi import ReadFile
import xlsxwriter
from openpyxl import load_workbook
import math
import shutil
from numpy import number
import pandas as pd

class DataAnalyzer:
        # Initializer / Instance Attributes
    def __init__(self,filepath, name):
        self.filepath = filepath
        self.name = name
        
    def listFiles(self):
        fileArray = []
 
        files = os.listdir(self.filepath)
        for name in files:
            fileArray.append(name)

        return fileArray
    
    def getAbsolutePath(self):
        absFile=self.filepath + '\\' +self.name
        return absFile
    
    def readFile(self):
        file = open(self.getAbsolutePath(), "r")
        fileStr = file.read()
        numarray=[]
        time=[]
        count=0
        for string in fileStr.splitlines():
            count+=1
            numbers = string.split(',')
            samet=0.0
            if numbers[2]=="\"bits/sec\"" or numbers[2]=="\"Kbits/sec\"":
                samet = round(float(numbers[1].replace("\"",""))*0.001,2)
            elif numbers[2]=="\"Mbits/sec\"":
                samet= round(float(numbers[1].replace("\"","")),2)
            else:
                print(str(count)+"-NONE")
                continue
            try:
                numarray.append(samet)
                time.append(numbers[0])
            except:
                print(str(count)+"-SKIPPED")
        return numarray, time

    
    

filename="C:\\Users\\sametyildiz\\Google Drive\\PhD\\Backup Data\\CSV files"
fsothroughput = DataAnalyzer(filename,"fsothroughput.csv")


"""df = pd.read_csv(fsothroughput.getAbsolutePath())
i=0
fsoarray=[]
while i < len(df.fso):
    num = 0.0
    if df.fsopacket[i] =="Kbits/sec":
        num=num*0.001
        fsoarray.append(round(num,2))
    elif  df.fsopacket[i] =="bits/sec": 
        num=num*0.001
        fsoarray.append(round(num,2))
    elif  df.fsopacket[i] =="Mbits/sec": 
        num=num*0.001
        fsoarray.append(round(num,2))
    
        
"""
fsoarray , time = fsothroughput.readFile()
print(fsoarray)