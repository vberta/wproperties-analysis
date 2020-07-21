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

class fakeRate : public Module
{

private:
  std::vector<ROOT::RDF::RResultPtr<TH1D>> _h1List;
  std::vector<ROOT::RDF::RResultPtr<TH2D>> _h2List;
  std::vector<ROOT::RDF::RResultPtr<TH3D>> _h3List;

  // groups of histos
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> _h1Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> _h2Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> _h3Group;

  TFile *_SF;

  std::map<std::string, TH2D *> _FR;

  std::vector<std::string> _variations = {"Nominal_", "WHSFVars_WHSFSyst0Up", "WHSFVars_WHSFSyst1Up",
                                         "WHSFVars_WHSFSyst2Up", "WHSFVars_WHSFSystFlatUp", "WHSFVars_WHSFSyst0Down", "WHSFVars_WHSFSyst1Down",
                                         "WHSFVars_WHSFSyst2Down", "WHSFVars_WHSFSystFlatDown", "LHEScaleWeightVars_LHEScaleWeight_muR0p5_muF0p5",
                                         "LHEScaleWeightVars_LHEScaleWeight_muR0p5_muF1p0", "LHEScaleWeightVars_LHEScaleWeight_muR1p0_muF0p5",
                                         "LHEScaleWeightVars_LHEScaleWeight_muR1p0_muF2p0", "LHEScaleWeightVars_LHEScaleWeight_muR2p0_muF1p0",
                                         "LHEScaleWeightVars_LHEScaleWeight_muR2p0_muF2p0", "ptScaleVars_correctedUp", "ptScaleVars_correctedDown",
                                         "jmeVars_jerUp", "jmeVars_jerDown", "jmeVars_jesTotalUp", "jmeVars_jesTotalDown", "jmeVars_unclustEnUp", "jmeVars_unclustEnDown"};

public:
  fakeRate(TFile *SF)
  {
    _SF = SF;
    for (auto s : _variations)
    {
      _FR.insert(std::pair<std::string, TH2D *>("fake_offset_" + s, (TH2D *)_SF->Get(Form("%s/fake_offset",s.c_str()))));
      _FR.insert(std::pair<std::string, TH2D *>("fake_slope_" + s, (TH2D *)_SF->Get(Form("%s/fake_slope",s.c_str()))));
      _FR.insert(std::pair<std::string, TH2D *>("prompt_offset_" + s, (TH2D *)_SF->Get(Form("%s/prompt_offset",s.c_str()))));
      _FR.insert(std::pair<std::string, TH2D *>("prompt_slope_" + s, (TH2D *)_SF->Get(Form("%s/prompt_slope",s.c_str()))));
      _FR.insert(std::pair<std::string, TH2D *>("prompt_2deg_" + s, (TH2D *)_SF->Get(Form("%s/prompt_2deg",s.c_str()))));
    }
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
