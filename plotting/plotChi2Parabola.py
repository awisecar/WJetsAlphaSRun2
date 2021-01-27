#! /usr/bin/env python3
import os
import sys
import re
import math
import argparse
from array import array
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import ROOT
##################################################
'''
...comments...
'''
##################################################
### R21 (list num first, then denom)
numerator = 'W2J'
denominator = 'W1J'
tablenames = [ ['d07-x01-y01.merged','d06-x01-y01.merged'], ['d07-x01-y01.merged','d31-x01-y01.merged'], ['d57-x01-y01.merged','d56-x01-y01.merged'], ['d57-x01-y01.merged','d81-x01-y01.merged'] ]
variables = [ ["LepPtPlusLeadingJetPt_Zinc2jet_TUnfold", "LepPtPlusLeadingJetPt_Zinc1jet_TUnfold"], ["LepPtPlusLeadingJetPt_Zinc2jet_TUnfold", "LepPtPlusLeadingJetPt_Zexc1jet_TUnfold"], ["LepPtPlusLeadingJetAK8Pt_Zinc2jet_TUnfold", "LepPtPlusLeadingJetAK8Pt_Zinc1jet_TUnfold"], ["LepPtPlusLeadingJetAK8Pt_Zinc2jet_TUnfold", "LepPtPlusLeadingJetAK8Pt_Zexc1jet_TUnfold"] ]
## --
#pdfnames = ['CT10nlo', 'CT14nlo', 'NNPDF23_nlo', 'NNPDF30_nlo', 'NNPDF31_nnlo']
pdfnames = ['CT14nlo']
## also consider... NNPDF31_nlo, ABMP16_5_nlo, HERAPDF20_NLO, MMHT2014nlo68cl
## --
doNP = True
# doNP = False
## --
# doTheoryErrs = True
doTheoryErrs = False
##################################################
MEgen = "Openloops"
order = "NLO"
basedir = "./"+MEgen+"/"+order+"/"
outDir = ("plotsFastNLO/")
os.system(("mkdir -p ")+basedir+outDir)

ROOT.gStyle.SetLineStyleString(11,"10 10")
ROOT.gStyle.SetLegendTextSize(0.022)

for tablename in tablenames:
    print ("\n----------------> Doing distribution: "+str(tablename))
    for pdfname in pdfnames:
        print ("\n--------> Doing PDF series: "+str(pdfname))

        ##################################################################################
        ## -- Load all necessary files, distributions, corrections --

        ## --
        ## Load csv files for FastNLO xsecs, ROOT file for unfolded distributions
        ## --





        ## Get FastNLO csv files
        csvInfileMEPDFnum = "aSVarMEPDF-"+pdfname+"-"+numerator+"-"+tablename[0]+".csv"
        csvInfileMEPDFdenom = "aSVarMEPDF-"+pdfname+"-"+denominator+"-"+tablename[1]+".csv"
        dataInMEPDFnum = pd.read_csv(basedir+csvInfileMEPDFnum, skiprows=[1])
        dataInMEPDFdenom = pd.read_csv(basedir+csvInfileMEPDFdenom, skiprows=[1])

        ## Grab the alpha-s value for each dataseries to use as label
        ## Only need to do this for numerator
        alphasNamesMEPDF = pd.read_csv(basedir+csvInfileMEPDFnum, nrows=1)
        alphasvalsMEPDF = alphasNamesMEPDF.values.tolist()[0][3:]
        numVarMEPDF = int(alphasNamesMEPDF.values.tolist()[0][2])  #total number of alpha-s variations for ME+PDF
        print ("Number of ME+PDF variations: "+str(int(numVarMEPDF)))
        print ("Doing ME+PDF variations: "+str(alphasvalsMEPDF))

        ## Number of bins should be the same for two different files
        numBins = int(alphasNamesMEPDF.values.tolist()[0][0])  #number of bins in the distribution
        print ("Number of bins in histogram: "+str(int(numBins)))
        ## Check that binnings between num and denom are the same
        binCenNum = array('d')
        binCenDenom = array('d')
        for i in range(int(numBins)):
            binCenNum.append((dataInMEPDFnum["'BINCENTER'"].values)[i])
            binCenDenom.append(dataInMEPDFdenom["'BINCENTER'"].values[i])
        if (binCenNum == binCenDenom):
            print ("\nBinning of two distributions is equal: \n"+str(binCenNum))
        else:
            print ("\nBinning of two distributions is not equal! Exiting...")
            sys.exit()






        ## Get input data file
        variableNum   = variables[iTab][0]
        variableDenom = variables[iTab][1]
        fileNameRatio = ("UnfoldedFilesRatio_Run2/SMu_RATIO_"+variableNum+"_TO_"+variableDenom+"_JetPtMin_30_JetEtaMax_24_MGPYTHIA6_.root")
        print ("\nOpening file: "+fileNameRatio)
        fRatio = ROOT.TFile.Open(fileNameRatio, "READ")

        ## Remember differences in number of leading bins between unfolded and FastNLO distributions
        if ((numerator == 'W2J') and (denominator == 'W1J')):
            if (tablename[0] == 'd07-x01-y01.merged' and tablename[1] == 'd06-x01-y01.merged'):
                binDataOffset = 2
            if (tablename[0] == 'd07-x01-y01.merged' and tablename[1] == 'd31-x01-y01.merged'):
                binDataOffset = 2
            if (tablename[0] == 'd57-x01-y01.merged' and tablename[1] == 'd56-x01-y01.merged'):
                binDataOffset = 1
            if (tablename[0] == 'd57-x01-y01.merged' and tablename[1] == 'd81-x01-y01.merged'):
                binDataOffset = 1

        print ("\n===========================================================================")
        print("\nDoing variables: "+str(variableNum)+" & "+str(variableDenom))
        print ("Number of ME+PDF variations: "+str(int(numVarMEPDF)))
        print ("Number of bins in histogram: "+str(int(numBins)))




        ## --
        ## Get all corrections to FastNLO fixed order xsecs
        ## --

        ## Non-perturbative corrections
        if not (doNP):
            isNP = ""
            nonpertSFs = np.ones(numBins)
        else:
            print ("\n~~~ Adding non-perturbative corrections! ~~~")
            isNP = "-NP"
            nonpertSFs = []
            if (tablename[0] == 'd07-x01-y01.merged' and tablename[1] == 'd06-x01-y01.merged'): 
                nonpertSFnum = [1.3896005897157113, 1.2470054856288724, 1.137700633319125, 1.0706067860636121, 1.0364868374388996, 1.0204210577848034, 1.0121440610542551, 1.0071749547041193, 1.0043442086436452, 1.0026876020828206]
                nonpertSFdenom = [1.2010625918051203, 1.1298239392566556, 1.07133490626799, 1.0322962846450936, 1.0105480864823724, 0.9993642232331477, 0.9931152945868026, 0.9890435762337125, 0.9865012348803278, 0.9848357027014492]
            if (tablename[0] == 'd07-x01-y01.merged' and tablename[1] == 'd31-x01-y01.merged'): 
                nonpertSFnum = [1.3896005897157113, 1.2470054856288724, 1.137700633319125, 1.0706067860636121, 1.0364868374388996, 1.0204210577848034, 1.0121440610542551, 1.0071749547041193, 1.0043442086436452, 1.0026876020828206]
                nonpertSFdenom = [1.19275844350739, 1.1199652421556099, 1.0589974205974122, 1.0173041320196443, 0.9934555951734685, 0.9808749675176636, 0.9736785761375525, 0.9688768894234097, 0.9657979786368535, 0.9637136791419829]
            if (tablename[0] == 'd57-x01-y01.merged' and tablename[1] == 'd56-x01-y01.merged'): 
                nonpertSFnum = [1.285717560676564, 1.1578183804295012, 1.0885000425493627, 1.0508123713199902, 1.03434786285872, 1.0273568362470915, 1.024286202584473, 1.0232033623310892, 1.0229147149114493]
                nonpertSFdenom = [1.1011794317605685, 1.0899096172250768, 1.078483162968084, 1.0659008006921162, 1.053810096192782, 1.0420880619495763, 1.0290413747579634, 1.0146062990008113, 0.9980935928741425]
            if (tablename[0] == 'd57-x01-y01.merged' and tablename[1] == 'd81-x01-y01.merged'): 
                nonpertSFnum = [1.285717560676564, 1.1578183804295012, 1.0885000425493627, 1.0508123713199902, 1.03434786285872, 1.0273568362470915, 1.024286202584473, 1.0232033623310892, 1.0229147149114493]
                nonpertSFdenom = [1.1010032257492965, 1.0898741520851927, 1.0785332788034736, 1.0659734773716554, 1.053827625966885, 1.041973526047908, 1.028679393484072, 1.013831966294646, 0.9966404959289775]
            for i in range(int(numBins)):
                nonpertSFs.append(nonpertSFnum[i]/nonpertSFdenom[i])
            print("\nApplying non-pertrubative corrections:\n"+str(nonpertSFs))

        ## --
        ## Get xsec ratio distributions, error information
        ## --

        ## Get unfolded ratio 
        hUnfRatio = fRatio.Get("UnfXSecRatio_Central")
        hUnfRatio.SetLineColor(ROOT.kBlack)
        hUnfRatio.SetLineWidth(3)
        hUnfRatio.SetMarkerColor(ROOT.kBlack)

        ## Get experimental uncertainty covariance matrix
        hTotCovMatrix = fRatio.Get("CovTotSyst")

        ## Get FastNLO xsecs, take ratios
        varArrayMEPDFlist = []
        print ("\nDoing ME+PDF xsec ratios with PDF set "+pdfname+"!")
        for i, alphas in enumerate(alphasvalsMEPDF):
            print ("alpha-s = "+str(round(alphas,3)))
            ## -- First get array for the ratio values --
            varArray = array('d')
            for j in range(int(numBins)):
                SFtemp = nonpertSFs[j]
                ratioTemp  = ((dataInMEPDFnum[("'aS=")+str(round(alphas,3))+("'")]).values)[j]
                ratioTemp /= ((dataInMEPDFdenom[("'aS=")+str(round(alphas,3))+("'")]).values)[j]
                ratioTemp *= SFtemp
                varArray.append(ratioTemp)
            varArrayMEPDFlist.append(varArray)
      


        ## Get theory uncertainties (scale and PDF), form covariance matrix
        # if (doTheoryErrs):
        #     xErrLow = array('d') #x-errors should just be the bin widths
        #     xErrUp = array('d')
        #     yErrLow = array('d')
        #     yErrUp = array('d')
                
        #     #stat error
        #     csvInfileStatUncertNum = "statUncert-"+pdfname+"-"+numerator+"-"+tablename[0]+".csv"
        #     csvInfileStatUncertDenom = "statUncert-"+pdfname+"-"+denominator+"-"+tablename[1]+".csv"
        #     dataInStatUncertNum = pd.read_csv(basedir+csvInfileStatUncertNum)
        #     dataInStatUncertDenom = pd.read_csv(basedir+csvInfileStatUncertDenom)
        #     yErrLowStat = array('d')
        #     yErrUpStat = array('d')
        #     for i in range(numBins):
        #         #x-errors are just the bin widths
        #         xErrLow.append( ((dataInStatUncertNum["'XERRLOW'"]).values)[i] )
        #         xErrUp.append( ((dataInStatUncertNum["'XERRUP'"]).values)[i] )

        #         binContentNumTemp = (dataInMEPDFnum[("'aS=0.118'")].values)[i]
        #         binContentDenomTemp = (dataInMEPDFdenom[("'aS=0.118'")].values)[i]
        #         binContentRatioTemp = binContentNumTemp/binContentDenomTemp

        #         #currently, stat errors are just derived as they would be for 0.118 distributions
        #         #and then applied to all the distributions
        #         yErrLowStatNum = ((dataInStatUncertNum["'YERRLOW'"]).values)[i]
        #         yErrLowStatDenom = ((dataInStatUncertDenom["'YERRLOW'"]).values)[i]
        #         yErrLowStat.append( binContentRatioTemp*math.sqrt((yErrLowStatNum/binContentNumTemp)**2 + (yErrLowStatDenom/binContentDenomTemp)**2)  )
        #         yErrUpStatNum = ((dataInStatUncertNum["'YERRUP'"]).values)[i]
        #         yErrUpStatDenom = ((dataInStatUncertDenom["'YERRUP'"]).values)[i]
        #         yErrUpStat.append( binContentRatioTemp*math.sqrt((yErrUpStatNum/binContentNumTemp)**2 + (yErrUpStatDenom/binContentDenomTemp)**2)  )
                
        #     #set y-error equal to contributions
        #     yErrLow = yErrLowStat
        #     yErrUp = yErrUpStat


        ##################################################################################
        ## -- Compute Chi-2 values --

        ## --
        ## Add all covariance matrices together into one object
        ## --


        ## --
        ## Do a loop over all alpha-s ratio distributions; 
        ## for each of these distributions, do a double-loop to compute chi-2
        ## Store chi-2 values in a list
        ## --

        ## Chi-2 method already in ROOT?


        chi2values = []



        
            
            
















        ##################################################################################
        ## -- Plot Chi-2 values, fit points with 2nd-order polynomial, extract alpha-s(Mz) --
        
        ## --
        ## Set up TCanvas and TH1
        ## --

        c1 = ROOT.TCanvas('can_', 'can_', 500, 500)
        c1.Update()
        c1.Draw()

        xmin = 0.108
        xmax - 0.128
        ymin = 0.
        ymax = 1000.

        htemp = ROOT.TH1D('htemp_', "htemp_", 100, xmin, xmax)
        htemp.SetStats(0)
        htemp.GetXaxis().SetTitle(xtitle)
        htemp.GetXaxis().SetTitleOffset(1.2)
        htemp.GetYaxis().SetTitle('Chi-2 vs. #alpha_{s}(Mz)')
        htemp.GetYaxis().SetTitleOffset(1.3)
        htemp.GetYaxis().SetRangeUser(ymin, ymax)
        htemp.SetTitle("")
        htemp.Draw()

        leg = ROOT.TLegend(0.34,0.775,0.9,0.9)

        ## --
        ## Plot chi-2 values vs alpha-s(Mz) values
        ## --

        chi2graph = ROOT.TGraph(int(numBins), xxx, chi2values)

        chi2graph.SetLineColorAlpha(4, 1.)
        chi2graph.SetLineWidth(2)
        chi2graph.SetLineStyle(1)
        chi2graph.SetMarkerColor(4)
        chi2graph.SetMarkerStyle(20)
        chi2graph.SetMarkerSize(0.7)
        chi2graph.Draw('P same')

        leg.AddEntry(chi2graph, "Chi-2 Fit", "lp")

        ## --
        ## Fit distribution with 2nd order polynomial
        ## https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
        ## --

        def func(x, c1, c2, c3):
            return c1 + c2/(x ** c3)
        popt, pcov = curve_fit(func, binCent_NPOn, corrNP, sigma=corrNPerrs, bounds=((0.9, -np.inf, -np.inf), (1.1, np.inf, np.inf)))
        print("\nResults of fit --")
        print("Constants of fit: "+str(popt))
        print("NP correction values from the fit:\n"+str( list(func(binCent_NPOn, *popt)) ))



        

        ## --
        ## Extract alpha-s(Mz) from minimum of fit, errors using (chi-2)+1
        ## --


        ## --
        ## Draw legend, then final result on plot using TLatex object
        ## --
        
        leg.Draw("same")

        procLatex = ROOT.TLatex()
        procLatex.SetNDC()
        procLatex.SetTextSize(0.025)
        procLatex.SetLineWidth(2)
        procLatex.SetTextFont(42)
        procLatex.SetTextColor(ROOT.kBlack)
        procLatex.SetTextAlign(11)
        procLatex.SetName("procLatex")
        procLatex.DrawLatex(0.55,legLowY-0.04, MEgen+"+Sherpa, NLO QCD")
        if (numerator == "W2J"):
            if (tablename[1] == 'd31-x01-y01.merged' or tablename[1] == 'd81-x01-y01.merged'):
                wtitle = "R_{21_{excl.}} = #frac{W(#rightarrow#mu#nu) + 2j + X}{W(#rightarrow#mu#nu) + 1j}"
            else:
                wtitle = "R_{21} = #frac{W(#rightarrow#mu#nu) + 2j + X}{W(#rightarrow#mu#nu) + 1j + X}"
        if (tablename[1] == 'd31-x01-y01.merged' or tablename[1] == 'd81-x01-y01.merged'):
            procLatex.DrawLatex(0.58,legLowY-0.1, wtitle)
        else:
            procLatex.DrawLatex(0.58,legLowY-0.1, wtitle)
        
        ##################################################################################

        print("")
        c1.Update()
        c1.Print(basedir+outDir+"chi2Dist-"+numerator+"-"+denominator+"-"+tablename[0]+"-"+tablename[1]+"-"+pdfname+isNP+".pdf")
        del c1
        del htemp

print ('\nFinished!\n')        