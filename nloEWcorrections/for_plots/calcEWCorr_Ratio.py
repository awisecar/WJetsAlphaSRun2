#! /usr/bin/env python3
import os
import sys
import numpy as np
import pandas as pd
import math
from array import array
import ROOT
#############################################

#variableNUM   = "genLepPtPlusLeadingJetAK8Pt_Zinc2jet_TUnfold"
#variableDENOM = "genLepPtPlusLeadingJetAK8Pt_Zinc1jet_TUnfold"

#variableNUM   = "genLepPtPlusLeadingJetAK8Pt_Zinc3jet_TUnfold"
#variableDENOM = "genLepPtPlusLeadingJetAK8Pt_Zinc2jet_TUnfold"

#variableNUM   = "genLepPtPlusLeadingJetAK8Pt_Zinc3jet_TUnfold"
#variableDENOM = "genLepPtPlusLeadingJetAK8Pt_Zinc1jet_TUnfold"

variableNUM   = "genLepPtPlusLeadingJetAK8Pt_Zexc2jet_TUnfold"
variableDENOM = "genLepPtPlusLeadingJetAK8Pt_Zexc1jet_TUnfold"

# ---

#year = "2016"
year = "Run2"

#############################################

print ("\nBegin!")

#fileNamePrefix = "SMu_13TeV_WJets_FxFx_dR_5311_List_EffiCorr_1_TrigCorr_1_Syst_0_JetPtMin_30_VarWidth_"
#fileNamePrefix = "SMu_13TeV_WJets_FxFx_Wpt_dR_5311_List_EffiCorr_1_TrigCorr_1_Syst_0_JetPtMin_30_VarWidth_"
#fileNamePrefix = "SMu_13TeV_WJets_FxFx_012J_dR_5311_List_EffiCorr_1_TrigCorr_1_Syst_0_JetPtMin_30_VarWidth_"
#fileNamePrefix = "SMu_13TeV_WJets_FxFx_ALL_SAMPLES_dR_5311_List_EffiCorr_1_TrigCorr_1_Syst_0_JetPtMin_30_VarWidth_"
fileNamePrefix = "SMu_13TeV_WJets_FxFx_JET_AND_PT_dR_5311_List_EffiCorr_1_TrigCorr_1_Syst_0_JetPtMin_30_VarWidth_"

#########################

fOff = ROOT.TFile.Open(fileNamePrefix+year+"_EWcorrOFF.root", "READ")
fOn  = ROOT.TFile.Open(fileNamePrefix+year+"_EWcorrON.root", "READ")

# NUM
hEWoffNUM = fOff.Get(variableNUM)
hEWonNUM  = fOn.Get(variableNUM)
hEWoffNUM.SetDirectory(0)
hEWonNUM.SetDirectory(0)

# DENOM
hEWoffDENOM = fOff.Get(variableDENOM)
hEWonDENOM  = fOn.Get(variableDENOM)
hEWoffDENOM.SetDirectory(0)
hEWonDENOM.SetDirectory(0)

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

numBinsX = hEWoffNUM.GetNbinsX()
xmin = 200.
xmax = 1400.
#xtitle = 'Muon p_{T} + Leading AK8 Jet p_{T} [GeV]'
xtitle = 'p_{T}(#mu) + p_{T}(j_{1}) [GeV]'

htemp = ROOT.TH1D("htemp", "htemp", 100, xmin, xmax)
htemp.GetYaxis().SetRangeUser(0.851, 1.049)
htemp.SetStats(0)
htemp.GetXaxis().SetTitle(xtitle)
htemp.GetXaxis().SetTitleOffset(1.2)
htemp.GetYaxis().SetTitle('EW_{On}/EW_{Off}')
htemp.GetYaxis().SetTitleOffset(1.3)

selectionName = 'Ratio'
if (variableNUM == 'genLepPtPlusLeadingJetAK8Pt_Zinc2jet_TUnfold' and variableDENOM == 'genLepPtPlusLeadingJetAK8Pt_Zinc1jet_TUnfold'):
    selectionName = 'R_{21}'
elif (variableNUM == 'genLepPtPlusLeadingJetAK8Pt_Zexc2jet_TUnfold' and variableDENOM == 'genLepPtPlusLeadingJetAK8Pt_Zexc1jet_TUnfold'):
    selectionName = 'R_{W+2j/W+1j}'
htemp.SetTitle("NLO EW Correction, "+selectionName)

htemp.Draw()

line1 = ROOT.TLine(xmin, 1., xmax, 1.);
line1.SetLineColor(ROOT.kBlack);
line1.SetLineWidth(1);
line1.Draw("SAME")

# NUM
hRatioNUM = hEWoffNUM.Clone()
hRatioNUM.Divide(hEWonNUM, hEWoffNUM)
# DENOM
hRatioDENOM = hEWoffDENOM.Clone()
hRatioDENOM.Divide(hEWonDENOM, hEWoffDENOM)
# RATIO
hRatioRATIO = hRatioNUM.Clone()
hRatioRATIO.Divide(hRatioNUM, hRatioDENOM)

hRatioRATIO.SetMarkerColor(4)
hRatioRATIO.SetMarkerStyle(20)
hRatioRATIO.SetMarkerSize(0.7)
hRatioRATIO.SetLineColorAlpha(4, 1.);
hRatioRATIO.SetLineWidth(2)
hRatioRATIO.SetLineStyle(1)
hRatioRATIO.Draw("PE SAME")

# print and store output values
nloEWcorr = []
print("\nhRatioRATIO:")
for iBin in range(1, numBinsX+1):
    print( "Bin #"+str(iBin)+": "+str(hRatioRATIO.GetBinContent(iBin)) )
    nloEWcorr.append(hRatioRATIO.GetBinContent(iBin))
print("\n >>> nloEWcorr = "+str(nloEWcorr)+"\n")

#########################

c1.Update()
c1.Print("/Users/alwisecarver/Desktop/prezzies/SMP-VJ/20210917/*temp_9july21/nloEWcorrections_21_07_14/"+"nloEWcorr_RATIO_"+variableNUM+"_TO_"+variableDENOM+"_"+year+".pdf")
if (c1):
    c1.Close()
    ROOT.gSystem.ProcessEvents()
del c1, htemp

print ("\nFinished!")
