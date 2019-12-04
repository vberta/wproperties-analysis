#include "interface/getSystVar.hpp"


RNode getSystVar::run(RNode d){
    
    auto getRVec = [](ROOT::VecOps::RVec<float> statUp, ROOT::VecOps::RVec<float> statDown, int idx){
        ROOT::VecOps::RVec<float> v;
        v.emplace_back(statUp[idx]);
        v.emplace_back(statDown[idx]);
        return v;
    };

    auto d1 = d.Define(_syst_weight, getRVec,{_syst_name[0], _syst_name[1], _idx1});
    return d1;
}

std::vector<ROOT::RDF::RResultPtr<TH1D>> getSystVar::getTH1(){ 
    return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> getSystVar::getTH2(){ 
    return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> getSystVar::getTH3(){ 
    return _h3List;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> getSystVar::getGroupTH1(){ 
  return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> getSystVar::getGroupTH2(){ 
  return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> getSystVar::getGroupTH3(){ 
  return _h3Group;
}

void getSystVar::reset(){
    _h1List.clear();
    _h2List.clear();
    _h3List.clear();

    _h1Group.clear();
    _h2Group.clear();
    _h3Group.clear();
}
