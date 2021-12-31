#! /usr/bin/env python2
import os
import sys
import datetime
#######################################
basedir = "./"  
num = 200  
# ---
#tablenums = ["d56"] # w+1j
#tablenums = ["d57", "d63"] # w+2j
tablenums = ["d58", "d64"] # w+3j
# ---
#tablenums = ["d56"] # w+1j 
#tablenums = ["d57"] # w+2j 
#tablenums = ["d58"] # w+3j
#######################################
for itab, tablenum in enumerate(tablenums):
    print("\n >>> Merging all tables for tablenum: "+str(tablenum))
    command = "fnlo-tk-merge "+str(tablenum)+"-x01-y01-0000.tab.gz"
    #command = "fnlo-tk-merge "
    for i in range(1, num+1):
        tableIn = str(tablenum)+"-x01-y01."+str(i)+".tab.gz"
        if not os.path.isfile(basedir+tableIn):
            print ('Could not find table: '+str(tableIn)+', skipping!')
            continue
        command += " "+str(tablenum)+"-x01-y01."+str(i)+".tab.gz"
    command += " "+str(tablenum)+"-x01-y01.merged.tab.gz"
    print ("\nExecuting... \n"+command+"\n")
    os.system(command)
    
print("\nFinished!\n")

