#include "interface/bkgHistos.hpp"

RNode bkgHistos::run(RNode d)
{

    // add here all the plots to be used for inputs for extracting the fake rates

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