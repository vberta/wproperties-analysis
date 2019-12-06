#include "interface/getSystWeight.hpp"


RNode getSystWeight::run(RNode d){
    
    auto getRVec = [](ROOT::VecOps::RVec<float> statUp, ROOT::VecOps::RVec<float> statDown, ROOT::VecOps::RVec<float> systUp, ROOT::VecOps::RVec<float> systDown, int idx){
        ROOT::VecOps::RVec<float> v;
        v.emplace_back(statUp[idx]);
        v.emplace_back(statDown[idx]);
        v.emplace_back(systUp[idx]);
        v.emplace_back(systDown[idx]);
        return v;
    };

    auto getRVecRange = [this](ROOT::VecOps::RVec<float> statUp){
      ROOT::VecOps::RVec<float> v;
      for(unsigned int i=_range.first; i<=_range.second ; i++) v.emplace_back(statUp[i]);
      return v;
    };

    // group element-i four columns into one new column
    if(_idx1!=""){
      std::cout << "getSystWeight::run(): getRVec" << std::endl;
      auto d1 = d.Define(_new_syst_column, getRVec,{_syst_columns[0], _syst_columns[1], _syst_columns[2], _syst_columns[3], _idx1});
      return d1;
    }
    // group N adjacent elements of one colum into one new column
    else{
      std::cout << "getSystWeight::run(): getRVecRange" << std::endl;
      auto d1 = d.Define(_new_syst_column, getRVecRange, {_syst_columns[0]});
      return d1;
    }
}

std::vector<ROOT::RDF::RResultPtr<TH1D>> getSystWeight::getTH1(){ 
    return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> getSystWeight::getTH2(){ 
    return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> getSystWeight::getTH3(){ 
    return _h3List;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> getSystWeight::getGroupTH1(){ 
  return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> getSystWeight::getGroupTH2(){ 
  return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> getSystWeight::getGroupTH3(){ 
  return _h3Group;
}

void getSystWeight::reset(){
    _h1List.clear();
    _h2List.clear();
    _h3List.clear();

    _h1Group.clear();
    _h2Group.clear();
    _h3Group.clear();
}
