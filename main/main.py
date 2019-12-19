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
import pandas as pd
#import dill
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import datetime as dt
# Python code to illustrate
# inserting data in MongoDB
#from pymongo import MongoClient

import sys
from cmath import nan


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
        absFile=self.filepath +'\\'+self.name
        return absFile

    def readWeather(self):
        file = open(self.getAbsolutePath(), "r")
        fileStr = file.read()
        numarray=[]
        timearray=[]
        count=0
        for string in fileStr.splitlines():
            #20190730-09:42:40.4


            timeval = string.split(',')[0].replace("Weather:","")
            #InTemp:86.0,InHum:49.0,OutTemp:75.5,WindS:6.0,WindD:355.0,OutHum:83.0,UV:0.0,SolRad:0.0
            intemp = str(round(float(string.split(',')[1].replace("InTemp:","")),2))
            inhum = str(round(float(string.split(',')[2].replace("InHum:","")),2))
            outtemp = str(round(float(string.split(',')[3].replace("OutTemp:","")),2))
            winds = str(round(float(string.split(',')[4].replace("WindS:","")),2))
            windd = str(round(float(string.split(',')[5].replace("WindD:","")),2))
            outhum = str(round(float(string.split(',')[6].replace("OutHum:","")),2))
            uv = str(round(float(string.split(',')[7].replace("UV:","")),2))
            solrad = str(round(float(string.split(',')[8].replace("SolRad:","")),2))
            print(self.round_time(timeval)+','+intemp+','+inhum+','+outtemp+','+winds+','+windd+','+outhum+','+uv+','+solrad)
            """numarray.append(round(float(number),2))
            timearray.append(self.round_time(timeval))"""

            count+=1

        return numarray, timearray

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
            tmp = str('%02d' % int(str(seconds).split(".")[0])) + '.'+str(seconds).split(".")[1]
            seconds =tmp

        x=str(date)
        date_str_new= x[0]+x[1]+x[2]+x[3]+"-"+x[4]+x[5]+"-"+x[6]+x[7]
        #objDate = datetime.strptime(, '%y%m%d')
        final_datetime = str(date_str_new)+" " +str('%02d' % hour)+":"+str('%02d' % minute)+":"+str(seconds)
        #datetime_object_final = datetime.strptime(final_datetime, '%Y-%m-%d %H:%M:%S.%f')
        return final_datetime

    def printFile(self):
        file = open(self.getAbsolutePath(), "r")
        fileStr = file.read()
        for i in fileStr.splitlines():
            print(i)

    def getFileStr(self):
        file = open(self.getAbsolutePath(), "r")
        fileStr = file.read()
        return fileStr

    def readFile(self):
        file = open(self.getAbsolutePath(), "r")
        fileStr = file.read()
        numarray=[]
        timearray=[]
        count=0
        for string in fileStr.splitlines():
            #20190730-09:42:40.4
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
                    print(str(count)+" - EXCEPTION")
            count+=1

        return numarray, timearray
"""def pushToDatabaset(rf):
    conn = MongoClient('localhost',27017)

    # database
    db = conn.example
    # Created or Switched to collection names: my_gfg_collection
    collection = db.throughput_collection_fso
    #collection_fso = db.throuhgput_collection_fso

    for i in rf.splitlines():
        time = i.split(",")[0]

        throughput = i.split(",")[1]

        dbobject = {
                "time": time,
                "throughput":throughput
                }
        rec_id1 = collection.insert_one(dbobject)
        print("Data inserted with record ids",rec_id1)
"""
def compare_time_throughput(time_rf,time_fso,throughput_rf,throughput_fso):
    i=0
    time_ind_for_fso=[]
    time_ind_for_rf=[]
    tmp=0
    total_array = []
    while i < len(time_rf):

        throughput = []
        try:
            if time_rf[i] in time_fso:
                condition =True
                print(time_rf[i], end =",")
                print(throughput_rf[i], end =",")
                #print("RF: " + time_rf[i])
                while condition:
                    if time_rf[i] != time_fso[tmp]:
                        tmp+=1
                    else:
                        #print("FSO: " + time_fso[tmp])
                        print(throughput_fso[i])
                        condition = False

            else:
                print(str(i) + " - SKIPPED")
                #time_ind_for_fso.append(1)
                #time_ind_for_rf.append(time_fso.index(i))
        except:
            print("Nope")
        total_array.append(throughput)
        i += 1

    return total_array

def checkDuplicate(rf):
    oldtime=""
    for i in rf:
        if oldtime != i.split(',')[0]:
            print(i.split(',')[0]+','+i.split(',')[1])
            oldtime = i.split(',')[0]
        else:
            print("Hop")

def printFso(timeval, rf, fso):
    r_ind=0
    f_ind=0
    cnt_rf = 0
    cnt_fso=0
    for time_tmp in timeval:
        time_str=time_tmp
        tptval_rf =""
        tptval_fso =""
        if time_tmp == rf[r_ind].split(',')[0]:
            tptval_rf = rf[r_ind].split(',')[1]
            time_str = time_str + ',' + rf[r_ind].split(',')[1]
            r_ind+=1
        else:
            time_str = time_str + ',NORF'

        if time_tmp == fso[f_ind].split(',')[0]:
            tptval_fso = fso[f_ind].split(',')[1]
            time_str = time_str + ',' + fso[f_ind].split(',')[1]
            f_ind+=1
        else:
            time_str = time_str + ',NOFSO'
        #print(time_str)

        if tptval_rf != "" and tptval_fso != "":
            if float(tptval_rf) >= float(tptval_fso):
                cnt_rf +=1
                print("RF:"+str(cnt_rf))
            else:
                cnt_fso +=1
                print("FSO:"+str(cnt_fso))

    print(cnt_rf)
    print(cnt_fso)

def printWeather(timeval, weather):
    r_ind=0

    for time_tmp in timeval:
        time_str=time_tmp
        tptval_rf =""
        if time_tmp == weather[r_ind].split(',')[0]:
            tptval_rf = ','.join(weather[r_ind].split(',')[1:])
            time_str = time_str + ','+tptval_rf
            r_ind+=1
        else:
            time_str = time_str + ',NOWEATHER'

        print(time_str)

def printWeatherline(weather):
    count=1
    for time_tmp in weather:
        if 'NOWEATHER' in time_tmp:
            #if weather[count-1].split(',')[0] == time_tmp.split(',')[0]:
            print(time_tmp.split(',')[0]+','+','.join(weather[count-2].split(',')[1:]))
        else:
            print(time_tmp)
        count+=1

def printall(timeval, weather):
    count=0
    for time_tmp in timeval:
        print(time_tmp +","+','.join(weather[count].split(',')[1:]))
        count+=1


def printKeyInterval(timeval, key):
    count=0
    samet=0
    keyval_array=[]
    exit_flag=True
    tmp=0
    old_flag = True
    for time_tmp in timeval:
        if key in time_tmp:
            keyval_array.append(count)

        count+=1

    print(keyval_array)


#printWeatherline(weather_data)
#rfthroughput.printFile()
def getNoneElementsOneArray(fso):
    counter=0
    none_counter=0
    index_list = []
    last_remaining_index_old = 0
    while counter < len(fso):
        if fso[counter]==None:

            none_counter +=1
            if none_counter ==1:
                last_remaining_index_old = counter
        else:
            if none_counter >1:
                index_list.append([last_remaining_index_old,none_counter])
            none_counter=0
        counter+=1
    return index_list


def getNoneElementsTwoArray(fso,rf):
    counter=0
    none_counter=0
    index_list = []
    last_remaining_index_old = 0
    while counter < len(fso):
        if fso[counter]==None and rf[counter]==None:

            none_counter +=1
            if none_counter ==1:
                last_remaining_index_old = counter
        else:
            if none_counter >1:
                index_list.append([last_remaining_index_old,none_counter])
            none_counter=0
        counter+=1
    return index_list

def printPrevious(noneElements,main_array):

    out_array = main_array
    timearray=[]
    count = 0
    index_end=0
    index_count=0
    k=0
    i=0
    while i <len(main_array):

        if k <len(noneElements):
            index_end = noneElements[k][0]
            index_count = noneElements[k][1]



        timeval = main_array[i].split(',')[0]
        copy_item = ','.join(main_array[i].split(',')[1:])
        if i < index_end:
        #timearray.append(timeval+','+copy_item)
            print(timeval+','+copy_item)
            i+=1

        else:
            #print(timeval+','+copy_item)
            tmp_count = index_count
            while tmp_count >1:
                print(main_array[i].split(',')[0] +','+ ','.join(main_array[index_end-tmp_count].split(',')[1:]) )
                tmp_count-=1
                i+=1

            k+=1

def compareThroughput(throughput_rf,throughput_fso):
    i=0
    time_ind_for_fso=[]
    time_ind_for_rf=[]
    tmp=0
    count=0
    total_array = []
    while i < len(throughput_rf):
        try:
            if throughput_rf[i] > throughput_fso[i]:
                count+=1
        except:
            print("None occured - " +str(i))
        i+=1
    return count/len(throughput_rf)


def printWeatherNone(timearray,rf,fso,weather):
    count=0
    repeat_count=0
    old_count=0
    for i in weather:
        if i == "NOWEATHER":
            if repeat_count==0:
                old_count = count
            repeat_count = 1
        else:
            repeat_count = 0
        
        if repeat_count > 0:
            print(timearray[count]+','+str(rf[count])+','+str(fso[count])+','+weather[old_count-1])
        else:
            print(timearray[count]+','+str(rf[count])+','+str(fso[count])+','+i )
        count +=1

def printRfNone(timearray,rf,fso,weather):
    count=0
    repeat_count=0
    old_count=0
    for i in rf:
        if i == None:
            if repeat_count==0:
                old_count = count
            repeat_count = 1
        else:
            repeat_count = 0
        
        if repeat_count > 0:
            print(timearray[count]+','+str(rf[old_count-1])+','+str(fso[count])+','+weather[count])
        else:
            print(timearray[count]+','+str(i)+','+str(fso[count])+','+weather[count] )
        count +=1

def printFsoNone(timearray,rf,fso,weather):
    count=0
    repeat_count=0
    old_count=0
    for i in fso:
        if i == None:
            if repeat_count==0:
                old_count = count
            repeat_count = 1
        else:
            repeat_count = 0
        
        if repeat_count > 0:
            print(timearray[count]+','+str(rf[count])+','+str(fso[old_count-1])+','+weather[count])
        else:
            print(timearray[count]+','+str(rf[count])+','+str(i)+','+weather[count] )
        count +=1
def removePast(old,new,timeval,rf,fso,weather):
    c=0
    tmp_count=new-old
    while c < len(timeval):
        if c < old:
            print(timeval[c])
        elif old <=c <= new:
            print(timearray[c]+','+str(rf[old-tmp_count])+','+str(fso[old-tmp_count])+','+weather[old-tmp_count])
            tmp_count-=1
        elif c > new:
            print(timeval[c])
        c+=1
               
filename="E:\\PhD"
sys.stdout=open("E:\\PhD\\filtering_2.txt","w")
time_str = DataAnalyzer(filename,"filtering.txt")
timeval = time_str.getFileStr().splitlines()
####### TAKING THE VARIABLES INTO ARRAYS#######
timearray=[]
rf=[]
fso=[]
weather=[]
for i in timeval:
    timearray.append(i.split(',')[0])
    try:
        rf.append(float(i.split(',')[1]))
    except:
        rf.append(None)

    try:
        if float(i.split(',')[2])>99.0:
            fso.append(94.4)
        else:
            fso.append(float(i.split(',')[2]))
    except:
        fso.append(None)

    weather.append(','.join(i.split(',')[3:]))

###################################################
removePast(13352900,13453700,timeval,rf,fso,weather)
#printFsoNone(timearray,rf,fso,weather)
sys.stdout.close()
#print(compareThroughput(rf, fso))

### STATISTICAL CHEK FSO or RF is bigger###############
"""count_rf = 0
count_fso= 0
i=0
while i < len(rf):
    if rf[i] >= fso[i]:
        count_rf +=1
    else:
        count_fso +=1
    i+=1
print("Total length: " + str(len(rf)))
print("RF is better: " + str(count_rf))
print("FSO is better: " + str(count_fso))
print("RF is better by %"+ str(100.0* count_rf/len(rf)))
print("FSO is better by %"+ str(100.0* count_rf/len(rf)))"""
#################################################################

"""plt.plot(rf)

plt.plot(fso)
plt.show()"""