#ifndef GETMASSWEIGHT_H
#define GETMASSWEIGHT_H

#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"
#include "TH1D.h"
#include "TH2D.h"
#include "TString.h"
#include "TMath.h"
#include "interface/module.hpp"
#include "interface/functions.hpp"

using RNode = ROOT::RDF::RNode;

class getMassWeight : public Module {

private:
  
  std::vector<ROOT::RDF::RResultPtr<TH1D>> _h1List;
  std::vector<ROOT::RDF::RResultPtr<TH2D>> _h2List;
  std::vector<ROOT::RDF::RResultPtr<TH3D>> _h3List;
  
  // groups of histos
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> _h1Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> _h2Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> _h3Group;
  
  std::string _new_syst_column;
  std::vector<float> _syst_masses;
  float _nominal_mass, _nominal_width;
  std::string _leptonType;  
  std::string _scheme;
  
public:
    
  getMassWeight(std::string new_syst_column, 
		std::vector<float> syst_masses,
		float nominal_mass,
		float nominal_width,
		std::string leptonType,
		std::string scheme): 
    _new_syst_column(new_syst_column), _syst_masses(syst_masses), 
    _nominal_mass(nominal_mass), _nominal_width(nominal_width), 
    _leptonType(leptonType), _scheme(scheme){};

  ~getMassWeight() {};
  
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
