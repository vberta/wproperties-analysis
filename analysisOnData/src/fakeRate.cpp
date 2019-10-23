#include "interface/fakeRate.hpp"


RNode fakeRate::run(RNode d){

  auto applyFakeRate = [this](float pt, float eta){ 
    int binIdx = _hmap->FindBin(eta,pt);
    return _hmap->GetBinContent(binIdx);
  };   
  
  auto d1 = d.Define("SelMuon_corrected_pt", getFromIdx, {"Muon_corrected_pt", "Idx_mu1"})
    .Define("SelMuon_eta", getFromIdx, {"Muon_eta", "Idx_mu1"})
    .Define("FakeRate", applyFakeRate, {"SelMuon_corrected_pt", "SelMuon_eta"});
 
  return d1;

}

std::vector<ROOT::RDF::RResultPtr<TH1D>> fakeRate::getTH1(){ 
    return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> fakeRate::getTH2(){ 
    return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> fakeRate::getTH3(){ 
    return _h3List;
}

std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> fakeRate::getGroupTH1(){ 
  return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> fakeRate::getGroupTH2(){ 
  return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> fakeRate::getGroupTH3(){ 
  return _h3Group;
}

void fakeRate::reset(){
    
    _h1List.clear();
    _h2List.clear();
    _h3List.clear();

    _h1Group.clear();
    _h2Group.clear();
    _h3Group.clear();

}
