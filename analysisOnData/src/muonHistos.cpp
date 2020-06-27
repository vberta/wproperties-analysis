#include "interface/muonHistos.hpp"


RNode muonHistos::run(RNode d){
    
    auto d1 = d.Filter(_filter).Define("weight",_weight);    
    if(_hcat == HistoCategory::Nominal)
      return bookNominalhistos(d1);
    else if(_hcat == HistoCategory::Nominal)
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

RNode muonHistos::bookptCorrectedhistos(RNode df) {
  TH1weightsHelper helper_Ptup(std::string("Mu1_pt_correctedUp"), std::string(" ; muon p_{T} corrected Up(Rochester corr.); "), 100, _pTArr, _syst_name);
 _h1Group.emplace_back(df.Book<float, float, ROOT::VecOps::RVec<float>>(std::move(helper_Ptup), {"Mu1_pt_correctedUp", "weight", _syst_weight}));

  TH1weightsHelper helper_Ptdown(std::string("Mu1_pt_correctedDown"), std::string(" ; muon p_{T} corrected Down(Rochester corr.); "), 100, _pTArr, _syst_name);
  _h1Group.emplace_back(df.Book<float, float, ROOT::VecOps::RVec<float>>(std::move(helper_Ptdown), {"Mu1_pt_correctedDown", "weight", _syst_weight}));


  TH1weightsHelper helper_MTup(std::string("MT_correctedUp"), std::string(" ; M_{T} (Rochester corr./smear MET); "), 100, _MTArr, _syst_name);
  _h1Group.emplace_back(df.Book<float, float, ROOT::VecOps::RVec<float>>(std::move(helper_MTup), {"MT_correctedUp", "weight", _syst_weight}));

  TH1weightsHelper helper_MTdown(std::string("MT_correctedDown"), std::string(" ; M_{T} (Rochester corr./smear MET); "), 100, _MTArr, _syst_name);
  _h1Group.emplace_back(df.Book<float, float, ROOT::VecOps::RVec<float>>(std::move(helper_MTdown), {"MT_correctedDown", "weight", _syst_weight}));
  
  return df;
}

RNode muonHistos::bookJMEvarhistos(RNode df) {
  //jer
  TH1weightsHelper helper_MTjerup(std::string("MT_jerUp"), std::string(" ; M_{T} (Rochester corr./smear MET); "), 100, _MTArr, _syst_name);
  _h1Group.emplace_back(df.Book<float, float, ROOT::VecOps::RVec<float>>(std::move(helper_MTjerup), {"MT_jerUp", "weight", _syst_weight}));

  TH1weightsHelper helper_MTjerdown(std::string("MT_jerDown"), std::string(" ; M_{T} (Rochester corr./smear MET); "), 100, _MTArr, _syst_name);
  _h1Group.emplace_back(df.Book<float, float, ROOT::VecOps::RVec<float>>(std::move(helper_MTjerdown), {"MT_jerDown", "weight", _syst_weight}));
  
  //jes
  TH1weightsHelper helper_MTjesup(std::string("MT_jesTotalUp"), std::string(" ; M_{T} (Rochester corr./smear MET); "), 100, _MTArr, _syst_name);
  _h1Group.emplace_back(df.Book<float, float, ROOT::VecOps::RVec<float>>(std::move(helper_MTjesup), {"MT_jesTotalUp", "weight", _syst_weight}));

  TH1weightsHelper helper_MTjesdown(std::string("MT_jesTotalDown"), std::string(" ; M_{T} (Rochester corr./smear MET); "), 100, _MTArr, _syst_name);
  _h1Group.emplace_back(df.Book<float, float, ROOT::VecOps::RVec<float>>(std::move(helper_MTjesdown), {"MT_jesTotalDown", "weight", _syst_weight}));

  //jes
  TH1weightsHelper helper_MTuenup(std::string("MT_unclustEnUp"), std::string(" ; M_{T} (Rochester corr./smear MET); "), 100, _MTArr, _syst_name);
  _h1Group.emplace_back(df.Book<float, float, ROOT::VecOps::RVec<float>>(std::move(helper_MTuenup), {"MT_unclustEnUp", "weight", _syst_weight}));

  TH1weightsHelper helper_MTuendown(std::string("MT_unclustEnDown"), std::string(" ; M_{T} (Rochester corr./smear MET); "), 100, _MTArr, _syst_name);
  _h1Group.emplace_back(df.Book<float, float, ROOT::VecOps::RVec<float>>(std::move(helper_MTuendown), {"MT_unclustEnDown", "weight", _syst_weight}));

  return df;
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
