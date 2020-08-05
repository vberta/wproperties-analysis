#include "interface/accMap.hpp"


RNode accMap::run(RNode d){
    

    auto mapTot = d.Histo2D(TH2D("mapTot", "mapTot", _nBinsY, _yArr.data(), _nBinsPt, _ptArr.data()), "Wrap_preFSR_abs", "Wpt_preFSR", "lumiweight");
    auto mapAccEta = d.Filter("fabs(Mueta_preFSR)<2.4").Histo2D(TH2D("mapAccEta", "mapAccEta", _nBinsY, _yArr.data(), _nBinsPt, _ptArr.data()), "Wrap_preFSR_abs", "Wpt_preFSR", "lumiweight");
    auto mapAcc = d.Filter("fabs(Mueta_preFSR)<2.4 && Mupt_preFSR>25. && Mupt_preFSR<65.").Histo2D(TH2D("mapAcc", "mapAcc", _nBinsY, _yArr.data(), _nBinsPt, _ptArr.data()), "Wrap_preFSR_abs", "Wpt_preFSR", "lumiweight");
    auto sumw = d.Define("genratio", "Generator_weight/genEventSumw").Histo2D(TH2D("sumw", "sumw", _nBinsY, _yArr.data(), _nBinsPt, _ptArr.data()), "Wrap_preFSR_abs", "Wpt_preFSR", "genratio");

    _h2List.push_back(mapTot);
    _h2List.push_back(mapAccEta);
    _h2List.push_back(mapAcc);
    _h2List.push_back(sumw);
    
    return d;

}

std::vector<ROOT::RDF::RResultPtr<TH1D>> accMap::getTH1(){ 
    return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> accMap::getTH2(){ 
    return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> accMap::getTH3(){ 
    return _h3List;
}

std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> accMap::getGroupTH1(){ 
  return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> accMap::getGroupTH2(){ 
  return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> accMap::getGroupTH3(){ 
  return _h3Group;
}

void accMap::reset(){
    
    _h1List.clear();
    _h2List.clear();
    _h3List.clear();

    _h1Group.clear();
    _h2Group.clear();
    _h3Group.clear();

}