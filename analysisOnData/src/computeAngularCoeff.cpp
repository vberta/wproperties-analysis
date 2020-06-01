#include "interface/computeAngularCoeff.hpp"


RNode computeAngularCoeff::run(RNode d){

  std::vector<unsigned int> coeffs = {0,1,2,3,4,9};

  auto prod     = [](float x, float y)->float{ return x*y; };
  auto prodErr  = [](float x, float y)->float{ return x*x*y; };

  RNode d_start = d;

  if(_syst_names.size()==0){
    for(auto c : coeffs){
      auto d_post = d_start
	.Define("weight_test_"+_category+"_A"+std::to_string(c),    prod,    {"test_A"+std::to_string(c), _weight} )
	.Define("weight_testErr_"+_category+"_A"+std::to_string(c), prodErr, {"test_A"+std::to_string(c), _weight});
      d_start = d_post;
    }
    for(auto c : coeffs){
      std::string hname = (c<9 ? _category+"_A"+std::to_string(c) : _category+"_MC");
      auto hc    =  d_start.Histo2D({ hname.c_str(),         "", int(_xbins.size()-1), _xbins.data() , int(_ybins.size()-1), _ybins.data()}, 
				    "GenV_"+_leptonType+"_absy", "GenV_"+_leptonType+"_qt", "weight_test_"+_category+"_A"+std::to_string(c));    
      auto hcErr =  d_start.Histo2D({ (hname+"Err").c_str(), "", int(_xbins.size()-1), _xbins.data() , int(_ybins.size()-1), _ybins.data()}, 
				    "GenV_"+_leptonType+"_absy", "GenV_"+_leptonType+"_qt", "weight_testErr_"+_category+"_A"+std::to_string(c));    
      _h2List.emplace_back( hc );
      _h2List.emplace_back( hcErr );
    }
    return d_start;
  }

  std::vector<float> xbins;
  for(auto b : _xbins) xbins.push_back(float(b));
  std::vector<float> ybins;
  for(auto b : _ybins) ybins.push_back(float(b));

  for(auto c : coeffs){
    std::string hname = (c<9 ? _category+"_A"+std::to_string(c) : _category+"_MC");
    std::vector<std::string> total = _syst_names;
    if(total.size()==0) total.emplace_back("");
    TH2weightsHelper w_helper(hname, "GenV_"+_leptonType+"_absy_GenV_"+_leptonType+"_qt", "", int(_xbins.size()-1), xbins , int(_ybins.size()-1), ybins, total);         
    _h2Group.emplace_back(d_start.Book<float,float,float,ROOT::VecOps::RVec<float>>(std::move(w_helper), {"GenV_"+_leptonType+"_absy", "GenV_"+_leptonType+"_qt", "weight_test_"+_category+"_A"+std::to_string(c), _syst_column}) ); 
    //TH2weightsHelper w_helperErr(hname+"Err", std::string("GenV_"+_leptonType+"_absy_GenV_"+_leptonType+"_qt"), "", int(_xbins.size()-1), xbins , int(_ybins.size()-1), ybins, total);         
    //_h2Group.emplace_back(d_start.Book<float,float,float,ROOT::VecOps::RVec<float>>(std::move(w_helper), {"GenV_"+_leptonType+"_absy", "GenV_"+_leptonType+"_qt", "weight_testErr_"+_category+"_A"+std::to_string(c), _syst_column}) ); 
  }
  
  return d_start;
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
