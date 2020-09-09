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

    auto d1 = d.Define("GenV_dress_qt", [&](ROOT::VecOps::RVec<float> vec) { return vec[0];}, {"GenV_dress"})
               .Define("GenV_dress_y", [&](ROOT::VecOps::RVec<float> vec)  { return vec[1];}, {"GenV_dress"})
               .Define("weightPt", getWeightPt, {"GenV_dress_qt"})
               .Define("weightY", getWeightY, {"GenV_dress_y"});

    return d1;
}
