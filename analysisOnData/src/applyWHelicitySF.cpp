#include "interface/applyWHelicitySF.hpp"


RNode applyWHelicitySF::run(RNode d){

  RNode d_start = d;
  
  auto get_trigger_SF = [this](float pt, float eta, float charge)->float{ 
    std::string c = charge>0. ? "plus" : "minus";
    TH2D* h = _hmap.at("trigger_"+c);
    int bin = h->FindBin(eta,pt);          
    if( h->IsBinOverflow(bin)  || h->IsBinUnderflow(bin)) return 1.0;
    return h->GetBinContent(bin);
  };

  auto get_reco_SF = [this](float pt, float eta)->float{ 
    TH2D* h = _hmap.at("reco");
    int bin = h->FindBin(eta,pt);          
    if( h->IsBinOverflow(bin)  || h->IsBinUnderflow(bin)) return 1.0;
    return h->GetBinContent(bin);
  };

  auto get_id_SF = []()->float{ return 1.0; };

  auto d_post = d_start
    .Define("SelMuon1_Trigger_WHelicitySF", get_trigger_SF, {"SelMuon1_corrected_pt", "SelMuon1_eta", "SelMuon1_charge"})
    .Define("SelMuon1_ISO_WHelicitySF",     get_reco_SF,    {"SelMuon1_corrected_pt", "SelMuon1_eta"})
    .Define("SelMuon1_ID_WHelicitySF",      get_id_SF,      {});
  d_start = d_post;

  if(_idx2!=""){
    auto d_post = d_start
      .Define("SelMuon2_Trigger_WHelicitySF", get_trigger_SF, {"SelMuon2_corrected_pt", "SelMuon2_eta", "SelMuon2_charge"})
      .Define("SelMuon2_ISO_WHelicitySF",     get_reco_SF,    {"SelMuon2_corrected_pt", "SelMuon2_eta"})
      .Define("SelMuon2_ID_WHelicitySF",      get_id_SF,      {});
    d_start = d_post;
  }


  if( _syst_columns_trigger.size()>0){
    auto get_trigger_systSFAll = [this](float pt, float eta, float charge)->ROOT::VecOps::RVec<float>{ 
      ROOT::VecOps::RVec<float> v;
      for( auto s : _syst_columns_trigger){
	std::string c = charge>0. ? "plus" : "minus";
	TH2D* h = _hmap.at(s+"_"+c);
	int bin = h->FindBin(eta,pt);          
	float val = 1.0;
	if( !(h->IsBinOverflow(bin) || h->IsBinUnderflow(bin))) val = h->GetBinContent(bin); 
	v.emplace_back(val);
      }
      return v;
    };
    auto d_post = d_start.Define("SelMuon1_Trigger_WHelicitySFAll", get_trigger_systSFAll, {"SelMuon1_corrected_pt", "SelMuon1_eta", "SelMuon1_charge"});
    d_start = d_post;    
    if(_idx2!=""){
      auto d_post = d_start.Define("SelMuon2_Trigger_WHelicitySFAll", get_trigger_systSFAll, {"SelMuon2_corrected_pt", "SelMuon2_eta", "SelMuon2_charge"});
      d_start = d_post;
    }   
  }

  if( _syst_columns_reco.size()>0){
    auto get_reco_systSFAll = [this](float pt, float eta)->ROOT::VecOps::RVec<float>{ 
      ROOT::VecOps::RVec<float> v;
      for( auto s : _syst_columns_reco){
	TH2D* h = _hmap.at(s);
	int bin = h->FindBin(eta,pt);          
	float val = 1.0;
	if( !(h->IsBinOverflow(bin) || h->IsBinUnderflow(bin))) val = h->GetBinContent(bin); 
	v.emplace_back(val);
      }
      return v;
    };
    auto d_post = d_start.Define("SelMuon1_ISO_WHelicitySFAll", get_reco_systSFAll, {"SelMuon1_corrected_pt", "SelMuon1_eta"});
    d_start = d_post;    
    if(_idx2!=""){
      auto d_post = d_start.Define("SelMuon2_ISO_WHelicitySFAll", get_reco_systSFAll, {"SelMuon2_corrected_pt", "SelMuon2_eta"});
      d_start = d_post;
    }   
  }
    
  

  
  return d_start; 
}

std::vector<ROOT::RDF::RResultPtr<TH1D>> applyWHelicitySF::getTH1(){ 
    return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> applyWHelicitySF::getTH2(){ 
    return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> applyWHelicitySF::getTH3(){ 
    return _h3List;
}

std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> applyWHelicitySF::getGroupTH1(){ 
  return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> applyWHelicitySF::getGroupTH2(){ 
  return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> applyWHelicitySF::getGroupTH3(){ 
  return _h3Group;
}

void applyWHelicitySF::reset(){
    
    _h1List.clear();
    _h2List.clear();
    _h3List.clear();

    _h1Group.clear();
    _h2Group.clear();
    _h3Group.clear();

}
