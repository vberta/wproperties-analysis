#include "interface/fakeRate.hpp"
#include<iostream>
RNode fakeRate::run(RNode d)
{

  RNode d1(d);
  for (auto s : _variations)
  {
    std::cout << "Variation:" << s << std::endl;
    d1 = d1.Define(Form("fakeRate_%s", s.c_str()), [this, s](float pt, float eta, float charge, int vtype) {
      int binX = charge > 0. ? 1 : 2;
      int binY = _FR["fake_offset_" + s]->GetYaxis()->FindBin(eta);
      float f_offset = _FR["fake_offset_" + s]->GetBinContent(binX, binY);
      float f_slope = _FR["fake_slope_" + s]->GetBinContent(binX, binY);
      float p_offset = _FR["prompt_offset_" + s]->GetBinContent(binX, binY);
      float p_slope = _FR["prompt_slope_" + s]->GetBinContent(binX, binY);
      float p_2deg = _FR["prompt_2deg_" + s]->GetBinContent(binX, binY);
      float f = f_offset + (pt - 25.0) * f_slope;
      float p = p_offset * TMath::Erf(p_slope * pt + p_2deg);
      float res = vtype == 1 ? p * f / (p - f) : -(1 - p) * f / (p - f);
      
      return res;
    },
                   {"Mu1_pt", "Mu1_eta", "Mu1_charge", "Vtype"});
  }

  auto d2 = d1
                .Define("fakeRate_WHSFVars", [](float f1, float f2, float f3, float f4, float f5, float f6, float f7, float f8) {
                  ROOT::VecOps::RVec<float> fR;
                  fR.emplace_back(f1);
                  fR.emplace_back(f2);
                  fR.emplace_back(f3);
                  fR.emplace_back(f4);
                  fR.emplace_back(f5);
                  fR.emplace_back(f6);
                  fR.emplace_back(f7);
                  fR.emplace_back(f8);

                  return fR;
                },
                        {"fakeRate_WHSFVars_WHSFSyst0Up", "fakeRate_WHSFVars_WHSFSyst1Up", "fakeRate_WHSFVars_WHSFSyst2Up", "fakeRate_WHSFVars_WHSFSystFlatUp", "fakeRate_WHSFVars_WHSFSyst0Down", "fakeRate_WHSFVars_WHSFSyst1Down", "fakeRate_WHSFVars_WHSFSyst2Down", "fakeRate_WHSFVars_WHSFSystFlatDown"})
                .Define("fakeRate_LHEScaleWeightred", [](float f1, float f2, float f3, float f4, float f5, float f6) {
                  ROOT::VecOps::RVec<float> fR;
                  fR.emplace_back(f1);
                  fR.emplace_back(f2);
                  fR.emplace_back(f3);
                  fR.emplace_back(f4);
                  fR.emplace_back(f5);
                  fR.emplace_back(f6);

                  return fR;
                },
                        {"fakeRate_LHEScaleWeightVars_LHEScaleWeight_muR0p5_muF0p5", "fakeRate_LHEScaleWeightVars_LHEScaleWeight_muR0p5_muF1p0", "fakeRate_LHEScaleWeightVars_LHEScaleWeight_muR1p0_muF0p5", "fakeRate_LHEScaleWeightVars_LHEScaleWeight_muR1p0_muF2p0", "fakeRate_LHEScaleWeightVars_LHEScaleWeight_muR2p0_muF1p0", "fakeRate_LHEScaleWeightVars_LHEScaleWeight_muR2p0_muF2p0"})
                .Define("fakeRate_ptScale", [](float f1, float f2) {
                  ROOT::VecOps::RVec<float> fR;
                  fR.emplace_back(f1);
                  fR.emplace_back(f2);
                  return fR;
                },
                        {"fakeRate_ptScaleVars_correctedUp", "fakeRate_ptScaleVars_correctedDown"})
                // .Define("fakeRate_jme", [](float f1, float f2, float f3, float f4, float f5, float f6) {
                .Define("fakeRate_jme", [](float f1, float f2, float f3, float f4) {
                  ROOT::VecOps::RVec<float> fR;
                  fR.emplace_back(f1);
                  fR.emplace_back(f2);
                  fR.emplace_back(f3);
                  fR.emplace_back(f4);
                  // fR.emplace_back(f5);
                  // fR.emplace_back(f6);

                  return fR;
                },
                        // {"fakeRate_jmeVars_jerUp", "fakeRate_jmeVars_jerDown", "fakeRate_jmeVars_jesTotalUp", "fakeRate_jmeVars_jesTotalDown", "fakeRate_jmeVars_unclustEnUp", "fakeRate_jmeVars_unclustEnDown"});
		  {"fakeRate_jmeVars_jesTotalUp", "fakeRate_jmeVars_jesTotalDown", "fakeRate_jmeVars_unclustEnUp", "fakeRate_jmeVars_unclustEnDown"})
                .Define("fakeRate_PrefireWeightVars", [](float f1, float f2) {
                  ROOT::VecOps::RVec<float> fR;
                  fR.emplace_back(f1);
                  fR.emplace_back(f2);
                  return fR;
		  }, {"fakeRate_PrefireWeightVars_PrefireWeightUp","fakeRate_PrefireWeightVars_PrefireWeightDown"});
  

  return d2;
}
