import os
import pandas as pd


#A function that grabs a specific joint
#person = the dataframe of a person
#element = the x,y,z element which to extract
#joint = the joint name

#output = a list of converted x,y or z coords of the joint
def GetJoint(person,element,joint):
    x = person[person.jointName == joint]
    y = list()
    if(len(x) < 1):
        return None
    y = [0 for i in range(len(x))]
    x = x.reset_index(drop=True)
    for i in range(0,len(x)):
        y[i] = float(str(x[element][i].replace(',','.')))
    return y
        

#Function that returns a list of all folders in the given path
#path= a string containing the path from which the folders will be extracted

#returns a list with paths
def GetFolders(path):    
    for root,dirs,files in os.walk(path):
        return dirs
    return

#Function to grab a file with the given parameters
#Folder = the path towards the folder from which the file will be given
#nr = the x'th file in the folder [return NULL if nr is greater than the amount
#of files]
#extension = a string containing the extension which the file needs to match

#returns a string containing the path to the file
def GetFile(folder,nr,extension):
    f = 1
    for root,dirs,files in os.walk(folder):
        files.sort()
        for x in files:
            if(x.endswith(extension)):
                if(f == nr):
                    return x
                else:
                    f+=1
    return
            
#Function to convert a timestring to seconds
#timestring = input string containing timestamp

#returns the timestring converted to seconds
def GetSeconds(timestring):    
    j = 0
    hours = 0
    minutes = 0
    seconds = 0
    milliseconds = 0    
    time = 0.0
    while timestring[j] != ':':
        hours+=int(timestring[j])
        hours*=10
        j+=1
    hours/=10
    j+=1
    while timestring[j] != ':':
        minutes+=int(timestring[j])
        minutes*=10
        j+=1
    minutes/=10
    j+=1
    while timestring[j] != '.':
        seconds+=int(timestring[j])
        seconds*=10
        j+=1
    seconds/=10
    j+=1
    i = 0
    while(j != len(timestring) and i != 2):
        milliseconds+=int(timestring[j])
        milliseconds*=10
        j+=1
        i+=1
    milliseconds/=10
    time = hours * 60 * 60 + minutes * 60 + seconds + milliseconds / (10 ** i)    
    return time


#function to extract a person from the given csvfile
#csvfile = the location of the inputfile from which a person gets extracted
#needperson = a number that will try to get that person returns nothing if
#person is not in file

#returns a csvfile with the given person + the lenght of the file in seconds +
#the number of the selected person
def GetPerson(csvfile,needperson=-1):
    df = pd.read_csv(csvfile)
    if(len(df) == 0):
        return
    check = df.trackingId.unique()
    humans = len(check)    
    selectedhuman = 1       
    forced = False
    if(needperson > 0):
        forced = True
        selectedhuman = needperson
        if(selectedhuman >= humans):
            return        
    done = False
    while (not done):
        file = df[df.trackingId == check[selectedhuman - 1]]
        file = file.reset_index(drop=True)        
        startframe = file.frameNum[0]
        starttime = GetSeconds(file.time[0])
        endframe = file.frameNum[len(file) - 1]
        endtime = GetSeconds(file.time[len(file) - 1])
        deltaframe = endframe - startframe
        deltatime = endtime - starttime                
        if(deltatime < 10 and humans != selectedhuman and not forced):
            selectedhuman+=1
            continue
        done = True    
    #accuracy = file[file.trackState=="Tracked"]
    #print(str((len(accuracy)/len(file))*100)+'%')
    return file,deltatime,selectedhuman

#Function to obtain a list of delta values.  (pads the first and last value)
#pos = input list that will be used for comparisons.
#timeframe = list that contains the time values for pos.
#deltatime = the time over which a delta needs to be calculated.
def CalcDelta(pos,timeframe,deltatime):
    if(len(pos) != len(timeframe)):
        raise ValueError("Lists are of unequal sizes")
        return []
    Delta = list()
    Delta.append(0)
    set1 = pos[0]   
    second = deltatime
    relation = 0.0
    for x in range(0,len(pos)):        
        if(timeframe[x] >= second):            
            if(relation == 0):
                relation = x
            second+=deltatime                                                  
            Delta.append(pos[x] - set1)
            set1 = pos[x]
    if(set1 != 0):
        Delta.append(pos[len(pos) - 1] - set1)    
    return Delta            


#Function to get the highest value from input x that occurs 'times' times.
#x = a list with values.
#times = the minimum number of times a match has to occur to return a value.
#higher = a bit that if False only checks for exact matches else it also checks
#for higher values.
def GetHeight(x,times,higher):
    blacklist = []
    j = 0
    h = int(x[j] * 100)
    hi = 0
    t = 0
    while(1):
        t = 0
        for i in range(j + 1,len(x)):
            y = int(x[i] * 100)
            if(h == y and not higher):               
                t+=1
            elif(h <= y and higher):
                t+=1
            if(h < y):
                if(y in blacklist):                    
                    continue
                t = 0
                h = y
                hi = i
                if(higher):
                    i = 0
        if(t >= times):           
            return h / 100        
        else:
            j+=1
            blacklist.append(h)          
            h = int(x[j] * 100)
        if(len(blacklist) == len(x) + times - 1): 
            raise ValueError("Unable to find a height with the given parameters")
            return
        
        
#Function to get the lowest value from input x that occurs 'times' times.
#x = a list with values.
#times = the minimum number of times a match has to occur to return a value.
#higher = a bit that if False only checks for exact matches else it also checks
#for lower values.
def GetLow(x,times,lower):
    blacklist = []
    j = 0
    h = int(x[j] * 100)
    hi = 0
    t = 0
    while(1):
        t = 0
        for i in range(j + 1,len(x)):
            y = int(x[i] * 100)
            if(h == y and not lower):               
                t+=1
            elif(h >= y and lower):
                t+=1
            if(h > y):
                if(y in blacklist):                    
                    continue
                t = 0
                h = y
                hi = i
                if(lower):
                    i = 0
        if(t >= times):          
            return h / 100        
        else:
            j+=1
            blacklist.append(h)            
            h = int(x[j] * 100)
        if(len(blacklist) == len(x) + times - 1):
            raise ValueError("Unable to find a height with the given parameters")
            return
        
        
#Function to create a new timestamp
#T1 = the original timestamp
#note = time to add in seconds (2 decimal accuracy)
#cannot subtract
def NewTime(T1,note):
    m1 = (note * 10) % 10
    m10 = (note * 100) % 10
    if(m10 != 0 or m1 != 0):
        millis1 = int(T1[9])
        millis10 = int(T1[10])
        m1_extra = int((m10 + millis10) / 10)
        note+=m1_extra
        
        T1 = T1[:9] + chr(int((millis1 + m1 + m1_extra) % 10) + 48) + chr(int((millis10 + m10) % 10) + 48)
    else:
        T1 = T1[:9] + '00'
    note = int(note)
    sec1 = int(T1[7])
    sec2 = int(T1[6])

    if(note + sec1 > 9):
        note2 = int((note + sec1) / 10)
        T1 = T1[:6] + chr((ord(T1[6]) - 48 + note2) % 6 + 48) + chr((ord(T1[7]) - 48 + note) % 10 + 48) + T1[8:]
        if(note2 + sec2 > 5):
            m = int((note2 + sec2) / 6)
            if(ord(T1[4]) - 48 + m < 10):
                T1 = T1[:4] + chr(ord(T1[4]) + m) + T1[5:]                
            else:                
                m2 = int((ord(T1[4]) - 48 + m) / 10)                
                if((ord(T1[3]) - 48 + m2 > 5)):
                    ####OOB if hour mark is overflown
                    T1 = T1[:1] + chr(ord(T1[1]) + 1) + T1[2] + chr((ord(T1[3]) - 48 + m2) % 6 + 48) + chr((ord(T1[4]) - 48 + m) % 10 + 48) + T1[5:]
                else:
                    T1 = T1[:3] + chr(ord(T1[3]) + 1) + chr((ord(T1[4]) - 48 + m) % 10 + 48) + T1[5:]                
    else:        
        T1 = T1[:7] + chr(ord(T1[7]) + note) + T1[8:]    
    return T1
