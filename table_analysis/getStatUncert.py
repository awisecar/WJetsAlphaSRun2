#! /usr/bin/env python2
import os
import sys
import datetime
import csv
from array import array
#######################################
'''
 Script to grab statistical errors for a set of FastNLO tables -----
 1) First rename all tables to proper '0xxx' format
 2) Run fnlo-tk-statunc on this set of tables
 3) Rename YODA output to avoid overwriting
 4) Parse YODA file to grab bin content and errors
 5) Write this out in .csv format
'''
#########################################
numTables = 200  
# --
pdfsets = ['CT14nlo','NNPDF30_nlo_as_0118','NNPDF31_nlo_as_0118', 'HERAPDF20_NLO_ALPHAS_118'] #names of PDFs in LHAPDF6 library
pdfnames2 = ['CT14nlo','NNPDF30_nlo','NNPDF31_nlo','HERAPDF20_N'] #names of PDFs in output YODA file
# --
#process = 'W1J'
#basedir = "/home/awisecar/analysis/openloops/21_04_29/1j_submitted_25april21/"
#tablenames = ["d56"]
process = 'W2J'  
basedir = "/home/awisecar/analysis/openloops/21_04_29/2j_submitted_26april21/"
tablenames = ["d57"] 
#########################################

print ('Remember to rename the zeroth table!')
for itab, tablename in enumerate(tablenames):
    print ('\n----- Starting table set '+str(tablename)+'-x01-y01!')
    for i in range (1, numTables+1):
        if (i < 10):
            spacer = '000'
        elif ( (i >= 10) and (i < 100) ):
            spacer = '00'
        elif ( (i >= 100) and (i < 1000) ):
            spacer = '0'
        tableIn = basedir+str(tablename)+'-x01-y01.'+str(i)+'.tab.gz'
        tableOut = basedir+str(tablename)+'-x01-y01-'+spacer+str(i)+'.tab.gz'
        if not os.path.isfile(tableIn):
            print ('Could not find table: '+str(tableIn)+', skipping!')
            continue
        renameCmd = 'mv '+tableIn+' '+tableOut
        os.system(renameCmd)

    for ipdf, pdfset in enumerate(pdfsets):
        #fnloCmd = 'fnlo-tk-statunc '+str(tablename)+'-x01-y01- '+str(pdfset)+' NLO > '+str(tablename)+'-statUnc.out'
        fnloCmd = 'fnlo-tk-statunc '+basedir+str(tablename)+'-x01-y01- '+str(pdfset)+' NLO'
        print ('\nExecuting... \n'+fnloCmd+'\n')
        os.system(fnloCmd)

        #note: YODA file appears in the directory you run fnlo-tk-statunc
        #pdfnames2 = ['CT10nlo', 'CT14nlo', 'NNPDF23_nlo']
        YODAName = 'NLO_'+pdfnames2[ipdf]+'_stat.yoda'
        mvOutCmd = 'mv '+'./'+str(YODAName)+' '+'./'+str(tablename)+'-'+YODAName
        print ('Executing... '+str(mvOutCmd))
        os.system(mvOutCmd)

    print ('----- Finished with table set '+str(tablename)+'-x01-y01!')

print ('\n----- Parsing YODA files:')
for ipdf, pdfset in enumerate(pdfsets):
    print ('\nDoing PDF set '+str(pdfset))
    for itab, tablename in enumerate(tablenames):
        print ('----- Starting table set '+str(tablename)+'-x01-y01!')
        outFileName = str("statUncert-%s-%s-%s-x01-y01.merged.csv" % (pdfnames2[ipdf], process, tablename))

        inYODAName = str(tablename)+'-'+'NLO_'+pdfnames2[ipdf]+'_stat.yoda'

        inFileYODA = open('./'+inYODAName, "rt")
        contents = inFileYODA.read()
        contents = contents.split('Type=Scatter2D\n# ')[1]
        contents = contents.split('yerr+\n')[1]
        contents = contents.split('END YODA_SCATTER2D')[0]
        inFileYODA.close()
        #print(contents)

        contents = (contents.split('\n'))
        del contents[-1]
        #print(contents)

        xerrLowList = []
        xerrUpList = []
        yerrLowList = []
        yerrUpList = []

        for i, line in enumerate(contents):
            #print(line)
            xerrLowList.append( float(line.split()[1]) )
            xerrUpList.append( float(line.split()[2]) )
            yerrLowList.append( float(line.split()[4]) )
            yerrUpList.append( float(line.split()[5]) )

        del contents
      
        print ( 'xerrLow: '+str(xerrLowList) )
        print ( 'xerrUp: '+str(xerrUpList) )
        print ( 'yerrLow: '+str(yerrLowList) )
        print ( 'yerrUp: '+str(yerrUpList) )

        outFile = open(outFileName, "w")
        outFile.write("'XERRLOW','XERRUP','YERRLOW','YERRUP'\n")
        for i, xerrLow in enumerate(xerrLowList):
            outFile.write( '%s,%s,%s,%s\n' % (xerrLowList[i], xerrUpList[i], yerrLowList[i], yerrUpList[i]) )
        outFile.close()
       #del contents

print('\n')
for ipdf, pdfset in enumerate(pdfsets):
    for itab, tablename in enumerate(tablenames):
        inYODAName = str(tablename)+'-'+'NLO_'+pdfnames2[ipdf]+'_stat.yoda'
        fileYODA = './'+inYODAName
        print('Removing file... '+inYODAName)
        os.system('rm -f '+fileYODA)

print ('\nFinished!\n')
