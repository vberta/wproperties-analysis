#ifndef FAKERATE_H
#define FAKERATE_H


#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"
#include "TH1D.h"
#include "TH2D.h"
#include "TString.h"
#include "TMath.h"
#include "interface/module.hpp"
#include "interface/functions.hpp"

using RNode = ROOT::RDF::RNode;

class fakeRate : public Module {

 private:

  std::vector<ROOT::RDF::RResultPtr<TH1D>> _h1List;
  std::vector<ROOT::RDF::RResultPtr<TH2D>> _h2List;
  std::vector<ROOT::RDF::RResultPtr<TH3D>> _h3List;

    // groups of histos
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> _h1Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> _h2Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> _h3Group;

  TFile *_SF;

  TH2F *_hfake_offset;
  TH2F *_hfake_slope;
  TH2F *_hprompt_offset;
  TH2F *_hprompt_slope;
  TH2F *_hprompt_2deg;

public:
  fakeRate(TFile *SF)
  {
    _SF = SF;
    _hfake_offset = (TH2F *)_SF->Get("fake_offset");
    _hfake_slope = (TH2F *) _SF->Get("fake_slope");
    _hprompt_offset = (TH2F *)_SF->Get("prompt_offset");
    _hprompt_slope = (TH2F *)_SF->Get("prompt_slope");
    _hprompt_2deg = (TH2F *)_SF->Get("prompt_2deg");
   }

  RNode run(RNode) override;
  std::vector<ROOT::RDF::RResultPtr<TH1D>> getTH1() override;
  std::vector<ROOT::RDF::RResultPtr<TH2D>> getTH2() override;
  std::vector<ROOT::RDF::RResultPtr<TH3D>> getTH3() override;

  std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> getGroupTH1() override;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> getGroupTH2() override;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> getGroupTH3() override;
  
  void reset() override;

};

#endif
