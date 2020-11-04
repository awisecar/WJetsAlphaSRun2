#! /usr/bin/env python3
import os
import sys
import numpy as np
import pandas as pd
import math
from array import array
import ROOT
##################################################
processes =  ['W1J']
tablenames = ['d06-x01-y01.merged', 'd31-x01-y01.merged', 'd56-x01-y01.merged', 'd81-x01-y01.merged']
variables =  ["LeadingJetPt_2_Zinc1jet_R21", "LepPtPlusLeadingJetPt_2_Zinc1jet_R21", "ZPt_2_Zinc1jet", "ZPtPlusLeadingJetPt_2_Zinc1jet"]
#processes =  ['W2J']
#tablenames = ['d07-x01-y01.merged',  'd57-x01-y01.merged']
#variables =  ["LeadingJetPt_2_Zinc2jet_R21", "HTover2_2_Zinc2jet_R32"]
## --
#pdfnames = ['CT10nlo', 'CT14nlo', 'NNPDF23_nlo', 'NNPDF30_nlo', 'NNPDF31_nnlo']
pdfnames = ['CT14nlo']
## --
#doCutoff = True
doCutoff = False
## --
#doSyst = True
doSyst = False
systDir = "systFiles/"
##################################################
MEgen = "Openloops"
order = "NLO"
basedir = "./"+MEgen+"/"+order+"/"
outDir = ("plotsFastNLO/")
os.system(("mkdir -p ")+basedir+outDir)

ROOT.gStyle.SetLineStyleString(11,"10 10")
ROOT.gStyle.SetLegendTextSize(0.022)
#ROOT.gStyle.SetLegendTextSize(0.027)

print("\n---------------- Begin sensitivity study! ----------------")

for process in processes:
    for iTab, tablename in enumerate(tablenames):
        for pdfname in pdfnames:
            #########################################
            ## 1) Grab data
            
            csvInfileME = "aSVarME-"+pdfname+"-"+process+"-"+tablename+".csv"
            csvInfileMEPDF = "aSVarMEPDF-"+pdfname+"-"+process+"-"+tablename+".csv"
            
            ## Grab the alpha-s value for each dataseries to use as label
            # just ME var
            alphasNamesME = pd.read_csv(basedir+csvInfileME, nrows=1) #grabbing first row of diagonistic information
            alphasvalsME = alphasNamesME.values.tolist()[0][3:]
            numVarME = int( alphasNamesME.values.tolist()[0][2] ) #total number of alpha-s variations for ME
            print ("\nnumber of ME variations: "+str(int(numVarME)))
            # print ("ME variations: "+str(alphasvalsME))
            # ME and PDF var
            alphasNamesMEPDF = pd.read_csv(basedir+csvInfileMEPDF, nrows=1)
            alphasvalsMEPDF = alphasNamesMEPDF.values.tolist()[0][3:]
            numVarMEPDF = int( alphasNamesMEPDF.values.tolist()[0][2] )  #total number of alpha-s variations for ME+PDF
            print ("number of ME+PDF variations: "+str(int(numVarMEPDF)))
            # print ("ME+PDF variations: "+str(alphasvalsMEPDF))
            #num of bins should be the same for two different files
            numBins = int(alphasNamesME.values.tolist()[0][0])  #number of bins in the distribution
            print ("number of bins in histogram: "+str(numBins))
            
            ## Grab the data
            dataInME = pd.read_csv(basedir+csvInfileME, skiprows=[1]) #skip first row, but with keeping headers
            dataInMEPDF = pd.read_csv(basedir+csvInfileMEPDF, skiprows=[1])

            ##################################################
            ##

	        ## Get x-bins
            ## TGraph must take data as type array
            #values method converts from pandas series to numpy array
            binCenME = array('d')
            binCenMEPDF = array('d')
            for i in range(numBins):
                binCenME.append((dataInME["'BINCENTER'"].values)[i])
                binCenMEPDF.append(dataInMEPDF["'BINCENTER'"].values[i])
            if (binCenME == binCenMEPDF):
                print ("\nBinning of two distributions is equal: \n"+str(binCenME))
            else:
                print ("\nBinning of two distributions is not equal!")

            xtitle = tablename
            if (tablename == 'd06-x01-y01.merged' or tablename == 'd31-x01-y01.merged' or tablename == 'd56-x01-y01.merged' or tablename == 'd81-x01-y01.merged' or tablename == 'd07-x01-y01.merged' or tablename == 'd32-x01-y01.merged' or tablename == 'd57-x01-y01.merged' or tablename == 'd82-x01-y01.merged' or tablename == 'd08-x01-y01.merged'):
                xtitle = "Muon p_{T} + Leading Jet p_{T} [GeV]"
                boundLow = 90.

            varArrayMEPDFlist = []
            varArrayMElist = []

            for i, alphas in enumerate(alphasvalsMEPDF):
                varArray = array('d')
                for j in range(numBins):
                    varArray.append( ((dataInMEPDF[("'aS=")+str(round(alphas,3))+("'")]).values)[j] )
                varArrayMEPDFlist.append(varArray)

            for i, alphas in enumerate(alphasvalsME):
                varArray = array('d')
                for j in range(numBins):
                    varArray.append( ((dataInME[("'aS=")+str(round(alphas,3))+("'")]).values)[j] )
                varArrayMElist.append(varArray)

            centralMEPDFArray = array('d')
            centralMEArray = array('d')
            for i in range(numBins):
                centralMEPDFArray.append( ((dataInMEPDF[("'aS=0.118'")]).values)[i] )
                centralMEArray.append ( ((dataInME[("'aS=0.118'")]).values)[i] )

            ##################################################
            ## Now plot the ratio of each variation from central BH+Sherpa value
            c2 = ROOT.TCanvas('canVar2_'+process+'_'+tablename, 'canVar2_'+process+'_'+tablename, 500, 500)
            c2.Update()
            c2.Draw()

            xmin2 = binCenME[0]-3.
            xmax2 = binCenME[numBins-1]+3.
            ymin2 = 0.7
            ymax2 = 1.3

            print ("X-range from "+str(xmin2)+" to "+str(xmax2))
            print ("Y-range from "+str(ymin2)+" to "+str(ymax2))

            htemp2 = ROOT.TH1D('aS_'+process+'_'+tablename, "Ratio of MC Variations to "+MEgen+"+Sherpa "+order+" Central Dist.", 100, xmin2, xmax2)
            htemp2.SetStats(0)
            htemp2.GetXaxis().SetTitle(xtitle)
            htemp2.GetXaxis().SetTitleOffset(1.2)
            htemp2.GetYaxis().SetTitle('Ratio to Central MC #alpha_{s} Dist.')
            htemp2.GetYaxis().SetTitleOffset(1.3)
            htemp2.GetXaxis().SetRangeUser(xmin2, xmax2)
            htemp2.GetYaxis().SetRangeUser(ymin2, ymax2)
            htemp2.SetTitle("")
            htemp2.Draw()

            legLowY = 0.775
            if (doSyst):
                legLowY = 0.745
            leg2 = ROOT.TLegend(0.34,legLowY,0.9,0.9);

            procLatex = ROOT.TLatex()
            procLatex.SetNDC()
            procLatex.SetTextSize(0.025)
            procLatex.SetLineWidth(2)
            procLatex.SetTextFont(42)
            procLatex.SetTextColor(ROOT.kBlack)
            procLatex.SetTextAlign(11)
            procLatex.SetName("procLatex")
            if (process == "W1J"):
                if (tablename == 'd31-x01-y01.merged' or tablename == 'd81-x01-y01.merged'):
                    wtitle = "W(#rightarrow#mu#nu) + 1j"
                else:
                    wtitle = "W(#rightarrow#mu#nu) + 1j + X"
            elif (process == "W2J"):
                wtitle = "W(#rightarrow#mu#nu) + 2j + X"
            #top right
            # procLatex.DrawLatex(0.55,legLowY-0.04, MEgen+"+Sherpa, NLO QCD")
            # procLatex.DrawLatex(0.62,legLowY-0.08, wtitle)
            #bottom right
            procLatex.DrawLatex(0.55,legLowY-0.56, MEgen+"+Sherpa, NLO QCD")
            procLatex.DrawLatex(0.62,legLowY-0.6, wtitle)

            ## Keeping the graphs in a list allows us to draw multiple on canvas
            grMEPDFlist2 = []
            grMElist2 = []

            ##########################################
            ### Plot the ME variations
            print ("\n\n---> Doing ME ratios!")
            for i, alphas in enumerate(alphasvalsME):
                if ((round(alphas,3)) == 0.118): #don't want to redundantly plot the central variation
                    continue
                perdiffarray = array('d')
                for j in range(numBins):
                    perdiffarray.append(varArrayMElist[i][j]/centralMEArray[j])
                print ("~~~~~ Drawing ratio for alpha-s = "+str(round(alphas,3))+"!")
                # print ("Values for entry "+str(i)+": " +str(perdiffarray))
                ## Now draw the graph
                gr = ROOT.TGraph(numBins, binCenME, perdiffarray)
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
                if i==0:
                    leg2.AddEntry(gr, "ME Variation: "+pdfname+", #alpha_{s} = "+str(round(alphas,3)), "lp")
                elif i==(int(numVarME-1)):
                    leg2.AddEntry(gr, "ME Variation: "+pdfname+", #alpha_{s} = "+str(round(alphas,3)), "lp")
                gr.SetMarkerSize(0.5)
                gr.SetMarkerStyle(20)
                # gr.SetMarkerColor(2)
                grMElist2.append(gr)

            ### Draw graphs!
            for gr in grMElist2:
                # gr.Draw('C same')
                gr.Draw('CP same')


            ### Plot the ME+PDF variations
            print ("\n\n---> Doing ME+PDF ratio with PDF set "+pdfname+"!")
            for i, alphas in enumerate(alphasvalsMEPDF):
                if ((round(alphas,3)) == 0.118): #don't want to redundantly plot the central variation
                    continue
                perdiffarray = array('d')
                for j in range(numBins):
                    perdiffarray.append(varArrayMEPDFlist[i][j]/centralMEPDFArray[j])
                print ("~~~~~ Drawing MC ratio for alpha-s = "+str(round(alphas,3))+"!")
                # print ("Values for entry "+str(i)+": " +str(perdiffarray))
                ## Now draw the graph
                gr = ROOT.TGraph(numBins, binCenME, perdiffarray)
                gr.SetMarkerSize(0.7)
                if (i==0 or i==(numVarMEPDF-1)):
                    if (i==0):
                        gr.SetLineColorAlpha(2, 1.)
                        gr.SetMarkerColorAlpha(2, 1.)
                    else:
                        gr.SetLineColorAlpha(4, 1.)
                        gr.SetMarkerColorAlpha(4, 1.)
                    gr.SetLineWidth(2)
                    gr.SetLineStyle(7)
                else:
                    gr.SetLineColorAlpha(1, 0.5)
                    gr.SetMarkerColorAlpha(1, 0)
                    gr.SetLineWidth(1)
                    gr.SetLineStyle(11)
                if i==0:
                    leg2.AddEntry(gr, "ME+PDF Variation: "+pdfname+", #alpha_{s} = "+str(round(alphas,3)), "lp")
                elif i==(int(numVarMEPDF-1)):
                    leg2.AddEntry(gr, "ME+PDF Variation: "+pdfname+", #alpha_{s} = "+str(round(alphas,3)), "lp")
                gr.SetMarkerSize(0.5)
                gr.SetMarkerStyle(20)
                # gr.SetMarkerColor(4)
                grMEPDFlist2.append(gr)

            ### Draw graphs!
            for gr in grMEPDFlist2:
                # gr.Draw('C same')
                gr.Draw('CP same')


            if (doSyst):
                yErrLowSyst = array('d')
                yErrUpSyst = array('d')
                csvInfileSystUncert = "systUncert_"+variables[iTab]+".csv"
                dataInSystUncert = pd.read_csv(systDir+csvInfileSystUncert)
                for i in range(numBins):
                    yErrLowSyst.append( ((dataInSystUncert["'JESDown'"]).values)[i] )
                    yErrUpSyst.append( ((dataInSystUncert["'JESUp'"]).values)[i] )

                systArray = np.ones(numBins)
                xErrLow = np.zeros(numBins)
                xErrUp = np.zeros(numBins)
                grSyst = ROOT.TGraphAsymmErrors(numBins, binCenME, systArray, xErrLow, xErrUp, yErrLowSyst, yErrUpSyst)
                grSyst.SetLineWidth(2)
                grSyst.SetLineStyle(1)
                grSyst.SetMarkerStyle(20)
                grSyst.SetMarkerSize(0.)
                grSyst.Draw('PE same')
                leg2.AddEntry(grSyst , "Systematic Error", "lpe")

            line2 = ROOT.TLine(binCenME[0], 1., binCenME[numBins-1], 1.);
            line2.SetLineColor(ROOT.kBlack);
            line2.SetLineWidth(1);
            line2.Draw()

            ##########################################
            ## Find an average variation over a range
            if (doCutoff):
                if (boundLow < 30.):
                    boundLow = 100.
                boundUp = binCenME[numBins-1]
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
                ##Find average of all the MC ratio values for highest and lowest ME+PDF variations that are within the x-bounds
                for j in range(numBins):
                    if ( (binCenME[j] >= boundLow) and (binCenME[j] <= boundUp) ):
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

            ##########################################
            ## Finish

            leg2.Draw("same")

            isCutoff = ""
            if (doCutoff == True):
                isCutoff = "-cutoff"

            c2.Update()
            c2.Print(basedir+outDir+"SensitivityXSec-"+process+"-"+order+"-"+tablename+"-"+pdfname+"-"+MEgen+isCutoff+".pdf")
            del c2
            del htemp2

print ('\nFinished!\n')