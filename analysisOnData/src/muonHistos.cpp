#include "interface/muonHistos.hpp"


RNode muonHistos::run(RNode d){
    
  auto d1 = d.Filter(_cut);

  unsigned int nbins_pt = 50;
  std::vector<float> pt_Arr(nbins_pt+1); 
  for(unsigned int i=0; i<nbins_pt+1; i++) pt_Arr[i] = 25. + i*(65.-25.)/nbins_pt;      
  this->add_group( &d1, "Muon1_corrected_pt", "; muon p_{T} (Roch.)", pt_Arr, nbins_pt);
  //this->add_group( &d1, "Muon1_pt", "; muon p_{T}", pt_Arr, nbins_pt);

  unsigned int nbins_eta = 50;
  std::vector<float> eta_Arr(nbins_eta+1); 
  for(unsigned int i=0; i<nbins_eta+1; i++) eta_Arr[i] = -2.5 + i*(2.5 + 2.5)/nbins_eta;      
  this->add_group( &d1, "Muon1_eta", "; muon #eta", eta_Arr, nbins_eta);

  unsigned int nbins_mt = 50;
  std::vector<float> mt_Arr(nbins_mt+1); 
  for(unsigned int i=0; i<nbins_mt+1; i++) mt_Arr[i] = 0. + i*(150.-0.)/nbins_mt;
  this->add_group( &d1, "Muon1_corrected_MET_nom_mt", "M_{T} (Roch.+PF MET)", mt_Arr, nbins_mt);

  unsigned int nbins_hpt = 50;
  std::vector<float> hpt_Arr(nbins_hpt+1); 
  for(unsigned int i=0; i<nbins_hpt+1; i++) hpt_Arr[i] = 0. + i*(100.-0.)/nbins_hpt;
  //this->add_group( &d1, "Muon1_corrected_MET_nom_hpt", "h_{T} (Roch.+PF MET)", hpt_Arr, nbins_hpt);

  unsigned int nbins_met_pt = 50;
  std::vector<float> met_pt_Arr(nbins_met_pt+1); 
  for(unsigned int i=0; i<nbins_met_pt+1; i++) met_pt_Arr[i] = 0. + i*(100.-0.)/nbins_met_pt;
  //this->add_group( &d1, "MET_nom_pt", "PF MET", met_pt_Arr, nbins_met_pt);

  unsigned int nbins_met_phi = 50;
  std::vector<float> met_phi_Arr(nbins_met_phi+1); 
  for(unsigned int i=0; i<nbins_met_phi+1; i++) met_phi_Arr[i] = -TMath::Pi() + i*(2*TMath::Pi())/nbins_met_phi;
  //this->add_group( &d1, "MET_nom_phi", "PF MET", met_phi_Arr, nbins_met_phi);

  return d1;
}

std::string muonHistos::check_modifier(const std::string& var_name){
  const std::string sub = _modifier+"All";
  size_t pos = var_name.find(_modifier);  
  if(pos==std::string::npos) return var_name;    
  std::string in = var_name;
  std::string ret = in.replace(pos, _modifier.length(), sub);  
  return ret;
}

void muonHistos::add_group(ROOT::RDF::RInterface<ROOT::Detail::RDF::RJittedFilter, void>* d1, const std::string& var_name, const std::string& var_title, const std::vector<float>& arr, const unsigned int& nbins){
  std::vector<std::string> total = _syst_names;
  if(total.size()==0) total.emplace_back("");
  std::string var_name_mod;
  if(_modifier==""){
    if(_verbose) std::cout << "muonHistos::run(): TH1weightsHelper<f,f,V> for variable " << var_name << " (" << _weight << "*" << _syst_column << "[])" << std::endl;
    TH1weightsHelper w_helper(_category, var_name, var_title, nbins, arr, total);         
    _h1Group.emplace_back(d1->Book<float,float,ROOT::VecOps::RVec<float>>(std::move(w_helper), {var_name, _weight, _syst_names.size()>0 ? _syst_column: "dummy"}) ); 
  }
  else{
    var_name_mod = this->check_modifier(var_name);
    bool has_changed = (var_name_mod!=var_name);
    TH1varsHelper v_helper(_category, var_name, var_title, nbins, arr, total);
    if(has_changed){
      if(_multi_cuts){
	if(_verbose) std::cout << "muonHistos::run(): TH1varsHelper<V,V> for variable " << var_name_mod << "[] (" << _weight << "*" << _syst_column << "[])" << std::endl;
	_h1Group.emplace_back(d1->Book<ROOT::VecOps::RVec<float>,ROOT::VecOps::RVec<float>>(std::move(v_helper), {var_name_mod, _syst_column }));
      }
      else{
	if(_verbose) std::cout << "muonHistos::run(): TH1varsHelper<V,f> for variable " << var_name_mod << "[] (" << _weight << "*)" << std::endl;
	_h1Group.emplace_back(d1->Book<ROOT::VecOps::RVec<float>,float>(std::move(v_helper), {var_name_mod, _weight }));
      }
    }
    else{
      if(_multi_cuts){
	if(_verbose) std::cout << "muonHistos::run(): TH1varsHelper<f,V> for variable " << var_name << " (" << _weight << "*" << _syst_column << "[])" << std::endl;
	_h1Group.emplace_back(d1->Book<float,ROOT::VecOps::RVec<float>>(std::move(v_helper), {var_name, _syst_column }));
      }
      else{
	if(_verbose) std::cout << "muonHistos::run(): TH1varsHelper<f,f> for variable " << var_name << "[] (" << _weight << "*): DO NOTHING -- These are alike the nominal!" << std::endl;
	if(false) _h1Group.emplace_back(d1->Book<float,float>(std::move(v_helper), {var_name, _weight }));
      }
    }											 
  }
  return;
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
