#include "interface/functions.hpp"
#include "interface/rochesterVariations.hpp"
RNode rochesterVariations::run(RNode d)
{
  
  auto df = d.Define("Mu1_pt_zptsystUp", [this](float pt, float eta) { return getCorrfromhisto(_Zptcorv, pt, eta, 0); }, {"Mu1_pt", "Mu1_eta"})
                .Define("Mu1_pt_zptsystDown", [this](float pt, float eta) { return getCorrfromhisto(_Zptcorv, pt, eta, 1); }, {"Mu1_pt", "Mu1_eta"})
                .Define("MT_zptsystUp", W_mt, {"Mu1_pt_zptsystUp", "Mu1_phi", "MET_pt_nom", "MET_phi_nom"})
                .Define("MT_zptsystDown", W_mt, {"Mu1_pt_zptsystDown", "Mu1_phi", "MET_pt_nom", "MET_phi_nom"})
                .Define("Mu1_pt_EwksystUp", [this](float pt, float eta) { return getCorrfromhisto(_Ewkcorv, pt, eta, 0); }, {"Mu1_pt", "Mu1_eta"})
                .Define("Mu1_pt_EwksystDown", [this](float pt, float eta) { return getCorrfromhisto(_Ewkcorv, pt, eta, 1); }, {"Mu1_pt", "Mu1_eta"})
                .Define("MT_EwksystUp", W_mt, {"Mu1_pt_EwksystUp", "Mu1_phi", "MET_pt_nom", "MET_phi_nom"})
                .Define("MT_EwksystDown", W_mt, {"Mu1_pt_EwksystDown", "Mu1_phi", "MET_pt_nom", "MET_phi_nom"})
                .Define("Mu1_pt_deltaMsystUp", [this](float pt, float eta) { return getCorrfromhisto(_deltaMcorv, pt, eta, 0); }, {"Mu1_pt", "Mu1_eta"})
                .Define("Mu1_pt_deltaMsystDown", [this](float pt, float eta) { return getCorrfromhisto(_deltaMcorv, pt, eta, 1); }, {"Mu1_pt", "Mu1_eta"})
                .Define("MT_deltaMsystUp", W_mt, {"Mu1_pt_deltaMsystUp", "Mu1_phi", "MET_pt_nom", "MET_phi_nom"})
                .Define("MT_deltaMsystDown", W_mt, {"Mu1_pt_deltaMsystDown", "Mu1_phi", "MET_pt_nom", "MET_phi_nom"})
                .Define("Mu1_pt_Ewk2systUp", [this](float pt, float eta) { return getCorrfromhisto(_Ewk2corv, pt, eta, 0); }, {"Mu1_pt", "Mu1_eta"})
                .Define("Mu1_pt_Ewk2systDown", [this](float pt, float eta) { return getCorrfromhisto(_Ewk2corv, pt, eta, 1); }, {"Mu1_pt", "Mu1_eta"})
                .Define("MT_Ewk2systUp", W_mt, {"Mu1_pt_Ewk2systUp", "Mu1_phi", "MET_pt_nom", "MET_phi_nom"})
                .Define("MT_Ewk2systDown", W_mt, {"Mu1_pt_Ewk2systDown", "Mu1_phi", "MET_pt_nom", "MET_phi_nom"});

  for (unsigned int idx = 0; idx < 99; idx++)
  {
    std::string ptDown = "Mu1_pt_stateig" + std::to_string(idx) + "Down";
    std::string mtDown = "MT_stateig" + std::to_string(idx) + "Down";
    std::string ptUp = "Mu1_pt_stateig" + std::to_string(idx) + "Up";
    std::string mtUp = "MT_stateig" + std::to_string(idx) + "Up";

    auto cUp = [this, idx](float pt, float eta) {
      float cpt = 1.;
      if (_statUpv[idx])
      {
        int bin = _statUpv[idx]->FindBin(eta, pt);
        cpt = pt * _statUpv[idx]->GetBinContent(bin);
      }
      else std::cout << "Error: histo up not found at index" << idx << std::endl;
      return cpt;
    };

    auto cDown = [this,idx](float pt, float eta) {
      float cpt = 1.;
      if (_statDownv[idx])
      {
        int bin = _statDownv[idx]->FindBin(eta, pt);
        cpt = pt * _statDownv[idx]->GetBinContent(bin);
      }
      else std::cout<< "Error: histo down not found at index" << idx <<std::endl;
      return cpt;
    };

    df = df.Define(ptDown, cUp, {"Mu1_pt", "Mu1_eta"})
             .Define(mtDown, W_mt, {ptDown, "Mu1_phi", "MET_pt_nom", "MET_phi_nom"})
             .Define(ptUp, cDown, {"Mu1_pt", "Mu1_eta"})
             .Define(mtUp, W_mt, {ptUp, "Mu1_phi", "MET_pt_nom", "MET_phi_nom"});
  }
  return df;
}

float rochesterVariations::getCorrfromhisto(std::vector<TH2D *> hvec, float pt, float eta, unsigned int idx)
{
  float cpt = pt * hvec.at(idx)->GetBinContent(hvec.at(idx)->FindBin(eta, pt));
  return cpt;
};
