#include "interface/muonHistos.hpp"


RNode muonHistos::run(RNode d){
    
  auto d1 = d.Filter(_cut);

  unsigned int nbins_pt = 100;
  std::vector<float> pt_Arr(nbins_pt+1); 
  for(unsigned int i=0; i<nbins_pt+1; i++) pt_Arr[i] = 25. + i*(65.-25.)/nbins_pt;
    
  std::vector<std::string> total = _syst_name;
  if(total.size()==0) total.emplace_back("");
  
  std::string hname = "";
  hname = "Muon1_corrected_pt";
  TH1weightsHelper w_helper_corrected_pt(hname, std::string(" ; muon p_{T} (Rochester corr.); "), nbins_pt, pt_Arr, total);         
  _h1Group.emplace_back(d1.Book<float,float,ROOT::VecOps::RVec<float>>(std::move(w_helper_corrected_pt), {hname, _weight, _syst_name.size()>0 ? _syst_weight: "dummy"}) );  

  /*
  hname = "Muon1_pt";
  if(_var_modifier.find("corrected")!=std::string::npos){
    hname = ("Muon1_"+_var_modifier+"_pt");
    applies = true;
  }
  TH1weightsHelper w_helper_pt(hname, std::string(" ; muon p_{T}; "), nbins_pt, pt_Arr, total);
  if(save_all || applies){
    _h1Group.emplace_back(d1.Book<float,float,ROOT::VecOps::RVec<float>>(std::move(w_helper_corrected_pt), {hname, _weight, _syst_name.size()>0 ? _syst_weight: "dummy"}) );
    applies = false;
  } 
  */ 

  return d1;
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
