import telnetlib
import sys,os
import time
import re 
from statistics import mean , stdev
import xlsxwriter
from openpyxl import load_workbook
import math
import shutil
from numpy import number
from datetime import datetime
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
        absFile=self.filepath + '/' +self.name
        return absFile
    
    def round_time(self,key):
        minute = int(key.split(":")[-2])
        date = int(key.split(":")[0].split("-")[0])
        hour = int(key.split(":")[0].split("-")[1])
        
        seconds = round(float(key.split(":")[-1])*2)/2.0
        if seconds>=60.0:
            minute = minute +1
            seconds = 0.0
        
        if minute>=60.0:
            hour = hour+1
            minute= 0.0
            
        if hour >=24:
            date = date +1
            if date==20190931:
                date=20191001
            elif date==20190832:
                date=20190901
            elif date==20190732:
                date=20190801
            hour=0.0
                    
        if seconds < 10.0:
            tmp = str('%02d' % int(str(seconds).split(".")[0])) + ':'+str(seconds).split(".")[1]
            seconds =tmp
        return (str(date)+"-"+str('%02d' % hour)+":"+str('%02d' % minute)+":"+str(seconds) )
            
            
    
    def readFile(self):
        file = open(self.getAbsolutePath(), "r")
        fileStr = file.read()
        numarray=[]
        timearray=[]
        count=0
        for string in fileStr.splitlines():
            
            if "/sec" in string:
                try:
                    number  = string.split(',')[1].split(' ')[0]
                    tmpval  = string.split(',')[1].split(' ')[1]
                    timeval = string.split(',')[0].split(' ')[1]
                    if tmpval == "Mbits/sec":
                        numarray.append(round(float(number),2))
                        timearray.append(self.round_time(timeval))
                    elif tmpval == "Kbits/sec":
                        numarray.append(round(float(number)*0.001,2))
                        timearray.append(self.round_time(timeval))
                    elif tmpval == "bits/sec":
                        numarray.append(round(float(number)*0.001,2))
                        timearray.append(self.round_time(timeval))
                except:
                    print(count)
                    print("EXCEPTION")
            count+=1    
                
        return numarray, timearray

now = datetime. now()
current_time = now. strftime("%H:%M:%S")
print("Current Time =", current_time)
    

filename="/home/sy/Backup Data"
fsothroughput = DataAnalyzer(filename,"FSO_before_20191027.txt")
rfthroughput = DataAnalyzer(filename,"RF_before_20191027.txt")


throughput_fso , time_fso = fsothroughput.readFile()
thoruhgput_rf , time_rf = rfthroughput.readFile()

now = datetime. now()
current_time = now. strftime("%H:%M:%S")
print("Current Time =", current_time)



