#ifndef GETLUMIWEIGHT_H
#define GETLUMIWEIGHT_H

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

class getLumiWeight : public Module {
  
private:

  std::vector<ROOT::RDF::RResultPtr<TH1D>> _h1List;
  std::vector<ROOT::RDF::RResultPtr<TH2D>> _h2List;
  std::vector<ROOT::RDF::RResultPtr<TH3D>> _h3List;

  // groups of histos
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> _h1Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> _h2Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> _h3Group;

  double _genEventSumw;
  double _targetLumi;
  double _xsec;
 
public:
    
   getLumiWeight(std::string fname, double targetLumi, double xsec ){       
     ROOT::RDataFrame runs("Runs", fname);
     _targetLumi = targetLumi;
     _xsec = xsec*1e+03; // pb -> fb
     _genEventSumw = runs.Sum("genEventSumw").GetValue();
   };

  getLumiWeight(std::vector<std::string> fnames, double targetLumi, double xsec ){       
     ROOT::RDataFrame runs("Runs", fnames);
     _targetLumi = targetLumi;
     _xsec = xsec*1e+03; // pb -> fb
     _genEventSumw = runs.Sum("genEventSumw").GetValue();
   };
  
  ~getLumiWeight() {};
  
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
