#include "interface/fakeRate.hpp"


RNode fakeRate::run(RNode d){

  auto applyFakeRate = [this](float pt, float eta, float charge, int vtype){ 
    ROOT::VecOps::RVec<float> v;
    int binX = charge>0. ? 1 : 2;     
    int binY = _hmap["fake_offset_nominal"]->GetYaxis()->FindBin(eta);    
    for(unsigned int i = 0; i < _syst_columns.size(); i++){
      std::string var = _syst_columns[i];
      float f_offset = _hmap["fake_offset_"+var]->GetBinContent(binX,binY);
      float f_slope  = _hmap["fake_slope_"+var]->GetBinContent(binX,binY);
      float p_offset = _hmap["prompt_offset_"+var]->GetBinContent(binX,binY);
      float p_slope  = _hmap["prompt_slope_"+var]->GetBinContent(binX,binY);
      float p_2deg   = _hmap["prompt_2deg_"+var]->GetBinContent(binX,binY);
      float f = f_offset + (pt-25.0)*f_slope;
      float p = p_offset*TMath::Erf(p_slope*pt + p_2deg);
      float res = vtype==1 ? p*f/(p-f) : -(1-p)*f/(p-f);
      //std::cout << _category <<  "(" << pt << "," << eta << "," << charge << ") --> " << f << "," << p << ": " << res << std::endl;
      v.emplace_back(res);
    }
    return v;
  };   

  auto d1 = d.Define("fakeRateAll", applyFakeRate, {"SelMuon1_corrected_pt", "SelMuon1_eta", "SelMuon1_charge", "Vtype"});

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
