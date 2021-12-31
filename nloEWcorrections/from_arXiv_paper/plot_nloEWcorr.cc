{
  // ------------------
  #include <stdio.h>
  #include <iostream>
  #include <sstream>
  #include <string.h> 
  #include <math.h>
  #include "TGraph.h"
  #include "TAxis.h"
  #include "TMath.h"
  #include "TH1.h"
  // ------------------

  // fetch input .dat file
  TGraph2D *g1 = new TGraph2D("evj_VARIABLE_evj_pTV_kappa_EW.dat");
  g1->SetTitle("evj_pTV_kappa_EW");
  Double_t *xg1 = g1->GetX();
  Double_t *yg1 = g1->GetY();
  Double_t *zg1 = g1->GetZ();
  //int numPoints = g1->GetN();
  int numPoints = 42; // hard-coded
  std::cout << "numPoints = " << numPoints << std::endl;

  // for setting up final histogram
  //Double_t xBinsHisto[numPoints+1]; //array of bin edges for histogram
  Double_t xBinsHisto[42+1]; //array of bin edges for histogram, HARD-CODED BECAUSE THE COMPILER IS BEING MEAN

  for (int i(0); i < numPoints; i++){
      // print out contents
      std::cout << "bin " << i << ": " << "[" << xg1[i] << "," << yg1[i] << "]" << ": " << zg1[i] << std::endl;
      // set up binning for histogram
      xBinsHisto[i] = xg1[i];
      if (i == (numPoints-1)) xBinsHisto[i+1] = yg1[i]; // for the last upper bin edge
  }

  // using array of bin edges, set up new TH1
  TH1D *h_nloEW_corr = new TH1D("h_nloEW_corr", "h_nloEW_corr", numPoints, xBinsHisto);

  // fill TH1 with values for the NLO EW corrections
  std::cout << "\n --- NLO Electroweak Corrections --- " << std::endl;
  for (int i(1); i < numPoints+1; i++){
      double ewCorr = 1.0 + zg1[i-1]; // see Eq. 41 in paper
      h_nloEW_corr->SetBinContent(i, ewCorr);
      printf("Bin %i, (%.0f, %.0f): %.4f\n", i, h_nloEW_corr->GetBinLowEdge(i), h_nloEW_corr->GetXaxis()->GetBinUpEdge(i), h_nloEW_corr->GetBinContent(i));
  }

  // aesthetics
  h_nloEW_corr->SetTitle("nNLO EW Correction");
  h_nloEW_corr->GetXaxis()->SetTitle("p_{T}(W)");
  h_nloEW_corr->GetYaxis()->SetTitle("C_{EW}");
  h_nloEW_corr->GetYaxis()->SetRangeUser(0.25, 1.25);

  // write histogram to output file
  TFile *outputRootFile = new TFile("nloEWcorr.root", "RECREATE");
  outputRootFile->cd();
  h_nloEW_corr->Write("h_nloEW_corr");
  outputRootFile->Close();

  std::cout << "\nFinished!\n" << std::endl;
}
