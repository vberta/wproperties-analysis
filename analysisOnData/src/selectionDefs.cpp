#include "interface/selectionDefs.hpp"

RNode selectionDefs::run(RNode df)
{
  return df.Filter(_filter);
}

std::vector<ROOT::RDF::RResultPtr<TH1D>> selectionDefs::getTH1(){ 
  return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> selectionDefs::getTH2(){ 
  return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> selectionDefs::getTH3(){ 
  return _h3List;
}

std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> selectionDefs::getGroupTH1(){ 
  return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> selectionDefs::getGroupTH2(){ 
  return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> selectionDefs::getGroupTH3(){ 
  return _h3Group;
}

void selectionDefs::reset(){
  
  _h1List.clear();
  _h2List.clear();
  _h3List.clear();
  
  _h1Group.clear();
  _h2Group.clear();
  _h3Group.clear();
  
}
