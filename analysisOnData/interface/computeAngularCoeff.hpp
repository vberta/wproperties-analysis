#ifndef COMPUTEANGULARCOEFF_H
#define COMPUTEANGULARCOEFF_H


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

class computeAngularCoeff : public Module {

 private:

  std::vector<ROOT::RDF::RResultPtr<TH1D>> _h1List;
  std::vector<ROOT::RDF::RResultPtr<TH2D>> _h2List;
  std::vector<ROOT::RDF::RResultPtr<TH3D>> _h3List;

    // groups of histos
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> _h1Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> _h2Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> _h3Group;

  std::string _category;
  std::string _weight;
  std::string _leptonType;
  std::vector<double> _xbins;
  std::vector<double> _ybins;
  
 public:
    
  computeAngularCoeff(std::string category, std::string weight, std::string leptonType, TH2F* histo) : _category(category), _weight(weight), _leptonType(leptonType) {
    _xbins = {};
    int nbinsX = histo->GetXaxis()->GetNbins();
    for(int i = 1; i<=nbinsX; i++ ) _xbins.push_back( histo->GetXaxis()->GetBinLowEdge(i) );
    _xbins.push_back( histo->GetXaxis()->GetBinLowEdge(nbinsX) + histo->GetXaxis()->GetBinWidth(nbinsX) );
    _ybins = {};
    int nbinsY = histo->GetYaxis()->GetNbins();
    for(int i = 1; i<=nbinsY; i++ ) _ybins.push_back( histo->GetYaxis()->GetBinLowEdge(i) );
    _ybins.push_back( histo->GetYaxis()->GetBinLowEdge(nbinsY) + histo->GetYaxis()->GetBinWidth(nbinsY) );
  }

  ~computeAngularCoeff() {};
  
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
