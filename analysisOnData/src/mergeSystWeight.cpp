#include "interface/mergeSystWeight.hpp"


RNode mergeSystWeight::run(RNode d){
  
  auto getRVec = [this](ROOT::VecOps::RVec<float> systA, ROOT::VecOps::RVec<float> systB){
    ROOT::VecOps::RVec<float> v;
    for(unsigned int i=0; i<systA.size(); i++){
      v.emplace_back( _multiply ? systA[i]*systB[i] : systA[i]*_syst_ratios.first + systB[i]*_syst_ratios.second );
    }
    return v;
  };

  auto getF = [this](float systA, float systB){
    float syst = _multiply ? systA*systB : systA*_syst_ratios.first + systB*_syst_ratios.second;
    return syst;
  };

  if(_scalar){
    auto d1 = d.Define(_syst_weight, getF, {_syst_name.first, _syst_name.second});
    return d1;
  }
  else{
    auto d1 = d.Define(_syst_weight, getRVec, {_syst_name.first, _syst_name.second});
    return d1;
  }
  return d;
}

std::vector<ROOT::RDF::RResultPtr<TH1D>> mergeSystWeight::getTH1(){ 
    return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> mergeSystWeight::getTH2(){ 
    return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> mergeSystWeight::getTH3(){ 
    return _h3List;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> mergeSystWeight::getGroupTH1(){ 
  return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> mergeSystWeight::getGroupTH2(){ 
  return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> mergeSystWeight::getGroupTH3(){ 
  return _h3Group;
}

void mergeSystWeight::reset(){
    _h1List.clear();
    _h2List.clear();
    _h3List.clear();

    _h1Group.clear();
    _h2Group.clear();
    _h3Group.clear();
}
