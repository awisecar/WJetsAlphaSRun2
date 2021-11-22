#! /usr/bin/env python3
import os
import sys
import numpy as np
import pandas as pd
import math
from array import array
import ROOT
cwd = os.getcwd()
#############################################

#year = "2016"
year = "Run2"

#################

unfoldDir = "UnfoldingCheck_"+year+"/"
outputDir = "systFiles_XSec_"+year+"/"
os.system("mkdir -p "+outputDir)

#################

variables = [
             "FirstJetPt_Zinc1jet_TUnfold", "FirstJetAbsRapidity_Zinc1jet_TUnfold", "dPhiLepJet1_Zinc1jet_TUnfold",
             "SecondJetPt_Zinc2jet_TUnfold", "SecondJetAbsRapidity_Zinc2jet_TUnfold", "dPhiLepJet2_Zinc2jet_TUnfold",
             "dPhiJets_Zinc2jet_TUnfold", "dRapidityJets_Zinc2jet_TUnfold", "dRJets_Zinc2jet_TUnfold", "diJetMass_Zinc2jet_TUnfold",
             # ---
             "FirstJetAK8Pt_Zinc1jet_TUnfold", "FirstJetAK8AbsRapidity_Zinc1jet_TUnfold", "dPhiLepJet1AK8_Zinc1jet_TUnfold",
             "SecondJetAK8Pt_Zinc2jet_TUnfold", "SecondJetAK8AbsRapidity_Zinc2jet_TUnfold", "dPhiLepJet2AK8_Zinc2jet_TUnfold",
             "dPhiJetsAK8_Zinc2jet_TUnfold", "dRapidityJetsAK8_Zinc2jet_TUnfold", "dRJetsAK8_Zinc2jet_TUnfold", "diJetAK8Mass_Zinc2jet_TUnfold",
             "dRLepCloseJetCo300dR04_Zinc1jet_TUnfold", "dRLepCloseJetCo500dR04_Zinc1jet_TUnfold",
             # ---
             "LepPtPlusLeadingJetAK8Pt_Zinc1jet_TUnfold", "LepPtPlusLeadingJetAK8Pt_Zinc2jet_TUnfold", "LepPtPlusLeadingJetAK8Pt_Zinc3jet_TUnfold",
             "LepPtPlusLeadingJetAK8Pt_Zexc1jet_TUnfold", "LepPtPlusLeadingJetAK8Pt_Zexc2jet_TUnfold",
             "LepPtPlusHT2over2AK8_Zinc2jet_TUnfold", "LepPtPlusHT2over2AK8_Zinc3jet_TUnfold"
            ]

# variables = ["FirstJetPt_Zinc1jet_TUnfold"]

# Full systematics
names = ["Central", "PUUp", "PUDown", "JESUp", "JESDown", "XSECUp", "XSECDown", "JERUp", "JERDown", "LepSFUp", "LepSFDown", "L1PrefireUp", "L1PrefireDown", "LumiUp", "LumiDown", "Unfolding", "Unfolding"]
namesLegend = ["Pileup Modeling", "Jet Energy Scale", "Background Normalization", "Jet Energy Resolution", "Muon Selection Efficiency", "L1 Prefiring Effect", "Luminosity", "Unfolding Procedure"]

# Central, JES
# names = ["Central", "JESUp", "JESDown"]
# namesLegend = ["Jet Energy Scale"]

### Need to cut off some of the leading bins for the jet pT-centric variables
### These leading bins are passed through the unfolding to allow for migrations up into the following bins
### Strategy here is just to use this number to alter what we see on the plot, i.e. the axis ranges
chopLeadingBins = 0
chopEndingBins = 0

### Set as true if you want shaded bands as the total systematic uncertainty (added in quadrature)
doSystBands = True
#doSystBands = False

### Plots MG5 NLO FxFx and LO MLM gen cross sections
doGenRecoComp = True
#doGenRecoComp = False

###########################################################

ROOT.gStyle.SetHatchesSpacing(0.45)
ROOT.gStyle.SetHatchesLineWidth(1)

numVar = len(variables)
numNames = len(names)

print ("\nBegin!\n")
for iVar, variable in enumerate(variables):

    # chop off underflow and overflow bins kept in the unfolding for migrations
    if (variable == "FirstJetPt_Zinc1jet_TUnfold" or variable == "SecondJetPt_Zinc2jet_TUnfold"):
        chopLeadingBins = 1
        chopEndingBins = 1
    elif (variable == "FirstJetAK8Pt_Zinc1jet_TUnfold" or variable == "SecondJetAK8Pt_Zinc2jet_TUnfold"):
        chopLeadingBins = 1
        chopEndingBins = 1
    elif (variable == "dRJets_Zinc2jet_TUnfold" or variable == "dRJetsAK8_Zinc2jet_TUnfold"):
        chopEndingBins = 1
    elif (variable == "diJetAK8Mass_Zinc2jet_TUnfold" or variable == "diJetMass_Zinc2jet_TUnfold"):
        chopEndingBins = 1
    elif (variable == "dRLepCloseJetCo300dR04_Zinc1jet_TUnfold" or variable == "dRLepCloseJetCo500dR04_Zinc1jet_TUnfold"):
        if (variable == "dRLepCloseJetCo300dR04_Zinc1jet_TUnfold"):
            chopEndingBins = 2
        else:
            chopEndingBins = 1
    elif (variable == "LepPtPlusLeadingJetAK8Pt_Zinc1jet_TUnfold" or variable == "LepPtPlusLeadingJetAK8Pt_Zinc2jet_TUnfold" or variable == "LepPtPlusLeadingJetAK8Pt_Zinc3jet_TUnfold" or variable == "LepPtPlusLeadingJetAK8Pt_Zexc1jet_TUnfold" or variable == "LepPtPlusLeadingJetAK8Pt_Zexc2jet_TUnfold"):
        chopLeadingBins = 3
        chopEndingBins = 1
    elif (variable == "LepPtPlusHT2over2AK8_Zinc2jet_TUnfold" or variable == "LepPtPlusHT2over2AK8_Zinc3jet_TUnfold"):
        chopLeadingBins = 2
        chopEndingBins = 1
    else:
        chopLeadingBins = 0
        chopEndingBins = 0

    print("\n>>>>>>>>>> Doing variable: "+str(variable))
    histos = []
    histos_CentralRatio = []
    histos_PercentUncertainty = []

    ### Grab histo from each systematic variation ---
    for iName, name in enumerate(names):
        fileName = unfoldDir+"SMu_"+variable+"_"+name+".root"
        print ("Opening file: "+fileName)
        file = ROOT.TFile.Open(fileName, "READ")
        print ("-----> Getting UnfData hist with name #"+str(iName)+": "+name)
        hTemp = file.Get("hUnfData_"+name)
        hTemp.SetDirectory(0)
        for iBin in range(1, hTemp.GetNbinsX()+1):
            bincountTemp = hTemp.GetBinContent(iBin)
            if ( (bincountTemp < 0.0) or (math.isnan(bincountTemp)) ):
                print("---> Bin #"+str(iBin)+" count is below zero: "+str(bincountTemp))
                print("---> Setting bin content to 0.0000000000001")
                hTemp.SetBinContent(iBin, 0.0000000000001)
                hTemp.SetBinError(iBin, 0.0)
        histos.append(hTemp)
        if (file.IsOpen()):
            print ("File "+fileName+" is still open, closing...")
            file.Close()

    ## Get the MG5 NLO FxFx and LO MLM files, and the central reconstructed dist. ---
    if (doGenRecoComp):
        ## GEN
        print ("\n-----> Getting MG5 signal samples")
        fileNameGen = "UnfoldedFiles_"+year+"/"+"SMu_unfolded_"+variable+"_TUnfold_JetPtMin_30_JetEtaMax_24_MGPYTHIA6_.root"
        print ("Opening file: "+fileNameGen)
        fileGen = ROOT.TFile.Open(fileNameGen, "READ")
        hGenNLOFXFX = fileGen.Get("hMadGenCrossSection")
        hGenLOMLM = fileGen.Get("hGen1CrossSection")
        hGenNLOFXFX.SetDirectory(0)
        hGenLOMLM.SetDirectory(0)
        if (fileGen.IsOpen()):
            print ("File "+fileNameGen+" is still open, closing...")
            fileGen.Close()
        ## RECO
        print ("\n-----> Getting reco-level distribution")
        fileNameReco = unfoldDir+"SMu_"+variable+"_Central.root"
        print ("Opening file: "+fileNameReco)
        fileReco = ROOT.TFile.Open(fileNameReco, "READ")
        hRecoCentral = fileReco.Get("hRecDataBinsMerged_Central")
        hRecoCentral.SetDirectory(0)
        if (fileReco.IsOpen()):
            print ("File "+fileNameReco+" is still open, closing...")
            fileReco.Close()

    ## Get x- and y-axis bounds ---
    hCentral = histos[0]
    numBins = hCentral.GetNbinsX()
    # --- x-axis
    # xmin
    if (chopLeadingBins > 0):
        print("\nChopping off the first "+str(chopLeadingBins)+" bins from the distribution!")
        xmin = hCentral.GetXaxis().GetBinLowEdge(1+chopLeadingBins)
    else:
        xmin = hCentral.GetXaxis().GetXmin()
    # xmax
    if (chopEndingBins > 0):
        print("\nChopping off the last "+str(chopEndingBins)+" bins from the distribution!")
        xmax = hCentral.GetXaxis().GetBinUpEdge(numBins-chopEndingBins)
    else:
        xmax = hCentral.GetXaxis().GetXmax()
    # --- y-axis
    if (chopLeadingBins > 0):
        ### This is probably only going to work for steeply falling dist., like jet pT
        ymin = hCentral.GetBinContent(numBins)
        ymax = hCentral.GetBinContent(1+chopLeadingBins)*3.5
    else:
        ymin = hCentral.GetMinimum()*0.5
        ymax = hCentral.GetMaximum()*20.5

    print("\nNum. of bins: "+str(numBins)+", x-Min: "+str(xmin)+", x-Max: "+str(xmax)+", y-Min: "+str(ymin)+", y-Max: "+str(ymax))

    #########################

    c1 = ROOT.TCanvas("c1", "c1", 600, 800)
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

    ### Pad 1
    pad1.cd()
    pad1.SetLogy()

    htemp = ROOT.TH1D("htemp", "htemp", 100, xmin, xmax)
    htemp.SetStats(0)
    htemp.GetXaxis().SetTitle("")
    if not (variable == "dPhiLepJet1_Zinc1jet_TUnfold" or variable == "dPhiLepJet1AK8_Zinc1jet_TUnfold"):
        htemp.GetYaxis().SetRangeUser(ymin-(abs(ymin)*0.7), ymax+(abs(ymax)*2.5))
    else:
        htemp.GetYaxis().SetRangeUser(ymin-(abs(ymin)*0.93), ymax+(abs(ymax)*50.))
    htemp.GetYaxis().SetTitle("Diff. Cross Section")
    htemp.GetYaxis().SetTitleOffset(1.375)
    htemp.SetTitle(variable+", Unfolded")
    htemp.Draw()

    ### line and marker settings ---
    hCentral.SetLineColor(ROOT.kBlack)
    hCentral.SetLineWidth(1)
    hCentral.SetMarkerColor(ROOT.kBlack)
    hCentral.SetMarkerStyle(20)
    hCentral.SetMarkerSize(0.8)

    if (numNames > 1):
        j = 0
        colors = [ROOT.kRed, ROOT.kOrange-6, ROOT.kOrange-3, ROOT.kGreen,
                  ROOT.kAzure+8, ROOT.kBlue, ROOT.kViolet+1, ROOT.kPink+6]
        for i in range(1, numNames):
            histos[i].SetLineWidth(1)
            histos[i].SetMarkerStyle(20)
            histos[i].SetMarkerSize(0.8)
            if (i % 2 == 1):
                j = j+1
            histos[i].SetLineColor(colors[j-1])
            histos[i].SetMarkerColor(colors[j-1])

    if (doGenRecoComp):
        ## GEN
        hGenNLOFXFX.SetLineColor(ROOT.kGreen)
        hGenNLOFXFX.SetLineWidth(1)
        hGenNLOFXFX.SetMarkerColor(ROOT.kGreen)
        hGenNLOFXFX.SetMarkerStyle(20)
        hGenNLOFXFX.SetMarkerSize(0.8)
        hGenLOMLM.SetLineColor(ROOT.kSpring+3)
        hGenLOMLM.SetLineWidth(1)
        hGenLOMLM.SetMarkerColor(ROOT.kSpring+3)
        hGenLOMLM.SetMarkerStyle(20)
        hGenLOMLM.SetMarkerSize(0.8)
        ## RECO
        hRecoCentral.SetLineColor(ROOT.kRed)
        hRecoCentral.SetLineWidth(1)
        hRecoCentral.SetMarkerColor(ROOT.kRed)
        hRecoCentral.SetMarkerStyle(20)
        hRecoCentral.SetMarkerSize(0.8)

######################################################################################################################
### Error calculations to make the shaded error bands
    if (numNames > 1):

        if (doSystBands):
            systErrsUp = []
            systErrsDown = []
            for i in range(1, numNames, 2):
                print("\n>>>>>>>>>> Doing errors for "+str(names[i])+" and "+str(names[i+1]))
                errsTempUp = []
                errsTempDown = []
                for jBin in range(1, numBins+1):
                    varCentral = histos[0].GetBinContent(jBin)
                    ### By grabbing these varMax and varMin, I'm disregarding which variation produced the up and the down
                    ### I believe that this means that I'm disregarding (anti)correlation, but we can compute covariance matrices later
                    varMax = max(varCentral, histos[i].GetBinContent(jBin), histos[i+1].GetBinContent(jBin))
                    varMin = min(varCentral, histos[i].GetBinContent(jBin), histos[i+1].GetBinContent(jBin))
                    print("Bin #"+str(jBin)+":")
                    print(names[0]+", "+str(varCentral))
                    print(names[i]+", "+str(histos[i].GetBinContent(jBin)))
                    print(names[i+1]+", "+str(histos[i+1].GetBinContent(jBin)))
                    print("Max: "+str(varMax)+", "+str(100.*(varMax-varCentral)/varCentral)+"% Up!")
                    print("Min: "+str(varMin)+", "+str(100.*(varMin-varCentral)/varCentral)+"% Down!"+"\n")
                    ### Take absolute value of deviations up/down because errors will eventually create TGraphAsymmErrors
                    errsTempUp.append(abs(varMax-varCentral))
                    errsTempDown.append(abs(varMin-varCentral))
                systErrsUp.append(errsTempUp)
                systErrsDown.append(errsTempDown)

            # print("systErrsUp: "+str(systErrsUp)+"\n")
            # print("systErrsDown: "+str(systErrsDown)+"\n")
            # print(str(systErrsUp[1][0])+"\n") #first number is the systematic, second number is the bin

            ### Okay now that we've computed all bins' errors for each pair of variations, let's add them in quadrature
            systErrTotalUp   = array('d')
            systErrTotalDown = array('d')
            ## Loop over the number of bins
            for iBin in range(0, numBins):
                sumUp = 0.
                sumDown = 0.
                ## Loop over the number of systematics
                for j in range(0, int((numNames-1)/2), 1):
                    # ---
                    # do in the general case where both up/down variations from central are non-zero
                    if ( (systErrsUp[j][iBin] > 0) and (systErrsDown[j][iBin] > 0) ):
                        sumUp   += (systErrsUp[j][iBin])*(systErrsUp[j][iBin])
                        sumDown += (systErrsDown[j][iBin])*(systErrsDown[j][iBin])
                    # but in the case of one of the variations being zero, must take the non-zero variation as a symmetric up/down uncertainty on that bin (e.g. the unfolding systematic)
                    else:
                        uncertTemp = max(systErrsUp[j][iBin], systErrsDown[j][iBin])
                        sumUp   += (uncertTemp * uncertTemp)
                        sumDown += (uncertTemp * uncertTemp)
                    # ---
                systErrTotalUp.append(math.sqrt(sumUp))
                systErrTotalDown.append(math.sqrt(sumDown))

            print("-----> Systematic Errors Added in Quadrature by Bin: ")
            print("-----> systErrTotalUp: "+str(systErrTotalUp))
            print("-----> systErrTotalDown: "+str(systErrTotalDown)+"\n")

            ### Now make graph that overlaps with the central distribution but with the syst error bands
            xsecCentral = array('d')
            binCenters = array('d')
            xErrLow = array('d')
            xErrUp = array('d')
            for iBin in range(1, numBins+1):
                xsecCentral.append(hCentral.GetBinContent(iBin))
                binCenters.append((hCentral.GetXaxis().GetBinLowEdge(iBin)+hCentral.GetXaxis().GetBinUpEdge(iBin))/2.)
                xErrLow.append(binCenters[iBin-1]-hCentral.GetXaxis().GetBinLowEdge(iBin))
                xErrUp.append(hCentral.GetXaxis().GetBinUpEdge(iBin)-binCenters[iBin-1])

            grCentralSystErrors = ROOT.TGraphAsymmErrors(numBins, binCenters, xsecCentral, xErrLow, xErrUp, systErrTotalDown, systErrTotalUp)
            grCentralSystErrors.SetLineWidth(1)
            grCentralSystErrors.SetLineStyle(1)
            grCentralSystErrors.SetFillStyle(3354)
            grCentralSystErrors.SetLineColor(ROOT.kBlack)
            grCentralSystErrors.SetFillColorAlpha(ROOT.kBlack, 0.6)
            grCentralSystErrors.SetMarkerSize(0.)
            grCentralSystErrors.Draw("E2 same") #draws just the hatched bands that represent only the total systematic uncertainty
            hCentral.Draw("PE same")            #draws the points with statistical error bars

        else:
            for i in range(1, numNames):
                histos[i].Draw("P same")
            hCentral.Draw("PE same")

    if (doGenRecoComp):
        hRecoCentral.Draw("PE SAME")
        hGenNLOFXFX.Draw("PE SAME")
        hGenLOMLM.Draw("PE SAME")

######################################################################################################################

    ### draw legends
    if not (variable == "dPhiLepJet1_Zinc1jet_TUnfold" or variable == "dPhiLepJet1AK8_Zinc1jet_TUnfold"):
        if (doGenRecoComp):
            leg1 = ROOT.TLegend(0.525,0.625,0.9,0.925)
        else:
            leg1 = ROOT.TLegend(0.625,0.525,0.9,0.925)
    else:
        if (doGenRecoComp):
            leg1 = ROOT.TLegend(0.1,0.625,0.475,0.925)
        else:
            leg1 = ROOT.TLegend(0.1,0.525,0.375,0.925)
    leg1.AddEntry(hCentral, "Unfolded", "lpe")
    if (numNames > 1):
#        if (doSystBands):
#            leg1.AddEntry(grCentralSystErrors , "Total Syst. Uncert.", "f")
        if (doGenRecoComp):
            leg1.AddEntry(hRecoCentral, "Reconstructed", "lpe")
            leg1.AddEntry(hGenNLOFXFX, "MG5 NLO FxFx GEN", "lpe")
            leg1.AddEntry(hGenLOMLM, "MG5 LO MLM GEN", "lpe")
        else:
            for i in range(1, numNames):
                leg1.AddEntry(histos[i], names[i], "lpe")
    leg1.Draw("same")

    ### Pad 2
    pad2.cd()

    htemp1 = ROOT.TH1D("htemp1", "htemp1", 100, xmin, xmax)
    htemp1.SetStats(0)
    htemp1.GetXaxis().SetTitle(hCentral.GetXaxis().GetTitle())
    htemp1.GetXaxis().SetTitleOffset(1.2)
    htemp1.GetXaxis().SetTitleSize(0.09)
    htemp1.GetXaxis().SetLabelSize(0.09)
    htemp1.GetYaxis().SetTitle("Ratio to Unfolded   ")
    htemp1.GetYaxis().SetTitleOffset(0.55)
    htemp1.GetYaxis().SetTitleSize(0.08)
    htemp1.GetYaxis().SetLabelSize(0.07)
#    htemp1.GetYaxis().SetRangeUser(0.499, 1.501)
    htemp1.GetYaxis().SetRangeUser(0.01, 2.15) # y-axis range for the unfolded dist's subplots in unfolding code
    htemp1.SetTitle("")
    htemp1.Draw()

    line1 = ROOT.TLine(xmin, 1., xmax, 1.)
    line1.SetLineColor(ROOT.kBlack)
    line1.SetLineWidth(1)
    line1.Draw()

    ### Draw ratio subplot
    if (numNames > 1):
        for i in range(1, numNames):
            ratioTemp = histos[i].Clone()
            ratioTemp.Divide(hCentral)
            for jBin in range(1, numBins+1):
                ratioTemp.SetBinError(jBin, 0.)
            histos_CentralRatio.append(ratioTemp)
            if not (doGenRecoComp):
                histos_CentralRatio[i-1].Draw("P same")

    if (doGenRecoComp):
        ratioRecoData = hRecoCentral.Clone()
        ratioGenNLOFXFXData = hGenNLOFXFX.Clone()
        ratioGenLOMLMData = hGenLOMLM.Clone()
        ratioRecoData.Divide(hCentral)
        ratioGenNLOFXFXData.Divide(hCentral)
        ratioGenLOMLMData.Divide(hCentral)
        ratioRecoData.Draw("PE SAME")
        ratioGenNLOFXFXData.Draw("PE SAME")
        ratioGenLOMLMData.Draw("PE SAME")

    #########################
    c1.Update()
    if (doGenRecoComp):
        print("wComp plot turned off for now!")
#        c1.Print(cwd+"/"+outputDir+"systPlot_"+variable+"-wComp.pdf")
    else:
        c1.Print(cwd+"/"+outputDir+"systPlot_"+variable+"-wSystXSecs.pdf")
    if (c1):
        c1.Close()
        ROOT.gSystem.ProcessEvents()

    ## Delete TCanvas and such
    del c1, htemp, htemp1, leg1

######################################################################################################################

    ## Make percent uncertainty systematics plot
    if (doSystBands):
        c1 = ROOT.TCanvas("c1", "c1", 400, 400)
        c1.cd()
        pad1 = ROOT.TPad("pad1.1", "pad1.1", 0, 0., 1, 1)
        pad1.SetTicks()
        pad1.Draw()

        ### Pad 1
        pad1.cd()
        pad1.SetLogy()

        htemp = ROOT.TH1D("htemp", "htemp", 100, xmin, xmax)
        htemp.GetYaxis().SetRangeUser(0.0005, 100.)
        htemp.GetYaxis().SetTitle("Percent Uncertainty")
        htemp.GetYaxis().SetTitleOffset(1.35)
        htemp.SetStats(0)
        htemp.GetXaxis().SetTitle(hCentral.GetXaxis().GetTitle())
        htemp.GetXaxis().SetTitleOffset(1.2)
        htemp.SetTitle(variable+", Syst. Uncert. Breakdown")
        htemp.Draw()

        for i in range(0, int((numNames-1)/2), 1):
            hTemp_PercUncert = hCentral.Clone()
            for jBin in range(0, numBins):
                percentUncertainty = 0.
                # print(max(systErrsUp[i][jBin], systErrsDown[i][jBin]))
                # print(hCentral.GetBinContent(jBin+1))
                # print( (max(systErrsUp[i][jBin], systErrsDown[i][jBin]))*100./hCentral.GetBinContent(jBin+1) )
                # print("---")
                # ---
                # general case where you have one variation above central and one variation below central
                # in this case, take the average of the up/down variations from central
                if ( (systErrsUp[i][jBin] > 0) and (systErrsDown[i][jBin] > 0) ):
                    uncertTemp = 0.5 * (systErrsUp[i][jBin] + systErrsDown[i][jBin])
                # special case (e.g. the unfolding uncertainty where you only have one variation above or below the central)
                else:
                    uncertTemp = max(systErrsUp[i][jBin], systErrsDown[i][jBin])
                percentUncertainty = (uncertTemp/hCentral.GetBinContent(jBin+1)) * 100.
                # ---
                hTemp_PercUncert.SetBinContent(jBin+1, percentUncertainty)
                hTemp_PercUncert.SetBinError(jBin+1, 0.)
            hTemp_PercUncert.SetLineWidth(2)
            hTemp_PercUncert.SetMarkerStyle(20)
            hTemp_PercUncert.SetMarkerSize(0.6)
            hTemp_PercUncert.SetLineColor(colors[i])
            hTemp_PercUncert.SetMarkerColor(colors[i])
            histos_PercentUncertainty.append(hTemp_PercUncert)
            histos_PercentUncertainty[i].Draw("SAME")

        hTemp_PercUncert = hCentral.Clone()
        print("\n ----- Total Percent Uncertainty -----")
        for iBin in range(0, numBins):
            percentUncertainty = 0.
            # --- 
            # averaging the final up and down uncertainties that are calculated above
            uncertTemp = 0.5 * (systErrTotalUp[iBin] + systErrTotalDown[iBin])
            percentUncertainty = (uncertTemp/hCentral.GetBinContent(iBin+1)) * 100.
            # ---
            hTemp_PercUncert.SetBinContent(iBin+1, percentUncertainty)
            hTemp_PercUncert.SetBinError(iBin+1, 0.)
            print("Bin #"+str(iBin+1)+": "+str(percentUncertainty)+" %")
        hTemp_PercUncert.SetLineWidth(2)
        hTemp_PercUncert.SetMarkerStyle(20)
        hTemp_PercUncert.SetMarkerSize(0.6)
        hTemp_PercUncert.SetLineColor(ROOT.kBlack)
        hTemp_PercUncert.SetMarkerColor(ROOT.kBlack)
        histos_PercentUncertainty.append(hTemp_PercUncert)
        histos_PercentUncertainty[int((numNames-1)/2)].Draw("SAME")

        ROOT.gPad.RedrawAxis()

#        leg1 = ROOT.TLegend(0.625,0.1,0.9,0.4) # nominal
        leg1 = ROOT.TLegend(0.1,0.1,0.425,0.33)
        if (numNames > 1):
            leg1.AddEntry(histos_PercentUncertainty[int((numNames-1)/2)], "Total Systematic Uncertainty", "l")
            for i in range(0, int((numNames-1)/2), 1):
                leg1.AddEntry(histos_PercentUncertainty[i], namesLegend[i], "l")
        leg1.Draw("same")

        #########################
        c1.Update()
        c1.Print(cwd+"/"+outputDir+"systPlot_"+variable+"_Uncertainties"+".pdf")
        if (c1):
            c1.Close()
            ROOT.gSystem.ProcessEvents()

        ## Delete TCanvas and such
        del c1, htemp, leg1

    ## Delete large objects
    del histos, histos_CentralRatio

print ("\nFinished!\n")