#include "interface/applyReweightZ.hpp"


RNode applyReweightZ::run(RNode d){
  
  auto getWeightQt = [this](float qt)->float {
    int bin = _hQt->FindBin(qt);
    if( _hQt->IsBinOverflow(bin) ) return _hQt->GetBinContent(_lastBinQt);
    else if( _hQt->IsBinUnderflow(bin) ) return _hQt->GetBinContent(1);
    else return _hQt->GetBinContent(bin);
  };
  auto getWeightY = [this](float y)->float {
    float absy = TMath::Abs(y);
    int bin = _hY->FindBin(absy);
    if( _hY->IsBinOverflow(bin) ) return _hY->GetBinContent(_lastBinY);
    else if( _hY->IsBinUnderflow(bin) ) return _hY->GetBinContent(1);
    else return _hY->GetBinContent(bin);
  };
  
  RNode d_start = d;
  if(_hQt!=nullptr){
    auto d_post = d_start.Define("reweight_"+_genV+"_qt", getWeightQt, {"GenV_"+_leptonType+"_qt"});
    d_start = d_post;
  }
  if(_hY!=nullptr){
    auto d_post = d_start.Define("reweight_"+_genV+"_y", getWeightY, {"GenV_"+_leptonType+"_y"});
    d_start = d_post;
  }

  return d_start;
}

std::vector<ROOT::RDF::RResultPtr<TH1D>> applyReweightZ::getTH1(){ 
    return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> applyReweightZ::getTH2(){ 
    return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> applyReweightZ::getTH3(){ 
    return _h3List;
}

std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> applyReweightZ::getGroupTH1(){ 
  return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> applyReweightZ::getGroupTH2(){ 
  return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> applyReweightZ::getGroupTH3(){ 
  return _h3Group;
}

void applyReweightZ::reset(){
    
    _h1List.clear();
    _h2List.clear();
    _h3List.clear();

    _h1Group.clear();
    _h2Group.clear();
    _h3Group.clear();

}
