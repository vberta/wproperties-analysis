#ifndef WEIGHTDEFINITIONS_H
#define WEIGHTDEFINITIONS_H

#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"
#include "TH1D.h"
#include "TH2D.h"
#include "TString.h"
#include "TMath.h"
#include "TFile.h"
#include "interface/module.hpp"

using RNode = ROOT::RDF::RNode;

class weightDefinitions : public Module
{

private:
    std::vector<ROOT::RDF::RResultPtr<TH1D>> _h1List;
    std::vector<ROOT::RDF::RResultPtr<TH2D>> _h2List;
    std::vector<ROOT::RDF::RResultPtr<TH3D>> _h3List;
    
    // groups of histos
    std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> _h1Group;
    std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> _h2Group;
    std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> _h3Group;

    TFile* _SF;
    TH2D* _Reco;
    TH2D* _TriggerPlus;
    TH2D* _TriggerMinus;
    TH2D* _TriggerPlusSyst0;
    TH2D* _TriggerPlusSyst1;
    TH2D* _TriggerPlusSyst2;
    TH2D* _TriggerMinusSyst0;
    TH2D* _TriggerMinusSyst1;
    TH2D* _TriggerMinusSyst2;


public:
    weightDefinitions(TFile *SF){
        _SF = SF;
        

        _Reco = (TH2D *)_SF->Get("Reco");
        _TriggerPlus = (TH2D *)_SF->Get("TriggerPlus");
        _TriggerMinus = (TH2D *)_SF->Get("TriggerMinus");

        _TriggerPlusSyst0 = (TH2D *)_SF->Get("TriggerPlusSyst0");
        _TriggerPlusSyst1 = (TH2D *)_SF->Get("TriggerPlusSyst1");
        _TriggerPlusSyst2 = (TH2D *)_SF->Get("TriggerPlusSyst2");
        _TriggerMinusSyst0 = (TH2D *)_SF->Get("TriggerMinusSyst0");
        _TriggerMinusSyst1 = (TH2D *)_SF->Get("TriggerMinusSyst1");
        _TriggerMinusSyst2 = (TH2D *)_SF->Get("TriggerMinusSyst2");
            
    };
    ~weightDefinitions(){};

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
