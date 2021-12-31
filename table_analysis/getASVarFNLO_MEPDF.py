#! /usr/bin/env python2
import os
import sys
import inspect
import datetime
import csv
import numpy as np
import matplotlib.pyplot as plt
from fastnlo import fastNLOLHAPDF
from fastnlo import fastNLOCRunDec
############################################

#process = 'W1J'
#basedir = "/home/awisecar/analysis/openloops/21_04_29/1j_submitted_25april21/"
#basedir = "/home/awisecar/analysis/openloops/21_07_20/1j_AndrewEdit_results/"
#basedir = "/home/awisecar/analysis/openloops/21_07_20/1j_JoonBinEdit_results/"
#basedir = "/home/awisecar/analysis/openloops/21_08_05/1j_5flavorCheck_tables/"
#basedir = "/home/awisecar/analysis/openloops/21_08_08/1j_5flavorCheck_take2_tables/"
#tablenames = ['d56-x01-y01.merged']
#process = 'W2J'
#basedir = "/home/awisecar/analysis/openloops/21_04_29/2j_submitted_26april21/"
#basedir = "/home/awisecar/analysis/openloops/21_07_29/2j_JoonBinEdit_results/"
#tablenames = ['d57-x01-y01.merged', 'd63-x01-y01.merged']
process = 'W3J'
#basedir = "/home/awisecar/analysis/openloops/21_07_22/3j_results/"
basedir = "/home/awisecar/analysis/openloops/21_08_15/3j_JoonBinEdit_tables/"
tablenames = ['d58-x01-y01.merged', 'd64-x01-y01.merged']

# ---

# 6.11.18 - OpenLoops tables need to be read with variable-flavor scheme in order for proper Rivet-FNLO closure
doOpenLoops = True   


#use PDFs determined with certain alpha-s values --

#CT18NLO only  
pdfsets = ['CT18NLO_as_']
alphasstrlist = [ ["110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "122", "123", "124"] ]

# #order of PDFs: CT14nlo, NNPDF30_nlo, NNPDF31_nlo, HERAPDF20_NLO, CT18NLO, ABMP16_5_nlo, MSHT20nlo
# pdfsets = ['CT14nlo', 'NNPDF30_nlo', 'NNPDF31_nlo', 'HERAPDF20_N', 'CT18NLO_as_', 'ABMP16als11', 'MSHT20nlo_a']
# alphasstrlist = [ 
#                   ["111","112","113","114","115","116","117","118","119","120","121","122","123"],
#                   ["115", "117", "118", "119", "121"],
#                   ["116","118", "120"],
#                   ["110","111","112","113","114","115","116","117","118","119","120","121","122","123","124","125","126","127","128","129","130"],
#                   ["110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "122", "123", "124"],
#                   ["114", "115", "116", "117", "118", "119", "120", "121", "122", "123"],
#                   ["108", "109", "110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "122", "123", "124", "125", "126", "127", "128", "129", "130"]
#                 ]

############################################
nowtime = datetime.datetime.now()
for tablename in tablenames:
    ## FNLO constructor: table, PDF to evaluate, PDF member
    ## fastNLOCRunDec inherits PDF setting functions from fastNLOLHAPDF
    #fnlo = fastNLOCRunDec(basedir+tablename+'.tab') #set PDFs iteratively
    fnlo = fastNLOCRunDec(basedir+tablename+'.tab.gz')
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
    
    for idx, pdfset in enumerate(pdfsets):

        alphasvals = []
        for i, alphas in enumerate(alphasstrlist[idx]):
            alphasvals.append(float("0."+alphas))
        
        numalphas = len(alphasvals)
        numObsBin = fnlo.GetNObsBin() #number of observable bins
        numDim = fnlo.GetNumDiffBin() #distributions differential in how many variables?
        
        ## Open file
        print("Doing alpha-s variations for "+basedir+tablename+", with PDF series: "+pdfset)
        print str("Current time: "+nowtime.strftime("%Y-%m-%d %H:%M"))
        filename = str("aSVarMEPDF-%s-%s-%s.csv" % (pdfset, process, tablename))
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
        
        # ---------------------------------------------------------------------------------

        ## Do alpha-s calculations
        alphaslist = []
        
        ##Uncomment next line to NLO piece off
        #setOn = fnlo.SetContributionON(0, 1, False)
        #print "setOn for 1 equals "+str(setOn)
        
        for i, alphas in enumerate(alphasvals):

            if (pdfset != 'MSHT20nlo_a'):
                if (pdfset == 'HERAPDF20_N'):
                    fnlo.SetLHAPDFFilename(pdfset+"LO_ALPHAS_"+alphasstrlist[idx][i])
                elif (pdfset == 'ABMP16als11'):
                    fnlo.SetLHAPDFFilename("ABMP16als"+alphasstrlist[idx][i]+"_5_nlo")
                elif (pdfset == 'CT18NLO_as_'):
                    fnlo.SetLHAPDFFilename("CT18NLO_as_0"+alphasstrlist[idx][i])
                else:
                    fnlo.SetLHAPDFFilename(pdfset+"_as_0"+alphasstrlist[idx][i])
                fnlo.SetLHAPDFMember(0)
                fnlo.SetAlphasMz(alphas, False)
                print '\nDoing alpha-s = ' + str(fnlo.GetAlphasMz()) #Double checking here that the aS and PDF have been properly set
                print 'Using PDF set: ' + str(fnlo.GetLHAPDFFilename())
                print 'Using PDF member: ' + str(fnlo.GetIPDFMember())
                fnlo.CalcCrossSection()
                fnlo.PrintCrossSections()
                xsecvals = fnlo.GetCrossSection()
                alphaslist.append(xsecvals)

            else:
                fnlo.SetLHAPDFFilename("MSHT20nlo_as_largerange")
                # mem=1-12 => alpha_S(M_Z) = 0.108, 0.109, 0.110, 0.111, 0.112, 0.113, 0.114, 0.115, 0.116, 0.117, 0.118, 0.119 
                if (i < 12):
                    fnlo.SetLHAPDFMember(i+1) 
                # mem=0 => best fit alpha_S(M_Z) = 0.120
                elif (i == 12):
                    fnlo.SetLHAPDFMember(0)   
                # mem=13-22 => alpha_S(M_Z) = 0.121, 0.122, 0.123, 0.124, 0.125, 0.126, 0.127, 0.128, 0.129, 0.130
                elif (i > 12):
                    fnlo.SetLHAPDFMember(i) 
                fnlo.SetAlphasMz(alphas, False)
                print '\nDoing alpha-s = ' + str(fnlo.GetAlphasMz()) #Double checking here that the aS and PDF have been properly set
                print 'Using PDF set: ' + str(fnlo.GetLHAPDFFilename())
                print 'Using PDF member: ' + str(fnlo.GetIPDFMember())
                fnlo.CalcCrossSection()
                fnlo.PrintCrossSections()
                xsecvals = fnlo.GetCrossSection()
                alphaslist.append(xsecvals)

        # ---------------------------------------------------------------------------------
        
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
        
        outfile.close()
    del fnlo

print ('\nFinished!\n')

