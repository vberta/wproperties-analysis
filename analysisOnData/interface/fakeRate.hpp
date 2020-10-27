#ifndef FAKERATE_H
#define FAKERATE_H

#include "module.hpp"

class fakeRate : public Module
{

private:
  TFile *_SF;

  std::map<std::string, TH2D *> _FR;

  std::vector<std::string> _variations = {"Nominal_", "WHSF_WHSFSyst0Up", "WHSF_WHSFSyst1Up",
                                         "WHSF_WHSFSyst2Up", "WHSF_WHSFSystFlatUp", "WHSF_WHSFSyst0Down", "WHSF_WHSFSyst1Down",
                                         "WHSF_WHSFSyst2Down", "WHSF_WHSFSystFlatDown", "LHEScaleWeight_LHEScaleWeight_muR0p5_muF0p5",
                                         "LHEScaleWeight_LHEScaleWeight_muR0p5_muF1p0", "LHEScaleWeight_LHEScaleWeight_muR1p0_muF0p5",
                                         "LHEScaleWeight_LHEScaleWeight_muR1p0_muF2p0", "LHEScaleWeight_LHEScaleWeight_muR2p0_muF1p0",
                                         "LHEScaleWeight_LHEScaleWeight_muR2p0_muF2p0", "ptScale_correctedUp", "ptScale_correctedDown",
					  "jme_jerUp", "jme_jerDown", "jme_jesTotalUp", "jme_jesTotalDown", "jme_unclustEnUp", "jme_unclustEnDown"};
  //, "PrefireWeight_PrefireWeightUp", "PrefireWeight_PrefireWeightDown"};

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
};

#endif
