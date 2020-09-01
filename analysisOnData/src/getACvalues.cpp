#include "interface/getACValues.hpp"


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
