#include "interface/bkgHistos.hpp"

RNode bkgHistos::run(RNode d)
{
    /*
    // add here all the plots to be used for inputs for extracting the fake rates
    TH3weightsHelper helper(std::string("muon_pt"), std::string(" ; muon p_{T} (Rochester corr.); "), 100, pTArr, _weight);

    auto hpT = d1.Book<float, float, ROOT::VecOps::RVec<float>>(std::move(helper), {"muon_pt", "weight", _syst_name.size() > 0 ? _syst_weight : "dummy"});
    _h1Group.emplace_back(hpT);
    */
    return d;
}

std::vector<ROOT::RDF::RResultPtr<TH1D>> bkgHistos::getTH1()
{
    return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> bkgHistos::getTH2()
{
    return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> bkgHistos::getTH3()
{
    return _h3List;
}

std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> bkgHistos::getGroupTH1()
{
    return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> bkgHistos::getGroupTH2()
{
    return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> bkgHistos::getGroupTH3()
{
    return _h3Group;
}

void bkgHistos::reset()
{

    _h1List.clear();
    _h2List.clear();
    _h3List.clear();

    _h1Group.clear();
    _h2Group.clear();
    _h3Group.clear();
}