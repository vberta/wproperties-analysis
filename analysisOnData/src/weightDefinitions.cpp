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
	  auto sf = _Reco->GetBinContent(binReco)*_TriggerPlus->GetBinContent(binTrigger);
          if (sf < 0.001) sf = 1.;
            return sf;
            //return _Reco->GetBinContent(binReco)*_TriggerPlus->GetBinContent(binTrigger);
        }
        else
        {	  
	  auto sf = _Reco->GetBinContent(binReco)*_TriggerMinus->GetBinContent(binTrigger);
          if (sf < 0.001) sf = 1.;
            return sf;
	  //return _Reco->GetBinContent(binReco)*_TriggerMinus->GetBinContent(binTrigger);
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
            if(nomSF < 0.001)  nomSF = 1.;
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
            if(nomSF < 0.001) nomSF = 1.;

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
