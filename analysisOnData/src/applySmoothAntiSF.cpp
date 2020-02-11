#include "interface/applySmoothAntiSF.hpp"


RNode applySmoothAntiSF::run(RNode d){

  RNode d_start = d;

  for(unsigned int i = 0; i < _syst_columns.size(); i++){

    std::string var = _syst_columns[i];

    auto antiSF_smooth = [this,var](float pt, float eta, float charge)->float{ 
      int binX = charge>0. ? 1 : 2;     
      int binY = _hmap.at("wSF_prompt_offset_"+var)->GetYaxis()->FindBin(eta);          
      float wSF_p_offset  = _hmap.at("wSF_prompt_offset_"+var)->GetBinContent(binX,binY);
      float wSF_p_slope   = _hmap.at("wSF_prompt_slope_"+var)->GetBinContent(binX,binY);
      float wSF_p_2deg    = _hmap.at("wSF_prompt_2deg_"+var)->GetBinContent(binX,binY);
      float woSF_p_offset = _hmap.at("woSF_prompt_offset_"+var)->GetBinContent(binX,binY);
      float woSF_p_slope  = _hmap.at("woSF_prompt_slope_"+var)->GetBinContent(binX,binY);
      float woSF_p_2deg   = _hmap.at("woSF_prompt_2deg_"+var)->GetBinContent(binX,binY);
      float wSF_p = wSF_p_offset*TMath::Erf(wSF_p_slope*pt + wSF_p_2deg);
      float woSF_p = woSF_p_offset*TMath::Erf(woSF_p_slope*pt + woSF_p_2deg);
      float res = 1-woSF_p>0. ? (1-wSF_p)/(1-woSF_p) : 1.0; 
      //std::cout << _variable <<  "(" << pt << "," << eta << "," << charge << ") --> " << ": " <<  1-wSF_p << "/" << 1-woSF_p << " = " << res << std::endl;
      return res;
    };

   auto SF_smooth = [this,var](float pt, float eta, float charge)->float{ 
      int binX = charge>0. ? 1 : 2;     
      int binY = _hmap.at("wSF_prompt_offset_"+var)->GetYaxis()->FindBin(eta);          
      float wSF_p_offset  = _hmap.at("wSF_prompt_offset_"+var)->GetBinContent(binX,binY);
      float wSF_p_slope   = _hmap.at("wSF_prompt_slope_"+var)->GetBinContent(binX,binY);
      float wSF_p_2deg    = _hmap.at("wSF_prompt_2deg_"+var)->GetBinContent(binX,binY);
      float woSF_p_offset = _hmap.at("woSF_prompt_offset_"+var)->GetBinContent(binX,binY);
      float woSF_p_slope  = _hmap.at("woSF_prompt_slope_"+var)->GetBinContent(binX,binY);
      float woSF_p_2deg   = _hmap.at("woSF_prompt_2deg_"+var)->GetBinContent(binX,binY);
      float wSF_p = wSF_p_offset*TMath::Erf(wSF_p_slope*pt + wSF_p_2deg);
      float woSF_p = woSF_p_offset*TMath::Erf(woSF_p_slope*pt + woSF_p_2deg);
      float res = woSF_p>0. ? wSF_p/woSF_p : 1.0;
      //std::cout << _variable <<  "(" << pt << "," << eta << "," << charge << ") --> " << ": " <<  wSF_p << "/" << woSF_p << " = " << res << std::endl;
      return res;
    };

    std::string var_name = (var=="nominal") ? "" : var;
    auto d_post = d_start
      .Define("SelMuon1_"+_variable+"_SmoothAntiSF"+var_name, antiSF_smooth, {"SelMuon1_corrected_pt", "SelMuon1_eta", "SelMuon1_charge"})
      .Define("SelMuon1_"+_variable+"_SmoothSF"+var_name, SF_smooth, {"SelMuon1_corrected_pt", "SelMuon1_eta", "SelMuon1_charge"})
      ;
    d_start = d_post;
  }
  
  return d_start;

}

std::vector<ROOT::RDF::RResultPtr<TH1D>> applySmoothAntiSF::getTH1(){ 
    return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> applySmoothAntiSF::getTH2(){ 
    return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> applySmoothAntiSF::getTH3(){ 
    return _h3List;
}

std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> applySmoothAntiSF::getGroupTH1(){ 
  return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> applySmoothAntiSF::getGroupTH2(){ 
  return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> applySmoothAntiSF::getGroupTH3(){ 
  return _h3Group;
}

void applySmoothAntiSF::reset(){
    
    _h1List.clear();
    _h2List.clear();
    _h3List.clear();

    _h1Group.clear();
    _h2Group.clear();
    _h3Group.clear();

}
