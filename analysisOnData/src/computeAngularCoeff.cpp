#include "interface/computeAngularCoeff.hpp"


RNode computeAngularCoeff::run(RNode d){

  for(unsigned int c = 0; c<10; c++){
    std::string hname = c<9 ? _category+"_A"+std::to_string(c) : _category+"_MC"; 
    auto h =  d
      .Histo2D({ hname.c_str(), "", 
	    _histo->GetNbinsX(), _histo->GetXaxis()->GetXmin(),  _histo->GetXaxis()->GetXmax(),
	    _histo->GetNbinsY(), _histo->GetYaxis()->GetXmin(),  _histo->GetYaxis()->GetXmax()
	    }, "GenV_"+_leptonType+"_absy", "GenV_"+_leptonType+"_qt", "weight_test_A"+std::to_string(c));
    _h2List.emplace_back( h );
  }
  
  return d;
}

std::vector<ROOT::RDF::RResultPtr<TH1D>> computeAngularCoeff::getTH1(){ 
    return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> computeAngularCoeff::getTH2(){ 
    return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> computeAngularCoeff::getTH3(){ 
    return _h3List;
}

std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> computeAngularCoeff::getGroupTH1(){ 
  return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> computeAngularCoeff::getGroupTH2(){ 
  return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> computeAngularCoeff::getGroupTH3(){ 
  return _h3Group;
}

void computeAngularCoeff::reset(){
    
    _h1List.clear();
    _h2List.clear();
    _h3List.clear();

    _h1Group.clear();
    _h2Group.clear();
    _h3Group.clear();

}
