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
from scipy.optimize import minimize
from scipy import linalg
import ROOT
#############################################################
'''
...comments...
'''
#############################################################
### R21 (list num first, then denom)
numerator = 'W2J'
denominator = 'W1J'
tablenames = [ ['d57-x01-y01.merged','d56-x01-y01.merged'] ]
variables = [ ["LepPtPlusLeadingJetAK8Pt_Zinc2jet_TUnfold", "LepPtPlusLeadingJetAK8Pt_Zinc1jet_TUnfold"] ]
## --
#pdfnames = ['CT10nlo', 'CT14nlo', 'NNPDF23_nlo', 'NNPDF30_nlo', 'NNPDF31_nnlo']
pdfnames = ['CT14nlo']
## also consider... NNPDF31_nlo, ABMP16_5_nlo, HERAPDF20_NLO, MMHT2014nlo68cl
## --
#doNP = True
doNP = False
## --
# doTheoryErrs = True
doTheoryErrs = False
## --

# ----------------------------------------------
# -- KEEP TRUE UNTIL WE ARE READY TO UNBLIND --
doBlinding = True
# ----------------------------------------------

#############################################################
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

        ############################################################################################
        ##
        ## -- Load all necessary files, distributions, corrections --
        ##


        ## -----------------------------------------------------------------------
        ## Load csv files for FastNLO xsecs, ROOT file for unfolded distributions
        ## -----------------------------------------------------------------------

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
#        fileNameRatio = ("UnfoldedFilesRatio_2016/SMu_RATIO_"+variableNum+"_TO_"+variableDenom+"_JetPtMin_30_JetEtaMax_24_MGPYTHIA6_.root")
        print ("\nOpening file: "+fileNameRatio)
        fRatio = ROOT.TFile.Open(fileNameRatio, "READ")

        ## Remember differences in number of leading bins between unfolded and FastNLO distributions
        if ((numerator == 'W2J') and (denominator == 'W1J')):
            if (tablename[0] == 'd57-x01-y01.merged' and tablename[1] == 'd56-x01-y01.merged'):
                binDataOffset = 3

        print ("\n===========================================================================")
        print ("\nDoing variables: "+str(variableNum)+" & "+str(variableDenom))
        print ("Number of ME+PDF variations: "+str(int(numVarMEPDF)))
        print ("Number of bins in histogram: "+str(int(numBins)))


        ## -----------------------------------------------------------------------
        ## Get all corrections to FastNLO fixed order xsecs
        ## -----------------------------------------------------------------------

        ## Non-perturbative corrections
        if not (doNP):
            isNP = ""
            nonpertSFs = np.ones(numBins)
        else:
            print ("\n~~~ Adding non-perturbative corrections! ~~~")
            isNP = "-NPapplied"
            nonpertSFs = []
            if (tablename[0] == 'd57-x01-y01.merged' and tablename[1] == 'd56-x01-y01.merged'): 
                nonpertSFnum = [1.077566633105699, 0.9977636710165873, 0.9841403236031283, 0.980882310651964, 0.9801803073066212]
                nonpertSFdenom = [1.0669975256706226, 1.0180740407938955, 1.003429262670792, 0.9975915151870831, 0.9954401505789361]
            for i in range(int(numBins)):
                nonpertSFs.append(nonpertSFnum[i]/nonpertSFdenom[i])
            print("\nApplying non-pertrubative corrections:\n"+str(nonpertSFs))

        ## NLO electroweak corrections
        ## ...TBD...


        ## -----------------------------------------------------------------------
        ## Get xsec ratio distributions, error information
        ## -----------------------------------------------------------------------

        ## Get unfolded ratio (data) 
        hUnfRatio = fRatio.Get("UnfXSecRatio_Central")
        hUnfRatio.SetLineColor(ROOT.kBlack)
        hUnfRatio.SetLineWidth(3)
        hUnfRatio.SetMarkerColor(ROOT.kBlack)

        ## Get NLO FxFx signal MC ratio (used for blinding!)
        # hSignalMCRatio = fRatio.Get("GenSignalXSecRatio_NLOFxFx")
        hSignalMCRatio = fRatio.Get("GenSignalXSecRatio_NLOFxFx_InclSample")
        hSignalMCRatio.SetLineColor(ROOT.kOrange)
        hSignalMCRatio.SetLineWidth(3)
        hSignalMCRatio.SetMarkerColor(ROOT.kOrange)

        ## Get experimental uncertainty covariance matrices
        hDataStatCovMatrix = fRatio.Get("CovDataStat") # statistical error
        hExpCovMatrix = fRatio.Get("CovTotSyst")       # systematic error (all sources)
        # hExpCovMatrix = fRatio.Get("CovJES") # TEST

        ## Get FastNLO xsecs, take ratios (theory)
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
        print("")


        ## NOTE: COME BACK TO THIS LATER!!!
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




        ############################################################################################
        ##
        ## -- Compute Chi-2 values --
        ##


        ## -----------------------------------------------------------------------
        ## Add all covariance matrices together into one object, invert matrix
        ## -----------------------------------------------------------------------
        # https://docs.scipy.org/doc/scipy/reference/tutorial/linalg.html
        # https://numpy.org/devdocs/reference/generated/numpy.ndarray.html#numpy.ndarray
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.inv.html#scipy.linalg.inv

        hTotCovMatrix = hDataStatCovMatrix.Clone()
        hTotCovMatrix.Add(hExpCovMatrix)
        # add here all of the theory error covariance matrices...

        # first read these values into a 2d python list, then convert to a 2d numpy array
        # https://stackoverflow.com/questions/7717380/how-to-convert-2d-list-to-2d-numpy-array
        covMatrixList = []

        for i in range(int(numBins)):
            tmplist = []
            for j in range(int(numBins)):
                tmplist.append( hTotCovMatrix.GetBinContent( i+1+binDataOffset, j+1+binDataOffset) )
            covMatrixList.append(tmplist)

        covMatrix = np.array(covMatrixList)
        print("covMatrix = \n"+str(covMatrix))

        # A square matrix that is not invertible is called singular or degenerate. 
        # A square matrix is singular if and only if its determinant is zero.
        covMatrix_det = linalg.det(covMatrix)
        print("determinant of covMatrix = "+str(covMatrix_det)) 

        covMatrixInv = linalg.inv(covMatrix)
        print("\ncovMatrixInv = \n"+str(covMatrixInv))
        
        identity = covMatrix.dot(covMatrixInv)
        print("\nidentity matrix check! \n"+str(identity))

        ## -----------------------------------------------------------------------
        ## Do a loop over all alpha-s ratio distributions; 
        ## for each of these distributions, do a double-loop to compute chi-2
        ## Store chi-2 values in a list
        ## -----------------------------------------------------------------------

        chi2values = array('d')
        chi2valuesList = []

        for i, alphas in enumerate(alphasvalsMEPDF):
            dataTheoryDiffList = []
            for j in range(int(numBins)):

                # -----------------------
                # Blinding of the data --
                if (doBlinding):
                    dataTmp = hSignalMCRatio.GetBinContent(j+1+binDataOffset)
                else:
                    dataTmp = hUnfRatio.GetBinContent(j+1+binDataOffset)
                # -----------------------

                theoryTmp = varArrayMEPDFlist[i][j]
                dataTheoryDiffList.append(dataTmp - theoryTmp)
                # print(str(round(alphas,3))+": "+str(dataTmp - theoryTmp))

            dataTheoryDiff = np.array(dataTheoryDiffList)
            dataTheoryDiffTranspose = dataTheoryDiff.T

            chi2 = dataTheoryDiffTranspose.dot(covMatrixInv.dot(dataTheoryDiff))
            chi2values.append(chi2)
            chi2valuesList.append(chi2)

        print("\nChi-2 Values: \n"+str(chi2values))


        ############################################################################################
        ##
        ## -- Plot Chi-2 values, fit points with 2nd-order polynomial, extract alpha-s(Mz) --
        ##
        
        ## -----------------------------------------------------------------------
        ## Set up TCanvas and TH1
        ## -----------------------------------------------------------------------

        # c1 = ROOT.TCanvas('can_', 'can_', 500, 500)
        c1 = ROOT.TCanvas('can_', 'can_', 550, 450)
        c1.Update()
        c1.Draw()

        xmin = alphasvalsMEPDF[0]-0.03
        xmax = alphasvalsMEPDF[numVarMEPDF-1]+0.03
        ymin = min(chi2values)*0.95
        ymax = max(chi2values)*1.07

        htemp = ROOT.TH1D('htemp_', "htemp_", 100, xmin, xmax)
        htemp.SetStats(0)
        htemp.GetXaxis().SetTitle("#alpha_{s}(M_{Z})")
        htemp.GetXaxis().SetTitleOffset(1.2)
        htemp.GetYaxis().SetTitle("#chi^{2}")
        htemp.GetYaxis().SetTitleOffset(1.3)
        htemp.GetYaxis().SetRangeUser(ymin, ymax)
        htemp.SetTitle("")
        htemp.Draw()

        leg = ROOT.TLegend(0.34,0.775,0.9,0.9)

        ## -----------------------------------------------------------------------
        ## Plot chi-2 values vs alpha-s(Mz) values
        ## -----------------------------------------------------------------------

        # Get array of alpha-s values (the different variations)
        # Not sure if this exists previously
        alphaSvalues = array('d')
        alphaSvaluesList = []
        for i, alphas in enumerate(alphasvalsMEPDF):
            alphaSvalues.append(alphas)
            alphaSvaluesList.append(alphas)

        # Make the TGraph to plot the points
        chi2graph = ROOT.TGraph(numVarMEPDF, alphaSvalues, chi2values)
        chi2graph.SetLineColorAlpha(2, 1.)
        chi2graph.SetLineWidth(2)
        chi2graph.SetLineStyle(1)
        chi2graph.SetMarkerColor(2)
        chi2graph.SetMarkerStyle(20)
        chi2graph.SetMarkerSize(0.7)
        chi2graph.Draw('P same')
        leg.AddEntry(chi2graph, "Chi-2 Values", "p")

        ## -----------------------------------------------------------------------
        ## Fit distribution with 2nd order polynomial
        ## https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
        ## -----------------------------------------------------------------------

        def func(x, c1, c2, c3):
            return c1 + c2*(x) + c3*(x*x)
        popt, pcov = curve_fit(func, alphaSvaluesList, chi2valuesList, bounds=((-np.inf, -np.inf, -np.inf), (np.inf, np.inf, np.inf)))
        print("\nResults of fit --")
        print("Constants of fit: "+str(popt))




        # X is a <class 'numpy.ndarray'>
    #    X = 0.1 * np.arange(10)
    #    print("X = "+str(X))
    #    print("NEW Values from the fit:\n"+str( list(func(X, *popt)) )) # THIS WORKS, FIGURE OUT WHY THE ONE BELOW DOESN'T
    #    print ("alphaSvaluesList = "+str(type(np.array(alphaSvaluesList))))

        # !!!
        print("Values from the fit:\n"+str( list(func(np.array(alphaSvalues), *popt)) )) # NOW IT WORKS! (now have to clean up some of the code below... because we can just set fit_values equal to this line now instead of having to loop over every element!!!!!)

        fit_values = array('d')

        # just try this out... to get an arbitrarily large range
        temp_extended_range = np.arange(alphasvalsMEPDF[0]-0.005, alphasvalsMEPDF[numVarMEPDF-1]+0.02, 0.001).tolist()

        temp_extended_range_Array = array('d')
        for i in range(len(temp_extended_range)):
            temp_extended_range_Array.append(temp_extended_range[i])

#        for i in range(len(alphaSvaluesList)): # normal one
        for i in range(len(temp_extended_range)): # test
#            fit_values.append( func(alphaSvaluesList[i], *popt) ) # normal one
            fit_values.append( func(temp_extended_range[i], *popt) ) # test
        print("\nValues from the fit:\n"+str(fit_values))





        # Draw the fit
#        chi2Fit = ROOT.TGraph(numVarMEPDF, alphaSvalues, fit_values) # normal one
        chi2Fit = ROOT.TGraph(len(temp_extended_range), temp_extended_range_Array, fit_values) # test
        chi2Fit.SetLineColorAlpha(2, 1.)
        chi2Fit.SetLineWidth(2)
        chi2Fit.SetLineStyle(1)
        chi2Fit.SetMarkerColor(2)
        chi2Fit.SetMarkerStyle(20)
        chi2Fit.SetMarkerSize(1.)
        chi2Fit.Draw('L same')
        leg.AddEntry(chi2Fit, "Chi-2 Fit", "l")


        ## -----------------------------------------------------------------------
        ## Extract alpha-s(Mz) from minimum of fit, errors using (chi-2)+1
        ## https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
        ## -----------------------------------------------------------------------


        print("\n")

        # get minimum value from chi-2 fit
        x_guess = [0.118]
        chi2min = minimize(func, x_guess, args=(popt[0], popt[1], popt[2]), method='Nelder-Mead', tol=1e-6)
        if(chi2min.success):
            print("Minimization successful! "+str(chi2min.message))
        else:
            print("Minimization failed! "+str(chi2min.message))
        alphaSMin = chi2min.x
        print("alpha-s min. value = "+str(alphaSMin))
        print("chi-2 min. = "+str(func(alphaSMin, *popt)))

        # draw minimum point on plot
        fitMin = ROOT.TGraph(1, alphaSMin, func(alphaSMin, *popt))
        fitMin.SetLineColorAlpha(4, 1.)
        fitMin.SetLineWidth(2)
        fitMin.SetLineStyle(1)
        fitMin.SetMarkerColor(4)
        fitMin.SetMarkerStyle(47)
        fitMin.SetMarkerSize(1.5)
        fitMin.Draw('P same')
        leg.AddEntry(chi2graph, "Minimum of Fit", "p")

        # now do errors: find x-values such that we get (chi-2_min + 1)...
        chi2minAdd1 = func(alphaSMin, *popt) + 1.0

        # simply solving using the quadratic formula
        const_a = popt[2]
        const_b = popt[1]
        const_c = popt[0] - chi2minAdd1
        sol1 = ( -1.*const_b + math.sqrt(const_b**2. - 4.*const_a*const_c) )/(2*const_a)
        sol2 = ( -1.*const_b - math.sqrt(const_b**2. - 4.*const_a*const_c) )/(2*const_a)
        print("sol1 = "+str(sol1))
        print("sol2 = "+str(sol2))

        alphaSMinErrPlus = sol1 - alphaSMin
        alphaSMinErrMinus = alphaSMin - sol2

        # print final result
        print("\n\n                    ---------------------------------------------------------------- \n")
        print("                          alpha_S = "+str(alphaSMin)+" + "+str(alphaSMinErrPlus)+" - "+str(alphaSMinErrMinus))
        if(doBlinding):
            print("\n                                                BLINDED!")
        else:
            print("\n                                              UN-BLINDED!")
        print("\n                    ---------------------------------------------------------------- \n")



        # draw the error points for the chi2_min+1,,,
        # actually draw a horizontal line above the min value point to where it intersects the parabola at chi2min+1
        # use a TLine
















        ## -----------------------------------------------------------------------
        ## Draw legend, then final result on plot using TLatex object
        ## -----------------------------------------------------------------------
        
#        leg.Draw("same")

        procLatex = ROOT.TLatex()
        procLatex.SetNDC()
        procLatex.SetTextSize(0.025)
        procLatex.SetLineWidth(2)
        procLatex.SetTextFont(42)
        procLatex.SetTextColor(ROOT.kBlack)
        procLatex.SetTextAlign(11)
        procLatex.SetName("procLatex")
        procLatex.DrawLatex(0.63,0.89-0.04, MEgen+"+Sherpa, NLO QCD")
        procLatex.DrawLatex(0.69,0.89-0.08, pdfname+" PDF set")
        if (numerator == "W2J" and denominator == "W1J"):
            wtitle = "R_{21} = #frac{W(#rightarrow#mu#nu) + 2j + X}{W(#rightarrow#mu#nu) + 1j + X}"
#        procLatex.DrawLatex(0.66,0.89-0.16, wtitle)

        if (doBlinding):
            blindedLatex = ROOT.TLatex()
            blindedLatex.SetNDC()
            blindedLatex.SetTextSize(0.038)
            blindedLatex.SetLineWidth(1)
            blindedLatex.SetTextFont(52)
            blindedLatex.SetTextColor(ROOT.kBlack)
            blindedLatex.SetTextAlign(11)
            blindedLatex.SetName("blindedLatex")
            blindedLatex.DrawLatex(0.45,0.65, "Blinded")

        # draw final alpha-s result on plot
        # ...

        
        ############################################################################################

        print("")
        c1.Update()
        c1.Print(basedir+outDir+"chi2Dist-"+numerator+"-"+denominator+"-"+tablename[0]+"-"+tablename[1]+"-"+pdfname+isNP+".pdf")
        del c1
        del htemp

print ('\nFinished!\n')        
