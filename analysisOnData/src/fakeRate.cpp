#include "interface/fakeRate.hpp"


RNode fakeRate::run(RNode d){

  auto defineFakeRate = [this](float pt, float eta, float charge, int vtype) {
    
    int binX = charge > 0. ? 1 : 2;
    int binY = _hfake_offset->GetYaxis()->FindBin(eta);
    
    float f_offset = _hfake_offset->GetBinContent(binX, binY);
    float f_slope = _hfake_slope->GetBinContent(binX, binY);
    float p_offset = _hprompt_offset->GetBinContent(binX, binY);
    float p_slope = _hprompt_slope->GetBinContent(binX, binY);
    float p_2deg = _hprompt_2deg->GetBinContent(binX, binY);
    float f = f_offset + (pt - 26.0) * f_slope;
    float p = p_offset * TMath::Erf(p_slope * pt + p_2deg);
    float res = vtype == 1 ? p * f / (p - f) : -(1 - p) * f / (p - f);
    
    return res;

  };

  auto d1 = d.Define("fakeRate", defineFakeRate, {"Mu1_pt", "Mu1_eta", "Mu1_charge", "Vtype"});

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
