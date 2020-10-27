#include "interface/functions.hpp"
#include "interface/rochesterWeights.hpp"
#include "interface/TH3weightsHelper.hpp"
RNode rochesterWeights::run(RNode d)
{

  auto getValue = [this](float eta, float pt, float charge) mutable {
    ROOT::VecOps::RVec<float> rochWeights;
    for (auto w : _weights)
    {
      int bin = w->FindBin(eta, pt,charge);
      float val = w->GetBinContent(bin);
      rochWeights.emplace_back(val);
    }
    return rochWeights;
  };

  auto d1 = d.Define("rochWeights", getValue, {"Mu1_eta", "Mu1_pt", "Mu1_charge"});
  
  // std::vector<float> _pTArr = std::vector<float>(61);
  // std::vector<float> _etaArr = std::vector<float>(49);
  // std::vector<float> _chargeArr = std::vector<float>(3);
  // for (unsigned int i = 0; i < 61; i++)
  // {
  //   float binSize = (55. - 25.) / 60;
  //   _pTArr[i] = 25. + i * binSize;
  // }
  // for (unsigned int i = 0; i < 49; i++)
  //   _etaArr[i] = -2.4 + i * 4.8 / 48;
  // for (int i = 0; i < 3; i++)
  //   _chargeArr[i] = -2. + i * 2.;
  // std::vector<std::string> _syst_name;
  // for (auto w : _weights) _syst_name.emplace_back(w->GetName());

  // TH3weightsHelper helper(std::string("Mu1_pt_eta"), std::string(" ; muon #{eta}; muon p_{T} (Rochester corr.); muon charge"), _etaArr.size() - 1, _etaArr, _pTArr.size() - 1, _pTArr, _chargeArr.size() - 1, _chargeArr, _syst_name);
  // auto h = d1.Book<float, float, float, float, ROOT::VecOps::RVec<float>>(std::move(helper), {"Mu1_eta", "Mu1_pt", "Mu1_charge", "weight", "rochWeights"});
  // _h3Group.emplace_back(h);

  return d1;
};
