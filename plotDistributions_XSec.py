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
This script is designed to plot xsecs from FastNLO tables against the unfolded data 
and other theory predictions
> processes, tablenames are for selecting the distributions
> pdfnames is for selecting the PDF set that the FastNLO tables are read with
> doErrors turns on the statistical errors for the FastNLO xsecs
> doNP turns on the application of non-perturbative corrections to FastNLO xsecs
> doData gets the unfolded data and other theory predictions from unfolding code
'''
##################################################
# processes = ['W1J']
# tablenames = ['d06-x01-y01.merged', 'd31-x01-y01.merged', 'd56-x01-y01.merged', 'd81-x01-y01.merged']
processes = ['W2J']
tablenames = ['d07-x01-y01.merged', 'd57-x01-y01.merged']
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

print("\n---------------- Begin distribution plotting! ----------------")

for process in processes:
    for tablename in tablenames:
        for pdfname in pdfnames:

            ##################################################################################
            ## 1) Grab data
            
            csvInfileME = "aSVarME-"+pdfname+"-"+process+"-"+tablename+".csv"
            csvInfileMEPDF = "aSVarMEPDF-"+pdfname+"-"+process+"-"+tablename+".csv"
            
            ## Grab the alpha-s value for each dataseries to use as label
            # just ME var
            alphasNamesME = pd.read_csv(basedir+csvInfileME, nrows=1) #grabbing first row of diagonistic information
            alphasvalsME = alphasNamesME.values.tolist()[0][3:]
            numVarME = int( alphasNamesME.values.tolist()[0][2] ) #total number of alpha-s variations for ME
            # ME and PDF var
            alphasNamesMEPDF = pd.read_csv(basedir+csvInfileMEPDF, nrows=1)
            alphasvalsMEPDF = alphasNamesMEPDF.values.tolist()[0][3:]
            numVarMEPDF = int( alphasNamesMEPDF.values.tolist()[0][2] )  #total number of alpha-s variations for ME+PDF
            #num of bins should be the same for two different files
            numBins = int(alphasNamesME.values.tolist()[0][0])  #number of bins in the distribution
            
            ## Grab the data
            dataInME = pd.read_csv(basedir+csvInfileME, skiprows=[1]) #skip first row, but with keeping headers
            dataInMEPDF = pd.read_csv(basedir+csvInfileMEPDF, skiprows=[1])
            
            ## Grab unfolded data and signal W+jets MC
            if (process == 'W1J'):
                if (tablename == 'd06-x01-y01.merged'):
                    variable = "LepPtPlusLeadingJetPt_Zinc1jet_TUnfold"
                if (tablename == 'd31-x01-y01.merged'):
                    variable = "LepPtPlusLeadingJetPt_Zexc1jet_TUnfold"
                if (tablename == 'd56-x01-y01.merged'):
                    variable = "LepPtPlusLeadingJetAK8Pt_Zinc1jet_TUnfold"
                if (tablename == 'd81-x01-y01.merged'):
                    variable = "LepPtPlusLeadingJetAK8Pt_Zexc1jet_TUnfold"
            if (process == 'W2J'):
                if (tablename == 'd07-x01-y01.merged'):
                    variable = "LepPtPlusLeadingJetPt_Zinc2jet_TUnfold"
                if (tablename == 'd57-x01-y01.merged'):
                    variable = "LepPtPlusLeadingJetAK8Pt_Zinc2jet_TUnfold"

            print ("\n===========================================================================")
            print ("\nDoing variable: "+str(variable))
            print ("Number of ME variations: "+str(int(numVarME)))
            print ("Number of ME+PDF variations: "+str(int(numVarMEPDF)))
            print ("Number of bins in histogram: "+str(numBins))

            if (doData):
                fileNameUnf = ("UnfoldedFiles_Run2/SMu_unfolded_"+variable+"_TUnfold_JetPtMin_30_JetEtaMax_24_MGPYTHIA6_.root")
                print ("\nOpening: "+fileNameUnf)
                fUnf = ROOT.TFile.Open(fileNameUnf, "READ")

            ##################################################################################
            ## 1b) Grab uncertainties and SFs

            ####### Errors
            if (doErrors):
                xErrLow = array('d') #x-error should just be the bin widths
                xErrUp = array('d')
                yErrLow = array('d')
                yErrUp = array('d')

                #stat error
                csvInfileStatUncert = "statUncert-"+pdfname+"-"+process+"-"+tablename+".csv"
                dataInStatUncert = pd.read_csv(basedir+csvInfileStatUncert)
                yErrLowStat = array('d')
                yErrUpStat = array('d')
                for i in range(numBins):
                    xErrLow.append( ((dataInStatUncert["'XERRLOW'"]).values)[i] )
                    xErrUp.append( ((dataInStatUncert["'XERRUP'"]).values)[i] )
                    yErrLowStat.append( ((dataInStatUncert["'YERRLOW'"]).values)[i] )
                    yErrUpStat.append( ((dataInStatUncert["'YERRUP'"]).values)[i] )
            
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
                # W+1J
                if (tablename == 'd06-x01-y01.merged'): 
                    nonpertSFs = [1.2010625918051203, 1.1298239392566556, 1.07133490626799, 1.0322962846450936, 1.0105480864823724, 0.9993642232331477, 0.9931152945868026, 0.9890435762337125, 0.9865012348803278, 0.9848357027014492]
                if (tablename == 'd31-x01-y01.merged'): 
                    nonpertSFs = [1.19275844350739, 1.1199652421556099, 1.0589974205974122, 1.0173041320196443, 0.9934555951734685, 0.9808749675176636, 0.9736785761375525, 0.9688768894234097, 0.9657979786368535, 0.9637136791419829]
                if (tablename == 'd56-x01-y01.merged'): 
                    nonpertSFs = [1.1011794317605685, 1.0899096172250768, 1.078483162968084, 1.0659008006921162, 1.053810096192782, 1.0420880619495763, 1.0290413747579634, 1.0146062990008113, 0.9980935928741425]
                if (tablename == 'd81-x01-y01.merged'): 
                    nonpertSFs = [1.1010032257492965, 1.0898741520851927, 1.0785332788034736, 1.0659734773716554, 1.053827625966885, 1.041973526047908, 1.028679393484072, 1.013831966294646, 0.9966404959289775]
                # W+2J
                if (tablename == 'd07-x01-y01.merged'): 
                    nonpertSFs = [1.3896005897157113, 1.2470054856288724, 1.137700633319125, 1.0706067860636121, 1.0364868374388996, 1.0204210577848034, 1.0121440610542551, 1.0071749547041193, 1.0043442086436452, 1.0026876020828206]
                if (tablename == 'd57-x01-y01.merged'): 
                    nonpertSFs = [1.285717560676564, 1.1578183804295012, 1.0885000425493627, 1.0508123713199902, 1.03434786285872, 1.0273568362470915, 1.024286202584473, 1.0232033623310892, 1.0229147149114493]
                print("\nApplying non-pertrubative corrections:\n"+str(nonpertSFs))

            ##################################################################################
            ## 2) Plot xsec distributions
            
            ## Plot
            #Note: if don't want any pads, just uncommented the following three lines and comment out the tpad stuff
            # c1 = ROOT.TCanvas('canVar_'+process+'_'+tablename, 'canVar_'+process+'_'+tablename, 500, 500)
            # c1.Update()
            # c1.Draw()

            # Doing canvas with two pads
            c1 = ROOT.TCanvas('canVar_'+process+'_'+tablename, 'canVar_'+process+'_'+tablename, 600, 800)
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

            ## Get x-bins
            ## TGraph must take data as type array
            ## Values method converts from pandas series to numpy array
            binCenME = array('d')
            binCenMEPDF = array('d')
            for i in range(numBins):
                binCenME.append((dataInME["'BINCENTER'"].values)[i])
                binCenMEPDF.append(dataInMEPDF["'BINCENTER'"].values[i])
            if (binCenME == binCenMEPDF):
                print ("\nBinning of ME & ME+PDF distributions is equal: \n"+str(binCenME))
            else:
                print ("\nBinning of ME & ME+PDF distributions is not equal! Exiting code!")
                sys.exit()
            
            ## Open unfolded histogram here to fetch x-axis values
            ## Plot after the htemp histo is plotted
            # Don't forget about SetLineStyle, SetMarkerStyle commands if needed
            if (doData):
                hUnf = fUnf.Get("hUnfData_Central")
                hUnf.SetLineColor(ROOT.kBlack)
                hUnf.SetLineWidth(2)
                hUnf.SetMarkerColor(ROOT.kBlack)
                hWJetsNLOFxFx = fUnf.Get("hMadGenCrossSection")
                hWJetsNLOFxFx.SetLineColor(ROOT.kOrange)
                hWJetsNLOFxFx.SetLineWidth(2)
                hWJetsNLOFxFx.SetMarkerColor(ROOT.kOrange)
                hWJetsLOMLM = fUnf.Get("hGen1CrossSection")
                hWJetsLOMLM.SetLineColor(ROOT.kOrange+3)
                hWJetsLOMLM.SetLineWidth(2)
                hWJetsLOMLM.SetMarkerColor(ROOT.kOrange+3)
                # # Getting x-axis bounds from unfolded data histogram
                # xmin = hUnf.GetXaxis().GetXmin()
                # xmax = hUnf.GetXaxis().GetXmax()
            # else:
            # Get x-axis bounds from FastNLO distributions
            xmin = binCenME[0]-(binCenME[1]-binCenME[0])/2.
            xmax = binCenME[numBins-1]+(binCenME[numBins-1]-binCenME[numBins-2])/2.

            ## Get y-bounds and titles depending on distribution
            ## Note: binDataOffset only applies to the histograms from the WJets analysis code,
            ## since there are often leading bins that are empty
            ## Distributions from FastNLO tables are not allowed to have any bins with zero entries
            ROOT.gPad.SetLogy() #set y-axis as logarithmic
            if (process == 'W1J'):
                if (tablename == 'd06-x01-y01.merged'):
                    ymin = 0.0015
                    ymax = 100
                    xtitle = 'Muon p_{T} + Leading Jet p_{T} [GeV]'
                    ytitle = 'd#sigma/dp_{T} [pb/GeV]'
                    binDataOffset = 2
                elif (tablename == 'd31-x01-y01.merged'):
                    ymin = 0.0004
                    ymax = 100
                    xtitle = 'Muon p_{T} + Leading Jet p_{T} [GeV]'
                    ytitle = 'd#sigma/dp_{T} [pb/GeV]'
                    binDataOffset = 2
                elif (tablename == 'd56-x01-y01.merged'):
                    ymin = 0.0007
                    ymax = 0.45
                    xtitle = 'Muon p_{T} + Leading Jet p_{T} [GeV]'
                    ytitle = 'd#sigma/dp_{T} [pb/GeV]'
                    binDataOffset = 1
                elif (tablename == 'd81-x01-y01.merged'):
                    ymin = 0.0005
                    ymax = 0.45
                    xtitle = 'Muon p_{T} + Leading Jet p_{T} [GeV]'
                    ytitle = 'd#sigma/dp_{T} [pb/GeV]'
                    binDataOffset = 1
            if (process == 'W2J'):
                if (tablename == 'd07-x01-y01.merged'):
                    ymin = 0.0015
                    ymax = 20.
                    xtitle = 'Muon p_{T} + Leading Jet p_{T} [GeV]'
                    ytitle = 'd#sigma/dp_{T} [pb/GeV]'
                    binDataOffset = 2
                elif (tablename == 'd57-x01-y01.merged'):
                    ymin = 0.0002
                    ymax = 0.08
                    xtitle = 'Muon p_{T} + Leading Jet p_{T} [GeV]'
                    ytitle = 'd#sigma/dp_{T} [pb/GeV]'
                    binDataOffset = 1

            ## Easier to change axis ranges if you draw a TH1 with those ranges first
            htemp = ROOT.TH1D("aSXSec_"+tablename, process+" "+order+", "+tablename, 100, xmin, xmax)
            htemp.GetYaxis().SetRangeUser(ymin, ymax)
            htemp.SetStats(0)
            htemp.GetXaxis().SetTitle(xtitle)
            htemp.GetXaxis().SetTitleOffset(1.2)
            htemp.GetYaxis().SetTitle(ytitle)
            htemp.GetYaxis().SetTitleOffset(1.3)
            htemp.SetTitle("")
            htemp.Draw()
            
            ## Plot unfolded data and signal MC
            if (doData):
                hUnf.Draw("E same")
                hWJetsNLOFxFx.Draw("E same")
                # hWJetsLOMLM.Draw("E same")

            # Make legend
            leg1 = ROOT.TLegend(0.3,0.75,0.935,0.975)
            leg1.SetTextSize(0.027)
            if (doData):
                leg1.AddEntry(hUnf, "Unfolded Data", "lp")
                leg1.AddEntry(hWJetsNLOFxFx, "MG5_aMC FxFx + PY8 (#leq 2j NLO + PS)", "lp")
                # leg1.AddEntry(hWJetsLOMLM, "MG5_aMC MLM + PY8 (#leq 4j LO + PS)", "lp")

            #Keeping the graphs in a list allows us to draw multiple on canvas
            grMElist = []
            grMEPDFlist = []
            varArrayMElist = []
            varArrayMEPDFlist = []
            
            ## Get the ME xsec variations --------------------
            print ("\nDoing ME xsecs!")
            for i, alphas in enumerate(alphasvalsME):
                print ("alpha-s = "+str(round(alphas,3)))
                ## -- First get array for the xsec values --
                varArray = array('d')
                for j in range(numBins):
                    SFtemp = nonpertSFs[j]
                    xSecTemp = ((dataInME[("'aS=")+str(round(alphas,3))+("'")]).values)[j]
                    xSecTemp *= SFtemp
                    varArray.append(xSecTemp)
                varArrayMElist.append(varArray)
                ## -- Now create the TGraph using this array --
                if (doErrors):
                    gr = ROOT.TGraphAsymmErrors(numBins, binCenME, varArray, xErrLow, xErrUp, yErrLow, yErrUp)
                else:
                    gr = ROOT.TGraphAsymmErrors(numBins, binCenME, varArray)
                ## -- Cosmetics --
                gr.SetLineColorAlpha(2, 1.);
                gr.SetLineWidth(2)
                gr.SetLineStyle(1)
                gr.SetMarkerColor(2)
                gr.SetMarkerStyle(43)
                gr.SetMarkerSize(0.7)
                grMElist.append(gr)

            ## Get the ME+PDF xsec variations ----------------
            print ("\nDoing ME+PDF xsecs with PDF set "+pdfname+"!")
            for i, alphas in enumerate(alphasvalsMEPDF):
                print ("alpha-s = "+str(round(alphas,3)))
                ## -- First get array for the xsec values --
                varArray = array('d')
                for j in range(numBins):
                    SFtemp = nonpertSFs[j]
                    xSecTemp  = ((dataInMEPDF[("'aS=")+str(round(alphas,3))+("'")]).values)[j]
                    xSecTemp *= SFtemp
                    varArray.append(xSecTemp)
                varArrayMEPDFlist.append(varArray)
                ## -- Now create the TGraph using this array --
                if (doErrors):
                    gr = ROOT.TGraphAsymmErrors(numBins, binCenME, varArray, xErrLow, xErrUp, yErrLow, yErrUp)
                else:
                    gr = ROOT.TGraphAsymmErrors(numBins, binCenME, varArray)
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
            
            ## Now plot --------------------------------------
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

            ## TLatex stuff ----------------------------------
            cmsLogo = ROOT.TLatex()
            cmsLogo.SetNDC()
            cmsLogo.SetTextSize(0.054)
            cmsLogo.SetLineWidth(2)
            cmsLogo.SetTextFont(61)
            cmsLogo.SetTextColor(ROOT.kBlack)
            cmsLogo.SetTextAlign(11)
            cmsLogo.SetName("cmsLogo")
            cmsLogo.DrawLatex(0.545,0.61,"CMS")
            del cmsLogo
            cmsPrelim = ROOT.TLatex()
            cmsPrelim.SetNDC()
            cmsPrelim.SetTextSize(0.038)
            cmsPrelim.SetLineWidth(1)
            cmsPrelim.SetTextFont(52)
            cmsPrelim.SetTextColor(ROOT.kBlack)
            cmsPrelim.SetTextAlign(11)
            cmsPrelim.SetName("cmsPrelim")
            cmsPrelim.DrawLatex(0.645,0.61,"Work in Progress")
            del cmsPrelim
            latexWJet = ROOT.TLatex()
            latexWJet.SetNDC()
            latexWJet.SetTextSize(0.035)
            latexWJet.SetLineWidth(2)
            latexWJet.SetTextFont(42)
            latexWJet.SetTextColor(ROOT.kBlack)
            latexWJet.SetTextAlign(11)
            latexWJet.SetName("latexWJet")
            if (MEgen == "Openloops"):
                if (process == "W1J"):
                    if (tablename == 'd31-x01-y01.merged' or tablename == 'd81-x01-y01.merged'):
                        wtitle = "W(#rightarrow#mu#nu) + 1j"
                    else:
                        wtitle = "W(#rightarrow#mu#nu) + 1j + X"
                elif (process == "W2J"):
                    wtitle = "W(#rightarrow#mu#nu) + 2j + X"
            latexWJet.DrawLatex(0.63,0.55, wtitle)
            if (doNP):
                MEgentitle = "NP Corr. Applied"
                latexWJet.SetTextFont(52)
                latexWJet.SetTextSize(0.025)
                latexWJet.DrawLatex(0.645, 0.495, MEgentitle)
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
                for i in range(numBins):
                    SFtemp = nonpertSFs[i]
                    xsecMEtemp = ((dataInME[("'aS=0.118'")]).values)[i]
                    xsecMEPDFtemp = ((dataInMEPDF[("'aS=0.118'")]).values)[i]
                    centralMEArray.append(xsecMEtemp * SFtemp)
                    centralMEPDFArray.append(xsecMEPDFtemp * SFtemp)

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
            
                #Do error calculations in quadrature
                #Note: errors for all alpha-s variations are currently taken to be the same
                for i in range(numBins):
                    binContentUnfTemp = ( hUnf.GetBinContent(i+binDataOffset+1) )
                    yErrUnfTemp = ( hUnf.GetBinError(i+binDataOffset+1) )

                    arrayMCToData1.append((hWJetsNLOFxFx.GetBinContent(i+binDataOffset+1))/binContentUnfTemp)
                    arrayMCToData2.append(centralMEPDFArray[i]/binContentUnfTemp)
                    arrayMCToData3.append(varArrayMEPDFlist[0][i]/binContentUnfTemp)
                    arrayMCToData4.append(varArrayMEPDFlist[numVarMEPDF-1][i]/binContentUnfTemp)

                    if (doErrors):
                        yErrLowMCRatio1.append(arrayMCToData1[i]*math.sqrt( (yErrUnfTemp/binContentUnfTemp)**2 + ( (hWJetsNLOFxFx.GetBinError(i+binDataOffset+1))/(hWJetsNLOFxFx.GetBinContent(i+binDataOffset+1)) )**2 ))
                        yErrUpMCRatio1.append(arrayMCToData1[i]*math.sqrt( (yErrUnfTemp/binContentUnfTemp)**2 + ( (hWJetsNLOFxFx.GetBinError(i+binDataOffset+1))/(hWJetsNLOFxFx.GetBinContent(i+binDataOffset+1)) )**2 ))
                        yErrLowMCRatio2.append(arrayMCToData2[i]*math.sqrt( (yErrUnfTemp/binContentUnfTemp)**2 + (yErrLow[i]/centralMEPDFArray[i])**2 ))
                        yErrUpMCRatio2.append(arrayMCToData2[i]*math.sqrt( (yErrUnfTemp/binContentUnfTemp)**2 + (yErrUp[i]/centralMEPDFArray[i])**2 ))
                        yErrLowMCRatio3.append(arrayMCToData3[i]*math.sqrt( (yErrUnfTemp/binContentUnfTemp)**2 + (yErrLow[i]/varArrayMEPDFlist[0][i])**2 ))
                        yErrUpMCRatio3.append(arrayMCToData3[i]*math.sqrt( (yErrUnfTemp/binContentUnfTemp)**2 + (yErrUp[i]/varArrayMEPDFlist[0][i])**2 ))
                        yErrLowMCRatio4.append(arrayMCToData4[i]*math.sqrt( (yErrUnfTemp/binContentUnfTemp)**2 + (yErrLow[i]/varArrayMEPDFlist[numVarMEPDF-1][i])**2 ))
                        yErrUpMCRatio4.append(arrayMCToData4[i]*math.sqrt( (yErrUnfTemp/binContentUnfTemp)**2 + (yErrUp[i]/varArrayMEPDFlist[numVarMEPDF-1][i])**2 ))

                if (doErrors):
                    grMCtoData1 = ROOT.TGraphAsymmErrors(numBins, binCenME, arrayMCToData1, xErrLow, xErrUp, yErrLowMCRatio1, yErrUpMCRatio1)
                    grMCtoData2 = ROOT.TGraphAsymmErrors(numBins, binCenME, arrayMCToData2, xErrLow, xErrUp, yErrLowMCRatio2, yErrUpMCRatio2)
                    grMCtoData3 = ROOT.TGraphAsymmErrors(numBins, binCenME, arrayMCToData3, xErrLow, xErrUp, yErrLowMCRatio3, yErrUpMCRatio3)
                    grMCtoData4 = ROOT.TGraphAsymmErrors(numBins, binCenME, arrayMCToData4, xErrLow, xErrUp, yErrLowMCRatio4, yErrUpMCRatio4)
                else:
                    grMCtoData1 = ROOT.TGraphAsymmErrors(numBins, binCenME, arrayMCToData1)
                    grMCtoData2 = ROOT.TGraphAsymmErrors(numBins, binCenME, arrayMCToData2)
                    grMCtoData3 = ROOT.TGraphAsymmErrors(numBins, binCenME, arrayMCToData3)
                    grMCtoData4 = ROOT.TGraphAsymmErrors(numBins, binCenME, arrayMCToData4)

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
            c1.Print(basedir+outDir+"aSVarXSec-"+process+"-"+order+"-"+tablename+"-"+pdfname+"-"+MEgen+isNP+".pdf")
            del c1
            del htemp, htemp1

print ('\nFinished!\n')