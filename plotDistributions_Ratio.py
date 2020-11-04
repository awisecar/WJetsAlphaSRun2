#! /usr/bin/env python3
import os
import sys
import numpy as np
import pandas as pd
import math
from array import array
import ROOT
##################################################
'''
This script is designed to plot ratios of xsecs from FastNLO tables against the  
unfolded data and other theory predictions
> numerator, denominator, tablenames are for selecting the distributions
> pdfnames is for selecting the PDF set that the FastNLO tables are read with
> doErrors turns on the statistical errors for the FastNLO xsecs
> doNP turns on the application of non-perturbative corrections to FastNLO xsecs
> doData gets the unfolded data and other theory predictions from unfolding code
'''
##################################################
### R21 (list num first, then denom)
numerator = 'W2J'
denominator = 'W1J'
tablenames = [ ['d07-x01-y01.merged','d06-x01-y01.merged'], ['d07-x01-y01.merged','d31-x01-y01.merged'], ['d57-x01-y01.merged','d56-x01-y01.merged'], ['d57-x01-y01.merged','d81-x01-y01.merged'] ]
## --
#pdfnames = ['CT10nlo', 'CT14nlo', 'NNPDF23_nlo', 'NNPDF30_nlo', 'NNPDF31_nnlo']
pdfnames = ['CT14nlo']
## --
# doErrors = True
doErrors = False
## --
doNP = True
# doNP = False
## --
doData = True
# doData = False
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
        ## 1) Grab data
        
        csvInfileMEnum = "aSVarME-"+pdfname+"-"+numerator+"-"+tablename[0]+".csv"
        csvInfileMEdenom = "aSVarME-"+pdfname+"-"+denominator+"-"+tablename[1]+".csv"
        csvInfileMEPDFnum = "aSVarMEPDF-"+pdfname+"-"+numerator+"-"+tablename[0]+".csv"
        csvInfileMEPDFdenom = "aSVarMEPDF-"+pdfname+"-"+denominator+"-"+tablename[1]+".csv"

        ## Grab the alpha-s value for each dataseries to use as label
        ## Only need to do this for numerator
        # just ME var
        alphasNamesME = pd.read_csv(basedir+csvInfileMEnum, nrows=1) #grabbing first row of diagonistic information
        alphasvalsME = alphasNamesME.values.tolist()[0][3:]
        numVarME = int(alphasNamesME.values.tolist()[0][2]) #total number of alpha-s variations for ME
#        print ("\nDoing ME variations: "+str(alphasvalsME))
        # ME and PDF var
        alphasNamesMEPDF = pd.read_csv(basedir+csvInfileMEPDFnum, nrows=1)
        alphasvalsMEPDF = alphasNamesMEPDF.values.tolist()[0][3:]
        numVarMEPDF = int(alphasNamesMEPDF.values.tolist()[0][2])  #total number of alpha-s variations for ME+PDF
#        print ("Doing ME+PDF variations: "+str(alphasvalsMEPDF))
        #num of bins should be the same for two different files
        numBins = int(alphasNamesME.values.tolist()[0][0])  #number of bins in the distribution
        
        ## Grab the FNLO distributions
        dataInMEnum = pd.read_csv(basedir+csvInfileMEnum, skiprows=[1]) #skip first row, but with keeping headers
        dataInMEdenom = pd.read_csv(basedir+csvInfileMEdenom, skiprows=[1])
        dataInMEPDFnum = pd.read_csv(basedir+csvInfileMEPDFnum, skiprows=[1])
        dataInMEPDFdenom = pd.read_csv(basedir+csvInfileMEPDFdenom, skiprows=[1])

        ## Grab unfolded data and signal W+jets MC
        ## Need to make sure that these unfolded variables exist
        if ((numerator == 'W2J') and (denominator == 'W1J')):
            if (tablename[0] == 'd07-x01-y01.merged' and tablename[1] == 'd06-x01-y01.merged'):
                variableNum = "LepPtPlusLeadingJetPt_Zinc2jet_TUnfold"
                variableDenom = "LepPtPlusLeadingJetPt_Zinc1jet_TUnfold"
            elif (tablename[0] == 'd07-x01-y01.merged' and tablename[1] == 'd31-x01-y01.merged'):
                variableNum = "LepPtPlusLeadingJetPt_Zinc2jet_TUnfold"
                variableDenom = "LepPtPlusLeadingJetPt_Zexc1jet_TUnfold"
            elif (tablename[0] == 'd57-x01-y01.merged' and tablename[1] == 'd56-x01-y01.merged'):
                variableNum = "LepPtPlusLeadingJetAK8Pt_Zinc2jet_TUnfold"
                variableDenom = "LepPtPlusLeadingJetAK8Pt_Zinc1jet_TUnfold"
            elif (tablename[0] == 'd57-x01-y01.merged' and tablename[1] == 'd81-x01-y01.merged'):
                variableNum = "LepPtPlusLeadingJetAK8Pt_Zinc2jet_TUnfold"
                variableDenom = "LepPtPlusLeadingJetAK8Pt_Zexc1jet_TUnfold"

        print ("\n===========================================================================")
        print("\nDoing variables: "+str(variableNum)+" & "+str(variableDenom))
        print ("Number of ME variations: "+str(int(numVarME)))
        print ("Number of ME+PDF variations: "+str(int(numVarMEPDF)))
        print ("Number of bins in histogram: "+str(int(numBins)))

        # If including data, first get input filename
        if (doData):
            fileNameRatio = ("UnfoldedFilesRatio_Run2/SMu_RATIO_"+variableNum+"_TO_"+variableDenom+"_JetPtMin_30_JetEtaMax_24_MGPYTHIA6_.root")
            print ("\nOpening file: "+fileNameRatio)
            fRatio = ROOT.TFile.Open(fileNameRatio, "READ")
        
        ##################################################################################
        ## 1b) Grab uncertainties and SFs

        ####### Errors
        if (doErrors):
            xErrLow = array('d') #x-errors should just be the bin widths
            xErrUp = array('d')
            yErrLow = array('d')
            yErrUp = array('d')
                
            #stat error
            csvInfileStatUncertNum = "statUncert-"+pdfname+"-"+numerator+"-"+tablename[0]+".csv"
            csvInfileStatUncertDenom = "statUncert-"+pdfname+"-"+denominator+"-"+tablename[1]+".csv"
            dataInStatUncertNum = pd.read_csv(basedir+csvInfileStatUncertNum)
            dataInStatUncertDenom = pd.read_csv(basedir+csvInfileStatUncertDenom)
            yErrLowStat = array('d')
            yErrUpStat = array('d')
            for i in range(numBins):
                #x-errors are just the bin widths
                xErrLow.append( ((dataInStatUncertNum["'XERRLOW'"]).values)[i] )
                xErrUp.append( ((dataInStatUncertNum["'XERRUP'"]).values)[i] )

                binContentNumTemp = (dataInMEPDFnum[("'aS=0.118'")].values)[i]
                binContentDenomTemp = (dataInMEPDFdenom[("'aS=0.118'")].values)[i]
                binContentRatioTemp = binContentNumTemp/binContentDenomTemp

                #currently, stat errors are just derived as they would be for 0.118 distributions
                #and then applied to all the distributions
                yErrLowStatNum = ((dataInStatUncertNum["'YERRLOW'"]).values)[i]
                yErrLowStatDenom = ((dataInStatUncertDenom["'YERRLOW'"]).values)[i]
                yErrLowStat.append( binContentRatioTemp*math.sqrt((yErrLowStatNum/binContentNumTemp)**2 + (yErrLowStatDenom/binContentDenomTemp)**2)  )
                yErrUpStatNum = ((dataInStatUncertNum["'YERRUP'"]).values)[i]
                yErrUpStatDenom = ((dataInStatUncertDenom["'YERRUP'"]).values)[i]
                yErrUpStat.append( binContentRatioTemp*math.sqrt((yErrUpStatNum/binContentNumTemp)**2 + (yErrUpStatDenom/binContentDenomTemp)**2)  )
                
            #set y-error equal to contributions
            yErrLow = yErrLowStat
            yErrUp = yErrUpStat

        ####### Non-Perturbative Corrections
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

        ##################################################################################
        ## 2) Plot xsec distributions
        
        #Note: if don't want any pads, just uncommented the following three lines and comment out the tpad stuff
        # c1 = ROOT.TCanvas('canRatios_', 'canRatios_', 500, 500)
        # c1.Update()
        # c1.Draw()

        # Doing canvas with two pads
        c1 = ROOT.TCanvas('canRatios_', 'canRatios_', 600, 800)
        c1.cd()
        pad1 = ROOT.TPad("pad1.1", "pad1.1", 0, 0.3, 1, 1)
        pad2 = ROOT.TPad("pad1.2", "pad1.2", 0, 0, 1, 0.3);
        pad1.SetTopMargin(0.075)
        pad1.SetBottomMargin(0)
        pad1.SetTicks()
        pad1.Draw()
        pad2.SetTopMargin(0)
        pad2.SetBottomMargin(0.3)
        pad2.SetTicks()
        pad2.Draw()

        ## ---------------------------------------------------
        ## ---------------------- PAD 1 ----------------------
        ## ---------------------------------------------------
        pad1.cd()

        ## Check binnings between num and denom are the same
        binCenMEnum = array('d')
        binCenMEdenom = array('d')
        for i in range(int(numBins)):
            binCenMEnum.append((dataInMEnum["'BINCENTER'"].values)[i])
            binCenMEdenom.append(dataInMEdenom["'BINCENTER'"].values[i])
        if (binCenMEnum == binCenMEdenom):
            print ("\nBinning of num and denom ME distributions is equal: \n"+str(binCenMEnum))
        else:
            print ("\nBinning of num and denom ME distributions is not equal! Exiting code!")
            sys.exit()

        ## Open unfolded ratio here to fetch x-axis values
        ## Plot after the htemp histo is plotted
        # Don't forget about SetLineStyle, SetMarkerStyle commands if needed
        if (doData):
            hUnfRatio = fRatio.Get("UnfXSecRatio_Central")
            hUnfRatio.SetLineColor(ROOT.kBlack)
            hUnfRatio.SetLineWidth(2)
            hUnfRatio.SetMarkerColor(ROOT.kBlack)
            hSignalMCRatio = fRatio.Get("GenSignalXSecRatio_NLOFxFx")
            hSignalMCRatio.SetLineColor(ROOT.kOrange)
            hSignalMCRatio.SetLineWidth(2)
            hSignalMCRatio.SetMarkerColor(ROOT.kOrange)
            # # Getting x-axis bounds from unfolded data histogram
            # xmin = hUnfRatio.GetXaxis().GetXmin()
            # xmax = hUnfRatio.GetXaxis().GetXmax()
        # else:
        # Get x-axis bounds from FastNLO distributions
        xmin = binCenMEnum[0]-(binCenMEnum[1]-binCenMEnum[0])/2.
        xmax = binCenMEnum[numBins-1]+(binCenMEnum[numBins-1]-binCenMEnum[numBins-2])/2.

        ## Get y-bounds and titles depending on distribution
        ## Using linear y-axis for ratios
        if ((numerator == 'W2J') and (denominator == 'W1J')):
            title = 'Ratio of W+2j+X/W+1j+X'
            if (tablename[0] == 'd07-x01-y01.merged' and tablename[1] == 'd06-x01-y01.merged'):
                ymax = 1.4
                xtitle = 'Muon pT + Leading Jet pT [GeV]'
                title += ', Muon pT + Leading Jet pT'
                binDataOffset = 2
            if (tablename[0] == 'd07-x01-y01.merged' and tablename[1] == 'd31-x01-y01.merged'):
                ymax = 7.
                xtitle = 'Muon pT + Leading Jet pT [GeV]'
                title += ', Muon pT + Leading Jet pT'
                binDataOffset = 2
            if (tablename[0] == 'd57-x01-y01.merged' and tablename[1] == 'd56-x01-y01.merged'):
                ymax = 0.6
                xtitle = 'Muon pT + Leading Jet pT [GeV]'
                title += ', Muon pT + Leading Jet pT'
                binDataOffset = 1
            if (tablename[0] == 'd57-x01-y01.merged' and tablename[1] == 'd81-x01-y01.merged'):
                ymax = 0.8
                xtitle = 'Muon pT + Leading Jet pT [GeV]'
                title += ', Muon pT + Leading Jet pT'
                binDataOffset = 1
                
        ## Easier to change axis ranges if you draw a TH1 with those ranges first
        htemp = ROOT.TH1D("aSRatio_"+tablename[0]+"_TO_"+tablename[1], title, 100, xmin, xmax)
        htemp.GetYaxis().SetRangeUser(0.0001, ymax)
        htemp.SetStats(0)
        htemp.GetXaxis().SetTitle(xtitle)
        htemp.GetXaxis().SetTitleOffset(1.2)
        htemp.GetYaxis().SetTitle('Ratio')
        htemp.GetYaxis().SetTitleOffset(1.3)
        htemp.SetTitle("")
        htemp.Draw()

        ## Plot unfolded data and signal MC
        ## Ratios here use simple binomial errors for division
        ## More complicated setup with TEfficiency elsewhere
        if (doData):
            hUnfRatio.Draw("E same")
            hSignalMCRatio.Draw("E same")

        # Make legend
        leg1 = ROOT.TLegend(0.3,0.75,0.935,0.975)
        leg1.SetTextSize(0.027)
        if (doData):
            leg1.AddEntry(hUnfRatio, "Unfolded Data", "lp")
            leg1.AddEntry(hSignalMCRatio, "MG5_aMC FxFx + PY8 (#leq 2j NLO + PS)", "lp")

        #Keeping the graphs in a list allows us to draw multiple on canvas
        grMElist = []
        grMEPDFlist = []
        varArrayMElist = []
        varArrayMEPDFlist = []

        ## Get the ME xsec ratio variations --------------------
        print ("\nDoing ME xsec ratios!")
        for i, alphas in enumerate(alphasvalsME):
            print ("alpha-s = "+str(round(alphas,3)))
            ## -- First get array for the ratio values --
            varArray = array('d')
            for j in range(int(numBins)):
                SFtemp = nonpertSFs[j]
                ratioTemp  = (((dataInMEnum[("'aS=")+str(round(alphas,3))+("'")]).values)[j])
                ratioTemp /= (((dataInMEdenom[("'aS=")+str(round(alphas,3))+("'")]).values)[j])
                ratioTemp *= SFtemp
                varArray.append(ratioTemp)
            varArrayMElist.append(varArray)
            ## -- Now create the TGraph using this array --
            if (doErrors):
                gr = ROOT.TGraphAsymmErrors(int(numBins), binCenMEnum, varArray, xErrLow, xErrUp, yErrLow, yErrUp)
            else:
                gr = ROOT.TGraphAsymmErrors(int(numBins), binCenMEnum, varArray)
            ## -- Cosmetics --
            gr.SetLineColorAlpha(2, 1.);
            gr.SetLineWidth(2)
            gr.SetLineStyle(7)
            gr.SetMarkerColor(2)
            gr.SetMarkerStyle(43)
            grMElist.append(gr)

        ## Get the ME+PDF xsec ratio variations ----------------
        print ("\nDoing ME+PDF xsec ratios with PDF set "+pdfname+"!")
        for i, alphas in enumerate(alphasvalsMEPDF):
            print ("alpha-s = "+str(round(alphas,3)))
            ## -- First get array for the ratio values --
            varArray = array('d')
            for j in range(int(numBins)):
                SFtemp = nonpertSFs[j]
                ratioTemp  = (((dataInMEPDFnum[("'aS=")+str(round(alphas,3))+("'")]).values)[j])
                ratioTemp /= (((dataInMEPDFdenom[("'aS=")+str(round(alphas,3))+("'")]).values)[j])
                ratioTemp *= SFtemp
                varArray.append(ratioTemp)
            varArrayMEPDFlist.append(varArray)
            ## -- Now create the TGraph using this array --
            if (doErrors):
                gr = ROOT.TGraphAsymmErrors(int(numBins), binCenMEnum, varArray, xErrLow, xErrUp, yErrLow, yErrUp)
            else:
                gr = ROOT.TGraphAsymmErrors(int(numBins), binCenMEnum, varArray)
            ## -- Cosmetics --
            if (i == 0):
                gr.SetMarkerColor(2)
                gr.SetLineColorAlpha(2, 1.);
            elif (i == numVarMEPDF-1):
                gr.SetMarkerColor(8)
                gr.SetLineColorAlpha(8, 1.);
            else:
                gr.SetMarkerColor(4)
                gr.SetLineColorAlpha(4, 1.);
            gr.SetLineWidth(2)
            gr.SetLineStyle(1)
            gr.SetMarkerStyle(20)
            gr.SetMarkerSize(0.7)
            ## -- Legend --
            if (i == 0):
                leg1.AddEntry(gr, "NLO QCD: ME+PDF("+pdfname+"), #alpha_{s }= "+str(round(alphas,3)), "lp")
            if ((round(alphas,3)) == 0.118):
                leg1.AddEntry(gr, "NLO QCD: ME+PDF("+pdfname+"), #alpha_{s }= "+str(round(alphas,3)), "lp")
            if (i == numVarMEPDF-1):
                leg1.AddEntry(gr, "NLO QCD: ME+PDF("+pdfname+"), #alpha_{s }= "+str(round(alphas,3)), "lp")
            grMEPDFlist.append(gr)

        ## Now plot --------------------------------------------
        ## Only plotting the lowest, central and highest ME+PDF variations for now
        for i, alphas in enumerate(alphasvalsMEPDF):
            if (i == 0):
               grMEPDFlist[i].Draw('PEL same')
            if ((round(alphas,3)) == 0.118):
               grMEPDFlist[i].Draw('PEL same')
            if (i == numVarMEPDF-1):
               grMEPDFlist[i].Draw('PEL same')
        ## And draw legend
        leg1.Draw("same")

        ## TLatex stuff ----------------------------------------
        cmsLogo = ROOT.TLatex()
        cmsLogo.SetNDC()
        cmsLogo.SetTextSize(0.054)
        cmsLogo.SetLineWidth(2)
        cmsLogo.SetTextFont(61)
        cmsLogo.SetTextColor(ROOT.kBlack)
        cmsLogo.SetTextAlign(11)
        cmsLogo.SetName("cmsLogo")
        cmsLogo.DrawLatex(0.545,0.18,"CMS")
        del cmsLogo
        cmsPrelim = ROOT.TLatex()
        cmsPrelim.SetNDC()
        cmsPrelim.SetTextSize(0.038)
        cmsPrelim.SetLineWidth(1)
        cmsPrelim.SetTextFont(52)
        cmsPrelim.SetTextColor(ROOT.kBlack)
        cmsPrelim.SetTextAlign(11)
        cmsPrelim.SetName("cmsPrelim")
        cmsPrelim.DrawLatex(0.645,0.18,"Work in Progress")
        del cmsPrelim
        latexWJet = ROOT.TLatex()
        latexWJet.SetNDC()
        latexWJet.SetTextSize(0.044)
        latexWJet.SetLineWidth(2)
        latexWJet.SetTextFont(42)
        latexWJet.SetTextColor(ROOT.kBlack)
        latexWJet.SetTextAlign(11)
        latexWJet.SetName("latexWJet")
        if (MEgen == "Openloops"):
            MEgentitle = "OpenLoops+Sherpa"
            if (numerator == "W2J"):
                if (tablename[1] == 'd31-x01-y01.merged' or tablename[1] == 'd81-x01-y01.merged'):
                    wtitle = "R_{21_{excl.}} = #frac{#sigma_{W(#rightarrow#mu#nu) + 2j + X}}{#sigma_{W(#rightarrow#mu#nu) + 1j}}"
                else:
                    wtitle = "R_{21} = #frac{#sigma_{W(#rightarrow#mu#nu) + 2j + X}}{#sigma_{W(#rightarrow#mu#nu) + 1j + X}}"
        if (tablename[1] == 'd31-x01-y01.merged' or tablename[1] == 'd81-x01-y01.merged'):
            latexWJet.DrawLatex(0.526,0.08, wtitle)
        else:
            latexWJet.DrawLatex(0.56,0.08, wtitle)
        if (doNP):
            MEgentitle = "NP Corr. Applied"
            latexWJet.SetTextFont(52)
            latexWJet.SetTextSize(0.025)
            latexWJet.DrawLatex(0.545, 0.695, MEgentitle)
        del latexWJet

        ## ---------------------------------------------------
        ## ---------------------- PAD 2 ----------------------
        ## ---------------------------------------------------
        pad2.cd()

        htemp1 = ROOT.TH1D("htemp1", "htemp1", 100, xmin, xmax)
        htemp1.SetStats(0)
        htemp1.GetXaxis().SetTitle(xtitle)
        htemp1.GetXaxis().SetTitleOffset(1.1)
        htemp1.GetXaxis().SetTitleSize(0.09)
        htemp1.GetXaxis().SetLabelSize(0.09)
        htemp1.GetYaxis().SetTitle("Theory/Data      ")
        htemp1.GetYaxis().SetTitleOffset(0.45)
        htemp1.GetYaxis().SetTitleSize(0.09)
        htemp1.GetYaxis().SetLabelSize(0.06)
        htemp1.GetYaxis().SetRangeUser(0.01, 2.15)
        htemp1.SetTitle("")
        htemp1.Draw()

        line1 = ROOT.TLine(xmin, 1., xmax, 1.);
        line1.SetLineColor(ROOT.kBlack);
        line1.SetLineWidth(1);
        line1.Draw()

        if (doData):
            ## Get central distributions
            centralMEArray = array('d')
            centralMEPDFArray = array('d')
            for i in range(int(numBins)):
                SFtemp = nonpertSFs[i]
                ratioMEtemp  = (((dataInMEnum[("'aS=0.118'")]).values)[i])
                ratioMEtemp /= (((dataInMEdenom[("'aS=0.118'")]).values)[i])
                ratioMEPDFtemp  = (((dataInMEPDFnum[("'aS=0.118'")]).values)[i])
                ratioMEPDFtemp /= (((dataInMEPDFdenom[("'aS=0.118'")]).values)[i])
                centralMEArray.append(ratioMEtemp * SFtemp)
                centralMEPDFArray.append(ratioMEPDFtemp * SFtemp)

            #signal MC used in unfolding
            arrayMCToData1  = array('d') 
            yErrLowMCRatio1 = array('d')
            yErrUpMCRatio1  = array('d')
            #central ME+PDF variation
            arrayMCToData2  = array('d') 
            yErrLowMCRatio2 = array('d')
            yErrUpMCRatio2  = array('d')
            #lowest ME+PDF variation
            arrayMCToData3  = array('d') 
            yErrLowMCRatio3 = array('d')
            yErrUpMCRatio3  = array('d')
            #highest ME+PDF variation
            arrayMCToData4  = array('d') 
            yErrLowMCRatio4 = array('d')
            yErrUpMCRatio4  = array('d')

            for i in range(numBins):
                binContentUnfTemp = ( hUnfRatio.GetBinContent(i+binDataOffset+1) )
                yErrUnfTemp = ( hUnfRatio.GetBinError(i+binDataOffset+1) )

                arrayMCToData1.append((hSignalMCRatio.GetBinContent(i+binDataOffset+1))/binContentUnfTemp)
                arrayMCToData2.append(centralMEPDFArray[i]/binContentUnfTemp)
                arrayMCToData3.append(varArrayMEPDFlist[0][i]/binContentUnfTemp)
                arrayMCToData4.append(varArrayMEPDFlist[numVarMEPDF-1][i]/binContentUnfTemp)

                if (doErrors):
                    yErrLowMCRatio1.append( arrayMCToData1[i]*math.sqrt((yErrUnfTemp/binContentUnfTemp)**2 + ((hSignalMCRatio.GetBinError(i+binDataOffset+1))/(hSignalMCRatio.GetBinContent(i+binDataOffset+1)))**2) )
                    yErrUpMCRatio1.append( arrayMCToData1[i]*math.sqrt((yErrUnfTemp/binContentUnfTemp)**2 + ((hSignalMCRatio.GetBinError(i+binDataOffset+1))/(hSignalMCRatio.GetBinContent(i+binDataOffset+1)))**2) )
                    yErrLowMCRatio2.append(arrayMCToData2[i]*math.sqrt((yErrUnfTemp/binContentUnfTemp)**2 + (yErrLow[i]/centralMEPDFArray[i])**2))
                    yErrUpMCRatio2.append(arrayMCToData2[i]*math.sqrt((yErrUnfTemp/binContentUnfTemp)**2 + (yErrUp[i]/centralMEPDFArray[i])**2))
                    yErrLowMCRatio3.append(arrayMCToData3[i]*math.sqrt((yErrUnfTemp/binContentUnfTemp)**2 + (yErrLow[i]/varArrayMEPDFlist[0][i])**2))
                    yErrUpMCRatio3.append(arrayMCToData3[i]*math.sqrt((yErrUnfTemp/binContentUnfTemp)**2 + (yErrUp[i]/varArrayMEPDFlist[0][i])**2))
                    yErrLowMCRatio4.append(arrayMCToData4[i]*math.sqrt((yErrUnfTemp/binContentUnfTemp)**2 + (yErrLow[i]/varArrayMEPDFlist[numVarMEPDF-1][i])**2))
                    yErrUpMCRatio4.append(arrayMCToData4[i]*math.sqrt((yErrUnfTemp/binContentUnfTemp)**2 + (yErrUp[i]/varArrayMEPDFlist[numVarMEPDF-1][i])**2))

            if (doErrors):
                grMCtoData1 = ROOT.TGraphAsymmErrors(numBins, binCenMEnum, arrayMCToData1, xErrLow, xErrUp, yErrLowMCRatio1, yErrUpMCRatio1)
                grMCtoData2 = ROOT.TGraphAsymmErrors(numBins, binCenMEnum, arrayMCToData2, xErrLow, xErrUp, yErrLowMCRatio2, yErrUpMCRatio2)
                grMCtoData3 = ROOT.TGraphAsymmErrors(numBins, binCenMEnum, arrayMCToData3, xErrLow, xErrUp, yErrLowMCRatio3, yErrUpMCRatio3)
                grMCtoData4 = ROOT.TGraphAsymmErrors(numBins, binCenMEnum, arrayMCToData4, xErrLow, xErrUp, yErrLowMCRatio4, yErrUpMCRatio4)
            else:
                grMCtoData1 = ROOT.TGraphAsymmErrors(numBins, binCenMEnum, arrayMCToData1)
                grMCtoData2 = ROOT.TGraphAsymmErrors(numBins, binCenMEnum, arrayMCToData2)
                grMCtoData3 = ROOT.TGraphAsymmErrors(numBins, binCenMEnum, arrayMCToData3)
                grMCtoData4 = ROOT.TGraphAsymmErrors(numBins, binCenMEnum, arrayMCToData4)

            grMCtoData1.SetLineColor(ROOT.kOrange)
            grMCtoData1.SetLineWidth(2)
            grMCtoData1.SetLineStyle(1)
            grMCtoData1.SetMarkerColor(ROOT.kOrange)
            grMCtoData1.SetMarkerStyle(20)
            grMCtoData1.SetMarkerSize(0.7)

            grMCtoData2.SetLineColorAlpha(4, 1.)
            grMCtoData2.SetLineWidth(2)
            grMCtoData2.SetLineStyle(1)
            grMCtoData2.SetMarkerColor(4)
            grMCtoData2.SetMarkerStyle(20)
            grMCtoData2.SetMarkerSize(0.7)

            grMCtoData3.SetLineColorAlpha(2, 1.)
            grMCtoData3.SetLineWidth(2)
            grMCtoData3.SetLineStyle(1)
            grMCtoData3.SetMarkerColor(2)
            grMCtoData3.SetMarkerStyle(20)
            grMCtoData3.SetMarkerSize(0.7)

            grMCtoData4.SetLineColorAlpha(8, 1.)
            grMCtoData4.SetLineWidth(2)
            grMCtoData4.SetLineStyle(1)
            grMCtoData4.SetMarkerColor(8)
            grMCtoData4.SetMarkerStyle(20)
            grMCtoData4.SetMarkerSize(0.7)

            grMCtoData2.Draw('PE same')
            grMCtoData3.Draw('PE same')
            grMCtoData4.Draw('PE same')
            grMCtoData1.Draw('PE same') #draw this one on top

        ##################################################################################

        print("")
        c1.Update()
        c1.Print(basedir+outDir+"aSVarRatio-"+numerator+"-"+denominator+"-"+tablename[0]+"-"+tablename[1]+"-"+pdfname+isNP+".pdf")
        del c1
        del htemp, htemp1

print ('\nFinished!\n')        