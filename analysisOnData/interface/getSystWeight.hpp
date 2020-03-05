#ifndef GETSYSTWEIGHT_H
#define GETSYSTWEIGHT_H

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

class getSystWeight : public Module {

private:
  
  std::vector<ROOT::RDF::RResultPtr<TH1D>> _h1List;
  std::vector<ROOT::RDF::RResultPtr<TH2D>> _h2List;
  std::vector<ROOT::RDF::RResultPtr<TH3D>> _h3List;
  
  // groups of histos
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> _h1Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> _h2Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> _h3Group;
  
  std::vector<std::string> _syst_columns;
  std::string _new_syst_column, _idx1, _nom_column;
  const std::pair<unsigned int,unsigned int> _range;
  const std::vector<unsigned int>* _set;
  std::string _type;
  bool _verbose;
  
public:
    
  getSystWeight(std::vector<std::string> syst_columns, 
		std::string new_syst_column, 
		std::string idx1, 
		std::string nom_column,
		std::pair<unsigned int,unsigned int> range,
		std::vector<unsigned int> set,
		std::string type): 
    _syst_columns(syst_columns), _new_syst_column(new_syst_column), _idx1(idx1), _nom_column(nom_column), _range(range), _type(type) {
    _set = new std::vector<unsigned int>(set);
    _verbose = false;
  };

  ~getSystWeight() {
    delete _set;
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
