#include "interface/getCoeffVars.hpp"


RNode getCoeffVars::run(RNode d){

  auto abs = [](float x)->float{ return TMath::Abs(x); };
 
  RNode d_start = d;

  RNode d_post = d_start
    .Define("GenV_"+_leptonType+"_absy", abs, {"GenV_"+_leptonType+"_y"});
  d_start = d_post;

  // BUG FIX
  auto fixCS = [](float phiold, float y)->float{
    if(y>=0.) return phiold;
    if ( phiold >=0.) return +TMath::Pi()-phiold;
    else return -TMath::Pi()-phiold;
  };
  d_post = d_start.Define("GenV_"+_leptonType+"_CSphiFIX", fixCS, {"GenV_"+_leptonType+"_CSphi", "GenV_"+_leptonType+"_y"});
  d_start = d_post;
  
  for(unsigned int c = 0; c<10; c++){
    auto tester = [c](float cos, float phi)->float{
      float val = 1.0;
      switch(c){
      case 0:
	val = 20./3.*(0.5*(1-3*cos*cos)) + 2./3.;
	break;
      case 1:
	val = 5.*2.*TMath::Sqrt(1-cos*cos)*cos*TMath::Cos(phi);
	break;
      case 2:
	val = 10.*(1-cos*cos)*TMath::Cos(2*phi);
	break;
      case 3:
	val =  4.*TMath::Sqrt(1-cos*cos)*TMath::Cos(phi);
	break;
      case 4:
	val = 4.*cos;
	break;
      case 5:
	val = 5.*(1-cos*cos)*TMath::Sin(2*phi);
	break;
      case 6:
	val = 5.*2.*TMath::Sqrt(1-cos*cos)*cos*TMath::Sin(phi);
	break;
      case 7:
	val = 4.*TMath::Sqrt(1-cos*cos)*TMath::Sin(phi);
	break;
      case 8:
	val = 14.-10.*(1+cos*cos);
	break;
      case 9:
	val = 1.0;
	break;
	default:
	  break;
      }
      return val;
    };
    auto d_post = d_start.Define("test_A"+std::to_string(c), tester, {"GenV_"+_leptonType+"_CStheta", "GenV_"+_leptonType+"_CSphiFIX"});
    d_start = d_post;    
  }
  return d_start;

}

std::vector<ROOT::RDF::RResultPtr<TH1D>> getCoeffVars::getTH1(){ 
    return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> getCoeffVars::getTH2(){ 
    return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> getCoeffVars::getTH3(){ 
    return _h3List;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> getCoeffVars::getGroupTH1(){ 
  return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> getCoeffVars::getGroupTH2(){ 
  return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> getCoeffVars::getGroupTH3(){ 
  return _h3Group;
}

void getCoeffVars::reset(){
    _h1List.clear();
    _h2List.clear();
    _h3List.clear();

    _h1Group.clear();
    _h2Group.clear();
    _h3Group.clear();
}
