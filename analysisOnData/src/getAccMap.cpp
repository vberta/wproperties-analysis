#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"
#include "interface/getAccMap.hpp"

RNode getAccMap::run(RNode d){

    auto fillAccMapEta = [this](float y, float pt)mutable->float{

        int bin = _mapAccEta->FindBin(y, pt);
        return _mapAccEta->GetBinContent(bin);

    };

    auto fillAccMap = [this](float y, float pt) mutable -> float {
        int bin = _mapAcc->FindBin(y, pt);
        return _mapAcc->GetBinContent(bin);
    };

    auto fillTotMap = [this](float y, float pt) mutable -> float {
        int bin = _mapTot->FindBin(y, pt);
        return _mapTot->GetBinContent(bin);
    };

    auto d1 = d.Define("accMapEta", fillAccMapEta, {"Wrap_preFSR_abs", "Wpt_preFSR"}).Define("accMap", fillAccMap, {"Wrap_preFSR_abs", "Wpt_preFSR"}).Define("totMap", fillTotMap, {"Wrap_preFSR_abs", "Wpt_preFSR"});
    return d1;

}