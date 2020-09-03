#include "interface/weightDefinitions.hpp"
#include "interface/functions.hpp"
RNode weightDefinitions::run(RNode d)
{


    auto definePUweights = [](float weightUp, float weightDown) {
        ROOT::VecOps::RVec<float> PUVars;
        PUVars.emplace_back(weightUp);
        PUVars.emplace_back(weightDown);

        return PUVars;
    };
    
    
    auto defineWHSF = [this](float pt, float eta, float charge){

        int binReco = _Reco->FindBin(eta,pt);
        int binTrigger= _TriggerPlus->FindBin(eta,pt);
        if(charge>0)
        {
            return _Reco->GetBinContent(binReco)*_TriggerPlus->GetBinContent(binTrigger);
        }
        else
        {
            return _Reco->GetBinContent(binReco)*_TriggerMinus->GetBinContent(binTrigger);
        }

    };

    // Define SF: WHSF = Trigger * ISO * ID
    auto defineWHSFVars = [this](float pt, float eta, float charge) {
        ROOT::VecOps::RVec<float> WHSF;

        int binReco = _Reco->FindBin(eta,pt);
        int binTrigger= _TriggerPlus->FindBin(eta,pt);
        int binSyst = _TriggerPlusSyst0->FindBin(eta, pt);
        
        float flatVar = 0;
        if(fabs(eta)<1) flatVar=0.002;
        else if(abs(eta)<1.5) flatVar=0.004;
        else flatVar=0.014;
        
        if (charge > 0)
        {
            float nomSF = _Reco->GetBinContent(binReco)*_TriggerPlus->GetBinContent(binTrigger);
            WHSF.emplace_back(nomSF*(1+TMath::Sqrt(2)*_TriggerPlusSyst0->GetBinContent(binSyst)));
            WHSF.emplace_back(nomSF*(1+TMath::Sqrt(2)*_TriggerPlusSyst1->GetBinContent(binSyst)));
            WHSF.emplace_back(nomSF*(1+TMath::Sqrt(2)*_TriggerPlusSyst2->GetBinContent(binSyst)));
            WHSF.emplace_back(nomSF*(1+flatVar));
            WHSF.emplace_back(nomSF*(1-TMath::Sqrt(2)*_TriggerPlusSyst0->GetBinContent(binSyst)));
            WHSF.emplace_back(nomSF*(1-TMath::Sqrt(2)*_TriggerPlusSyst1->GetBinContent(binSyst)));
            WHSF.emplace_back(nomSF*(1-TMath::Sqrt(2)*_TriggerPlusSyst2->GetBinContent(binSyst)));
            WHSF.emplace_back(nomSF*(1-flatVar));
        }
        else
        {
            float nomSF = _Reco->GetBinContent(binReco)*_TriggerMinus->GetBinContent(binTrigger);
            WHSF.emplace_back(nomSF*(1+TMath::Sqrt(2)*_TriggerMinusSyst0->GetBinContent(binSyst)));
            WHSF.emplace_back(nomSF*(1+TMath::Sqrt(2)*_TriggerMinusSyst1->GetBinContent(binSyst)));
            WHSF.emplace_back(nomSF*(1+TMath::Sqrt(2)*_TriggerMinusSyst2->GetBinContent(binSyst)));
            WHSF.emplace_back(nomSF*(1+flatVar));
            WHSF.emplace_back(nomSF*(1-TMath::Sqrt(2)*_TriggerMinusSyst0->GetBinContent(binSyst)));
            WHSF.emplace_back(nomSF*(1-TMath::Sqrt(2)*_TriggerMinusSyst1->GetBinContent(binSyst)));
            WHSF.emplace_back(nomSF*(1-TMath::Sqrt(2)*_TriggerMinusSyst2->GetBinContent(binSyst)));
            WHSF.emplace_back(nomSF*(1-flatVar));
        }

        return WHSF;
    };

    
    auto d1 = d.Define("WHSF", defineWHSF, {"Mu1_pt", "Mu1_eta", "Mu1_charge"})
                  .Define("WHSFVars", defineWHSFVars, {"Mu1_pt", "Mu1_eta", "Mu1_charge"})
                  .Define("puWeightVars", definePUweights, {"puWeightUp", "puWeightDown"});
     
    return d1;
}