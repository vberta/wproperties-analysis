#include "interface/mergeSystWeight.hpp"


RNode mergeSystWeight::run(RNode d){
  
  auto getRVec_weight = [this](ROOT::VecOps::RVec<float> systA, ROOT::VecOps::RVec<float> systB){
    ROOT::VecOps::RVec<float> v;
    for(unsigned int i=0; i<systA.size(); i++){
      v.emplace_back( systA[i]*_syst_ratios.first + systB[i]*_syst_ratios.second );
    }
    return v;
  };

  auto getF_weight = [this](float systA, float systB){
    float syst =  systA*_syst_ratios.first + systB*_syst_ratios.second;
    return syst;
  };

  auto getRVec_mult = [this](ROOT::VecOps::RVec<float> systA, ROOT::VecOps::RVec<float> systB){
    ROOT::VecOps::RVec<float> v;
    for(unsigned int i=0; i<systA.size(); i++){
      v.emplace_back( systA[i]*systB[i] );
    }
    return v;
  };

  auto getF_mult = [this](float systA, float systB){
    float syst = systA*systB;
    return syst;
  };

  if(_type=="V,V->aV+bV"){
    if(_verbose) std::cout << "mergeSystWeight::run(): getRVec_weight" << std::endl;
    auto d1 = d.Define(_new_syst_column, getRVec_weight, {_syst_columns.first, _syst_columns.second});
    return d1;
  }
  else if(_type=="f,f->af+bf"){
    if(_verbose) std::cout << "mergeSystWeight::run(): getF_weight" << std::endl;
    auto d1 = d.Define(_new_syst_column, getF_weight, {_syst_columns.first, _syst_columns.second});
    return d1;
  }
  else if(_type=="V,V->V*V"){
    if(_verbose) std::cout << "mergeSystWeight::run(): getRVec_mult" << std::endl;
    auto d1 = d.Define(_new_syst_column, getRVec_mult, {_syst_columns.first, _syst_columns.second});
    return d1;
  }
  else if(_type=="f,f->f*f"){
    if(_verbose) std::cout << "mergeSystWeight::run(): getF_mult" << std::endl;
    auto d1 = d.Define(_new_syst_column, getF_mult, {_syst_columns.first, _syst_columns.second});
    return d1;
  }
  else{    
    return d;
  }
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
