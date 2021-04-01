#include "interface/reweightFromZ.hpp"
#include "interface/functions.hpp"

RNode reweightFromZ::run(RNode d)
{

    auto getWeightPt = [this](float Pt) -> float {
        int bin = _hPt->FindBin(Pt);
        if (_hPt->IsBinOverflow(bin))
            return _hPt->GetBinContent(_hPt->GetNbinsX());
        else if (_hPt->IsBinUnderflow(bin))
            return _hPt->GetBinContent(1);
        else
            return _hPt->GetBinContent(bin);
    };
    auto getWeightY = [this](float y) -> float {
        float absy = TMath::Abs(y);
        int bin = _hY->FindBin(absy);
        if (_hY->IsBinOverflow(bin))
            return _hY->GetBinContent(_hY->GetNbinsX());
        else if (_hY->IsBinUnderflow(bin))
            return _hY->GetBinContent(1);
        else
            return _hY->GetBinContent(bin);
    };
    
    // auto getQtweights = [&](float Pt) { // used only for 10Mev study
    //     ROOT::VecOps::RVec<float> v;
    //     float vUp = 1.;//Pt;
    //     float vDown = 1.;//#Pt;
    //     if(Pt< 10) {
    //         vUp = vUp*1.04;
    //         vDown = vDown/1.04;
    //     }
    //     v.emplace_back(vUp);
    //     v.emplace_back(vDown);  
    //     return v;
    // };

    if(!_WJets) {
        auto d1 = d.Define("Wpt_dress", "GenV_dress[0]").Define("Wrap_dress", "GenV_dress[1]")
                   .Define("weightPt", getWeightPt, {"Wpt_dress"}).Define("weightY", getWeightY, {"Wrap_dress"});
        return d1;
        }
    auto d1 = d.Define("weightPt", getWeightPt, {"Wpt_dress"}).Define("weightY", getWeightY, {"Wrap_dress"});
    // auto d1 = d.Define("weightPt", getWeightPt, {"Wpt_dress"}).Define("weightY", getWeightY, {"Wrap_dress"}).Define("Qtweights", getQtweights, {"Wpt_dress"}); // used only for 10Mev study

    return d1;
}
