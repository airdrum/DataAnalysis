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
        absFile=self.filepath +'/'+self.name
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


def getWeekAverage(array,number):
    if number == 31:
        return np.average(array[0:966878])
    elif number == 32:
        return np.average(array[966879:2176478])
    elif number == 33:
        return np.average(array[2176479:3386078])
    elif number == 34:
        return np.average(array[3386079:4595678])
    elif number == 35:
        return np.average(array[4595679:5805278])
    elif number == 36:
        return np.average(array[5805279:7014878])
    elif number == 37:
        return np.average(array[7014879:8224478])
    elif number == 38:
        return np.average(array[8224479:9434078])
    elif number == 39:
        return np.average(array[9434079:10643678])
    elif number == 40:
        return np.average(array[10643679:11853278])
    elif number == 41:
        return np.average(array[11853279:13062878])
    elif number == 42:
        return np.average(array[13062879:14272478])
    elif number == 43:
        return np.average(array[14272479:-1])

def getDuration(array):
    
    i = 1
    switch_count=0
    duration=0
    switch_duration=[]
    while i< len(array):
        if array[i]==1 and array[i-1] == 0:
            duration=0.5
        elif array[i]==1 and array[i-1] == 1:
            duration+=0.5
        elif array[i]==0 and array[i-1] == 0:
            if duration > 0.0:
                switch_duration.append(duration)
            duration=0.0
        i+=1

def getWeekSwitchCount(array,number):
    if number == 31:
        switch_array = array[0:966878]
    elif number == 32:
        switch_array = array[966879:2176478]
    elif number == 33:
        switch_array = array[2176479:3386078]
    elif number == 34:
        switch_array = array[3386079:4595678]
    elif number == 35:
        switch_array = array[4595679:5805278]
    elif number == 36:
        switch_array = array[5805279:7014878]
    elif number == 37:
        switch_array = array[7014879:8224478]
    elif number == 38:
        switch_array = array[8224479:9434078]
    elif number == 39:
        switch_array = array[9434079:10643678]
    elif number == 40:
        switch_array = array[10643679:11853278]
    elif number == 41:
        switch_array = array[11853279:13062878]
    elif number == 42:
        switch_array = array[13062879:14272478]
    elif number == 43:
        switch_array = array[14272479:-1]



x = [1,1,1,0,0,1,0,0,0,1,0] 
switch_dur, switch_count = getDuration(x)              
filename="."
#sys.stdout=open("E:\\PhD\\filtering_2.txt","w")
time_str = DataAnalyzer(filename,"latest_dataset_rf_fso_20191219.txt")
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

    #weather.append(','.join(i.split(',')[3:]))

count_rf = 0
count_fso= 0
i=0
hard_rf_fso=[]
switching=[]
while i < len(rf):
    if rf[i] >= fso[i]:
        count_rf +=1
        hard_rf_fso.append(rf[i])
        switching.append(1)
    else:
        count_fso +=1
        hard_rf_fso.append(fso[i])
        switching.append(0)
    i+=1




"""rf_31 = getWeekAverage(rf, 31)
rf_32 = getWeekAverage(rf, 32)
rf_33 = getWeekAverage(rf, 33)
rf_34 = getWeekAverage(rf, 34)
rf_35 = getWeekAverage(rf, 35)
rf_36 = getWeekAverage(rf, 36)
rf_37 = getWeekAverage(rf, 37)
rf_38 = getWeekAverage(rf, 38)
rf_39 = getWeekAverage(rf, 39)
rf_40 = getWeekAverage(rf, 40)
rf_41 = getWeekAverage(rf, 41)
rf_42 = getWeekAverage(rf, 42)
rf_43 = getWeekAverage(rf, 43)

fso_31 = getWeekAverage(fso, 31)
fso_32 = getWeekAverage(fso, 32)
fso_33 = getWeekAverage(fso, 33)
fso_34 = getWeekAverage(fso, 34)
fso_35 = getWeekAverage(fso, 35)
fso_36 = getWeekAverage(fso, 36)
fso_37 = getWeekAverage(fso, 37)
fso_38 = getWeekAverage(fso, 38)
fso_39 = getWeekAverage(fso, 39)
fso_40 = getWeekAverage(fso, 40)
fso_41 = getWeekAverage(fso, 41)
fso_42 = getWeekAverage(fso, 42)
fso_43 = getWeekAverage(fso, 43)

rffso_31 = getWeekAverage(hard_rf_fso, 31)
rffso_32 = getWeekAverage(hard_rf_fso, 32)
rffso_33 = getWeekAverage(hard_rf_fso, 33)
rffso_34 = getWeekAverage(hard_rf_fso, 34)
rffso_35 = getWeekAverage(hard_rf_fso, 35)
rffso_36 = getWeekAverage(hard_rf_fso, 36)
rffso_37 = getWeekAverage(hard_rf_fso, 37)
rffso_38 = getWeekAverage(hard_rf_fso, 38)
rffso_39 = getWeekAverage(hard_rf_fso, 39)
rffso_40 = getWeekAverage(hard_rf_fso, 40)
rffso_41 = getWeekAverage(hard_rf_fso, 41)
rffso_42 = getWeekAverage(hard_rf_fso, 42)
rffso_43 = getWeekAverage(hard_rf_fso, 43)

print("31- RF: " + str(rf_31) + "Mbps , FSO: " + str(fso_31) + "Mbps, RF-FSO: " + str(rffso_31) +"Mbps")
print("32- RF: " + str(rf_32) + "Mbps , FSO: " + str(fso_32) + "Mbps, RF-FSO: " + str(rffso_32) +"Mbps")
print("33- RF: " + str(rf_33) + "Mbps , FSO: " + str(fso_33) + "Mbps, RF-FSO: " + str(rffso_33) +"Mbps")
print("34- RF: " + str(rf_34) + "Mbps , FSO: " + str(fso_34) + "Mbps, RF-FSO: " + str(rffso_34) +"Mbps")
print("35- RF: " + str(rf_35) + "Mbps , FSO: " + str(fso_35) + "Mbps, RF-FSO: " + str(rffso_35) +"Mbps")
print("36- RF: " + str(rf_36) + "Mbps , FSO: " + str(fso_36) + "Mbps, RF-FSO: " + str(rffso_36) +"Mbps")
print("37- RF: " + str(rf_37) + "Mbps , FSO: " + str(fso_37) + "Mbps, RF-FSO: " + str(rffso_37) +"Mbps")
print("38- RF: " + str(rf_38) + "Mbps , FSO: " + str(fso_38) + "Mbps, RF-FSO: " + str(rffso_38) +"Mbps")
print("39- RF: " + str(rf_39) + "Mbps , FSO: " + str(fso_39) + "Mbps, RF-FSO: " + str(rffso_39) +"Mbps")
print("40- RF: " + str(rf_40) + "Mbps , FSO: " + str(fso_40) + "Mbps, RF-FSO: " + str(rffso_40) +"Mbps")
print("41- RF: " + str(rf_41) + "Mbps , FSO: " + str(fso_41) + "Mbps, RF-FSO: " + str(rffso_41) +"Mbps")
print("42- RF: " + str(rf_42) + "Mbps , FSO: " + str(fso_42) + "Mbps, RF-FSO: " + str(rffso_42) +"Mbps")
print("43- RF: " + str(rf_43) + "Mbps , FSO: " + str(fso_43) + "Mbps, RF-FSO: " + str(rffso_43) +"Mbps")
"""


"""
31- RF: 32.123Mbps , FSO: 85.861Mbps, RF-FSO: 87.206Mbps
32- RF: 33.127Mbps , FSO: 85.713Mbps, RF-FSO: 86.602Mbps
33- RF: 34.352Mbps , FSO: 86.576Mbps, RF-FSO: 87.830Mbps
34- RF: 40.232Mbps , FSO: 83.781Mbps, RF-FSO: 87.140Mbps
35- RF: 41.699Mbps , FSO: 76.555Mbps, RF-FSO: 81.003Mbps
36- RF: 41.740Mbps , FSO: 78.845Mbps, RF-FSO: 82.418Mbps
37- RF: 40.638Mbps , FSO: 82.372Mbps, RF-FSO: 84.690Mbps
38- RF: 36.752Mbps , FSO: 85.669Mbps, RF-FSO: 87.956Mbps
39- RF: 37.007Mbps , FSO: 90.152Mbps, RF-FSO: 90.962Mbps
40- RF: 37.389Mbps , FSO: 83.195Mbps, RF-FSO: 86.241Mbps
41- RF: 35.434Mbps , FSO: 89.823Mbps, RF-FSO: 91.193Mbps
42- RF: 33.507Mbps , FSO: 89.699Mbps, RF-FSO: 91.133Mbps
43- RF: 38.751Mbps , FSO: 90.152Mbps, RF-FSO: 90.634Mbps
"""
