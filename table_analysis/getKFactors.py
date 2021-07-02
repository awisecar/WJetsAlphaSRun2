#! /usr/bin/env python2
import os
import sys
import datetime
import csv
from array import array

#########################################
pdfsets = ['CT14nlo']

#process = 'W1J'
#basedir = '/home/awisecar/analysis/openloops/June21/1j/mcgrid/MCgrid_CMS_2018_WJetsAlphaS_1j_OL/'
#tablenames = ['d02', 'd06', 'd16', 'd20', 'd52', 'd56', 'd66', 'd70']
process = 'W2J'
basedir = '/home/awisecar/analysis/openloops/June21/2j/mcgrid/MCgrid_CMS_2018_WJetsAlphaS_2j_OL/'
tablenames = ['d03', 'd07', 'd10', 'd13', 'd17', 'd21', 'd24', 'd53', 'd57', 'd60', 'd63', 'd67', 'd71', 'd74']
#process = 'W3J'
#basedir = '/home/awisecar/AlphaSVar-WJets/openloops/Nov06/3j/mcgrid/MCgrid_CMS_2018_WJetsAlphaS_3j_OL/20M/'
#tablenames = ['d04', 'd08', 'd11', 'd14', 'd18', 'd22', 'd25']

#########################################
print ('\n------- Running fnlo-tk-cppread...')
for ipdf, pdfset in enumerate(pdfsets):
    for itab, tablename in enumerate(tablenames):
        print ('Doing '+str(tablename)+'-x01-y01.merged.tab with PDF set: '+str(pdfset))
        outfileName = 'kFactors-'+str(tablename)+'-x01-y01.out'
        fnloCmd = 'fnlo-tk-cppread '+basedir+str(tablename)+'-x01-y01.merged.tab.gz '+str(pdfset)+' > '+outfileName
        print fnloCmd
        os.system(fnloCmd)

print ('\n------- Parsing output files...')
for ipdf, pdfset in enumerate(pdfsets):
    for itab, tablename in enumerate(tablenames):
        print ('\nDoing '+str(tablename)+'-x01-y01.merged.tab with PDF set: '+str(pdfset))
        outfileName = 'kFactors-'+str(tablename)+'-x01-y01.out'
        readinFile = open(outfileName, "rt")
        contents = readinFile.read()
        readinFile.close()
        contents = contents.split('KNLO\n')[1]
        contents = contents.split('#-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n')[1]
        #readinFile.close()
        #print(contents)

        binCenters = []
        kFactors = []

        #Removing last element of splittted list, which is an empty string
        #Don't know why it's there
        contents = (contents.split('\n'))
        del contents[-1]

        #Loop through each line of the output, which stands for each bin
        for i, line in enumerate(contents):
            #print(line)
            binLow = float(line.split()[3])
            binUp = float(line.split()[4])
            binCenter = (binLow+binUp)/2.
            kFactor = float(line.split()[8])
            binCenters.append(binCenter)
            kFactors.append(kFactor)
        print ('binCenters: '+str(binCenters))
	print ('kFactors: '+str(kFactors))
        del contents         

        outCSVName = 'kFactors-'+str(tablename)+'-x01-y01.csv'   
        outFile = open(outCSVName, "w")
        outFile.write("'BINCENTER','KFACTOR'")
        outFile.write("\n")
        for i, kFactor in enumerate(kFactors):
            outFile.write( '%s,%s\n' % (binCenters[i], kFactors[i]) )
        outFile.close()
        
print ('\n')
for itab, tablename in enumerate(tablenames):
    outfileName = 'kFactors-'+str(tablename)+'-x01-y01.out'
    print( 'Removing file... '+outfileName )
    os.system('rm -f '+str(outfileName))

print ('\n------- All finished!')
