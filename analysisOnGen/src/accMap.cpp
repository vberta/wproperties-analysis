#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"
#include "interface/accMap.hpp"

RNode accMap::run(RNode d){
    
    auto d1 = d.Filter(_filter);

    auto mapTot = d1.Histo2D(TH2D("mapTot", "mapTot", _nBinsY, _yArr.data(), _nBinsPt, _ptArr.data()), "Wrap_preFSR_abs", "Wpt_preFSR", "weight");
    auto mapAccEta = d1.Filter("fabs(Mueta_preFSR)<2.4").Histo2D(TH2D("mapAccEta", "mapAccEta", _nBinsY, _yArr.data(), _nBinsPt, _ptArr.data()), "Wrap_preFSR_abs", "Wpt_preFSR", "weight");
    auto mapAcc = d1.Filter("fabs(Mueta_preFSR)<2.4 && Mupt_preFSR>25. && Mupt_preFSR<65.").Histo2D(TH2D("mapAcc", "mapAcc", _nBinsY, _yArr.data(), _nBinsPt, _ptArr.data()), "Wrap_preFSR_abs", "Wpt_preFSR", "weight");
    auto sumw = d1.Define("genratio", "Generator_weight/genEventSumw").Define("genratioRew", "genratio*weightPt*weightY").Histo2D(TH2D("sumw", "sumw", _nBinsY, _yArr.data(), _nBinsPt, _ptArr.data()), "Wrap_preFSR_abs", "Wpt_preFSR", "genratioRew");

    _h2List.push_back(mapTot);
    _h2List.push_back(mapAccEta);
    _h2List.push_back(mapAcc);
    _h2List.push_back(sumw);
    
    return d;

}