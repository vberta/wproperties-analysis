#include "interface/weightDefinitions.hpp"
#include "interface/functions.hpp"
RNode weightDefinitions::run(RNode d)
{

    // Define SF: trigger, RECO = (ISO + ID)
    auto defineTriggerSF = [this](float pt, float eta, float charge){

        int bin = _TriggerPlus->FindBin(eta,pt);
        if(charge>0)
        {
            return _TriggerPlus->GetBinContent(bin);
        }
        else
        {
            return _TriggerMinus->GetBinContent(bin);
        }

    };

    // Define SF: trigger, RECO = (ISO + ID)
    auto defineTriggerSFVars = [this](float pt, float eta, float charge) {
        ROOT::VecOps::RVec<float> TriggSF;

        int bin = _TriggerPlusSyst1Up->FindBin(eta, pt);
        if (charge > 0)
        {
            TriggSF.emplace_back(_TriggerPlusSyst0Up->GetBinContent(bin));
            TriggSF.emplace_back(_TriggerPlusSyst1Up->GetBinContent(bin));
            TriggSF.emplace_back(_TriggerPlusSyst2Up->GetBinContent(bin));
            TriggSF.emplace_back(_TriggerPlusSyst0Down->GetBinContent(bin));
            TriggSF.emplace_back(_TriggerPlusSyst1Down->GetBinContent(bin));
            TriggSF.emplace_back(_TriggerPlusSyst2Down->GetBinContent(bin));
        }
        else
        {
            TriggSF.emplace_back(_TriggerMinusSyst0Up->GetBinContent(bin));
            TriggSF.emplace_back(_TriggerMinusSyst1Up->GetBinContent(bin));
            TriggSF.emplace_back(_TriggerMinusSyst2Up->GetBinContent(bin));
            TriggSF.emplace_back(_TriggerMinusSyst0Down->GetBinContent(bin));
            TriggSF.emplace_back(_TriggerMinusSyst1Down->GetBinContent(bin));
            TriggSF.emplace_back(_TriggerMinusSyst2Down->GetBinContent(bin));
        }

        return TriggSF;
    };

    auto defineRecoSF = [this](float pt, float eta) {

        int bin = _Reco->FindBin(eta, pt);
        return _Reco->GetBinContent(bin);

    };

    auto defineRecoSFVars = [this](float pt, float eta) {
        ROOT::VecOps::RVec<float> RecoSF;

        int bin = _RecoStatUp->FindBin(eta, pt);
        RecoSF.emplace_back(_RecoStatUp->GetBinContent(bin));
        RecoSF.emplace_back(_RecoSystUp->GetBinContent(bin));
        RecoSF.emplace_back(_RecoStatDown->GetBinContent(bin));
        RecoSF.emplace_back(_RecoSystDown->GetBinContent(bin));

        return RecoSF;
    };

    auto definePUweights = [](float weightUp, float weightDown) {
        ROOT::VecOps::RVec<float> PUVars;
        PUVars.emplace_back(weightUp);
        PUVars.emplace_back(weightDown);

        return PUVars;
    };

 
    auto d1 = d.Define("TriggerSF", defineTriggerSF, {"Mu1_pt", "Mu1_eta", "Mu1_charge"})
                  .Define("TriggerSFVars", defineTriggerSFVars, {"Mu1_pt", "Mu1_eta", "Mu1_charge"})
                  .Define("RecoSF", defineRecoSF, {"Mu1_pt", "Mu1_eta"})
                  .Define("RecoSFVars", defineRecoSFVars, {"Mu1_pt", "Mu1_eta"})
                  .Define("puWeightVars", definePUweights, {"puWeightUp", "puWeightDown"});
     
    return d1;
}

std::vector<ROOT::RDF::RResultPtr<TH1D>> weightDefinitions::getTH1()
{
    return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> weightDefinitions::getTH2()
{
    return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> weightDefinitions::getTH3()
{
    return _h3List;
}

std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> weightDefinitions::getGroupTH1()
{
    return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> weightDefinitions::getGroupTH2()
{
    return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> weightDefinitions::getGroupTH3()
{
    return _h3Group;
}

void weightDefinitions::reset()
{

    _h1List.clear();
    _h2List.clear();
    _h3List.clear();

    _h1Group.clear();
    _h2Group.clear();
    _h3Group.clear();
}
