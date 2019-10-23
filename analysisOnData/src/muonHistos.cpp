#include "interface/muonHistos.hpp"


RNode muonHistos::run(RNode d){
    
    auto d1 = d.Filter(_filter).Define("weight",_weight).Define("dummy", dummy, {"event"});

    std::vector<float> pTArr(101); 
    for(int i=0; i<101; i++) {
        pTArr[i] = 25. + i*(65.-25.)/100;
    }

    std::vector<float> etaArr(11); 
    for(int i=0; i<11; i++) {
      etaArr[i] = -2.5 + i*(2.5-(-2.5))/11;
    }
    
    std::vector<std::string> total = _syst_name;

    if(total.size()==0) total.emplace_back("");

    TH1weightsHelper helperPt(std::string("SelMuon_corrected_pt"),  std::string(" ; muon p_{T} (Rochester corr.); "), pTArr.size()-1, pTArr, total);

    TH1weightsHelper helperEta(std::string("SelMuon_eta"), std::string(" ; eta p_{T} (Rochester corr.); "), etaArr.size()-1, etaArr, total);
 
    TH2weightsHelper helperPtEta(std::string("SelMuon_PtEta"), std::string(" ; eta p_{T} (Rochester corr.); muon p_{T} (Rochester corr.)"), etaArr.size()-1, etaArr, pTArr.size()-1, pTArr, total);

    auto hpT = d1.Book<float,  float, ROOT::VecOps::RVec<float>>(std::move(helperPt), {"SelMuon_corrected_pt", "weight", _syst_name.size()>0 ? _syst_weight: "dummy"});

    auto hEta = d1.Book<float,  float, ROOT::VecOps::RVec<float>>(std::move(helperEta), {"SelMuon_eta", "weight", _syst_name.size()>0 ? _syst_weight: "dummy"});
    
    auto hPtEta = d1.Book<float,  float, float, ROOT::VecOps::RVec<float>>(std::move(helperPtEta), {"SelMuon_eta", "SelMuon_corrected_pt", "weight", _syst_name.size()>0 ? _syst_weight: "dummy"});
    
    

    _h1Group.emplace_back(hpT);
    _h1Group.emplace_back(hEta);
    _h2Group.emplace_back(hPtEta);

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
