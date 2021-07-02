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
#process = 'W1J'
#basedir = '/home/awisecar/AlphaSVar-WJets/openloops/Jan10/1j/mcgrid/MCgrid_CMS_2018_WJetsAlphaS_1j_OL/'
#tablenames = ['d02-x01-y01.merged', 'd06-x01-y01.merged', 'd16-x01-y01.merged', 'd20-x01-y01.merged']
#tablenames = ['d02-x01-y01.merged']
#tablenames = ['d06-x01-y01.merged']
#tablenames = ['d16-x01-y01.merged']
#tablenames = ['d20-x01-y01.merged']
#process = 'W2J'
#basedir = '/home/awisecar/AlphaSVar-WJets/openloops/Jan10/2j/mcgrid/MCgrid_CMS_2018_WJetsAlphaS_2j_OL/'
#tablenames = ['d03-x01-y01.merged', 'd07-x01-y01.merged', 'd10-x01-y01.merged', 'd13-x01-y01.merged', 'd17-x01-y01.merged', 'd21-x01-y01.merged', 'd24-x01-y01.merged']
#tablenames = ['d03-x01-y01.merged']
#tablenames = ['d07-x01-y01.merged']
#tablenames = ['d10-x01-y01.merged']
#tablenames = ['d13-x01-y01.merged']
#tablenames = ['d17-x01-y01.merged']
#tablenames = ['d21-x01-y01.merged']
#tablenames = ['d24-x01-y01.merged']
process = 'W3J'
basedir = '/home/awisecar/AlphaSVar-WJets/openloops/Jan23/3j/mcgrid/MCgrid_CMS_2018_WJetsAlphaS_3j_OL/50M/'
#tablenames = ['d04-x01-y01.merged', 'd08-x01-y01.merged', 'd11-x01-y01.merged', 'd14-x01-y01.merged', 'd18-x01-y01.merged', 'd22-x01-y01.merged', 'd25-x01-y01.merged']
#tablenames = ['d04-x01-y01.merged']
#tablenames = ['d08-x01-y01.merged']
#tablenames = ['d11-x01-y01.merged']
tablenames = ['d14-x01-y01.merged']
#tablenames = ['d18-x01-y01.merged']
#tablenames = ['d22-x01-y01.merged']
#tablenames = ['d25-x01-y01.merged']

# 6.11.18: OpenLoops tables need to be read with flexible flavor scheme in order for proper Rivet-FNLO closure
doOpenLoops = True

#pdfsets = ['NNPDF23_nlo', 'CT10nlo', 'CT14nlo', 'NNPDF31_nnlo', 'NNPDF30_nlo']
#pdfsets = ['NNPDF30_nlo_as_0118']
#pdfsets = ['NNPDF30_nnlo_as_0118']
#pdfsets = ['CT10nlo']
pdfsets = ['CT14nlo']
#pdfsets = ['CT14nnlo']

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

        #fnlo.SetAlphasMz(0.1181, True); #2018 PDG value
        fnlo.SetAlphasMz(0.1181) #2018 PDG value
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

        print("\nIs this table 'flexible-scale'?")
        print("fnlo.GetIsFlexibleScaleTable() = "+str(fnlo.GetIsFlexibleScaleTable()))
        xMuR = [0.5, 2.0, 0.5, 1.0, 1.0, 2.0]
        xMuF = [0.5, 2.0, 1.0, 0.5, 2.0, 1.0]
        #initialize list of all xsec vals, organized by bin
        xsecvalsList = [[0 for x in range(len(xMuR)+1)] for y in range(numObsBin)]

        print ("\n--- Doing nominal xsec first ---")
        print ("--- mu_R scale factor = "+str(fnlo.GetScaleFactorMuR())+", mu_F scale factor = "+str(fnlo.GetScaleFactorMuF())+" ---")
        fnlo.CalcCrossSection()
        fnlo.PrintCrossSections()
        xsecvalsNominal = fnlo.GetCrossSection()
        #print ("Nominal xsec vals:\n"+str(xsecvalsNominal))
        xCheck_Nominal = []
        for iBin in range(0, numObsBin):
            xsecvalsList[iBin][0] = xsecvalsNominal[iBin]
            xCheck_Nominal.append(xsecvalsNominal[iBin]/xsecvalsNominal[iBin])
       
        print("\n-------> Starting scale variations!")
        fnlo.UseHoppetScaleVariations(True)
        for iVar,variation in enumerate(xMuR):
            print("\nAttempting: mu_R scale = "+str(xMuR[iVar])+", mu_F scale = "+str(xMuF[iVar])+" ---")
            scaleSetCheck = fnlo.SetScaleFactorsMuRMuF(xMuR[iVar], xMuF[iVar])
            #print("scaleSetCheck = "+str(scaleSetCheck))
            print ("Check: mu_R scale factor = "+str(fnlo.GetScaleFactorMuR())+", mu_F scale factor = "+str(fnlo.GetScaleFactorMuF())+" ---")
            print ("Getting cross sections...")
            fnlo.CalcCrossSection()
            memxsecvals = fnlo.GetCrossSection()
            xsecvalsRatio = []
            for iBin in range(0, numObsBin):
                xsecvalsList[iBin][iVar+1] = memxsecvals[iBin]
                xsecvalsRatio.append( memxsecvals[iBin]/xsecvalsNominal[iBin] )
            ax.plot( binCenters, xsecvalsRatio, color='#808080', linestyle=':', linewidth=1, markersize=0 )

        #print("\n"+str(xsecvalsList))
        #print("\n"+str(xsecvalsList[0]))

        ax.plot( binCenters, xCheck_Nominal, color='black', linestyle='--', linewidth=2, marker='D', markersize=4 )
        ax.set_ylabel('Ratio to Central')
        ax.set_xlabel(xtitle+' [GeV]')
        ax.set_ylim(0.5, 1.5)
        ax.set_xlim(binCenters[0]-5., binCenters[numObsBin-1]+5.)

        ######################################################

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
            yerrLowList.append( abs(min(xsecvalsList[iBin])-xsecvalsNominal[iBin]) )
            yerrUpList.append( abs(max(xsecvalsList[iBin])-xsecvalsNominal[iBin]) )
            print( "Up Error (Abs Value): "+str(yerrUpList[iBin])+", Down Error (Abs Value): "+str(yerrLowList[iBin]) )
            ploterrLowList.append( abs((min(xsecvalsList[iBin])-xsecvalsNominal[iBin])/(xsecvalsNominal[iBin])) )
            ploterrUpList.append( abs((max(xsecvalsList[iBin])-xsecvalsNominal[iBin])/(xsecvalsNominal[iBin])) )
            print( "% Up Error: "+str( (max(xsecvalsList[iBin])-xsecvalsNominal[iBin])*100./(xsecvalsNominal[iBin]) )+" % , % Down Error: "+str( (min(xsecvalsList[iBin])-xsecvalsNominal[iBin])*100./(xsecvalsNominal[iBin]) )+" %" )

        print("\nWriting the out .csv file!")
        outFileName = str("scaleUncert-%s-%s-%s.csv" % (pdfset, process, tablename))
        outFile = open(outFileName, "w")
        outFile.write("'YERRLOW','YERRUP'\n")
        for i, yerrLow in enumerate(yerrLowList):
            outFile.write( '%s,%s\n' % (yerrLowList[i], yerrUpList[i]) )
        outFile.close()

        ax.errorbar( binCenters, xCheck_Nominal, xerr=None, yerr=[ploterrLowList, ploterrUpList], fmt='ko', ecolor='k', capthick=1.5 )
        outName = "scaleUncertPlot-"+str(pdfset)+"-"+str(process)+"-"+str(tablename)+".pdf"
        fig.savefig(outName)


print '\nFinished!'
