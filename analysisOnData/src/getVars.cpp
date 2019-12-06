#include "interface/getVars.hpp"


RNode getVars::run(RNode d){
    
  auto d1 = d
    .Define("dummy", dummy, {"event"})
    .Define("Muon1_ISO_BCDEF_SF",   getFromIdx, {"Muon_ISO_BCDEF_SF",  _idx1})
    .Define("Muon1_ISO_GH_SF",      getFromIdx, {"Muon_ISO_GH_SF",     _idx1})
    .Define("Muon1_ID_BCDEF_SF",    getFromIdx, {"Muon_ID_BCDEF_SF",  _idx1})
    .Define("Muon1_ID_GH_SF",       getFromIdx, {"Muon_ID_GH_SF",     _idx1})
    .Define("Muon1_Trigger_BCDEF_SF", getFromIdx, {"Muon_Trigger_BCDEF_SF",_idx1})
    .Define("Muon1_Trigger_GH_SF",    getFromIdx, {"Muon_Trigger_GH_SF",   _idx1})
    .Define("Muon1_corrected_pt",     getFromIdx, {"Muon_corrected_pt",    _idx1})
    .Define("Muon1_pt",  getFromIdx, {"Muon_pt",  _idx1})
    .Define("Muon1_eta", getFromIdx, {"Muon_eta", _idx1})
    .Define("Muon1_phi", getFromIdx, {"Muon_phi", _idx1})
    .Define("Muon1_corrected_MET_nom_mt",     getFromIdx, {"Muon_corrected_MET_nom_mt",     _idx1})
    .Define("Muon1_corrected_MET_nom_hpt",    getFromIdx, {"Muon_corrected_MET_nom_hpt",     _idx1})
    // These are needed as may appear in category cuts
    .Define("Muon1_correctedUp_pt",   getFromIdx, {"Muon_correctedUp_pt",  _idx1})
    .Define("Muon1_correctedDown_pt", getFromIdx, {"Muon_correctedDown_pt",_idx1})
    .Define("Muon1_correctedUp_MET_nom_mt",   getFromIdx, {"Muon_correctedUp_MET_nom_mt",   _idx1})
    .Define("Muon1_correctedDown_MET_nom_mt", getFromIdx, {"Muon_correctedDown_MET_nom_mt", _idx1})
    .Define("Muon1_corrected_MET_jesTotalUp_mt",   getFromIdx, {"Muon_corrected_MET_jesTotalUp_mt",     _idx1})
    .Define("Muon1_corrected_MET_jesTotalDown_mt", getFromIdx, {"Muon_corrected_MET_jesTotalDown_mt",   _idx1})
    .Define("Muon1_corrected_MET_jerUp_mt",   getFromIdx, {"Muon_corrected_MET_jerUp_mt",     _idx1})
    .Define("Muon1_corrected_MET_jerDown_mt", getFromIdx, {"Muon_corrected_MET_jerDown_mt",     _idx1})
    .Define("Muon1_corrected_MET_unclustEnUp_mt",   getFromIdx, {"Muon_corrected_MET_unclustEnUp_mt",     _idx1})
    .Define("Muon1_corrected_MET_unclustEnDown_mt", getFromIdx, {"Muon_corrected_MET_unclustEnDown_mt",     _idx1});

  return d1;
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
