#! /usr/bin/env python2
import os
import sys
import datetime
import csv
import numpy as np
import matplotlib.pyplot as plt
import fastnlo
from fastnlo import fastNLOLHAPDF
from fastnlo import fastNLOCRunDec
############################################

process = 'W1J' 
#basedir = "/home/awisecar/analysis/openloops/21_04_29/1j_submitted_25april21/"
#basedir = "/home/awisecar/analysis/openloops/21_07_20/1j_AndrewEdit_results/"
basedir = "/home/awisecar/analysis/openloops/21_07_20/1j_JoonBinEdit_results/"
#basedir = "/home/awisecar/analysis/openloops/21_08_05/1j_5flavorCheck_tables/"
#basedir = "/home/awisecar/analysis/openloops/21_08_08/1j_5flavorCheck_take2_tables/"
tablenames = ['d56-x01-y01.merged']
#process = 'W2J' 
#basedir = "/home/awisecar/analysis/openloops/21_04_29/2j_submitted_26april21/"
#basedir = "/home/awisecar/analysis/openloops/21_07_29/2j_JoonBinEdit_results/"
#tablenames = ['d57-x01-y01.merged', 'd63-x01-y01.merged']
# process = 'W3J'
# #basedir = "/home/awisecar/analysis/openloops/21_07_22/3j_results/"
# basedir = "/home/awisecar/analysis/openloops/21_08_15/3j_JoonBinEdit_tables/"
# tablenames = ['d58-x01-y01.merged', 'd64-x01-y01.merged']

# ---

# 6.11.18: OpenLoops tables need to be read with flexible flavor scheme in order for proper Rivet-FNLO closure
doOpenLoops = True  

#CT14nlo only
pdfsets = [ 'CT14nlo' ]
pdfevals = [ 'CT14nlo_as_0118' ]
alphasvalslist = [ np.arange(0.111, 0.124, 0.001) ]


# #CT18NLO only
# pdfsets = [ 'CT18NLO_as_' ]
# pdfevals = [ 'CT18NLO_as_0118' ]
# alphasvalslist = [ np.arange(0.110, 0.125, 0.001) ]


# #order of PDFs: CT14nlo, NNPDF30_nlo, NNPDF31_nlo, HERAPDF20_NLO, CT18NLO, ABMP16_5_nlo, MSHT20nlo
# pdfsets = ['CT14nlo', 'NNPDF30_nlo', 'NNPDF31_nlo', 'HERAPDF20_N', 
#            'CT18NLO_as_', 'ABMP16als11', 'MSHT20nlo_a']
# pdfevals = ['CT14nlo_as_0118', 'NNPDF30_nlo_as_0118', 'NNPDF31_nlo_as_0118', 'HERAPDF20_NLO_ALPHAS_118', 
#             'CT18NLO_as_0118', 'ABMP16als118_5_nlo', 'MSHT20nlo_as118']
# alphasvalslist = [ np.arange(0.111, 0.124, 0.001), [0.115, 0.117, 0.118, 0.119, 0.121], [0.116, 0.118, 0.120], np.arange(0.110, 0.131, 0.001), 
#                    np.arange(0.110, 0.125, 0.001), np.arange(0.114, 0.124, 0.001), np.arange(0.108, 0.130, 0.001) ]

############################################
nowtime = datetime.datetime.now()
for ipdf, pdfeval in enumerate(pdfevals):
    for tablename in tablenames:    
        ## FNLO constructor: table, PDF to evaluate, PDF member
        #fnlo = fastNLOCRunDec(basedir+tablename+'.tab', pdfeval, 0)
        fnlo = fastNLOCRunDec(basedir+tablename+'.tab.gz', pdfeval, 0)
        #fnlo.SetUnits(fastnlo.kPublicationUnits) #can't get this to work
        
        #imaxpdf = fnlo.GetNPDFMaxMember()
        #print 'max number of PDF members: ' + str(imaxpdf)
        #fnlo.PrintPDFInformation()
        fnlo.PrintContributionSummary(0)
        fnlo.Print(0)
        fnlo.SetMz(91.1876) #2018 PDG fit
        #fnlo.GetScaleFactorMuR()
        #fnlo.GetScaleFactorMuF()

        if doOpenLoops:
            print("Setting flavor-matching in alpha-s running for OpenLoops tables!")
            fnlo.SetNFlavor(0)
            fnlo.SetNLoop(2)
 
        alphasvals = alphasvalslist[ipdf]
       
        #numalphas = alphasvals.size #size method only works for numpy arrays(?)
        numalphas = len(alphasvals)
        numObsBin = fnlo.GetNObsBin() #number of observable bins
        numDim = fnlo.GetNumDiffBin() #distributions differential in how many variables?
        
        ## Open file
        print("Doing alpha-s variations for "+basedir+tablename)
        print str("Current time: "+nowtime.strftime("%Y-%m-%d %H:%M"))
        filename = str("aSVarME-%s-%s-%s.csv" % (pdfsets[ipdf], process, tablename))
        outfile = open(filename, "w")
        
        ## Writing top row ("header") information
        outfile.write("'BINLOW','BINUP','BINCENTER'")
        for i, alphas in enumerate(alphasvals):
            outfile.write(",'aS="+str(alphas)+"'")
            #outfile.write(",'"+str(alphas)+"'")
        outfile.write("\n")
        
        ## Write out first row of information (diagonistic information)
        outfile.write(str(numObsBin)+","+str(numDim)+","+str(numalphas))
        for i, alphas in enumerate(alphasvals):
            outfile.write(","+str(alphas))
        outfile.write("\n")
        
        ## Do alpha-s calculations
        alphaslist = []
        
        ##Uncomment next line to turn NLO piece off
        #setOn = fnlo.SetContributionON(0, 1, False)
        #print "setOn for 1 equals "+str(setOn)
        
        for i, alphas in enumerate(alphasvals):
            fnlo.SetAlphasMz(alphas, False)
            print '\nDoing alpha-s = ' + str(fnlo.GetAlphasMz())
            print 'Using PDF set: ' + str(fnlo.GetLHAPDFFilename())
            fnlo.CalcCrossSection()
            fnlo.PrintCrossSections()
            xsecvals = fnlo.GetCrossSection()
            alphaslist.append(xsecvals)
        
        ## Write out data
        for i in range(0,numObsBin):
            for j in range(0,numDim):
                lowBinEdge = fnlo.GetObsBinLoBound(i,j)
                upBinEdge = fnlo.GetObsBinUpBound(i,j)
                binCenter = (lowBinEdge+upBinEdge)/2.
                outfile.write(str(lowBinEdge)+","+str(upBinEdge)+","+str(binCenter))
            for j, alphas in enumerate(alphasvals):
                outfile.write(',%s' % alphaslist[j][i])
            outfile.write('\n') #end the row of the csv file

        print 'Finished variations for '+str(pdfeval)+', '+str(tablename)        
        print 'Closing outfile!\n'
        outfile.close()

print ('\nFinished!\n')

