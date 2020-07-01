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

    TH2D* _TriggerPlus;
    TH2D* _TriggerMinus;

    TH2D* _TriggerPlusSyst0Up;
    TH2D* _TriggerPlusSyst1Up;
    TH2D* _TriggerPlusSyst2Up;
    TH2D* _TriggerPlusSyst0Down;
    TH2D* _TriggerPlusSyst1Down;
    TH2D* _TriggerPlusSyst2Down;

    TH2D* _TriggerMinusSyst0Up;
    TH2D* _TriggerMinusSyst1Up;
    TH2D* _TriggerMinusSyst2Up;
    TH2D* _TriggerMinusSyst0Down;
    TH2D* _TriggerMinusSyst1Down;
    TH2D* _TriggerMinusSyst2Down;

    TH2D* _Reco;

    TH2D* _RecoStatUp;
    TH2D* _RecoSystUp;
    TH2D* _RecoStatDown;
    TH2D* _RecoSystDown;

public:
    weightDefinitions(TFile *SF){
        _SF = SF;

        _TriggerPlus = (TH2D *)_SF->Get("TriggerPlus");
        _TriggerMinus = (TH2D *)_SF->Get("TriggerMinus");

        _TriggerPlusSyst0Up = (TH2D *)_SF->Get("TriggerPlusSyst0Up");
        _TriggerPlusSyst1Up = (TH2D *)_SF->Get("TriggerPlusSyst1Up");
        _TriggerPlusSyst2Up = (TH2D *)_SF->Get("TriggerPlusSyst2Up");
        _TriggerPlusSyst0Down = (TH2D *)_SF->Get("TriggerPlusSyst0Down");
        _TriggerPlusSyst1Down = (TH2D *)_SF->Get("TriggerPlusSyst1Down");
        _TriggerPlusSyst2Down = (TH2D *)_SF->Get("TriggerPlusSyst2Down");

        _TriggerMinusSyst0Up = (TH2D *)_SF->Get("TriggerMinusSyst0Up");
        _TriggerMinusSyst1Up = (TH2D *)_SF->Get("TriggerMinusSyst1Up");
        _TriggerMinusSyst2Up = (TH2D *)_SF->Get("TriggerMinusSyst2Up");
        _TriggerMinusSyst0Down = (TH2D *)_SF->Get("TriggerMinusSyst0Down");
        _TriggerMinusSyst1Down = (TH2D *)_SF->Get("TriggerMinusSyst1Down");
        _TriggerMinusSyst2Down = (TH2D *)_SF->Get("TriggerMinusSyst2Down");

        _Reco = (TH2D *)_SF->Get("Reco");

        _RecoStatUp = (TH2D *)_SF->Get("RecoStatUp");
        _RecoSystUp = (TH2D *)_SF->Get("RecoSystUp");
        _RecoStatDown = (TH2D *)_SF->Get("RecoStatDown");
        _RecoSystDown = (TH2D *)_SF->Get("RecoSystDown");
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
