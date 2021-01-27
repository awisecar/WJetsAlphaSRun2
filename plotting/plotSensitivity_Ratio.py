#! /usr/bin/env python3
import os
import sys
import numpy as np
import pandas as pd
import math
from array import array
import ROOT
##################################################
### R21 (list num first, then denom)
# numerator = 'W2J'
# denominator = 'W1J'
# tablenames = [ ['d57-x01-y01.merged','d56-x01-y01.merged'] ]
# variables = [ ["LepPtPlusLeadingJetAK8Pt_Zinc2jet_TUnfold", "LepPtPlusLeadingJetAK8Pt_Zinc1jet_TUnfold"] ]
### R32 (list num first, then denom)
# numerator = 'W3J'
# denominator = 'W2J'
# tablenames = [ ['d58-x01-y01.merged','d57-x01-y01.merged'], ['d64-x01-y01.merged','d63-x01-y01.merged'] ]
# variables = [ ["LepPtPlusLeadingJetAK8Pt_Zinc3jet_TUnfold", "LepPtPlusLeadingJetAK8Pt_Zinc2jet_TUnfold"], ["LepPtPlusHT2over2AK8_Zinc3jet_TUnfold", "LepPtPlusHT2over2AK8_Zinc2jet_TUnfold"] ]
### R31 (list num first, then denom)
numerator = 'W3J'
denominator = 'W1J'
tablenames = [ ['d58-x01-y01.merged','d56-x01-y01.merged'] ]
variables = [ ["LepPtPlusLeadingJetAK8Pt_Zinc3jet_TUnfold", "LepPtPlusLeadingJetAK8Pt_Zinc1jet_TUnfold"] ]
## --
#pdfnames = ['CT10nlo', 'CT14nlo', 'NNPDF23_nlo', 'NNPDF30_nlo', 'NNPDF31_nnlo']
pdfnames = ['CT14nlo']
## --
doSyst = True
# doSyst = False
## --
#doCutoff = True
doCutoff = False
##################################################
MEgen = "Openloops"
order = "NLO"
basedir = "./"+MEgen+"/"+order+"/"
outDir = ("plotsFastNLO/")
os.system(("mkdir -p ")+basedir+outDir)

ROOT.gStyle.SetLineStyleString(11,"10 10")
ROOT.gStyle.SetLegendTextSize(0.022)

for iTab, tablename in enumerate(tablenames):
    print ("\n----------------> Doing distribution: "+str(tablename))
    for pdfname in pdfnames:
        print ("\n--------> Doing PDF series: "+str(pdfname))

        #########################################
        ## 1) Grab data
        
        csvInfileMEnum = "aSVarME-"+pdfname+"-"+numerator+"-"+tablename[0]+".csv"
        csvInfileMEdenom = "aSVarME-"+pdfname+"-"+denominator+"-"+tablename[1]+".csv"
        csvInfileMEPDFnum = "aSVarMEPDF-"+pdfname+"-"+numerator+"-"+tablename[0]+".csv"
        csvInfileMEPDFdenom = "aSVarMEPDF-"+pdfname+"-"+denominator+"-"+tablename[1]+".csv"

        if (doSyst):
            variableNum   = variables[iTab][0]
            variableDenom = variables[iTab][1]
            fileNameRatio = ("UnfoldedFilesRatio_Run2/SMu_RATIO_"+variableNum+"_TO_"+variableDenom+"_JetPtMin_30_JetEtaMax_24_MGPYTHIA6_.root")
#            fileNameRatio = ("UnfoldedFilesRatio_2016/SMu_RATIO_"+variableNum+"_TO_"+variableDenom+"_JetPtMin_30_JetEtaMax_24_MGPYTHIA6_.root")
            print ("\nOpening file: "+fileNameRatio)
            fRatio = ROOT.TFile.Open(fileNameRatio, "READ")

        ## Grab the alpha-s value for each dataseries to use as label
        ## Only need to do this for numerator
        # just ME var
        alphasNamesME = pd.read_csv(basedir+csvInfileMEnum, nrows=1) #grabbing first row of diagonistic information
        alphasvalsME = alphasNamesME.values.tolist()[0][3:]
        numVarME = int(alphasNamesME.values.tolist()[0][2]) #total number of alpha-s variations for ME
        print ("\nNumber of ME variations: "+str(int(numVarME)))
        # print ("Doing ME variations: "+str(alphasvalsME))
        # ME and PDF var
        alphasNamesMEPDF = pd.read_csv(basedir+csvInfileMEPDFnum, nrows=1)
        alphasvalsMEPDF = alphasNamesMEPDF.values.tolist()[0][3:]
        numVarMEPDF = int(alphasNamesMEPDF.values.tolist()[0][2])  #total number of alpha-s variations for ME+PDF
        print ("Number of ME+PDF variations: "+str(int(numVarMEPDF)))
        # print ("Doing ME+PDF variations: "+str(alphasvalsMEPDF))
        #num of bins should be the same for two different files
        numBins = int(alphasNamesME.values.tolist()[0][0])  #number of bins in the distribution
        print ("Number of bins in histogram: "+str(int(numBins)))
        
        ## Grab the FNLO distributions
        dataInMEnum = pd.read_csv(basedir+csvInfileMEnum, skiprows=[1]) #skip first row, but with keeping headers
        dataInMEdenom = pd.read_csv(basedir+csvInfileMEdenom, skiprows=[1])
        dataInMEPDFnum = pd.read_csv(basedir+csvInfileMEPDFnum, skiprows=[1])
        dataInMEPDFdenom = pd.read_csv(basedir+csvInfileMEPDFdenom, skiprows=[1])
        
        ## Check binnings between num and denom are the same
        binCenMEnum = array('d')
        binCenMEdenom = array('d')
        for i in range(int(numBins)):
            binCenMEnum.append((dataInMEnum["'BINCENTER'"].values)[i])
            binCenMEdenom.append(dataInMEdenom["'BINCENTER'"].values[i])
        if (binCenMEnum == binCenMEdenom):
            print ("\nBinning of two distributions is equal: \n"+str(binCenMEnum))
        else:
            print ("\nBinning of two distributions is not equal! Exiting...")
            sys.exit()

        ## Get x-titles, binDataOffset depending on distribution
        boundLow = 90.
        xtitle = 'pT [GeV]'
        binDataOffset = 1
        if ((numerator == 'W2J') and (denominator == 'W1J')):
            if (tablename[0] == 'd07-x01-y01.merged' and tablename[1] == 'd06-x01-y01.merged'):
                xtitle = 'Muon pT + Leading Jet pT [GeV]'
                binDataOffset = 1
            if (tablename[0] == 'd07-x01-y01.merged' and tablename[1] == 'd31-x01-y01.merged'):
                xtitle = 'Muon pT + Leading Jet pT [GeV]'
                binDataOffset = 1
            if (tablename[0] == 'd57-x01-y01.merged' and tablename[1] == 'd56-x01-y01.merged'):
                xtitle = 'Muon pT + Leading AK8 Jet pT [GeV]'
                binDataOffset = 1
            if (tablename[0] == 'd57-x01-y01.merged' and tablename[1] == 'd81-x01-y01.merged'):
                xtitle = 'Muon pT + Leading Jet pT [GeV]'
                binDataOffset = 1
        elif ((numerator == 'W3J') and (denominator == 'W2J')):
            if (tablename[0] == 'd58-x01-y01.merged' and tablename[1] == 'd57-x01-y01.merged'):
                xtitle = 'Muon pT + Leading AK8 Jet pT [GeV]'
                binDataOffset = 1
            if (tablename[0] == 'd64-x01-y01.merged' and tablename[1] == 'd63-x01-y01.merged'):
                xtitle = 'Muon pT + H_{T,2}/2 [GeV]'
                binDataOffset = 1
        elif ((numerator == 'W3J') and (denominator == 'W1J')):
            if (tablename[0] == 'd58-x01-y01.merged' and tablename[1] == 'd56-x01-y01.merged'):
                xtitle = 'Muon pT + Leading AK8 Jet pT [GeV]'
                binDataOffset = 1

        ##################################################

        varArrayMEPDFlist = []
        varArrayMElist = []

        # print ("\n\n-----------------------> Doing ME ratios with PDF set "+pdfname+"!")
        for i, alphas in enumerate(alphasvalsME):
            varArray = array('d')
            for j in range(int(numBins)):
                ratioTemp = (((dataInMEnum[("'aS=")+str(round(alphas,3))+("'")]).values)[j])/(((dataInMEdenom[("'aS=")+str(round(alphas,3))+("'")]).values)[j])
                # have to make sure that this value is exists for both num and denom
                varArray.append(ratioTemp)
            varArrayMElist.append(varArray)
            # print ("~~~ Doing ME var for alpha-s="+str(round(alphas,3))+"!")
            # print ("Values for entry "+str(i)+": " +str(varArray))

        # print ("\n\n-----------------------> Doing ME+PDF ratios with PDF set "+pdfname+"!")
        for i, alphas in enumerate(alphasvalsMEPDF):
            varArray = array('d')
            for j in range(int(numBins)):
                ratioTemp = (((dataInMEPDFnum[("'aS=")+str(round(alphas,3))+("'")]).values)[j])/(((dataInMEPDFdenom[("'aS=")+str(round(alphas,3))+("'")]).values)[j])
                # have to make sure that this value exists for both num and denom
                varArray.append(ratioTemp)
            varArrayMEPDFlist.append(varArray)
            # print ("~~~ Doing ME+PDF var for alpha-s="+str(round(alphas,3))+"!")
            # print ("Values for entry "+str(i)+": " +str(varArray))

        ## Get central distributions
        centralMEPDFArray = array('d')
        centralMEArray = array('d')
        for i in range(int(numBins)):
            ratioMEPDFtemp = (((dataInMEPDFnum[("'aS=0.118'")]).values)[i])/(((dataInMEPDFdenom[("'aS=0.118'")]).values)[i])
            ratioMEtemp = (((dataInMEnum[("'aS=0.118'")]).values)[i])/(((dataInMEdenom[("'aS=0.118'")]).values)[i])
            centralMEPDFArray.append(ratioMEPDFtemp)
            centralMEArray.append(ratioMEtemp)

        ##################################################
        ## 3) Need to plot the ratio of the ratios (yes, really) for the variations
        c2 = ROOT.TCanvas('canRatios2_', 'canRatios2_', 500, 500)
        c2.Update()
        c2.Draw()

        xmin2 = binCenMEnum[0]-3.
        xmax2 = binCenMEnum[int(numBins)-1]+3.
        ymin2 = 0.851
        ymax2 = 1.149

        htemp2 = ROOT.TH1D('aSRatios2_', "Ratio to Central XSec Ratio (aS = 0.118)", 100, xmin2, xmax2)
        htemp2.SetStats(0)
        htemp2.GetXaxis().SetTitle(xtitle)
        htemp2.GetXaxis().SetTitleOffset(1.2)
        # htemp2.GetYaxis().SetTitle('Ratio to Central #alpha_{s} Prediction')
        # htemp2.GetYaxis().SetTitle('Fractional Sensitivity to #alpha_{s} Variations')
        htemp2.GetYaxis().SetTitle('#alpha_{s} Sensitivity')
        htemp2.GetYaxis().SetTitleOffset(1.3)
        htemp2.GetYaxis().SetRangeUser(ymin2, ymax2)
        htemp2.SetTitle("")
        htemp2.Draw()

        if (doSyst):
            legLowY = 0.725
        else:
            legLowY = 0.775
        leg2 = ROOT.TLegend(0.34,legLowY,0.9,0.9)

        procLatex = ROOT.TLatex()
        procLatex.SetNDC()
        procLatex.SetTextSize(0.025)
        procLatex.SetLineWidth(2)
        procLatex.SetTextFont(42)
        procLatex.SetTextColor(ROOT.kBlack)
        procLatex.SetTextAlign(11)
        procLatex.SetName("procLatex")
        # procLatex.DrawLatex(0.55, legLowY-0.04, MEgen+"+Sherpa, NLO QCD")
        procLatex.DrawLatex(0.57, 0.24, MEgen+"+Sherpa, NLO QCD")
        wtitle = ""
        if ((numerator == 'W2J') and (denominator == 'W1J')):
            if (tablename[1] == 'd31-x01-y01.merged' or tablename[1] == 'd81-x01-y01.merged'):
                wtitle = "R_{21_{excl.}} = #frac{W(#rightarrow#mu#nu) + 2j + X}{W(#rightarrow#mu#nu) + 1j}"
            else:
                wtitle = "R_{21} = #frac{W(#rightarrow#mu#nu) + 2j + X}{W(#rightarrow#mu#nu) + 1j + X}"
        elif ((numerator == 'W3J') and (denominator == 'W2J')):
            wtitle = "R_{32} = #frac{W(#rightarrow#mu#nu) + 3j + X}{W(#rightarrow#mu#nu) + 2j + X}"
        elif ((numerator == 'W3J') and (denominator == 'W1J')):
            wtitle = "R_{31} = #frac{W(#rightarrow#mu#nu) + 3j + X}{W(#rightarrow#mu#nu) + 1j + X}"
        if (tablename[1] == 'd31-x01-y01.merged' or tablename[1] == 'd81-x01-y01.merged'):
            procLatex.DrawLatex(0.58, legLowY-0.1, wtitle)
        else:
            # procLatex.DrawLatex(0.58, legLowY-0.1, wtitle)
            procLatex.DrawLatex(0.60, 0.18, wtitle)

        line2 = ROOT.TLine(binCenMEnum[0], 1., binCenMEnum[int(numBins)-1], 1.);
        line2.SetLineColor(ROOT.kBlack);
        line2.SetLineWidth(1);
        line2.Draw()

        ## Keeping the graphs in a list allows us to draw multiple on canvas
        grMEPDFlist2 = []
        grMElist2 = []

        ### Plot the ME variations
        print ("\n\n-----------------------> Doing ME ratio of ratios!")
        for i, alphas in enumerate(alphasvalsME):
            if ((round(alphas,3)) == 0.118): #don't want to redundantly plot the central variation
                continue
            perdiffarray = array('d')
            for j in range(int(numBins)):
                perdiffarray.append(varArrayMElist[i][j]/centralMEArray[j])
            print ("~~~~~ Drawing ratio of ratio where alpha-s = "+str(round(alphas,3))+"!")
            # print ("Values for entry "+str(i)+": " +str(perdiffarray))
            ## Now draw the graph
            gr = ROOT.TGraph(int(numBins), binCenMEnum, perdiffarray)
            if (i==0 or i==(numVarME-1)):
                if (i==0):
                    gr.SetLineColorAlpha(3, 1.)
                    gr.SetMarkerColorAlpha(3, 1.)
                else:
                    gr.SetLineColorAlpha(6, 1.)
                    gr.SetMarkerColorAlpha(6, 1.)
                gr.SetLineWidth(2)
                gr.SetLineStyle(1)
            else:
                gr.SetLineColorAlpha(0, 0.5); #make these go away for now
                gr.SetMarkerColorAlpha(0, 1.)
                gr.SetLineWidth(1)
                gr.SetLineStyle(11)
            # TURN THIS BACK ON IF YOU WANT ME-ONLY ALPHA-S VARIATIONS
            # if i==0:
            #     leg2.AddEntry(gr, "ME Variation: "+pdfname+", #alpha_{s} = "+str(round(alphas,3)), "l")
            # elif i==(int(numVarME-1)):
            #     leg2.AddEntry(gr, "ME Variation: "+pdfname+", #alpha_{s} = "+str(round(alphas,3)), "l")
            gr.SetMarkerSize(0.5)
            gr.SetMarkerStyle(20)
            grMElist2.append(gr)

        # TURN THIS BACK ON IF YOU WANT ME-ONLY ALPHA-S VARIATIONS
        # for gr in grMElist2:
        #     # gr.Draw('CP same')
        #     gr.Draw('C same')

        ### Plot the ME+PDF variations
        print ("\n\n-----------------------> Doing ME+PDF ratio of ratios with PDF set "+pdfname+"!")
        for i, alphas in enumerate(alphasvalsMEPDF):
            if ((round(alphas,3)) == 0.118): #don't want to redundantly plot the central variation
                continue
            perdiffarray = array('d')
            for j in range(int(numBins)):
                perdiffarray.append(varArrayMEPDFlist[i][j]/centralMEPDFArray[j])
            print ("~~~~~ Drawing ratio of ratio where alpha-s = "+str(round(alphas,3))+"!")
            # print ("Values for entry "+str(i)+": " +str(perdiffarray))
            ## Now draw the graph
            gr = ROOT.TGraph(int(numBins), binCenMEnum, perdiffarray)
            if (i==0 or i==(numVarMEPDF-1)):
                if (i==0):
                    gr.SetLineColorAlpha(2, 1.)
                    gr.SetMarkerColorAlpha(2, 1.)
                else:
                    gr.SetLineColorAlpha(4, 1.)
                    gr.SetMarkerColorAlpha(4, 1.)
                gr.SetLineWidth(3)
                gr.SetLineStyle(7)
            else:
                gr.SetLineColorAlpha(1, 0.5)
                gr.SetMarkerColorAlpha(1, 0)
                gr.SetLineWidth(1)
                gr.SetLineStyle(11)
            if i==0:
                leg2.AddEntry(gr, "ME+PDF Variation: "+pdfname+", #alpha_{s} = "+str(round(alphas,3)), "l")
            elif i==(int(numVarMEPDF-1)):
                leg2.AddEntry(gr, "ME+PDF Variation: "+pdfname+", #alpha_{s} = "+str(round(alphas,3)), "l")
            gr.SetMarkerSize(0.5)
            gr.SetMarkerStyle(20)
            grMEPDFlist2.append(gr)

        for gr in grMEPDFlist2:
            # gr.Draw('CP same')
            gr.Draw('C same')












        if (doSyst):

            # grab distributions to get stat. error and total syst. error
            hUnfRatio = fRatio.Get("UnfXSecRatio_Central")
            hTotCovMatrix = fRatio.Get("CovTotSyst")

            # make histograms for showing stat. and stat.+syst. uncertainties
            hStatError = hUnfRatio.Clone()
            hTotExpError = hUnfRatio.Clone()

            print("\nnumBins = "+str(numBins))
            for i in range(0, numBins):
                print("bin #"+str(i+1))

                # --- stat. uncertainty only ---
                # need to put the fractional uncertainty for this plot
                fractionalStatErrTemp = hUnfRatio.GetBinError(i+1+binDataOffset)/hUnfRatio.GetBinContent(i+1+binDataOffset)
                # set this fractional error value as the histogram error and fix at the points at 1
                hStatError.SetBinError(i+1+binDataOffset, fractionalStatErrTemp)
                hStatError.SetBinContent(i+1+binDataOffset, 1.)
                print("      percent error (stat.): "+str(fractionalStatErrTemp*100.)+" %")

                # --- stat.+syst. uncertainty (added in quadrature) ---
                statErrSqrd = pow(hUnfRatio.GetBinError(i+1+binDataOffset), 2.)
                systErrSqrd = hTotCovMatrix.GetBinContent(i+1+binDataOffset, i+1+binDataOffset) # getting error^2 from diagonal entries of covariance matrix
                errTemp = math.sqrt( statErrSqrd + systErrSqrd )
                # need to put the fractional uncertainty for this plot
                fractionalTotalErrTemp = errTemp/hUnfRatio.GetBinContent(i+1+binDataOffset)
                # set this fractional error as the errors and fix at the points at 1
                hTotExpError.SetBinError(i+1+binDataOffset, fractionalTotalErrTemp)
                hTotExpError.SetBinContent(i+1+binDataOffset, 1.)
                print("      percent error (stat.+syst.): "+str(fractionalTotalErrTemp*100.)+" %")

            # cosmetics
            # stat. only
            hStatError.SetLineColor(ROOT.kGreen)
            hStatError.SetLineWidth(3)
            hStatError.SetLineStyle(1)
            hStatError.SetMarkerColor(ROOT.kGreen)
            hStatError.SetMarkerSize(0.)
            # stat.+syst.
            hTotExpError.SetLineColor(ROOT.kBlack)
            hTotExpError.SetLineWidth(3)
            hTotExpError.SetLineStyle(1)
            hTotExpError.SetMarkerColor(ROOT.kBlack)
            hTotExpError.SetMarkerSize(0.)

            # draw
            hTotExpError.Draw('PE same') # draw the largest error bars first
            hStatError.Draw('PE same') # then draw the smaller error bars on top

            # legend entries
            leg2.AddEntry(hStatError, "Experimental Uncertainty (Stat.)", "lpe")
            leg2.AddEntry(hTotExpError, "Experimental Uncertainty (Stat.+Syst.)", "lpe")
            

















        leg2.Draw("same")

        ##########################################
        ## Find an average variation over a range
        if (doCutoff):
            if (boundLow < 30.):
                boundLow = 100.
            boundUp = binCenMEnum[numBins-1]
            lineBoundLow = ROOT.TLine(boundLow, ymin2, boundLow, ymax2)
            lineBoundLow.SetLineColorAlpha(ROOT.kBlack, 0.5)
            lineBoundLow.SetLineWidth(2)
            lineBoundLow.SetLineStyle(9)
            lineBoundLow.Draw()
            lineBoundUp = ROOT.TLine(boundUp, ymin2, boundUp, ymax2)
            lineBoundUp.SetLineColorAlpha(ROOT.kBlack, 0.5)
            lineBoundUp.SetLineWidth(2)
            lineBoundUp.SetLineStyle(9)
            lineBoundUp.Draw()
            arrBoundLow = ROOT.TArrow(boundLow, 0.8, boundLow+50., 0.8, 0.02, ">")
            arrBoundLow.SetLineWidth(2)
            arrBoundLow.SetLineColorAlpha(ROOT.kBlack, 0.5)
            arrBoundLow.Draw()
            arrBoundUp = ROOT.TArrow(boundUp-50., 0.8, boundUp, 0.8, 0.02, "<")
            arrBoundUp.SetLineWidth(2)
            arrBoundUp.SetLineColorAlpha(ROOT.kBlack, 0.5)
            arrBoundUp.Draw()

            upList = []
            lowList = []
            ## Find average of all the MC ratio values for highest and lowest ME+PDF variations that are within the x-bounds
            for j in range(numBins):
                if ( (binCenMEnum[j] >= boundLow) and (binCenMEnum[j] <= boundUp) ):
                    upList.append( varArrayMEPDFlist[numVarMEPDF-1][j]/centralMEPDFArray[j] )
                    lowList.append( varArrayMEPDFlist[0][j]/centralMEPDFArray[j] )
            avgUp = sum(upList)/float(len(upList))
            avgLow = sum(lowList)/float(len(lowList))
            avgUpPerc = (avgUp-1.)*100.
            avgLowPerc = (avgLow-1.)*100.
            totalBandPerc = abs(avgUpPerc)+abs(avgLowPerc)

            fitDetails = ROOT.TLatex()
            fitDetails.SetNDC()
            fitDetails.SetTextSize(0.025)
            fitDetails.SetLineWidth(1)
            fitDetails.SetTextFont(52)
            fitDetails.SetTextColor(ROOT.kBlack)
            fitDetails.SetTextAlign(11)
            fitDetails.SetName("latexWJet")
            fitDetails.DrawLatex(0.33,0.24, "Fit Range: "+str(boundLow)+" GeV to "+str(boundUp)+" GeV")
            fitDetails.SetTextSize(0.025)
            fitDetails.SetLineWidth(2)
            fitDetails.SetTextFont(42)
            fitDetails.SetTextColor(ROOT.kBlack)
            fitDetails.SetTextAlign(11)
            fitDetails.DrawLatex(0.3,0.20, "#alpha_{s} = "+str(round(alphasvalsMEPDF[numVarMEPDF-1],3))+" ME+PDF ratio average: "+str( round(avgUpPerc,2) )+"%")
            fitDetails.DrawLatex(0.3,0.17, "#alpha_{s} = "+str(round(alphasvalsMEPDF[0],3))+" ME+PDF ratio average: "+str( round(avgLowPerc,2) )+"%")
            fitDetails.DrawLatex(0.33,0.14, "Total width of variation band: "+str( round(totalBandPerc,2) )+"%")
            # fitDetails.DrawLatex(0.3,0.18, "#alpha_{s} = "+str(round(alphasvalsMEPDF[numVarMEPDF-1],3))+" ME+PDF ratio average: "+str( round(avgUp,3) )+"%")
            # fitDetails.DrawLatex(0.3,0.15, "#alpha_{s} = "+str(round(alphasvalsMEPDF[0],3))+" ME+PDF ratio average: "+str( round(avgLow,3) )+"%")

            lineUpAvg = ROOT.TLine(boundLow, avgUp, boundUp, avgUp)
            lineUpAvg.SetLineColorAlpha(ROOT.kBlack, 0.5)
            lineUpAvg.SetLineWidth(2)
            # lineUpAvg.SetLineStyle(9)
            lineUpAvg.Draw()
            lineLowAvg = ROOT.TLine(boundLow, avgLow, boundUp, avgLow)
            lineLowAvg.SetLineColorAlpha(ROOT.kBlack, 0.5)
            lineLowAvg.SetLineWidth(2)
            # lineLowAvg.SetLineStyle(9)
            lineLowAvg.Draw()

        isCutoff = ""
        if (doCutoff == True):
            isCutoff = "-cutoff"

        c2.Update()
        c2.Print(basedir+outDir+"SensitivityRatio-"+numerator+"-"+denominator+"-"+tablename[0]+"-"+tablename[1]+"-"+pdfname+isCutoff+".pdf")
        del c2
        del htemp2

print ('\nFinished!\n')
