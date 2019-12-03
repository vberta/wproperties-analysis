#include "interface/getLumiWeight.hpp"


RNode getLumiWeight::run(RNode d){
    
  auto getWeight = [this](float genWeight)->float {
    return _targetLumi*_xsec*genWeight/_genEventSumw;
  };
  auto d1 = d.Define("lumiweight", getWeight, {"Generator_weight"});
  return d1;

}

std::vector<ROOT::RDF::RResultPtr<TH1D>> getLumiWeight::getTH1(){ 
    return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> getLumiWeight::getTH2(){ 
    return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> getLumiWeight::getTH3(){ 
    return _h3List;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> getLumiWeight::getGroupTH1(){ 
  return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> getLumiWeight::getGroupTH2(){ 
  return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> getLumiWeight::getGroupTH3(){ 
  return _h3Group;
}

void getLumiWeight::reset(){
    _h1List.clear();
    _h2List.clear();
    _h3List.clear();

    _h1Group.clear();
    _h2Group.clear();
    _h3Group.clear();
}
