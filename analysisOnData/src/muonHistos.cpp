#include "interface/muonHistos.hpp"


RNode muonHistos::run(RNode d){
    
    auto d1 = d.Filter(_filter).Define("weight",_weight);
    
    std::vector<float> pTArr(101); 
    for(int i=0; i<101; i++) {
        pTArr[i] = 25. + i*(65.-25.)/100;
    }

    TH1weightsHelper helper(std::string("Mu1_pt"), std::string(" ; muon p_{T} (Rochester corr.); "), 100, pTArr, _syst_name);

    auto hpT = d1.Book<float, float, ROOT::VecOps::RVec<float>>(std::move(helper), {"Mu1_pt", "weight", _syst_weight});
    _h1Group.emplace_back(hpT);

    return d1;
}

std::vector<ROOT::RDF::RResultPtr<TH1D>> muonHistos::getTH1(){ 
  return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> muonHistos::getTH2(){ 
  return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> muonHistos::getTH3(){ 
  return _h3List;
}

std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> muonHistos::getGroupTH1(){ 
  return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> muonHistos::getGroupTH2(){ 
  return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> muonHistos::getGroupTH3(){ 
  return _h3Group;
}

void muonHistos::reset(){
  
  _h1List.clear();
  _h2List.clear();
  _h3List.clear();
  
  _h1Group.clear();
  _h2Group.clear();
  _h3Group.clear();
  
}
