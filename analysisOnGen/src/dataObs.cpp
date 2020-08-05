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
  
  auto dFix = d.Filter("accMapEta<0.4");

  TH2weightsHelper helperAcc(std::string("lowAcc"), std::string("lowAcc"), nBinsEta, etaArr, nBinsPt, ptArr, _syst_name);
  auto lowAcc = dFix.Book<float, float, float, ROOT::VecOps::RVec<float>>(std::move(helperAcc), { "Mueta_preFSR", "Mupt_preFSR", "lumiweight", _syst_weight});

  _h2Group.push_back(lowAcc);

  // pseudo data

  TH2weightsHelper helperData(std::string("data_obs"), std::string("data_obs"), nBinsEta, etaArr, nBinsPt, ptArr, _syst_name);
  auto pseudodata = d.Book<float, float, float, ROOT::VecOps::RVec<float>>(std::move(helperData), { "Mueta_preFSR", "Mupt_preFSR", "lumiweight", _syst_weight});

  _h2Group.push_back(pseudodata);

  
  return d;
  
  }

std::vector<ROOT::RDF::RResultPtr<TH1D>> dataObs::getTH1(){ 
    return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> dataObs::getTH2(){ 
    return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> dataObs::getTH3(){ 
    return _h3List;
}

std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> dataObs::getGroupTH1(){ 
  return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> dataObs::getGroupTH2(){ 
  return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> dataObs::getGroupTH3(){ 
  return _h3Group;
}

void dataObs::reset(){
    
    _h1List.clear();
    _h2List.clear();
    _h3List.clear();

    _h1Group.clear();
    _h2Group.clear();
    _h3Group.clear();

}