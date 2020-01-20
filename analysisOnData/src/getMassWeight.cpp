#include "interface/getMassWeight.hpp"


RNode getMassWeight::run(RNode d){

  auto BreitWigner = [](float Q2, float M2, float G2)->float{
    return 1./((Q2 - M2)*(Q2 - M2) + M2*G2);
  };

  auto BreitWignerRW = [](float Q2, float M2, float G2)->float{
    return Q2/((Q2 - M2)*(Q2 - M2) + Q2*Q2*G2/M2);
  };
      
  auto getRVec = [&](float Q){
    ROOT::VecOps::RVec<float> v;
    for(unsigned int n = 0 ; n < _syst_masses.size(); n++){
      float M = _syst_masses[n];
      float w = 1.0;
      if(_scheme=="Fixed")
	w = BreitWigner(Q*Q, _nominal_mass*_nominal_mass, _nominal_width*_nominal_width)/
	  BreitWigner(Q*Q, M*M, _nominal_width*_nominal_width);
      else if(_scheme=="Running")
	w = BreitWigner(Q*Q, _nominal_mass*_nominal_mass, _nominal_width*_nominal_width)/
	  BreitWignerRW(Q*Q, M*M, _nominal_width*_nominal_width) ;
      //std::cout << w << std::endl;
      v.emplace_back(w);
    }
    return v;
  };

  auto d1 = d.Define(_new_syst_column, getRVec, {"GenV_"+_leptonType+"_mass"});
  return d1;

}

std::vector<ROOT::RDF::RResultPtr<TH1D>> getMassWeight::getTH1(){ 
    return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> getMassWeight::getTH2(){ 
    return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> getMassWeight::getTH3(){ 
    return _h3List;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> getMassWeight::getGroupTH1(){ 
  return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> getMassWeight::getGroupTH2(){ 
  return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> getMassWeight::getGroupTH3(){ 
  return _h3Group;
}

void getMassWeight::reset(){
    _h1List.clear();
    _h2List.clear();
    _h3List.clear();

    _h1Group.clear();
    _h2Group.clear();
    _h3Group.clear();
}
