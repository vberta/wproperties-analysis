#ifndef MERGESYSTWEIGHT_H
#define MERGESYSTWEIGHT_H

#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"
#include "TH1D.h"
#include "TH2D.h"
#include "TString.h"
#include "TMath.h"
#include "interface/module.hpp"
#include "interface/functions.hpp"
#include <utility>

using RNode = ROOT::RDF::RNode;

class mergeSystWeight : public Module {

private:
  
  std::vector<ROOT::RDF::RResultPtr<TH1D>> _h1List;
  std::vector<ROOT::RDF::RResultPtr<TH2D>> _h2List;
  std::vector<ROOT::RDF::RResultPtr<TH3D>> _h3List;
  
  // groups of histos
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> _h1Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> _h2Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> _h3Group;
  
  std::pair<std::string, std::string> _syst_name;
  std::pair<float,float> _syst_ratios;  
  std::string _syst_weight;
  bool _scalar;
  bool _multiply;
  
public:
    
  mergeSystWeight(std::pair<std::string,std::string> syst_name, std::pair<float,float> syst_ratios, std::string syst_weight, bool scalar, bool multiply) :
    _syst_name(syst_name), _syst_ratios(syst_ratios), _syst_weight(syst_weight), _scalar(scalar), _multiply(multiply) {};
  
  ~mergeSystWeight() {};
  
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
