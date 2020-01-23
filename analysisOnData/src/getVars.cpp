#include "interface/getVars.hpp"


RNode getVars::run(RNode d){

  RNode d_start = d;

  /*
  auto getPositive = [](float pt1, float pt2, float q1)->float {
    if(q1>0.) return pt1;
    return pt2;
  };
  auto getNegative = [](float pt1, float pt2, float q1)->float {
    if(q1<0.) return pt1;
    return pt2;
  };
  */
    
  auto d_post = d_start
    .Define("dummy", dummy, {"event"})
    .Define("SelMuon1_charge",           getIFromIdx, {"Muon_charge",          _idx1})
    .Define("SelMuon1_pfRelIso04_all",   getFromIdx , {"Muon_pfRelIso04_all",  _idx1})
    .Define("SelMuon1_dxy",              getFromIdx,  {"Muon_dxy",             _idx1})
    .Define("SelMuon1_corrected_pt",     getFromIdx,  {"Muon_corrected_pt",    _idx1})
    .Define("SelMuon1_pt",               getFromIdx,  {"Muon_pt",              _idx1})
    .Define("SelMuon1_eta",              getFromIdx,  {"Muon_eta",             _idx1})
    .Define("SelMuon1_phi",              getFromIdx,  {"Muon_phi",             _idx1})
    .Define("nPVs",                      castToFloat, {"PV_npvsGood"})
    ;
  d_start = d_post;

  if(_isMC){
    auto d_post = d_start.Define("SelMuon1_ISO_BCDEF_SF",     getFromIdx,  {"Muon_ISO_BCDEF_SF",    _idx1})
      .Define("SelMuon1_ISO_GH_SF",        getFromIdx,  {"Muon_ISO_GH_SF",       _idx1})
      .Define("SelMuon1_ID_BCDEF_SF",      getFromIdx,  {"Muon_ID_BCDEF_SF",     _idx1})
      .Define("SelMuon1_ID_GH_SF",         getFromIdx,  {"Muon_ID_GH_SF",        _idx1})
      .Define("SelMuon1_Trigger_BCDEF_SF", getFromIdx,  {"Muon_Trigger_BCDEF_SF",_idx1})
      .Define("SelMuon1_Trigger_GH_SF",    getFromIdx,  {"Muon_Trigger_GH_SF",   _idx1})
      ;
    d_start = d_post;
  }
  
  if(_idx2!=""){
    auto d_post = d_start
      .Define("SelMuon2_charge",           getIFromIdx, {"Muon_charge",          _idx2})
      .Define("SelMuon2_pfRelIso04_all",   getFromIdx , {"Muon_pfRelIso04_all",  _idx2})
      .Define("SelMuon2_dxy",              getFromIdx,  {"Muon_dxy",             _idx2})
      .Define("SelMuon2_corrected_pt",     getFromIdx,  {"Muon_corrected_pt",    _idx2})
      .Define("SelMuon2_pt",               getFromIdx,  {"Muon_pt",              _idx2})
      .Define("SelMuon2_eta",              getFromIdx,  {"Muon_eta",             _idx2})
      .Define("SelMuon2_phi",              getFromIdx,  {"Muon_phi",             _idx2})
      //.Define("SelMuonP_pt",               getPositive, {"SelMuon1_pt", "SelMuon2_pt", "SelMuon1_charge"})
      //.Define("SelMuonN_pt",               geNegative,  {"SelMuon1_pt", "SelMuon2_pt", "SelMuon1_charge"})
      //.Define("SelMuonP_corrected_pt",     getPositive, {"SelMuon1_corrected_pt", "SelMuon2_corrected_pt", "SelMuon1_charge"})
      //.Define("SelMuonN_corrected_pt",     geNegative,  {"SelMuon1_corrected_pt", "SelMuon2_corrected_pt", "SelMuon1_charge"})
      //.Define("SelMuonP_eta",              getPositive, {"SelMuon1_eta", "SelMuon2_eta", "SelMuon1_charge"})
      //.Define("SelMuonN_eta",              geNegative,  {"SelMuon1_eta", "SelMuon2_eta", "SelMuon1_charge"})
      //.Define("SelMuonP_phi",              getPositive, {"SelMuon1_phi", "SelMuon2_phi", "SelMuon1_charge"})
      //.Define("SelMuonN_phi",              geNegative,  {"SelMuon1_phi", "SelMuon2_phi", "SelMuon1_charge"})
      //.Define("SelMuonP_charge",           getPositive, {"SelMuon1_charge", "SelMuon2_charge", "SelMuon1_charge"})
      //.Define("SelMuonN_charge",           geNegative,  {"SelMuon1_charge", "SelMuon2_charge", "SelMuon1_charge"})
      //.Define("SelMuonP_dxy",              getPositive, {"SelMuon1_dxy", "SelMuon2_dxy", "SelMuon1_charge"})
      //.Define("SelMuonN_dxy",              geNegative,  {"SelMuon1_dxy", "SelMuon2_dxy", "SelMuon1_charge"})
      //.Define("SelMuonP_pfRelIso04_all",   getPositive, {"SelMuon1_pfRelIso04_all", "SelMuon2_pfRelIso04_all", "SelMuon1_charge"})
      //.Define("SelMuonN_pfRelIso04_all",   geNegative,  {"SelMuon1_pfRelIso04_all", "SelMuon2_pfRelIso04_all", "SelMuon1_charge"})
      ;
    d_start = d_post;

    if(_isMC){
      auto d_post = d_start
	.Define("SelMuon2_ISO_BCDEF_SF",     getFromIdx,  {"Muon_ISO_BCDEF_SF",    _idx2})
	.Define("SelMuon2_ISO_GH_SF",        getFromIdx,  {"Muon_ISO_GH_SF",       _idx2})
	.Define("SelMuon2_ID_BCDEF_SF",      getFromIdx,  {"Muon_ID_BCDEF_SF",     _idx2})
	.Define("SelMuon2_ID_GH_SF",         getFromIdx,  {"Muon_ID_GH_SF",        _idx2})
	.Define("SelMuon2_Trigger_BCDEF_SF", getFromIdx,  {"Muon_Trigger_BCDEF_SF",_idx2})
	.Define("SelMuon2_Trigger_GH_SF",    getFromIdx,  {"Muon_Trigger_GH_SF",   _idx2})
	;
      d_start = d_post;
    }    
  }  

  return d_start;
}

std::vector<ROOT::RDF::RResultPtr<TH1D>> getVars::getTH1(){ 
    return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> getVars::getTH2(){ 
    return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> getVars::getTH3(){ 
    return _h3List;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> getVars::getGroupTH1(){ 
  return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> getVars::getGroupTH2(){ 
  return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> getVars::getGroupTH3(){ 
  return _h3Group;
}

void getVars::reset(){
    _h1List.clear();
    _h2List.clear();
    _h3List.clear();

    _h1Group.clear();
    _h2Group.clear();
    _h3Group.clear();
}
