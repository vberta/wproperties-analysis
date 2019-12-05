#include "interface/baseDefinitions.hpp"


RNode baseDefinitions::run(RNode d){

  auto d1 = d.Define("SelMuon_corrected_pt", getFromIdx, {"Muon_corrected_pt", "Idx_mu1"})
    .Define("SelMuon_eta", getFromIdx, {"Muon_eta", "Idx_mu1"})
    .Filter(_filter);
 
  return d1;

}

std::vector<ROOT::RDF::RResultPtr<TH1D>> baseDefinitions::getTH1(){ 
    return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> baseDefinitions::getTH2(){ 
    return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> baseDefinitions::getTH3(){ 
    return _h3List;
}

std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> baseDefinitions::getGroupTH1(){ 
  return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> baseDefinitions::getGroupTH2(){ 
  return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> baseDefinitions::getGroupTH3(){ 
  return _h3Group;
}

void baseDefinitions::reset(){
    
    _h1List.clear();
    _h2List.clear();
    _h3List.clear();

    _h1Group.clear();
    _h2Group.clear();
    _h3Group.clear();

}
