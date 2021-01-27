// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/VetoedFinalState.hh"
#include "Rivet/Projections/WFinder.hh"
#include "Rivet/AnalysisLoader.hh"
#include "Rivet/AnalysisInfo.hh"
#include "Rivet/Tools/RivetYODA.hh"
#include "mcgrid/mcgrid.hh"
#include <iostream>

namespace Rivet {

  class MCgrid_CMS_2018_WJetsAlphaS_1j_OL : public Analysis {
  public:

    MCgrid_CMS_2018_WJetsAlphaS_1j_OL()
      : Analysis("MCgrid_CMS_2018_WJetsAlphaS_1j_OL")
    {    }

  public:

    void init() {

      // Initialise and register projections
      FinalState fs;
      WFinder wfinder_mu(fs, Cuts::abseta < 2.4 && Cuts::pT > 0*GeV, PID::MUON, 0*GeV, 1000000*GeV, 0*GeV, 0.1, WFinder::CLUSTERNODECAY, WFinder::TRACK, WFinder::TRANSMASS);
      addProjection(wfinder_mu, "WFinder_mu");

      // Define veto FS
      VetoedFinalState vfs;
      vfs.addVetoOnThisFinalState(wfinder_mu);
      vfs.addVetoPairId(PID::MUON);
      vfs.vetoNeutrinos();

      // Grab jet collections from this lepton-cleaned FinalState object
      // AK4 jets
      FastJets fastjets(vfs, FastJets::ANTIKT, 0.4);
      addProjection(fastjets, "Jets");
      // AK8 jets
      FastJets fastjetsAK8(vfs, FastJets::ANTIKT, 0.8);
      addProjection(fastjetsAK8, "JetsAK8");

      //AK4 jets
      _hist_Mult_exc          = bookHisto1D("d01-x01-y01");
      _hist_JetPt_1j          = bookHisto1D("d02-x01-y01");
      _hist_LepPtJetPt_1j     = bookHisto1D("d06-x01-y01");
      _hist_WPt_1j            = bookHisto1D("d16-x01-y01");
      _hist_WPtJetPt_1j       = bookHisto1D("d20-x01-y01");
      //AK4 jet exclusive dist.
      _hist_JetPt_Exc_1j      = bookHisto1D("d27-x01-y01");
      _hist_LepPtJetPt_Exc_1j = bookHisto1D("d31-x01-y01");

      //AK8 jets
      _hist_Mult_exc_AK8          = bookHisto1D("d51-x01-y01");
      _hist_JetPt_1j_AK8          = bookHisto1D("d52-x01-y01");
      _hist_LepPtJetPt_1j_AK8     = bookHisto1D("d56-x01-y01");
      _hist_WPt_1j_AK8            = bookHisto1D("d66-x01-y01");
      _hist_WPtJetPt_1j_AK8       = bookHisto1D("d70-x01-y01");
      //AK8 jet exclusive dist.
      _hist_JetPt_Exc_1j_AK8      = bookHisto1D("d77-x01-y01");
      _hist_LepPtJetPt_Exc_1j_AK8 = bookHisto1D("d81-x01-y01");


#if USE_FNLO
      const std::string subproc_config_fnlo_file("basic.str");
      MCgrid::subprocessConfig subproc_config_fnlo(subproc_config_fnlo_file, MCgrid::BEAM_PROTON, MCgrid::BEAM_PROTON);
      MCgrid::fastnloGridArch arch_fnlo(25, 10, "Lagrange", "Lagrange", "sqrtlog10", "loglog025");
      MCgrid::fastnloConfig config_fnlo(1, subproc_config_fnlo, arch_fnlo, 13000.0);

      // //AK4 grids
      // _fnlo_JetPt_1j          = MCgrid::bookGrid(_hist_JetPt_1j, histoDir(), config_fnlo);
      // _fnlo_LepPtJetPt_1j     = MCgrid::bookGrid(_hist_LepPtJetPt_1j, histoDir(), config_fnlo);
      // _fnlo_WPt_1j            = MCgrid::bookGrid(_hist_WPt_1j, histoDir(), config_fnlo);
      // _fnlo_WPtJetPt_1j       = MCgrid::bookGrid(_hist_WPtJetPt_1j, histoDir(), config_fnlo);
      // //AK4 exclusive jet
      // _fnlo_JetPt_Exc_1j      = MCgrid::bookGrid(_hist_JetPt_Exc_1j, histoDir(), config_fnlo);
      // _fnlo_LepPtJetPt_Exc_1j = MCgrid::bookGrid(_hist_LepPtJetPt_Exc_1j, histoDir(), config_fnlo);
     
      //AK8 grids
      // _fnlo_JetPt_1j_AK8          = MCgrid::bookGrid(_hist_JetPt_1j_AK8, histoDir(), config_fnlo);
      _fnlo_LepPtJetPt_1j_AK8     = MCgrid::bookGrid(_hist_LepPtJetPt_1j_AK8, histoDir(), config_fnlo);
      // _fnlo_WPt_1j_AK8            = MCgrid::bookGrid(_hist_WPt_1j_AK8, histoDir(), config_fnlo);
      // _fnlo_WPtJetPt_1j_AK8       = MCgrid::bookGrid(_hist_WPtJetPt_1j_AK8, histoDir(), config_fnlo);
      //AK8 exclusive jet
      // _fnlo_JetPt_Exc_1j_AK8      = MCgrid::bookGrid(_hist_JetPt_Exc_1j_AK8, histoDir(), config_fnlo);
      _fnlo_LepPtJetPt_Exc_1j_AK8 = MCgrid::bookGrid(_hist_LepPtJetPt_Exc_1j_AK8, histoDir(), config_fnlo);

#endif
        
    } //end void init

    /// Perform the per-event analysis
    void analyze(const Event& event) {
      MCgrid::PDFHandler::HandleEvent(event, histoDir());

      const double weight = event.weight();
      const WFinder& wfinder_mu = applyProjection<WFinder>(event, "WFinder_mu");

      if (wfinder_mu.bosons().size() != 1) {
        vetoEvent;
      }

      if (wfinder_mu.bosons().size() == 1) {

        const FourMomentum& wBoson = wfinder_mu.boson().momentum();
        double wBosonPt = wBoson.pT();

        const FourMomentum& lepton0 = wfinder_mu.constituentLepton().momentum();
        double WmT = wfinder_mu.mT();

        //W transverse mass cut
        if (WmT < 50.0*GeV) vetoEvent;

        double pt0 = lepton0.pT();
        double eta0 = lepton0.eta();

        //muon pT and eta cuts
        if ( (fabs(eta0) > 2.4) || (pt0 < 25.0*GeV) ) vetoEvent;

        // Obtain the jets (AK4 and AK8)
        vector<FourMomentum> finaljet_list;
        vector<FourMomentum> finaljet_list_AK8;

        // AK4 jets -----
        // loop over jets in an event, pushback in finaljet_list collection
        foreach (const Jet& j, applyProjection<FastJets>(event, "Jets").jetsByPt(30.0*GeV)) {
          const double jrap = j.momentum().rap();
          const double jpt = j.momentum().pT();
          //jet pT and dR(j,mu) cuts
          if ( (fabs(jrap) < 2.4) && (deltaR(lepton0, j.momentum()) > 0.4) ) {
            if (jpt > 30.0*GeV) {
              finaljet_list.push_back(j.momentum());
            }
          }
        } // end looping over jets

        // AK8 jets -----
        // loop over jets in an event, pushback in finaljet_list_AK8 collection
        foreach (const Jet& j, applyProjection<FastJets>(event, "JetsAK8").jetsByPt(200.0*GeV)) {
          const double jrap = j.momentum().rap();
          const double jpt = j.momentum().pT();
          //jet pT and dR(j,mu) cuts
          if ( (fabs(jrap) < 2.4) && (deltaR(lepton0, j.momentum()) > 0.8) ) {
            if (jpt > 200.0*GeV) {
              finaljet_list_AK8.push_back(j.momentum());
            }
          }
        } // end looping over jets
          

        //---------------------- FILL HISTOGRAMS ------------------

        // Exc jet multiplicity plots
        _hist_Mult_exc->fill(finaljet_list.size(), weight);
        _hist_Mult_exc_AK8->fill(finaljet_list_AK8.size(), weight);

        // AK4 histos/grids
        if(finaljet_list.size()>=1) {
          _hist_JetPt_1j->fill(finaljet_list[0].pT(), weight);
          _hist_LepPtJetPt_1j->fill(pt0+finaljet_list[0].pT(), weight);
          _hist_WPt_1j->fill(wBosonPt, weight);
          _hist_WPtJetPt_1j->fill(wBosonPt+finaljet_list[0].pT(), weight);
// #if USE_FNLO
//           _fnlo_JetPt_1j->fill(finaljet_list[0].pT(), event);
//           _fnlo_LepPtJetPt_1j->fill(pt0+finaljet_list[0].pT(), event);
//           _fnlo_WPt_1j->fill(wBosonPt, event);
//           _fnlo_WPtJetPt_1j->fill(wBosonPt+finaljet_list[0].pT(), event);
// #endif
        }
          // AK4 exclusive jet multiplicity dist.'s
          if(finaljet_list.size()==1) {
              _hist_JetPt_Exc_1j->fill(finaljet_list[0].pT(), weight);
              _hist_LepPtJetPt_Exc_1j->fill(pt0+finaljet_list[0].pT(), weight);
// #if USE_FNLO
//               _fnlo_JetPt_Exc_1j->fill(finaljet_list[0].pT(), event);
//               _fnlo_LepPtJetPt_Exc_1j->fill(pt0+finaljet_list[0].pT(), event);
// #endif
          }

        // AK8 histos/grids
        if(finaljet_list_AK8.size()>=1) {
          _hist_JetPt_1j_AK8->fill(finaljet_list_AK8[0].pT(), weight);
          _hist_LepPtJetPt_1j_AK8->fill(pt0+finaljet_list_AK8[0].pT(), weight);
          _hist_WPt_1j_AK8->fill(wBosonPt, weight);
          _hist_WPtJetPt_1j_AK8->fill(wBosonPt+finaljet_list_AK8[0].pT(), weight);
#if USE_FNLO
          // _fnlo_JetPt_1j_AK8->fill(finaljet_list_AK8[0].pT(), event);
          _fnlo_LepPtJetPt_1j_AK8->fill(pt0+finaljet_list_AK8[0].pT(), event);
          // _fnlo_WPt_1j_AK8->fill(wBosonPt, event);
          // _fnlo_WPtJetPt_1j_AK8->fill(wBosonPt+finaljet_list_AK8[0].pT(), event);
#endif
        }
          // AK8 exclusive jet multiplicity dist.'s
          if(finaljet_list_AK8.size()==1) {
              _hist_JetPt_Exc_1j_AK8->fill(finaljet_list_AK8[0].pT(), weight);
              _hist_LepPtJetPt_Exc_1j_AK8->fill(pt0+finaljet_list_AK8[0].pT(), weight);
#if USE_FNLO
              // _fnlo_JetPt_Exc_1j_AK8->fill(finaljet_list_AK8[0].pT(), event);
              _fnlo_LepPtJetPt_Exc_1j_AK8->fill(pt0+finaljet_list_AK8[0].pT(), event);
#endif
          }
          
      } // close the Wboson loop
    } // end void analyze


    /// Normalise histograms etc., after the run
    void finalize() {
      const double crossec = !std::isnan(crossSectionPerEvent()) ? crossSection() : 5198.46*picobarn; /// 5198.46 pb +- ( 59.3346 pb = 1.14 % )
      if (std::isnan(crossSectionPerEvent())){
        MSG_INFO("crossSectionPerEvent() is NaN, using " << crossec/picobarn << " pb");
      }

        // AK4 distributions
        scale(_hist_Mult_exc, crossec/picobarn/sumOfWeights());
        scale(_hist_JetPt_1j, crossec/picobarn/sumOfWeights());
        scale(_hist_LepPtJetPt_1j, crossec/picobarn/sumOfWeights());
        scale(_hist_WPt_1j, crossec/picobarn/sumOfWeights());
        scale(_hist_WPtJetPt_1j, crossec/picobarn/sumOfWeights());
        // AK4 exclusive jet distributions
        scale(_hist_JetPt_Exc_1j, crossec/picobarn/sumOfWeights());
        scale(_hist_LepPtJetPt_Exc_1j, crossec/picobarn/sumOfWeights());
        
        // AK8 distributions
        scale(_hist_Mult_exc_AK8, crossec/picobarn/sumOfWeights());
        scale(_hist_JetPt_1j_AK8, crossec/picobarn/sumOfWeights());
        scale(_hist_LepPtJetPt_1j_AK8, crossec/picobarn/sumOfWeights());
        scale(_hist_WPt_1j_AK8, crossec/picobarn/sumOfWeights());
        scale(_hist_WPtJetPt_1j_AK8, crossec/picobarn/sumOfWeights());
        // AK8 exclusive jet distributions
        scale(_hist_JetPt_Exc_1j_AK8, crossec/picobarn/sumOfWeights());
        scale(_hist_LepPtJetPt_Exc_1j_AK8, crossec/picobarn/sumOfWeights());

#if USE_FNLO
        // //AK4 grids
        // _fnlo_JetPt_1j->scale(crossec/picobarn/sumOfWeights());
        // _fnlo_JetPt_1j->exportgrid();
        // _fnlo_LepPtJetPt_1j->scale(crossec/picobarn/sumOfWeights());
        // _fnlo_LepPtJetPt_1j->exportgrid();
        // _fnlo_WPt_1j->scale(crossec/picobarn/sumOfWeights());
        // _fnlo_WPt_1j->exportgrid();
        // _fnlo_WPtJetPt_1j->scale(crossec/picobarn/sumOfWeights());
        // _fnlo_WPtJetPt_1j->exportgrid();
        // //AK4 exclusive jet mult. grids
        // _fnlo_JetPt_Exc_1j->scale(crossec/picobarn/sumOfWeights());
        // _fnlo_JetPt_Exc_1j->exportgrid();
        // _fnlo_LepPtJetPt_Exc_1j->scale(crossec/picobarn/sumOfWeights());
        // _fnlo_LepPtJetPt_Exc_1j->exportgrid();
        
        //AK8 grids
        // _fnlo_JetPt_1j_AK8->scale(crossec/picobarn/sumOfWeights());
        // _fnlo_JetPt_1j_AK8->exportgrid();
        _fnlo_LepPtJetPt_1j_AK8->scale(crossec/picobarn/sumOfWeights());
        _fnlo_LepPtJetPt_1j_AK8->exportgrid();
        // _fnlo_WPt_1j_AK8->scale(crossec/picobarn/sumOfWeights());
        // _fnlo_WPt_1j_AK8->exportgrid();
        // _fnlo_WPtJetPt_1j_AK8->scale(crossec/picobarn/sumOfWeights());
        // _fnlo_WPtJetPt_1j_AK8->exportgrid();
        //AK8 exclusive jet mult. grids
        // _fnlo_JetPt_Exc_1j_AK8->scale(crossec/picobarn/sumOfWeights());
        // _fnlo_JetPt_Exc_1j_AK8->exportgrid();
        _fnlo_LepPtJetPt_Exc_1j_AK8->scale(crossec/picobarn/sumOfWeights());
        _fnlo_LepPtJetPt_Exc_1j_AK8->exportgrid();
#endif

        MCgrid::PDFHandler::CheckOutAnalysis(histoDir());
    } //end void finalize

  private:
      //AK4 histos
      Histo1DPtr _hist_Mult_exc;
      Histo1DPtr _hist_JetPt_1j;
      Histo1DPtr _hist_LepPtJetPt_1j;
      Histo1DPtr _hist_WPt_1j;
      Histo1DPtr _hist_WPtJetPt_1j;
      //AK4 exclusive jet mult. histos
      Histo1DPtr _hist_JetPt_Exc_1j;
      Histo1DPtr _hist_LepPtJetPt_Exc_1j;

      //AK8 histos
      Histo1DPtr _hist_Mult_exc_AK8;
      Histo1DPtr _hist_JetPt_1j_AK8;
      Histo1DPtr _hist_LepPtJetPt_1j_AK8;
      Histo1DPtr _hist_WPt_1j_AK8;
      Histo1DPtr _hist_WPtJetPt_1j_AK8;
      //AK8 exclusive jet mult. histos
      Histo1DPtr _hist_JetPt_Exc_1j_AK8;
      Histo1DPtr _hist_LepPtJetPt_Exc_1j_AK8;

#if USE_FNLO
      // //AK4 grids
      // MCgrid::gridPtr _fnlo_JetPt_1j;
      // MCgrid::gridPtr _fnlo_LepPtJetPt_1j;
      // MCgrid::gridPtr _fnlo_WPt_1j;
      // MCgrid::gridPtr _fnlo_WPtJetPt_1j;
      // //AK4 exclusive jet mult. grids
      // MCgrid::gridPtr _fnlo_JetPt_Exc_1j;
      // MCgrid::gridPtr _fnlo_LepPtJetPt_Exc_1j;
      
      //AK8 grids
      // MCgrid::gridPtr _fnlo_JetPt_1j_AK8;
      MCgrid::gridPtr _fnlo_LepPtJetPt_1j_AK8;
      // MCgrid::gridPtr _fnlo_WPt_1j_AK8;
      // MCgrid::gridPtr _fnlo_WPtJetPt_1j_AK8;
      //AK8 exclusive jet mult. grids
      // MCgrid::gridPtr _fnlo_JetPt_Exc_1j_AK8;
      MCgrid::gridPtr _fnlo_LepPtJetPt_Exc_1j_AK8;
#endif

  }; //end class


  // The hook for the plugin system
  DECLARE_RIVET_PLUGIN(MCgrid_CMS_2018_WJetsAlphaS_1j_OL);


} //end Rivet