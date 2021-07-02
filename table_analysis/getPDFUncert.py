#! /usr/bin/env python2
import os
import sys
import datetime
import csv
import numpy as np
import matplotlib.pyplot as plt
import fastnlo
import math
from fastnlo import fastNLOLHAPDF
from fastnlo import fastNLOCRunDec

nowtime = datetime.datetime.now()

############################################
process = 'W1J'
basedir = '/home/awisecar/AlphaSVar-WJets/openloops/Jan10/1j/mcgrid/MCgrid_CMS_2018_WJetsAlphaS_1j_OL/'
#tablenames = ['d02-x01-y01.merged', 'd06-x01-y01.merged', 'd16-x01-y01.merged', 'd20-x01-y01.merged']
tablenames = ['d02-x01-y01.merged', 'd06-x01-y01.merged']
#process = 'W2J'
#basedir = '/home/awisecar/AlphaSVar-WJets/openloops/Jan10/2j/mcgrid/MCgrid_CMS_2018_WJetsAlphaS_2j_OL/'
#tablenames = ['d03-x01-y01.merged', 'd07-x01-y01.merged', 'd10-x01-y01.merged', 'd13-x01-y01.merged', 'd17-x01-y01.merged', 'd21-x01-y01.merged', 'd24-x01-y01.merged']
#tablenames = ['d03-x01-y01.merged', 'd07-x01-y01.merged', 'd13-x01-y01.merged']
#process = 'W3J'
#basedir = '/home/awisecar/AlphaSVar-WJets/openloops/Jan23/3j/mcgrid/MCgrid_CMS_2018_WJetsAlphaS_3j_OL/50M/'
#tablenames = ['d04-x01-y01.merged', 'd08-x01-y01.merged', 'd11-x01-y01.merged', 'd14-x01-y01.merged', 'd18-x01-y01.merged', 'd22-x01-y01.merged', 'd25-x01-y01.merged']
#tablenames = ['d04-x01-y01.merged', 'd08-x01-y01.merged', 'd14-x01-y01.merged']

# 6.11.18: OpenLoops tables need to be read with flexible flavor scheme in order for proper Rivet-FNLO closure
doOpenLoops = True

#pdfsets = ['NNPDF23_nlo', 'CT10nlo', 'CT14nlo', 'NNPDF31_nnlo', 'NNPDF30_nlo']
#pdfsets = ['CT14nlo']
#pdfsets = ['CT14nnlo']
#pdfsets = ['NNPDF31_nlo_as_0118']
pdfsets = ['NNPDF31_nnlo_as_0118']
#pdfsets = ['NNPDF31_nnlo_as_0118_hessian']

############################################

for iTab, tablename in enumerate(tablenames):
    print ("\n------------> Doing table: "+str(tablename))
    for iPdf, pdfset in enumerate(pdfsets):
        print ("----------> Doing PDF: "+str(pdfset))
        #initialize table with tablename, pdfset, and pdf member
        fnlo = fastNLOCRunDec(basedir+tablename+'.tab.gz', pdfset, 0)
        #fnlo.PrintContributionSummary(0)
        fnlo.Print(0)
        fnlo.PrintPDFInformation()

        numObsBin = fnlo.GetNObsBin() #number of observable bins
        numDim = fnlo.GetNumDiffBin() #distributions differential in how many variables?

        fnlo.SetAlphasMz(0.1181, True); #2018 PDG value
        fnlo.SetMz(91.1876) #2018 PDG value
        numMembers = fnlo.GetNPDFMembers()
        #print '\nNumber of PDF members: ' + str(numMembers)

        if (doOpenLoops):
            print("\nSetting flavor-matching in alpha-s running for OpenLoops tables!")
            fnlo.SetNFlavor(0)
            fnlo.SetNLoop(2)

        binCenters = []
        for iBin in range(0, numObsBin):
            for iDim in range(0, numDim): #assuming only single-diff. distributions here
                lowBinEdge = fnlo.GetObsBinLoBound(iBin, iDim)
                upBinEdge = fnlo.GetObsBinUpBound(iBin, iDim)
                binCenter = (lowBinEdge+upBinEdge)/2.
                binCenters.append(binCenter)

        print( "\nBin centers: "+str(binCenters) )

        names1 = ["d02-x01-y01", "d03-x01-y01", "d04-x01-y01", "d05-x01-y01"] #leading jet pt
        names2 = ["d06-x01-y01", "d07-x01-y01", "d08-x01-y01", "d09-x01-y01"] #muon pt + leading jet pt
        names3 = ["d10-x01-y01", "d11-x01-y01", "d12-x01-y01"] #HT,2/2
        names4 = ["d13-x01-y01", "d14-x01-y01", "d15-x01-y01"] #muon pt + HT,2/2
        names5 = ["d16-x01-y01", "d17-x01-y01", "d18-x01-y01", "d19-x01-y01"] #w boson pt
        names6 = ["d20-x01-y01", "d21-x01-y01", "d22-x01-y01", "d23-x01-y01"] #w boson pt + leading jet pt
        names7 = ["d24-x01-y01", "d25-x01-y01", "d26-x01-y01"] #w boson pt + HT,2/2
        if any(name in tablename for name in names1):
            xtitle = "Leading Jet pT"
        elif any(name in tablename for name in names2):
            xtitle = "Muon pT + Leading Jet pT"
        elif any(name in tablename for name in names3):
            xtitle = "HT,2/2"
        elif any(name in tablename for name in names4):
            xtitle = "Muon pT + HT,2/2"
        elif any(name in tablename for name in names5):
            xtitle = "W pT"
        elif any(name in tablename for name in names6):
            xtitle = "W pT + Leading Jet pT"
        elif any(name in tablename for name in names7):
            xtitle = "W pT + HT,2/2"
        else:
            xtitle = str(tablename)
       
        if (process == 'W1J'):
            xtitle += ", W+1 jet incl."
        elif (process == 'W2J'):
            xtitle += ", W+2 jet incl."
        elif (process == 'W3J'):
            xtitle += ", W+3 jet incl."

        #create figure
        fig, ax = plt.subplots()

        ######################################################

        #initialize list of all xsec vals, organized by bin
        xsecvalsList = [[0 for x in range(numMembers)] for y in range(numObsBin)]

        print ("\n--- Doing central/nominal PDF member first ---")
        print ("--- Doing PDF member #"+str(fnlo.GetIPDFMember())+" ---")
        fnlo.CalcCrossSection()
        fnlo.PrintCrossSections()
        xsecvalsNominal = fnlo.GetCrossSection()
        #print ("Nominal xsec vals:\n"+str(xsecvalsNominal))
        xCheck_Nominal = []
        for iBin in range(0, numObsBin):
            xsecvalsList[iBin][0] = xsecvalsNominal[iBin]
            xCheck_Nominal.append(xsecvalsNominal[iBin]/xsecvalsNominal[iBin])
        print("\n")

        #Start loop at 1, because nominal member number is #0
        for iMem in range(1, numMembers, 1):
            print (" --- Doing PDF member #"+str(iMem)+" ---")
            fnlo.SetLHAPDFMember( int(iMem) )
            fnlo.CalcCrossSection()
            memxsecvals = fnlo.GetCrossSection()
            xsecvalsRatio = []
            for iBin in range(0, numObsBin):
                #sorting each PDF member's xsec values by bin
                xsecvalsList[iBin][iMem] = memxsecvals[iBin]
                #for plotting the ratio to nominal
                xsecvalsRatio.append( memxsecvals[iBin]/xsecvalsNominal[iBin] )          
            ax.plot( binCenters, xsecvalsRatio, color='#808080', linestyle=':', linewidth=1, markersize=0 )

        ax.plot( binCenters, xCheck_Nominal, color='black', linestyle='--', linewidth=2, marker='D', markersize=4 )
        ax.set_ylabel('Ratio to Central XSec')
        ax.set_xlabel(xtitle+' [GeV]')
        ax.set_ylim(0.9, 1.1)
        ax.set_xlim(binCenters[0]-5., binCenters[numObsBin-1]+5.)
       
        ######################################################

        #determine analysis method of error sets
        if "NNPDF" in str(pdfset):
            if "hessian" in str(pdfset):
                doMCreplicas = False
                print("\n---------> NNPDF set but Hessian representation!")
                print("Treat Hessian uncertainties as symmetric!")
                numHessVectors = int((numMembers-1)/2.)
                print("Number of PDF members: "+str(numMembers)+", Number of Hessian eigenvectors: "+str(numHessVectors))
                ax.text(binCenters[numObsBin-3], 1.075, str(pdfset)+': Hessian Errors', fontsize=11)
            if not "hessian" in str(pdfset):
                doMCreplicas = True
                print("\n---------> Assuming error sets are MC replicas!")
                print("Number of PDF members: "+str(numMembers)+", Number of MC replicas: "+str(numMembers-1))
                ax.text(binCenters[numObsBin-3], 1.075, str(pdfset)+': MC Replica Errors', fontsize=11)
        else:
            doMCreplicas = False
            print("\n---------> Assuming error sets are Hessian uncertanties!")
            print("Treat Hessian uncertainties as anti-symmetric!")
            numHessVectors = int((numMembers-1)/2.)
            print("Number of PDF members: "+str(numMembers)+", Number of Hessian eigenvectors: "+str(numHessVectors))
            ax.text(binCenters[numObsBin-3], 1.075, str(pdfset)+': Hessian Errors', fontsize=11)

        #start analysis of error sets
        yerrLowList = []
        yerrUpList = []
        ploterrLowList = []
        ploterrUpList = []
        print("\nStatistics by bin:")
        for iBin in range(0, numObsBin):
            print("-------> Bin #"+str(iBin)+", "+str(binCenters[iBin])+" GeV")
            print("Maximum Value: "+str( max(xsecvalsList[iBin]) ))
            print("Nominal Value: "+str( xsecvalsNominal[iBin] ))
            print("Minimum Value: "+str( min(xsecvalsList[iBin]) ))

            if (doMCreplicas):
                sumUpTemp = 0.
                sumLowTemp = 0.
                for iMem in range(1, numMembers, 1):
                    sumUpTemp += (xsecvalsList[iBin][iMem]-xsecvalsNominal[iBin])**2
                    sumLowTemp += (xsecvalsList[iBin][iMem]-xsecvalsNominal[iBin])**2
                yerrLowList.append(math.sqrt( (1./(numMembers-2.))*sumLowTemp ))
                yerrUpList.append(math.sqrt( (1./(numMembers-2.))*sumUpTemp ))
                print( "Up Error (Abs Value): "+str(yerrUpList[iBin])+", Down Error (Abs Value): "+str(yerrLowList[iBin]) )
                ploterrLowList.append( yerrLowList[iBin]/xsecvalsNominal[iBin] )
                ploterrUpList.append( yerrUpList[iBin]/xsecvalsNominal[iBin] )
                print( "% Up Error: "+str( ploterrUpList[iBin]*100. )+" % , % Down Error: "+str( ploterrLowList[iBin]*100. )+" %" )

            if not (doMCreplicas):
                sumUpTemp = 0. 
                sumLowTemp = 0.
                scaleFactor = 1.
                if "NNPDF" in str(pdfset):
                    print("---> NNPDF set selected, assuming Hessian eigenvectors constructed for 68% CL!")
                    for iVec in range(0, numHessVectors, 1):
                        iMemUp = (2*iVec)+1 #Up variations are 1, 3, 5, ...
                        iMemDown = (2*iVec)+2 #Down variations are 2, 4, 6, ...
                        sumUpTemp += (xsecvalsList[iBin][iMemUp]-xsecvalsList[iBin][iMemDown])**2
                        sumLowTemp += (xsecvalsList[iBin][iMemUp]-xsecvalsList[iBin][iMemDown])**2
                    yerrLowList.append(scaleFactor*0.5*math.sqrt(sumLowTemp))
                    yerrUpList.append(scaleFactor*0.5*math.sqrt(sumUpTemp))
                    print( "Up Error: "+str(yerrUpList[iBin])+", Down Error: "+str(yerrLowList[iBin]) )
                    ploterrLowList.append( yerrLowList[iBin]/xsecvalsNominal[iBin] )
                    ploterrUpList.append( yerrUpList[iBin]/xsecvalsNominal[iBin] )
                    print( "% Up Error: "+str( ploterrUpList[iBin]*100. )+" % , % Down Error: "+str( ploterrLowList[iBin]*100. )+" %" )
                if not "NNPDF" in str(pdfset):
                    if "CT14" in (pdfset):
                        scaleFactor = 1./1.645
                        print("---> CT14 PDF set selected, scaling errors to go from 90% -> 68% CL!")
                    for iVec in range(0, numHessVectors, 1):
                        iMemUp = (2*iVec)+1 #Up variations are 1, 3, 5, ...
                        iMemDown = (2*iVec)+2 #Down variations are 2, 4, 6, ...
                        #print("Eigenvector #"+str(iVec+1)+", Up/Down: "+str(iMemUp)+"/"+str(iMemDown))
                        sumUpTemp += (max((xsecvalsList[iBin][iMemUp]-xsecvalsNominal[iBin]), (xsecvalsList[iBin][iMemDown]-xsecvalsNominal[iBin]), 0))**2
                        sumLowTemp += (max((xsecvalsNominal[iBin]-xsecvalsList[iBin][iMemUp]), (xsecvalsNominal[iBin]-xsecvalsList[iBin][iMemDown]), 0))**2
                    yerrLowList.append(scaleFactor*math.sqrt(sumLowTemp))
                    yerrUpList.append(scaleFactor*math.sqrt(sumUpTemp))
                    print( "Up Error: "+str(yerrUpList[iBin])+", Down Error: "+str(yerrLowList[iBin]) )
                    ploterrLowList.append( yerrLowList[iBin]/xsecvalsNominal[iBin] )
                    ploterrUpList.append( yerrUpList[iBin]/xsecvalsNominal[iBin] )
                    print( "% Up Error: "+str( ploterrUpList[iBin]*100. )+" % , % Down Error: "+str( ploterrLowList[iBin]*100. )+" %" )

        print("\nWriting the out .csv file!")
        outFileName = str("pdfUncert-%s-%s-%s.csv" % (pdfset, process, tablename))
        outFile = open(outFileName, "w")
        outFile.write("'YERRLOW','YERRUP'\n")
        for i, yerrLow in enumerate(yerrLowList):
            outFile.write( '%s,%s\n' % (yerrLowList[i], yerrUpList[i]) )
        outFile.close()

        #ax.errorbar( binCenters, xCheck_Nominal, xerr=None, yerr=None, fmt='ko', ecolor='k', capthick=1.5 ) 
        ax.errorbar( binCenters, xCheck_Nominal, xerr=None, yerr=[ploterrLowList, ploterrUpList], fmt='ko', ecolor='k', capthick=1.5 )
        outName = "pdfUncertPlot-"+str(pdfset)+"-"+str(process)+"-"+str(tablename)
        if (doMCreplicas):
            outName += "-MCreplicas"
        if not (doMCreplicas):
            outName += "-Hessian"
        outName += ".pdf"
        fig.savefig(outName)

print '\nFinished!'
