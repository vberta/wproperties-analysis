#include "interface/muonHistos.hpp"


RNode muonHistos::run(RNode d){

  bool veto_LHE = _syst_column.find("LHE")!=std::string::npos;
    
  // PT1,2 vs ETA1,2 vs CHARGE1,2
  unsigned int nbins_pt  = 29;
  unsigned int nbins_eta = 48;
  unsigned int nbins_charge = 2;
  std::vector<float> pt_Arr(nbins_pt+1); 
  std::vector<float> eta_Arr(nbins_eta+1); 
  std::vector<float> charge_Arr(nbins_charge+1); 
  for(unsigned int i=0; i<nbins_pt+1; i++)         pt_Arr[i] = 26.0 + i*(55.-26.)/nbins_pt;      
  for(unsigned int i=0; i<nbins_eta+1; i++)       eta_Arr[i] = -2.4 + i*(2.4 + 2.4)/nbins_eta;      
  for(unsigned int i=0; i<nbins_charge+1; i++) charge_Arr[i] = -2.0 + i*(4.0)/nbins_charge;      
  if(_category.find("SIGNAL")!=std::string::npos || _category.find("QCD")!=std::string::npos || _category.find("DIMUON")!=std::string::npos)
    this->add_group_3D( &d, "SelMuon1_eta", "SelMuon1_corrected_pt", "SelMuon1_charge", "", eta_Arr, pt_Arr, charge_Arr);
  
  // FAST DEBUG
  return d;

  if(_category.find("DIMUON")!=std::string::npos)
    this->add_group_3D( &d, "SelMuon2_eta", "SelMuon2_corrected_pt", "SelMuon2_charge", "", eta_Arr, pt_Arr, charge_Arr);

  // DXY1,2 vs ISO1,2 vs CHARGE1,2
  unsigned int nbins_dxy = 25;
  unsigned int nbins_iso = 25;
  std::vector<float> dxy_Arr(nbins_dxy+1); 
  std::vector<float> iso_Arr(nbins_eta+1); 
  for(unsigned int i=0; i<nbins_dxy+1; i++) dxy_Arr[i] = -0.02 + i*(+0.02+0.02)/nbins_dxy;      
  for(unsigned int i=0; i<nbins_iso+1; i++) iso_Arr[i] =  0.0  + i*(1.0)/nbins_iso;      
  if((_category.find("SIGNAL")!=std::string::npos || _category.find("QCD")!=std::string::npos || _category.find("DIMUON")!=std::string::npos) && veto_LHE) 
    this->add_group_3D( &d, "SelMuon1_pfRelIso04_all", "SelMuon1_dxy", "SelMuon1_charge", "", iso_Arr, dxy_Arr, charge_Arr);
  if((_category.find("DIMUON")!=std::string::npos) && veto_LHE)
    this->add_group_3D( &d, "SelMuon2_pfRelIso04_all", "SelMuon2_dxy", "SelMuon2_charge", "", iso_Arr, dxy_Arr, charge_Arr);  

  // MT1 vs HT1 vs CHARGE1
  unsigned int nbins_mt  = 75;
  unsigned int nbins_hpt = 20;
  std::vector<float> mt_Arr(nbins_mt+1); 
  std::vector<float> hpt_Arr(nbins_hpt+1); 
  for(unsigned int i=0; i<nbins_mt+1; i++)   mt_Arr[i] = 0. + i*(150.-0.)/nbins_mt;
  for(unsigned int i=0; i<nbins_hpt+1; i++) hpt_Arr[i] = 0. + i*(100.-0.)/nbins_hpt;
  if((_category.find("SIGNAL")!=std::string::npos || _category.find("QCD")!=std::string::npos) && veto_LHE)
    this->add_group_3D( &d, "SelMuon1_corrected_MET_nom_mt", "SelMuon1_corrected_MET_nom_hpt", "SelMuon1_charge", "", mt_Arr, hpt_Arr, charge_Arr);

  // MET_PT vs MET_phi vs N_PVs
  unsigned int nbins_MET_pt  = 25;
  unsigned int nbins_MET_phi = 25;
  unsigned int nbins_nPVs = 70;
  std::vector<float> MET_pt_Arr(nbins_MET_pt+1); 
  std::vector<float> MET_phi_Arr(nbins_MET_phi+1); 
  std::vector<float> nPVs_Arr(nbins_nPVs+1); 
  for(unsigned int i=0; i<nbins_MET_pt+1; i++)  MET_pt_Arr[i]  = 0. + i*(100.-0.)/nbins_MET_pt;
  for(unsigned int i=0; i<nbins_MET_phi+1; i++) MET_phi_Arr[i] = -TMath::Pi() + i*(2.0*TMath::Pi())/nbins_MET_phi;
  for(unsigned int i=0; i<nbins_nPVs+1; i++)    nPVs_Arr[i]    = 0.0 + i*(70.0)/nbins_nPVs;
  if((_category.find("SIGNAL")!=std::string::npos || _category.find("QCD")!=std::string::npos || _category.find("DIMUON")!=std::string::npos) && veto_LHE)
    this->add_group_3D( &d, "MET_nom_pt", "MET_nom_phi", "nPVs", "", MET_pt_Arr, MET_phi_Arr, nPVs_Arr);

  // ZQT vs ZY vs ZMASS
  unsigned int nbins_RecoZ_qt   = 50;
  unsigned int nbins_RecoZ_y    = 30;
  unsigned int nbins_RecoZ_mass = 60;
  std::vector<float> RecoZ_qt_Arr(nbins_RecoZ_qt+1); 
  std::vector<float> RecoZ_y_Arr(nbins_RecoZ_y+1); 
  std::vector<float> RecoZ_mass_Arr(nbins_RecoZ_mass+1); 
  for(unsigned int i=0; i<nbins_RecoZ_qt+1; i++)   RecoZ_qt_Arr[i]   =   0. + i*(100.)/nbins_RecoZ_qt;      
  for(unsigned int i=0; i<nbins_RecoZ_y+1; i++)    RecoZ_y_Arr[i]    = -3.0 + i*(3.0 + 3.0)/nbins_RecoZ_y;      
  for(unsigned int i=0; i<nbins_RecoZ_mass+1; i++) RecoZ_mass_Arr[i] =  60. + i*(120.)/nbins_RecoZ_mass;      
  if(_category.find("DIMUON")!=std::string::npos && veto_LHE) 
    this->add_group_3D( &d, "SelRecoZ_corrected_qt", "SelRecoZ_corrected_y", "SelRecoZ_corrected_mass", "", RecoZ_qt_Arr,RecoZ_y_Arr,RecoZ_mass_Arr);    

  return d;
}

std::string muonHistos::check_modifier(const std::string& var_name){
  const std::string sub = _modifier+"All";
  size_t pos = var_name.find(_modifier);  
  if(pos==std::string::npos) return var_name;    
  std::string in = var_name;
  std::string ret = in.replace(pos, _modifier.length(), sub);  
  return ret;
}

void muonHistos::add_group_1D(RNode* d1,const std::string& var_name, const std::string& var_title, const std::vector<float>& arr){
  unsigned int nbins = arr.size()-1;
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

void muonHistos::add_group_2D(RNode* d1,
			      const std::string& var_name1, const std::string& var_name2, 
			      const std::string& var_title, 
			      const std::vector<float>& arrX,const std::vector<float>& arrY){
  unsigned int nbinsX = arrX.size()-1;
  unsigned int nbinsY = arrY.size()-1;
  std::vector<std::string> total = _syst_names;
  if(total.size()==0) total.emplace_back("");
  std::string var_name1_mod, var_name2_mod;

  if(_modifier==""){
    if(_verbose) std::cout << "muonHistos::run(): TH2weightsHelper<f,f,V> for variables " << var_name1 << "," << var_name2 << " (" << _weight << "*" << _syst_column << "[])" << std::endl;
    TH2weightsHelper w_helper(_category, std::string(var_name1+"_"+var_name2), var_title, nbinsX, arrX, nbinsY, arrY, total);         
    _h2Group.emplace_back(d1->Book<float,float,float,ROOT::VecOps::RVec<float>>(std::move(w_helper), {var_name1, var_name2, _weight, _syst_names.size()>0 ? _syst_column: "dummy"}) ); 
  }

  else{
    var_name1_mod = this->check_modifier(var_name1);
    var_name2_mod = this->check_modifier(var_name2);

    bool has_changed1 = (var_name1_mod!=var_name1);
    bool has_changed2 = (var_name2_mod!=var_name2);

    TH2varsHelper v_helper(_category, std::string(var_name1+"_"+var_name2), var_title, nbinsX, arrX,  nbinsY, arrY, total);

    if(has_changed1 && !has_changed2){
      if(_multi_cuts){
	if(_verbose) std::cout << "muonHistos::run(): TH2varsHelper<V,f,V> for variable " << var_name1_mod << "[]," << var_name2 << " (" << _weight << "*" << _syst_column << "[])" << std::endl;
	_h2Group.emplace_back(d1->Book<ROOT::VecOps::RVec<float>,float, ROOT::VecOps::RVec<float>>(std::move(v_helper), {var_name1_mod, var_name2, _syst_column }));
      }
      else{
	if(_verbose) std::cout << "muonHistos::run(): TH2varsHelper<V,f,f> for variable " << var_name1_mod << "[]," <<  var_name2 <<" (" << _weight << "*)" << std::endl;
	_h2Group.emplace_back(d1->Book<ROOT::VecOps::RVec<float>,float, float>(std::move(v_helper), {var_name1_mod, var_name2, _weight }));
      }
    }
    else if(has_changed1 && has_changed2){
      if(_multi_cuts){
	if(_verbose) std::cout << "muonHistos::run(): TH2varsHelper<V,V,V> for variable " << var_name1_mod << "[]," << var_name2_mod << "[] (" << _weight << "*" << _syst_column << "[])" << std::endl;
	_h2Group.emplace_back(d1->Book<ROOT::VecOps::RVec<float>,ROOT::VecOps::RVec<float>, ROOT::VecOps::RVec<float>>(std::move(v_helper), {var_name1_mod, var_name2_mod, _syst_column }));
      }
      else{
	if(_verbose) std::cout << "muonHistos::run(): TH2varsHelper<V,V,f> for variable " << var_name1_mod << "[]," <<  var_name2_mod << "[] (" << _weight << "*)" << std::endl;
	_h2Group.emplace_back(d1->Book<ROOT::VecOps::RVec<float>,ROOT::VecOps::RVec<float>, float>(std::move(v_helper), {var_name1_mod, var_name2_mod, _weight }));
      }
    }
    else if(!has_changed1 && has_changed2){
      if(_multi_cuts){
	if(_verbose) std::cout << "muonHistos::run(): TH2varsHelper<f,V,V> for variable " << var_name1 << "," << var_name2_mod << "[] (" << _weight << "*" << _syst_column << "[])" << std::endl;
	_h2Group.emplace_back(d1->Book<float,ROOT::VecOps::RVec<float>, ROOT::VecOps::RVec<float>>(std::move(v_helper), {var_name1, var_name2_mod, _syst_column }));
      }
      else{
	if(_verbose) std::cout << "muonHistos::run(): TH2varsHelper<f,V,f> for variable " << var_name1 << "," <<  var_name2_mod <<"[] (" << _weight << "*)" << std::endl;
	_h2Group.emplace_back(d1->Book<float,ROOT::VecOps::RVec<float>, float>(std::move(v_helper), {var_name1, var_name2_mod, _weight }));
      }
    }
    else if(!has_changed1 && !has_changed2){
      if(_multi_cuts){
	if(_verbose) std::cout << "muonHistos::run(): TH2varsHelper<f,f,V> for variable " << var_name1 << "," << var_name2 << " (" << _weight << "*" << _syst_column << "[])" << std::endl;
	_h2Group.emplace_back(d1->Book<float,float,ROOT::VecOps::RVec<float>>(std::move(v_helper), {var_name1, var_name2, _syst_column }));
      }
      else{
	if(_verbose) std::cout << "muonHistos::run(): TH2varsHelper<f,f,f> for variable " << var_name1 << "," << var_name2 << "(" << _weight << "*): DO NOTHING -- These are alike the nominal!" << std::endl;
	if(false) _h2Group.emplace_back(d1->Book<float,float,float>(std::move(v_helper), {var_name1, var_name2, _weight }));
      }
    }											 

  }

  return;
}


void muonHistos::add_group_3D(RNode* d1,
			      const std::string& var_name1, const std::string& var_name2, const std::string& var_name3,
			      const std::string& var_title, 
			      const std::vector<float>& arrX, const std::vector<float>& arrY, const std::vector<float>& arrZ
			      ){
  unsigned int nbinsX = arrX.size()-1;
  unsigned int nbinsY = arrY.size()-1;
  unsigned int nbinsZ = arrZ.size()-1;
  std::vector<std::string> total = _syst_names;
  if(total.size()==0) total.emplace_back("");
  std::string var_name1_mod, var_name2_mod, var_name3_mod;

  if(_modifier==""){
    if(_verbose) std::cout << "muonHistos::run(): TH3weightsHelper<f,f,f,V> for variables " << var_name1 << "," << var_name2 << "," << var_name3 << " (" << _weight << "*" << _syst_column << "[])" << std::endl;
    TH3weightsHelper w_helper(_category, std::string(var_name1+"_"+var_name2+"_"+var_name3), var_title, nbinsX, arrX, nbinsY, arrY, nbinsZ, arrZ, total);         
    _h3Group.emplace_back(d1->Book<float,float,float,float,ROOT::VecOps::RVec<float>>(std::move(w_helper), {var_name1, var_name2, var_name3, _weight, _syst_names.size()>0 ? _syst_column: "dummy"}) ); 
  }

  else {
    var_name1_mod = this->check_modifier(var_name1);
    var_name2_mod = this->check_modifier(var_name2);
    var_name3_mod = this->check_modifier(var_name3);

    bool has_changed1 = (var_name1_mod!=var_name1);
    bool has_changed2 = (var_name2_mod!=var_name2);
    bool has_changed3 = (var_name3_mod!=var_name3);

    TH3varsHelper v_helper(_category, std::string(var_name1+"_"+var_name2+"_"+var_name3), var_title, nbinsX, arrX,  nbinsY, arrY, nbinsZ, arrZ, total);

    if(has_changed1 && !has_changed2 && !has_changed3){
      if(_multi_cuts){
	if(_verbose) std::cout << "muonHistos::run(): TH3varsHelper<V,f,f,V> for variable " << var_name1_mod << "[]," << var_name2 << "," << var_name3 << " (" << _weight << "*" << _syst_column << "[])" << std::endl;
	_h3Group.emplace_back(d1->Book<ROOT::VecOps::RVec<float>,float, float, ROOT::VecOps::RVec<float>>(std::move(v_helper), {var_name1_mod, var_name2, var_name3, _syst_column }));
      }
      else{
	if(_verbose) std::cout << "muonHistos::run(): TH3varsHelper<V,f,f,f> for variable " << var_name1_mod << "[]," <<  var_name2 << "," << var_name3 << " (" << _weight << "*)" << std::endl;
	_h3Group.emplace_back(d1->Book<ROOT::VecOps::RVec<float>,float, float, float>(std::move(v_helper), {var_name1_mod, var_name2, var_name3, _weight }));
      }
    }
    else if(has_changed1 && has_changed2 && !has_changed3){
      if(_multi_cuts){
	if(_verbose) std::cout << "muonHistos::run(): TH3varsHelper<V,V,f,V> for variable " << var_name1_mod << "[]," << var_name2_mod << "[]," << var_name3 << " (" << _weight << "*" << _syst_column << "[])" << std::endl;
	_h3Group.emplace_back(d1->Book<ROOT::VecOps::RVec<float>, ROOT::VecOps::RVec<float>, float, ROOT::VecOps::RVec<float>>(std::move(v_helper), {var_name1_mod, var_name2_mod, var_name3, _syst_column }));
      }
      else{
	if(_verbose) std::cout << "muonHistos::run(): TH3varsHelper<V,V,f,f> for variable " << var_name1_mod << "[]," <<  var_name2_mod << "[]," << var_name3 << " (" << _weight << "*)" << std::endl;
	_h3Group.emplace_back(d1->Book<ROOT::VecOps::RVec<float>,ROOT::VecOps::RVec<float>, float, float>(std::move(v_helper), {var_name1_mod, var_name2_mod, var_name3, _weight }));
      }
    }
    else if(!has_changed1 && has_changed2 && !has_changed3){
      if(_multi_cuts){
	if(_verbose) std::cout << "muonHistos::run(): TH3varsHelper<f,V,f,V> for variable " << var_name1 << "," << var_name2_mod << "[]," << var_name3 << " (" << _weight << "*" << _syst_column << "[])" << std::endl;
	_h3Group.emplace_back(d1->Book<float,ROOT::VecOps::RVec<float>, float, ROOT::VecOps::RVec<float>>(std::move(v_helper), {var_name1, var_name2_mod, var_name3, _syst_column }));
      }
      else{
	if(_verbose) std::cout << "muonHistos::run(): TH3varsHelper<f,V,f,f> for variable " << var_name1 << "," <<  var_name2_mod <<"[]," << var_name3 << " (" << _weight << "*)" << std::endl;
	_h3Group.emplace_back(d1->Book<float,ROOT::VecOps::RVec<float>, float, float>(std::move(v_helper), {var_name1, var_name2_mod, var_name3, _weight }));
      }
    }
    else if(!has_changed1 && !has_changed2 && !has_changed3){
      if(_multi_cuts){
	if(_verbose) std::cout << "muonHistos::run(): TH3varsHelper<f,f,f,V> for variable " << var_name1 << "," << var_name2 << "," << var_name3 << " (" << _weight << "*" << _syst_column << "[])" << std::endl;
	_h3Group.emplace_back(d1->Book<float,float,float, ROOT::VecOps::RVec<float>>(std::move(v_helper), {var_name1, var_name2, var_name3, _syst_column }));
      }
      else{
	if(_verbose) std::cout << "muonHistos::run(): TH3varsHelper<f,f,f,f> for variable " << var_name1 << "," << var_name2 << "," << var_name3 << " (" << _weight << "*): DO NOTHING -- These are alike the nominal!" << std::endl;
	if(false) _h3Group.emplace_back(d1->Book<float,float,float,float>(std::move(v_helper), {var_name1, var_name2, var_name3, _weight }));
      }
    }
    else if(has_changed1 && !has_changed2 && has_changed3){
      if(_multi_cuts){
	if(_verbose) std::cout << "muonHistos::run(): TH3varsHelper<V,f,V,V> for variable " << var_name1_mod << "[]," << var_name2 << "," << var_name3_mod << " (" << _weight << "*" << _syst_column << "[])" << std::endl;
	_h3Group.emplace_back(d1->Book<ROOT::VecOps::RVec<float>,float, ROOT::VecOps::RVec<float>, ROOT::VecOps::RVec<float>>(std::move(v_helper), {var_name1_mod, var_name2, var_name3_mod, _syst_column }));
      }
      else{
	if(_verbose) std::cout << "muonHistos::run(): TH3varsHelper<V,f,V,f> for variable " << var_name1_mod << "[]," <<  var_name2 << "," << var_name3_mod << " (" << _weight << "*)" << std::endl;
	_h3Group.emplace_back(d1->Book<ROOT::VecOps::RVec<float>,ROOT::VecOps::RVec<float>, ROOT::VecOps::RVec<float>, float>(std::move(v_helper), {var_name1_mod, var_name2, var_name3_mod, _weight }));
      }
    }
    else if(has_changed1 && has_changed2 && has_changed3){
      if(_multi_cuts){
	if(_verbose) std::cout << "muonHistos::run(): TH3varsHelper<V,V,V,V> for variable " << var_name1_mod << "[]," << var_name2_mod << "[]," << var_name3_mod << " (" << _weight << "*" << _syst_column << "[])" << std::endl;
	_h3Group.emplace_back(d1->Book<ROOT::VecOps::RVec<float>,ROOT::VecOps::RVec<float>, ROOT::VecOps::RVec<float>, ROOT::VecOps::RVec<float>>(std::move(v_helper), {var_name1_mod, var_name2_mod, var_name3_mod, _syst_column }));
      }
      else{
	if(_verbose) std::cout << "muonHistos::run(): TH3varsHelper<V,V,V,f> for variable " << var_name1_mod << "[]," <<  var_name2_mod << "[]," << var_name3_mod << " (" << _weight << "*)" << std::endl;
	_h3Group.emplace_back(d1->Book<ROOT::VecOps::RVec<float>,ROOT::VecOps::RVec<float>, ROOT::VecOps::RVec<float>, float>(std::move(v_helper), {var_name1_mod, var_name2_mod, var_name3_mod, _weight }));
      }
    }
    else if(!has_changed1 && has_changed2 && has_changed3){
      if(_multi_cuts){
	if(_verbose) std::cout << "muonHistos::run(): TH3varsHelper<f,V,V,V> for variable " << var_name1 << "," << var_name2_mod << "[]," << var_name3_mod << " (" << _weight << "*" << _syst_column << "[])" << std::endl;
	_h3Group.emplace_back(d1->Book<float,ROOT::VecOps::RVec<float>, ROOT::VecOps::RVec<float>, ROOT::VecOps::RVec<float>>(std::move(v_helper), {var_name1, var_name2_mod, var_name3_mod, _syst_column }));
      }
      else{
	if(_verbose) std::cout << "muonHistos::run(): TH3varsHelper<f,V,V,f> for variable " << var_name1 << "," <<  var_name2_mod <<"[]," << var_name3_mod << " (" << _weight << "*)" << std::endl;
	_h3Group.emplace_back(d1->Book<float,ROOT::VecOps::RVec<float>, ROOT::VecOps::RVec<float>, float>(std::move(v_helper), {var_name1, var_name2_mod, var_name3_mod, _weight }));
      }
    }
    else if(!has_changed1 && !has_changed2 && has_changed3){
      if(_multi_cuts){
	if(_verbose) std::cout << "muonHistos::run(): TH3varsHelper<f,f,V,V> for variable " << var_name1 << "," << var_name2 << "," << var_name3_mod << " (" << _weight << "*" << _syst_column << "[])" << std::endl;
	_h3Group.emplace_back(d1->Book<float,float,ROOT::VecOps::RVec<float>, ROOT::VecOps::RVec<float>>(std::move(v_helper), {var_name1, var_name2, var_name3_mod, _syst_column }));
      }
      else{
	if(_verbose) std::cout << "muonHistos::run(): TH3varsHelper<f,f,V,f> for variable " << var_name1 << "," << var_name2 << "," << var_name3_mod << "[] (" << _weight << "*):" << std::endl;
	if(false) _h3Group.emplace_back(d1->Book<float,float,ROOT::VecOps::RVec<float>,float>(std::move(v_helper), {var_name1, var_name2, var_name3_mod, _weight }));
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
