#! /usr/bin/env python3
import os
import sys
import numpy as np
import pandas as pd
import math
from array import array
import ROOT
#############################################


variables = ["genLepPtPlusLeadingJetAK8Pt_Zinc1jet_TUnfold",
             "genLepPtPlusLeadingJetAK8Pt_Zinc2jet_TUnfold",
             "genLepPtPlusLeadingJetAK8Pt_Zinc3jet_TUnfold",
             "genLepPtPlusLeadingJetAK8Pt_Zexc1jet_TUnfold",
             "genLepPtPlusLeadingJetAK8Pt_Zexc2jet_TUnfold"
             ]

#year = "2016"
year = "Run2"

#############################################

print ("\nBegin!")

#fileNamePrefix = "SMu_13TeV_WJets_FxFx_dR_5311_List_EffiCorr_1_TrigCorr_1_Syst_0_JetPtMin_30_VarWidth_"
#fileNamePrefix = "SMu_13TeV_WJets_FxFx_Wpt_dR_5311_List_EffiCorr_1_TrigCorr_1_Syst_0_JetPtMin_30_VarWidth_"
#fileNamePrefix = "SMu_13TeV_WJets_FxFx_012J_dR_5311_List_EffiCorr_1_TrigCorr_1_Syst_0_JetPtMin_30_VarWidth_"
#fileNamePrefix = "SMu_13TeV_WJets_FxFx_ALL_SAMPLES_dR_5311_List_EffiCorr_1_TrigCorr_1_Syst_0_JetPtMin_30_VarWidth_"
fileNamePrefix = "SMu_13TeV_WJets_FxFx_JET_AND_PT_dR_5311_List_EffiCorr_1_TrigCorr_1_Syst_0_JetPtMin_30_VarWidth_"

for iVar, variable in enumerate(variables):

    fOff = ROOT.TFile.Open(fileNamePrefix+year+"_EWcorrOFF.root", "READ")
    fOn  = ROOT.TFile.Open(fileNamePrefix+year+"_EWcorrON.root", "READ")
    hEWoff = fOff.Get(variable)
    hEWon  = fOn.Get(variable)
    hEWoff.SetDirectory(0)
    hEWon.SetDirectory(0)
    if (fOff.IsOpen):
        fOff.Close()
    if (fOn.IsOpen):
        fOn.Close()

    #########################

    c1 = ROOT.TCanvas("c1", "c1", 600, 400)
    c1.cd()
    pad1 = ROOT.TPad("pad1", "pad1", 0, 0, 1, 1)
    pad1.Draw()
    pad1.cd()

    numBinsX = hEWoff.GetNbinsX()
#    xmin = hEWoff.GetXaxis().GetXmin()
#    xmax = hEWoff.GetXaxis().GetXmax()
    xmin = 200.
    xmax = 1400.
#    xtitle = 'Muon p_{T} + Leading AK8 Jet p_{T} [GeV]'
    xtitle = 'p_{T}(#mu) + p_{T}(j_{1}) [GeV]'

    htemp = ROOT.TH1D("htemp", "htemp", 100, xmin, xmax)
    htemp.GetYaxis().SetRangeUser(0.851, 1.049)
    htemp.SetStats(0)
    htemp.GetXaxis().SetTitle(xtitle)
    htemp.GetXaxis().SetTitleOffset(1.2)
    htemp.GetYaxis().SetTitle('EW_{On}/EW_{Off}')
    htemp.GetYaxis().SetTitleOffset(1.3)

    selectionName = 'W + jets'
    if (variable == 'genLepPtPlusLeadingJetAK8Pt_Zinc1jet_TUnfold'):
        selectionName = 'W + #geq1 jets'
    elif (variable == 'genLepPtPlusLeadingJetAK8Pt_Zinc2jet_TUnfold'):
        selectionName = 'W + #geq2 jets'
    elif (variable == 'genLepPtPlusLeadingJetAK8Pt_Zinc3jet_TUnfold'):
        selectionName = 'W + #geq3 jets'
    elif (variable == 'genLepPtPlusLeadingJetAK8Pt_Zexc1jet_TUnfold'):
        selectionName = 'W + 1 jet'
    elif (variable == 'genLepPtPlusLeadingJetAK8Pt_Zexc2jet_TUnfold'):
        selectionName = 'W + 2 jets'
    htemp.SetTitle("NLO EW Correction, "+selectionName)

    htemp.Draw()

    line1 = ROOT.TLine(xmin, 1., xmax, 1.);
    line1.SetLineColor(ROOT.kBlack);
    line1.SetLineWidth(1);
    line1.Draw("SAME")

    hRatio = hEWoff.Clone()
    hRatio.Divide(hEWon, hEWoff)

#    for iBin in range(1, numBinsX+1):
#        hRatio.SetBinError(iBin, 0.0)

    hRatio.SetMarkerColor(4)
    hRatio.SetMarkerStyle(20)
    hRatio.SetMarkerSize(0.7)
    hRatio.SetLineColorAlpha(4, 1.);
    hRatio.SetLineWidth(2)
    hRatio.SetLineStyle(1)
    hRatio.Draw("PE SAME")

    # print and store output values
    nloEWcorr = []
    print("\nhRatio:")
    for iBin in range(1, numBinsX+1):
        print( "Bin #"+str(iBin)+": "+str(hRatio.GetBinContent(iBin)) )
        nloEWcorr.append(hRatio.GetBinContent(iBin))
    print("\nnloEWcorr = "+str(nloEWcorr)+"\n")

#########################

    c1.Update()
    c1.Print("/Users/alwisecarver/Desktop/prezzies/SMP-VJ/20210917/*temp_9july21/nloEWcorrections_21_07_14/"+"nloEWcorr_"+variable+"_"+year+".pdf")
    if (c1):
        c1.Close()
        ROOT.gSystem.ProcessEvents()
    del c1, htemp

print ("\nFinished!")
