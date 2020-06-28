#include "interface/muonHistos.hpp"


RNode muonHistos::run(RNode d){
    
    auto d1 = d.Filter(_filter).Define("weight",_weight);    
    if(_hcat == HistoCategory::Nominal)
      return bookNominalhistos(d1);
    else if(_hcat == HistoCategory::Corrected)
      return bookptCorrectedhistos(d1);
    else if(_hcat == HistoCategory::JME)
      return bookJMEvarhistos(d1);
    else 
      std::cout << "Warning!! Histocategory undefined!!\n";

    return d1;
}

RNode muonHistos::bookNominalhistos(RNode df) {
  TH1weightsHelper helperPt(std::string("Mu1_pt"), std::string(" ; muon p_{T} (Rochester corr.); "), 100, _pTArr, _syst_name);
  auto hpT = df.Book<float, float, ROOT::VecOps::RVec<float>>(std::move(helperPt), {"Mu1_pt", "weight", _syst_weight});
  _h1Group.emplace_back(hpT);

  TH1weightsHelper helperEta(std::string("Mu1_eta"), std::string(" ; muon #{eta}; "), 48, _etaArr, _syst_name);
  auto heta = df.Book<float, float, ROOT::VecOps::RVec<float>>(std::move(helperEta), {"Mu1_eta", "weight", _syst_weight});
  _h1Group.emplace_back(heta);

  TH1weightsHelper helperMT(std::string("MT"), std::string(" ; M_{T} (Rochester corr./smear MET); "), 100, _MTArr, _syst_name);
  auto hMt = df.Book<float, float, ROOT::VecOps::RVec<float>>(std::move(helperMT), {"MT", "weight", _syst_weight});
  _h1Group.emplace_back(hMt);
  
  return df;
}
//muon pt corrections affect both pt and MT
RNode muonHistos::bookptCorrectedhistos(RNode df) {
  TH1weightsHelper helper_Pt(std::string("Mu1_pt_" + _colvar), std::string(" ; muon p_{T} (Rochester corr.); "), 100, _pTArr, _syst_name);
 _h1Group.emplace_back(df.Book<float, float, ROOT::VecOps::RVec<float>>(std::move(helper_Pt), {"Mu1_pt_" + _colvar, "weight", _syst_weight}));

  TH1weightsHelper helper_MT(std::string("MT_" + _colvar), std::string(" ; M_{T} (Rochester corr./smear MET); "), 100, _MTArr, _syst_name);
  _h1Group.emplace_back(df.Book<float, float, ROOT::VecOps::RVec<float>>(std::move(helper_MT), {"MT_" + _colvar, "weight", _syst_weight}));
  return df;
}
//jme variations affect only MT
RNode muonHistos::bookJMEvarhistos(RNode df) {
  TH1weightsHelper helper_MT(std::string("MT_" + _colvar), std::string(" ; M_{T} (Rochester corr./smear MET); "), 100, _MTArr, _syst_name);
  _h1Group.emplace_back(df.Book<float, float, ROOT::VecOps::RVec<float>>(std::move(helper_MT), {"MT_" + _colvar, "weight", _syst_weight}));
  return df;
}

void muonHistos::setAxisarrays() {
  for(int i=0; i<101; i++) 
    _pTArr[i] = 25. + i*(65.-25.)/100;
  for(int i=0; i<49; i++) 
    _etaArr[i] = -2.4 + i*(4.8)/48;//eta -2.4 to 2.4
  for(int i=0; i<101; i++) 
    _MTArr[i] = i;
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
