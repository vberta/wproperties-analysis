#include "interface/getACValues.hpp"

void getACValues::getAngCoeff()
{

    _hA0->Divide(_mapTot);
    _hA1->Divide(_mapTot);
    _hA2->Divide(_mapTot);
    _hA3->Divide(_mapTot);
    _hA4->Divide(_mapTot);
    _hA5->Divide(_mapTot);
    _hA6->Divide(_mapTot);
    _hA7->Divide(_mapTot);

    for (int xbin = 1; xbin < _hA0->GetNbinsX() + 1; xbin++)
    {
        for (int ybin = 1; ybin < _hA0->GetNbinsY() + 1; ybin++)
        {

            auto content = _hA0->GetBinContent(xbin, ybin);
            _hA0->SetBinContent(xbin, ybin, 20. / 3. * (content + 1. / 10.));
        }
    }
    _hA2->Scale(20.);
    _hA1->Scale(5.);
    _hA5->Scale(5.);
    _hA6->Scale(5.);
    _hA3->Scale(4.);
    _hA4->Scale(4.);
    _hA7->Scale(4.);

}

RNode getACValues::run(RNode d)
{

    auto getACValues = [this](float y, float pt) mutable {
        
        ROOT::VecOps::RVec<float> AngCoeff;

        int bin = _hA0->FindBin(y, pt);
        AngCoeff.push_back(_hA0->GetBinContent(bin));
        AngCoeff.push_back(_hA1->GetBinContent(bin));
        AngCoeff.push_back(_hA2->GetBinContent(bin));
        AngCoeff.push_back(_hA3->GetBinContent(bin));
        AngCoeff.push_back(_hA4->GetBinContent(bin));
        AngCoeff.push_back(_hA5->GetBinContent(bin));
        AngCoeff.push_back(_hA6->GetBinContent(bin));
        AngCoeff.push_back(_hA7->GetBinContent(bin));
        AngCoeff.push_back(_hAUL->GetBinContent(bin));

        return AngCoeff;
    };

    auto d1 = d.Define("AngCoeffVec", getACValues, {"Wrap_preFSR_abs", "Wpt_preFSR"});

    return d1;
}

std::vector<ROOT::RDF::RResultPtr<TH1D>> getACValues::getTH1()
{
    return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> getACValues::getTH2()
{
    return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> getACValues::getTH3()
{
    return _h3List;
}

std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> getACValues::getGroupTH1()
{
    return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> getACValues::getGroupTH2()
{
    return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> getACValues::getGroupTH3()
{
    return _h3Group;
}

void getACValues::reset()
{

    _h1List.clear();
    _h2List.clear();
    _h3List.clear();

    _h1Group.clear();
    _h2Group.clear();
    _h3Group.clear();
}