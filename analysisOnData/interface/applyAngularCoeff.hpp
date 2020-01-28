#ifndef APPLYANGULARCOEFF_H
#define APPLYANGULARCOEFF_H


#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"
#include "TH1D.h"
#include "TH2D.h"
#include "TFile.h"
#include "TString.h"
#include "TMath.h"
#include "interface/module.hpp"
#include "interface/functions.hpp"
#include <algorithm>

using RNode = ROOT::RDF::RNode;

class applyAngularCoeff : public Module {

 private:

  std::vector<ROOT::RDF::RResultPtr<TH1D>> _h1List;
  std::vector<ROOT::RDF::RResultPtr<TH2D>> _h2List;
  std::vector<ROOT::RDF::RResultPtr<TH3D>> _h3List;

    // groups of histos
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> _h1Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> _h2Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> _h3Group;

  TFile* _file;
  std::vector<std::string> _categories;
  std::vector<std::string> _coefficients;
  std::string _leptonType;
  std::map<std::string,TH2F*> _hmap;
  
 public:

  applyAngularCoeff(std::string fname, std::vector<std::string> categories, std::vector<std::string> coefficients, std::string leptonType) : _categories(categories), _coefficients(coefficients), _leptonType(leptonType) {
    _file = TFile::Open(fname.c_str(), "READ");
    std::cout << "Opening file " << fname << std::endl;
    for(unsigned int i = 0; i<_categories.size(); i++){
      std::string cat = _categories[i];
      _file->cd(("GENINCLUSIVE_"+cat+"_nominal").c_str());
      for(unsigned int c = 0; c<_coefficients.size(); c++){
	std::string coeff = _coefficients[c];
	if(coeff=="UL") continue;
	TH2F* hN = (TH2F*)gDirectory->Get(("GENINCLUSIVE_"+cat+"_"+coeff).c_str());
	TH2F* hD = (TH2F*)gDirectory->Get(("GENINCLUSIVE_"+cat+"_MC").c_str());
	std::cout << "GENINCLUSIVE_"+cat+"_"+coeff << " / " << "GENINCLUSIVE_"+cat+"_MC" << std::endl;
	hN->Divide(hD);
	_hmap[cat+"_"+coeff] = (TH2F*)hN->Clone((cat+"_"+coeff).c_str());
      }
    }
  }

  ~applyAngularCoeff() {
    _file->Close();
  };
  
  RNode run(RNode) override;
  std::vector<ROOT::RDF::RResultPtr<TH1D>> getTH1() override;
  std::vector<ROOT::RDF::RResultPtr<TH2D>> getTH2() override;
  std::vector<ROOT::RDF::RResultPtr<TH3D>> getTH3() override;

  std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> getGroupTH1() override;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> getGroupTH2() override;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> getGroupTH3() override;
  
  void reset() override;

};

#endif
