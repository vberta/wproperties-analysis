#include "interface/getCompVars.hpp"


RNode getCompVars::run(RNode d){   
  
  RNode d_start = d;

  std::string postfix = "FIX";

  // muon1,2 corrected pt systs
  if( _muon_systs.size()>0 ){
    std::vector<std::string> mus = {"1"};
    if(_idx2!="") mus.push_back("2");
    for(unsigned int imu = 0 ; imu<mus.size(); imu++){
      std::string mu = mus[imu];
      ROOT::Detail::RDF::ColumnNames_t new_cols;
      for(unsigned int i=0 ; i < _muon_systs.size(); i++){   
	std::string new_col = "SelMuon"+mu+"_"+_muon_systs[i]+"_pt";
	auto d_post = d_start.Define(new_col, getFromIdx, {"Muon_"+_muon_systs[i]+"_pt", mu=="1"?_idx1:_idx2});
	d_start = d_post;
	new_cols.push_back("SelMuon"+mu+"_"+_muon_systs[i]+"_pt");
      }
      auto d_post = d_start.Define("SelMuon"+mu+"_correctedAll_pt", getRVec_FFtoV, new_cols);
      d_start = d_post;
    }
  }

  // MET systsAll
  else if( _MET_systs.size()>0 ){

    ///// FIX
    if(postfix=="FIX"){
      std::cout << "getCompVars(): applying FIX for MET systematics" << std::endl;
      auto rescaler_pt = [](float pt, float pt_nom, float pt_syst)->float{
	return pt_nom>0. ? pt*(pt_syst/pt_nom) : pt_nom ;
      };
      auto rescaler_phi = [](float phi, float phi_nom, float phi_syst)->float{
	float ret = phi + (phi_nom-phi_syst) ;
	if(ret > TMath::Pi())  return ret - 2*TMath::Pi(); 
	if(ret < -TMath::Pi()) return ret + 2*TMath::Pi(); 
	return ret;
      };
      for(unsigned int i=0 ; i < _MET_systs.size(); i++){
	auto d_post = d_start
	  .Define("MET_"+_MET_systs[i]+postfix+"_pt",  rescaler_pt,  {"MET_pt", "MET_nom_pt", "MET_"+_MET_systs[i]+"_pt"})
	  .Define("MET_"+_MET_systs[i]+postfix+"_phi", rescaler_phi, {"MET_phi", "MET_nom_phi", "MET_"+_MET_systs[i]+"_phi"});
	d_start = d_post;	
      }
    }
    

    ROOT::Detail::RDF::ColumnNames_t new_cols_pt, new_cols_phi;
    for(unsigned int i=0 ; i < _MET_systs.size(); i++){
      new_cols_pt.push_back( "MET_"+_MET_systs[i]+postfix+"_pt");
      new_cols_phi.push_back("MET_"+_MET_systs[i]+postfix+"_phi");
    }

    RNode d_post = d_start;
    switch(_MET_systs.size()){
    case 2:
      d_post = d_start
	.Define("MET_nomAll_pt",  getRVec_FFtoV, new_cols_pt)
	.Define("MET_nomAll_phi", getRVec_FFtoV, new_cols_phi);
      break;
    case 4:
      d_post = d_start
	.Define("MET_nomAll_pt",  getRVec_FFFFtoV, new_cols_pt)
	.Define("MET_nomAll_phi", getRVec_FFFFtoV, new_cols_phi);
      break;      
    case 6:
      d_post = d_start
	.Define("MET_nomAll_pt",  getRVec_FFFFFFtoV, new_cols_pt)
	.Define("MET_nomAll_phi", getRVec_FFFFFFtoV, new_cols_phi);
      break;            
    default:
      std::cout << "getCompVars(): " << _MET_systs.size() << " MET systs not supported" << std::endl;
      break;
    }
    d_start = d_post;
  }

  std::vector<std::string> compVars = {};

  // Composite muon-MET variables
  compVars = {"mt", "hpt"};
  for(unsigned int i=0; i<compVars.size(); i++){

    std::string compVar = compVars[i];
    float (*func)(float,float,float,float) = nullptr;
    if( compVar=="mt" ) func = W_mt;
    if( compVar=="hpt") func = W_hpt;
    
    std::vector<std::string> mus = {"1"};
    if(_idx2!="") mus.push_back("2");
    for(unsigned int imu = 0 ; imu<mus.size(); imu++){
      std::string mu = mus[imu];

      if(_muon_systs.size()==0 && _MET_systs.size()==0){      
	std::string new_col     = "SelMuon"+mu+"_corrected_MET_nom_"+compVar;
	std::string mu_pt_col   = "SelMuon"+mu+"_corrected_pt";
	std::string mu_phi_col  = "SelMuon"+mu+"_phi";      
	std::string met_pt_col  = "MET_nom_pt";
	std::string met_phi_col = "MET_nom_phi";
	if(postfix=="FIX"){
	  met_pt_col  = "MET_pt";
	  met_phi_col = "MET_phi";
	}
	auto d_post = d_start.Define(new_col, func, {mu_pt_col, mu_phi_col, met_pt_col, met_phi_col});
	d_start = d_post;
      }
      else{ 
	bool im =  _muon_systs.size()>0;     
	unsigned int syst_size = im ? _muon_systs.size() : _MET_systs.size();
	std::string new_colAll = im ? "SelMuon"+mu+"_correctedAll_MET_nom_"+compVar : "SelMuon"+mu+"_corrected_MET_nomAll_"+compVar;
	
	ROOT::Detail::RDF::ColumnNames_t new_cols;
	for(unsigned int i=0 ; i < syst_size; i++){
	  std::string new_col     = "SelMuon"+mu+"_"+(im?_muon_systs[i]:"corrected")+"_MET_"+(im?"nom":_MET_systs[i])+"_"+compVar;
	  std::string mu_pt_col   = "SelMuon"+mu+"_"+(im?_muon_systs[i]:"corrected")+"_pt";
	  std::string mu_phi_col  = "SelMuon"+mu+"_phi";
	  std::string met_pt_col  = "MET_"+(im?"nom":_MET_systs[i])+"_pt";
	  std::string met_phi_col = "MET_"+(im?"nom":_MET_systs[i])+"_phi";
	  if(postfix=="FIX"){
	    met_pt_col  = "MET"+(im?"":"_"+_MET_systs[i]+postfix)+"_pt";
	    met_phi_col = "MET"+(im?"":"_"+_MET_systs[i]+postfix)+"_phi";
	  }
	  new_cols.push_back(new_col);
	  auto d_post = d_start.Define(new_col, func, {mu_pt_col, mu_phi_col, met_pt_col, met_phi_col});
	  d_start = d_post;
	}
	
	RNode d_post = d_start;
 	switch(syst_size){
	case 2:
	  d_post = d_start.Define(new_colAll, getRVec_FFtoV, new_cols);
	  break;
	case 4:
	  d_post = d_start.Define(new_colAll, getRVec_FFFFtoV, new_cols);
	  break;      
	case 6:
	  d_post = d_start.Define(new_colAll, getRVec_FFFFFFtoV, new_cols);
	  break;            
	default:
	  break;
	}
	d_start = d_post;
      }
    }
  } // END Composite muon-MET variables

  if(_idx2=="") return d_start;

  // Composite muon-muon-MET variables
  compVars = {"Wlike_mt"};
  for(unsigned int i=0; i<compVars.size(); i++){

    std::string compVar = compVars[i];
    float (*func)(float,float,float,float,float,float) = nullptr;
    if( compVar=="Wlike_mt" ) func = Wlike_mt;
    
    std::vector<std::string> mus = {"1","2"};
    for(unsigned int imu = 0 ; imu<mus.size(); imu++){
      std::string mu1 = mus[imu];
      std::string mu2 = mus[imu==0?1:0];

      if(_muon_systs.size()==0 && _MET_systs.size()==0){      
	std::string new_col     = "SelMuon"+mu1+"_corrected_MET_nom_"+compVar;
	std::string mu1_pt_col  = "SelMuon"+mu1+"_corrected_pt";
	std::string mu1_phi_col = "SelMuon"+mu1+"_phi";      
	std::string mu2_pt_col  = "SelMuon"+mu2+"_corrected_pt";
	std::string mu2_phi_col = "SelMuon"+mu2+"_phi";      
	std::string met_pt_col  = "MET_nom_pt";
	std::string met_phi_col = "MET_nom_phi";
	if(postfix=="FIX"){
	  met_pt_col  = "MET_pt";
	  met_phi_col = "MET_phi";
	}
	auto d_post = d_start.Define(new_col, func, {mu1_pt_col, mu1_phi_col, mu2_pt_col, mu2_phi_col, met_pt_col, met_phi_col});
	d_start = d_post;
      }
      else{ 
	bool im =  _muon_systs.size()>0;     
	unsigned int syst_size = im ? _muon_systs.size() : _MET_systs.size();
	std::string new_colAll = im ? "SelMuon"+mu1+"_correctedAll_MET_nom_"+compVar : "SelMuon"+mu1+"_corrected_MET_nomAll_"+compVar;
	
	ROOT::Detail::RDF::ColumnNames_t new_cols;
	for(unsigned int i=0 ; i < syst_size; i++){
	  std::string new_col     = "SelMuon"+mu1+"_"+(im?_muon_systs[i]:"corrected")+"_MET_"+(im?"nom":_MET_systs[i])+"_"+compVar;
	  std::string mu1_pt_col  = "SelMuon"+mu1+"_"+(im?_muon_systs[i]:"corrected")+"_pt";
	  std::string mu1_phi_col = "SelMuon"+mu1+"_phi";
	  std::string mu2_pt_col  = "SelMuon"+mu2+"_"+(im?_muon_systs[i]:"corrected")+"_pt";
	  std::string mu2_phi_col = "SelMuon"+mu2+"_phi";
	  std::string met_pt_col  = "MET_"+(im?"nom":_MET_systs[i])+"_pt";
	  std::string met_phi_col = "MET_"+(im?"nom":_MET_systs[i])+"_phi";
	  if(postfix=="FIX"){
	    met_pt_col  = "MET"+(im?"":"_"+_MET_systs[i]+postfix)+"_pt";
	    met_phi_col = "MET"+(im?"":"_"+_MET_systs[i]+postfix)+"_phi";
	  }
	  new_cols.push_back(new_col);
	  auto d_post = d_start.Define(new_col, func, {mu1_pt_col, mu1_phi_col, mu2_pt_col, mu2_phi_col, met_pt_col, met_phi_col});
	  d_start = d_post;
	}
	
	RNode d_post = d_start;
	switch(syst_size){
	case 2:
	  d_post = d_start.Define(new_colAll, getRVec_FFtoV, new_cols);
	  break;
	case 4:
	  d_post = d_start.Define(new_colAll, getRVec_FFFFtoV, new_cols);
	  break;      
	case 6:
	  d_post = d_start.Define(new_colAll, getRVec_FFFFFFtoV, new_cols);
	  break;            
	default:
	  break;
	}
	d_start = d_post;
      }
    }
  } // END Composite muon-muon-MET variables

  // Composite muon-muon variables
  compVars = {"qt","mass","y"};
  for(unsigned int i=0; i<compVars.size(); i++){

    std::string compVar = compVars[i];
    float (*func4)(float,float,float,float) = nullptr;
    float (*func6)(float,float,float,float,float,float) = nullptr;
    if( compVar=="qt" )   func4 = Z_qt;
    if( compVar=="y" )    func4 = Z_y;
    if( compVar=="mass" ) func6 = Z_mass;    

    if(_muon_systs.size()==0 && _MET_systs.size()==0){      
      std::string new_col = "SelRecoZ_corrected_"+compVar;
      ROOT::Detail::RDF::ColumnNames_t in_cols;
      if(compVar=="qt"){
	in_cols.push_back("SelMuon1_corrected_pt");
	in_cols.push_back("SelMuon1_phi");            
	in_cols.push_back("SelMuon2_corrected_pt");
	in_cols.push_back("SelMuon2_phi");
	auto d_post = d_start.Define(new_col,func4, in_cols);
	d_start = d_post;
      }
      else if(compVar=="y"){
	in_cols.push_back("SelMuon1_corrected_pt");
	in_cols.push_back("SelMuon1_eta");      
	in_cols.push_back("SelMuon2_corrected_pt");     
	in_cols.push_back("SelMuon2_eta");
	auto d_post = d_start.Define(new_col,func4, in_cols);
	d_start = d_post;
      }
      else if(compVar=="mass"){
	in_cols.push_back("SelMuon1_corrected_pt");
	in_cols.push_back("SelMuon1_eta");      
	in_cols.push_back("SelMuon1_phi");            
	in_cols.push_back("SelMuon2_corrected_pt");     
	in_cols.push_back("SelMuon2_eta");
	in_cols.push_back("SelMuon2_phi");            
	auto d_post = d_start.Define(new_col,func6, in_cols);
	d_start = d_post;
      }
    }
    else if(_muon_systs.size()>0 && _MET_systs.size()==0){ 
      unsigned int syst_size = _muon_systs.size();
      std::string new_colAll = "SelRecoZ_correctedAll_"+compVar;
      ROOT::Detail::RDF::ColumnNames_t new_cols;
      for(unsigned int i=0 ; i < syst_size; i++){
	std::string new_col    = "SelRecoZ_"+_muon_systs[i]+"_"+compVar;
	std::string mu1_pt_col = "SelMuon1_"+_muon_systs[i]+"_pt";
	std::string mu2_pt_col = "SelMuon2_"+_muon_systs[i]+"_pt";
	ROOT::Detail::RDF::ColumnNames_t in_cols;
	if(compVar=="qt"){
	  in_cols.push_back(mu1_pt_col);
	  in_cols.push_back("SelMuon1_phi");            
	  in_cols.push_back(mu2_pt_col);
	  in_cols.push_back("SelMuon2_phi");
	  auto d_post = d_start.Define(new_col,func4, in_cols);
	  d_start = d_post;
	}
	else if(compVar=="y"){
	  in_cols.push_back(mu1_pt_col);
	  in_cols.push_back("SelMuon1_eta");      
	  in_cols.push_back(mu2_pt_col);     
	  in_cols.push_back("SelMuon2_eta");
	  auto d_post = d_start.Define(new_col,func4, in_cols);
	  d_start = d_post;
	}
	else if(compVar=="mass"){
	  in_cols.push_back(mu1_pt_col);
	  in_cols.push_back("SelMuon1_eta");      
	  in_cols.push_back("SelMuon1_phi");            
	  in_cols.push_back(mu2_pt_col);     
	  in_cols.push_back("SelMuon2_eta");
	  in_cols.push_back("SelMuon2_phi");            
	  auto d_post = d_start.Define(new_col,func6, in_cols);
	  d_start = d_post;
	}
	new_cols.push_back(new_col);
      }	
      RNode d_post = d_start;
      switch(syst_size){
      case 2:
	d_post = d_start.Define(new_colAll, getRVec_FFtoV, new_cols);
	break;
      case 4:
	d_post = d_start.Define(new_colAll, getRVec_FFFFtoV, new_cols);
	break;      
      case 6:
	d_post = d_start.Define(new_colAll, getRVec_FFFFFFtoV, new_cols);
	break;            
      default:
	break;
      }
      d_start = d_post;       
    }  
  } //END Composite muon-muon variable
  

  return d_start;
}

std::vector<ROOT::RDF::RResultPtr<TH1D>> getCompVars::getTH1(){ 
    return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> getCompVars::getTH2(){ 
    return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> getCompVars::getTH3(){ 
    return _h3List;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> getCompVars::getGroupTH1(){ 
  return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> getCompVars::getGroupTH2(){ 
  return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> getCompVars::getGroupTH3(){ 
  return _h3Group;
}

void getCompVars::reset(){
    _h1List.clear();
    _h2List.clear();
    _h3List.clear();

    _h1Group.clear();
    _h2Group.clear();
    _h3Group.clear();
}
