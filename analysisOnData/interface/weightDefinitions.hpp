#ifndef WEIGHTDEFINITIONS_H
#define WEIGHTDEFINITIONS_H

#include "module.hpp"

class weightDefinitions : public Module
{

private:
    TFile *_SF;
    TH2D *_Reco;
    TH2D *_TriggerPlus;
    TH2D *_TriggerMinus;
    TH2D *_TriggerPlusSyst0;
    TH2D *_TriggerPlusSyst1;
    TH2D *_TriggerPlusSyst2;
    TH2D *_TriggerMinusSyst0;
    TH2D *_TriggerMinusSyst1;
    TH2D *_TriggerMinusSyst2;

public:
    weightDefinitions(TFile *SF)
    {
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

};

#endif
