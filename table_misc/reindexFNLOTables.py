#! /usr/bin/env python2
import os
import sys
import datetime
import argparse
#######################################
# Parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument("table_num", help="Specify table number (e.g. d56, d57)")
parser.add_argument("spacer", type=int, help="Reindex files up by this number")
args = parser.parse_args()
#######################################
'''
e.g. ./reindexFNLOTables.py d57 149
'''
#######################################
print("\nNotes: Make sure to gzip tables first! (Script requires .tab.gz extension.)")
print("       Rename the zeroth table with a higher index before running script!")
print("           e.g. d57-x01-y01.tab.gz --> d57-x01-y01.50.tab.gz")
print("\nBegin!\n")
#######################################

basedir = "./" # get directory containing table files
maxFileIndex = 50 # maximum index of files in folder

for i in range(1, maxFileIndex+1):
    fileIn = str(args.table_num)+"-x01-y01."+str(i)+".tab.gz"
    if not os.path.isfile(basedir+fileIn):
        print ('Could not find file: '+str(fileIn)+', skipping!')
        continue
    # For each file found in folder, re-index up by "spacer"
    fileOut = str(args.table_num)+"-x01-y01."+str(i+args.spacer)+".tab.gz"

    command = "mv "+basedir+fileIn+" "+basedir+fileOut
    print(command)
    os.system(command) # execute command
    
print("\nFinished!\n")

