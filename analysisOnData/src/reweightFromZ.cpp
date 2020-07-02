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

std::vector<ROOT::RDF::RResultPtr<TH1D>> reweightFromZ::getTH1()
{
    return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> reweightFromZ::getTH2()
{
    return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> reweightFromZ::getTH3()
{
    return _h3List;
}

std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> reweightFromZ::getGroupTH1()
{
    return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> reweightFromZ::getGroupTH2()
{
    return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> reweightFromZ::getGroupTH3()
{
    return _h3Group;
}

void reweightFromZ::reset()
{

    _h1List.clear();
    _h2List.clear();
    _h3List.clear();

    _h1Group.clear();
    _h2Group.clear();
    _h3Group.clear();
}
