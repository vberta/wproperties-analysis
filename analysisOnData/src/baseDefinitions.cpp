#include "interface/baseDefinitions.hpp"
#include "interface/functions.hpp"

RNode baseDefinitions::run(RNode d)
{
    //define everything conerning muons
    auto d1 = d.Define("Mu1_eta", "Muon_eta[Idx_mu1]")
               .Define("Mu1_pt", "Muon_corrected_pt[Idx_mu1]")
               .Define("Mu1_phi", "Muon_phi[Idx_mu1]")
               .Define("Mu1_dz", "Muon_dz[Idx_mu1]")
               .Define("Mu1_relIso", "Muon_pfRelIso04_all[Idx_mu1]")
               .Define("Mu1_sip3d", "Muon_sip3d[Idx_mu1]")
               .Define("Mu1_dxy", "Muon_dxy[Idx_mu1]")
               .Define("Mu1_Up_pt", "Muon_correctedUp_pt[Idx_mu1]")
               .Define("Mu1_Down_pt", "Muon_correctedDown_pt[Idx_mu1]");
    //now get composite variables
    auto d1withCompvar = d1.Define("MT_nominal", W_mt, { "Mu1_pt", "Mu1_phi", "MET_pt_nom", "MET_phi_nom"})
                           .Define("MT_Up_pt", W_mt, { "Mu1_Up_pt", "Mu1_phi", "MET_pt_nom", "MET_phi_nom"})
                           .Define("MT_Down_pt", W_mt, { "Mu1_Down_pt", "Mu1_phi", "MET_pt_nom", "MET_phi_nom"});

    return d1withCompvar;
}

std::vector<ROOT::RDF::RResultPtr<TH1D>> baseDefinitions::getTH1()
{
    return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> baseDefinitions::getTH2()
{
    return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> baseDefinitions::getTH3()
{
    return _h3List;
}

std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> baseDefinitions::getGroupTH1()
{
    return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> baseDefinitions::getGroupTH2()
{
    return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> baseDefinitions::getGroupTH3()
{
    return _h3Group;
}

void baseDefinitions::reset()
{

    _h1List.clear();
    _h2List.clear();
    _h3List.clear();

    _h1Group.clear();
    _h2Group.clear();
    _h3Group.clear();
}
