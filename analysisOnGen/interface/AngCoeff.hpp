#ifndef ANGCOEFF_H
#define ANGCOEFF_H


#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"
#include "TH1D.h"
#include "TH2D.h"
#include "TString.h"
#include "TMath.h"
#include "interface/module.hpp"
#include "interface/TH2weightsHelper.hpp"
#include "interface/TH1weightsHelper.hpp"

using RNode = ROOT::RDF::RNode;

class AngCoeff : public Module {

    private:

    std::vector<ROOT::RDF::RResultPtr<TH1D>> _h1List;
    std::vector<ROOT::RDF::RResultPtr<TH2D>> _h2List;
    std::vector<ROOT::RDF::RResultPtr<TH3D>> _h3List;

    // groups of histos
    std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> _h1Group;
    std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> _h2Group;
    std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> _h3Group;

  std::vector<float> _yArr = {0, 0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 3.0, 6.0};
  std::vector<float> _ptArr = {0., 4., 8., 12., 16., 20., 24., 28., 32., 40., 60., 100., 200.};

  int _nBinsY = 8;
  int _nBinsPt = 12;
    std::vector<std::string> _coeff = {"A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "AUL"};

    std::vector<std::string> _syst_name;
    std::string _syst_weight;
    
    public:
    
    AngCoeff(){
        _syst_weight = "";
    };

    AngCoeff(std::vector<std::string> syst_name, std::string syst_weight){
        
        _syst_name = syst_name;
        _syst_weight = syst_weight;
    };

    ~AngCoeff() {};

    RNode run(RNode) override;
    std::vector<ROOT::RDF::RResultPtr<TH1D>> getTH1() override;
  	std::vector<ROOT::RDF::RResultPtr<TH2D>> getTH2() override;
  	std::vector<ROOT::RDF::RResultPtr<TH3D>> getTH3() override;

    std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> getGroupTH1() override;
    std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> getGroupTH2() override;
    std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> getGroupTH3() override;

    std::vector<std::string> stringMultiplication (const std::vector<std::string> &v1, const std::vector<std::string> &v2);

    void reset() override;

};

#endif
