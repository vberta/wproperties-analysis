#ifndef MUONHISTOS_H
#define MUONHISTOS_H


#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"
#include "TH1D.h"
#include "TH2D.h"
#include "TString.h"
#include "TMath.h"
#include "interface/module.hpp"
#include "interface/TH1weightsHelper.hpp"
#include "interface/TH2weightsHelper.hpp"
#include "interface/TH1varsHelper.hpp"
#include "interface/TH2varsHelper.hpp"
#include "interface/functions.hpp"

using RNode = ROOT::RDF::RNode;

class muonHistos : public Module {

private:

  std::vector<ROOT::RDF::RResultPtr<TH1D>> _h1List;
  std::vector<ROOT::RDF::RResultPtr<TH2D>> _h2List;
  std::vector<ROOT::RDF::RResultPtr<TH3D>> _h3List;
  
  // groups of histos
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> _h1Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> _h2Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> _h3Group;
  
  std::string _category; // category name to be hardcoded in h name
  std::string _cut; // cut string name
  std::string _weight; // event weight name
  std::vector<std::string> _syst_names; // names of syst variations for histo names
  std::string _syst_column; // the column comntaining the syst variations
  std::string _modifier; // var name modifier
  bool _multi_cuts; // 
  bool _verbose;
    
public:
  
  // to be called with THDweightsHelper (w/o systematics)
  muonHistos(std::string category, std::string cut, std::string weight) : _category(category), _cut(cut), _weight(weight), _syst_names({}), _syst_column(""), _modifier(""), _multi_cuts(false) {
    _verbose = true;
  };

  // to be called with THDweightsHelper (w/ systematics)
  muonHistos(std::string category, std::string cut, std::string weight, std::vector<std::string> syst_names, std::string syst_column) :
    _category(category), _cut(cut), _weight(weight), _syst_names(syst_names), _syst_column(syst_column), _modifier(""), _multi_cuts(false)  {
    _verbose = true;
  };
  
  // to be called with THDvarsHelper
  muonHistos(std::string category, std::string cut, std::string weight, std::vector<std::string> syst_names, std::string syst_column, std::string modifier, bool multi_cuts) :
    _category(category), _cut(cut), _weight(weight), _syst_names(syst_names), _syst_column(syst_column), _modifier(modifier), _multi_cuts(multi_cuts) {
    _verbose = true;
  };

  std::string check_modifier(const std::string& var_name);

  void add_group_1D(ROOT::RDF::RInterface<ROOT::Detail::RDF::RJittedFilter, void>*, const std::string&, const std::string&, 
		    const std::vector<float>&, const unsigned int&);
  void add_group_2D(ROOT::RDF::RInterface<ROOT::Detail::RDF::RJittedFilter, void>*, const std::string&, const std::string&, const std::string&, 
		    const std::vector<float>&, const unsigned int&, 
		    const std::vector<float>&, const unsigned int&);

  ~muonHistos() {};
  
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
