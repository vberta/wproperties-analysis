#ifndef FAKERATE_H
#define FAKERATE_H


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

using RNode = ROOT::RDF::RNode;

class fakeRate : public Module {

 private:

  std::vector<ROOT::RDF::RResultPtr<TH1D>> _h1List;
  std::vector<ROOT::RDF::RResultPtr<TH2D>> _h2List;
  std::vector<ROOT::RDF::RResultPtr<TH3D>> _h3List;

    // groups of histos
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> _h1Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> _h2Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> _h3Group;

  TFile* _file;
  std::string _category;
  std::vector<std::string> _syst_columns;
  std::map<std::string, TH2F*> _hmap;

 public:
    
  fakeRate(std::string fname, std::string category, std::vector<std::string> syst_columns) : _category(category), _syst_columns(syst_columns) {
    _file = TFile::Open(fname.c_str(), "READ");
    for(unsigned int i=0; i <_syst_columns.size(); i++){
      std::string var = _syst_columns[i];
      if(var=="nominal"){
	_hmap.insert( std::pair<std::string, TH2F*>("fake_offset_"+var,   (TH2F*)_file->Get("fake_offset") ) );
	_hmap.insert( std::pair<std::string, TH2F*>("fake_slope_"+var,    (TH2F*)_file->Get("fake_slope") ) );
	_hmap.insert( std::pair<std::string, TH2F*>("prompt_offset_"+var, (TH2F*)_file->Get("prompt_offset") ) );
	_hmap.insert( std::pair<std::string, TH2F*>("prompt_slope_"+var,  (TH2F*)_file->Get("prompt_slope") ) );
	_hmap.insert( std::pair<std::string, TH2F*>("prompt_2deg_"+var,   (TH2F*)_file->Get("prompt_2deg") ) );
      }
    }
  }

  ~fakeRate() {
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
