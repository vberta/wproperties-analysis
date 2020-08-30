#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"
#include "interface/dataObs.hpp"


RNode dataObs::run(RNode d){

  // inclusive gen binning
  const int nBinsEta = 100;
  const int nBinsPt = 80;

  std::vector<float> etaArr(nBinsEta + 1);
  std::vector<float> ptArr(nBinsPt + 1);

  for (int i = 0; i < nBinsEta + 1; i++)
  {

    float binSize = 5.0 / nBinsEta;
    etaArr[i] = -2.5 + i * binSize;
  }

  for (int i = 0; i < nBinsPt + 1; i++)
  {

    float binSize = (65. - 25.) / nBinsPt;
    ptArr[i] = 25. + i * binSize;
  }
  // then template to be fixed
  
  auto dFix = d.Filter("Wpt_preFSR>32. && Wrap_preFSR_abs>2.4");

  TH2weightsHelper helperAcc(std::string("lowAcc"), std::string("lowAcc"), nBinsEta, etaArr, nBinsPt, ptArr, _syst_name);
  auto lowAcc = dFix.Book<float, float, float, ROOT::VecOps::RVec<float>>(std::move(helperAcc), { "Mueta_preFSR", "Mupt_preFSR", "lumiweight", _syst_weight});

  _h2Group.push_back(lowAcc);

  // pseudo data

  TH2weightsHelper helperData(std::string("data_obs"), std::string("data_obs"), nBinsEta, etaArr, nBinsPt, ptArr, _syst_name);
  auto pseudodata = d.Book<float, float, float, ROOT::VecOps::RVec<float>>(std::move(helperData), { "Mueta_preFSR", "Mupt_preFSR", "lumiweight", _syst_weight});

  _h2Group.push_back(pseudodata);

  return d;
  
  }