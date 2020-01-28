#include "interface/applyAngularCoeff.hpp"


RNode applyAngularCoeff::run(RNode d){

  auto divide_safe = [](float x, float y)->float{
    return y>0. ? x/y : 1.0;
  };
  
  auto getBin = [this](float y, float qt)->int {
    TH2F* h = (this->_hmap.begin())->second;
    int bin = h->FindBin(y,qt);
    if( h->IsBinOverflow(bin) ||  h->IsBinUnderflow(bin) ) return -1;
    return bin;
  };
  
  RNode d_start = d.Define("bin_angular_pdf", getBin, {"GenV_"+_leptonType+"_absy", "GenV_"+_leptonType+"_qt"});

  for(unsigned int i = 0; i<_categories.size(); i++){
    std::string cat = _categories[i];
    auto weightD = [cat,this](float cos, float phi, int bin)->float {
      float val = 1.0;
      if( bin<0 ) return val;
      std::vector<float> A = {1.0};
      for(auto c : _coefficients){
	if(c!="UL") A.push_back( this->_hmap.at(cat+"_"+c)->GetBinContent(bin) );
      }
      std::vector<float> P = {};
      P.push_back(1.0 + cos*cos);
      P.push_back(0.5*(1.-3.*cos*cos));
      P.push_back(2.*cos*TMath::Sqrt(1.-cos*cos)*TMath::Cos(phi));
      P.push_back(0.5*(1.-cos*cos)*TMath::Cos(2.*phi));
      P.push_back(TMath::Sqrt(1.-cos*cos)*TMath::Cos(phi));
      P.push_back(cos);
      //P.push_back((1.-cos*cos)*TMath::Sin(2.*phi));
      //P.push_back(2.*cos*TMath::Sqrt(1.-cos*cos)*TMath::Sin(phi));
      //P.push_back(TMath::Sqrt(1.-cos*cos)*TMath::Sin(phi));
      val = std::inner_product(std::begin(A), std::end(A), std::begin(P), 0.0);
      //std::cout << "weightN :"  << cos << "," <<  phi<< ","  << bin << " => " << val << std::endl;
      return val;
    };

    auto d_post = d_start.Define("angular_pdf_"+cat, weightD, {"GenV_"+_leptonType+"_CStheta", "GenV_"+_leptonType+"_CSphiFIX", "bin_angular_pdf"} );
    d_start = d_post;

    for(unsigned int c = 0; c<_coefficients.size(); c++){
      std::string coeff = _coefficients[c];
      auto weightN = [this,coeff](float cos, float phi, int bin)->float {
	float val = 1.0;
	if( bin<0 ) return val;
	if     (coeff=="UL") val = 1+cos*cos;       
	else if(coeff=="A0") val = 0.5*(1.-3.*cos*cos);
	else if(coeff=="A1") val = 2.*cos*TMath::Sqrt(1.-cos*cos)*TMath::Cos(phi); 
	else if(coeff=="A2") val = 0.5*(1.-cos*cos)*TMath::Cos(2.*phi); 
	else if(coeff=="A3") val = TMath::Sqrt(1.-cos*cos)*TMath::Cos(phi); 
	else if(coeff=="A4") val = cos;
	//else if(coeff=="A5") val = (1.-cos*cos)*TMath::Sin(2.*phi); 
	//else if(coeff=="A6") val = 2.*cos*TMath::Sqrt(1.-cos*cos)*TMath::Sin(phi); 
	//else if(coeff=="A7") val = TMath::Sqrt(1.-cos*cos)*TMath::Sin(phi); 
	//std::cout << "weightN "+coeff+": " << cos << "," <<  phi<< ","  << bin << " => " << val << std::endl;
	return val;
      };

      auto d_post = d_start
	.Define("angular_pdf_"+cat+"_"+coeff, weightN, {"GenV_"+_leptonType+"_CStheta", "GenV_"+_leptonType+"_CSphiFIX", "bin_angular_pdf"})
	.Define("weight_coeff_"+cat+"_"+coeff, divide_safe, {"angular_pdf_"+cat+"_"+coeff, "angular_pdf_"+cat});
      d_start = d_post;

    }
  }
  
  return d_start;
}

std::vector<ROOT::RDF::RResultPtr<TH1D>> applyAngularCoeff::getTH1(){ 
    return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> applyAngularCoeff::getTH2(){ 
    return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> applyAngularCoeff::getTH3(){ 
    return _h3List;
}

std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> applyAngularCoeff::getGroupTH1(){ 
  return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> applyAngularCoeff::getGroupTH2(){ 
  return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> applyAngularCoeff::getGroupTH3(){ 
  return _h3Group;
}

void applyAngularCoeff::reset(){
    
    _h1List.clear();
    _h2List.clear();
    _h3List.clear();

    _h1Group.clear();
    _h2Group.clear();
    _h3Group.clear();

}
