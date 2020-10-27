#include "interface/functions.hpp"
#include "interface/rochesterVariations.hpp"
RNode rochesterVariations::run(RNode d)
{
  std::vector<float> _pTArr = std::vector<float>(61);
  std::vector<float> _etaArr = std::vector<float>(49);
  std::vector<float> _chargeArr = std::vector<float>(3);
  for (unsigned int i = 0; i < 61; i++)
  {
    float binSize = (55. - 25.) / 60;
    _pTArr[i] = 25. + i * binSize;
  }
  for (unsigned int i = 0; i < 49; i++)
    _etaArr[i] = -2.4 + i * 4.8 / 48;
  for (int i = 0; i < 3; i++)
    _chargeArr[i] = -2. + i * 2.;
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

  auto Mu1_pt = df.Histo3D(TH3D("Mu1_ptnom", "Mu1_ptnom", _etaArr.size() - 1, _etaArr.data(), _pTArr.size() - 1, _pTArr.data(), _chargeArr.size() - 1, _chargeArr.data()), "Mu1_eta","Mu1_pt", "Mu1_charge");
  _h3List.push_back(Mu1_pt);
  auto Mu1_ptzptsystUp = df.Histo3D(TH3D("Mu1_pt_zptsystUp", "Mu1_pt_zptsystUp", _etaArr.size() - 1, _etaArr.data(), _pTArr.size() - 1, _pTArr.data(), _chargeArr.size() - 1, _chargeArr.data()), "Mu1_eta" ,"Mu1_pt_zptsystUp", "Mu1_charge");
  _h3List.push_back(Mu1_ptzptsystUp);
  auto Mu1_ptzptsystDown = df.Histo3D(TH3D("Mu1_pt_zptsystDown", "Mu1_pt_zptsystDown", _etaArr.size() - 1, _etaArr.data(), _pTArr.size() - 1, _pTArr.data(), _chargeArr.size() - 1, _chargeArr.data()), "Mu1_eta", "Mu1_pt_zptsystDown", "Mu1_charge");
  _h3List.push_back(Mu1_ptzptsystDown);
  auto Mu1_ptEwksystUp = df.Histo3D(TH3D("Mu1_pt_EwksystUp", "Mu1_pt_EwksystUp", _etaArr.size() - 1, _etaArr.data(), _pTArr.size() - 1, _pTArr.data(), _chargeArr.size() - 1, _chargeArr.data()), "Mu1_eta", "Mu1_pt_EwksystUp", "Mu1_charge");
  _h3List.push_back(Mu1_ptEwksystUp);
  auto Mu1_ptEwksystDown = df.Histo3D(TH3D("Mu1_pt_EwksystDown", "Mu1_pt_EwksystDown", _etaArr.size() - 1, _etaArr.data(), _pTArr.size() - 1, _pTArr.data(), _chargeArr.size() - 1, _chargeArr.data()), "Mu1_eta", "Mu1_pt_EwksystDown", "Mu1_charge");
  _h3List.push_back(Mu1_ptEwksystDown);
  auto Mu1_ptEwk2systUp = df.Histo3D(TH3D("Mu1_pt_Ewk2systUp", "Mu1_pt_Ewk2systUp", _etaArr.size() - 1, _etaArr.data(), _pTArr.size() - 1, _pTArr.data(), _chargeArr.size() - 1, _chargeArr.data()), "Mu1_eta", "Mu1_pt_Ewk2systUp", "Mu1_charge");
  _h3List.push_back(Mu1_ptEwk2systUp);
  auto Mu1_ptEwk2systDown = df.Histo3D(TH3D("Mu1_pt_Ewk2systDown", "Mu1_pt_Ewk2systDown", _etaArr.size() - 1, _etaArr.data(), _pTArr.size() - 1, _pTArr.data(), _chargeArr.size() - 1, _chargeArr.data()), "Mu1_eta", "Mu1_pt_Ewk2systDown", "Mu1_charge");
  _h3List.push_back(Mu1_ptEwk2systDown);
  auto Mu1_ptdeltaMsystUp = df.Histo3D(TH3D("Mu1_pt_deltaMsystUp", "Mu1_pt_deltaMsystUp", _etaArr.size() - 1, _etaArr.data(), _pTArr.size() - 1, _pTArr.data(), _chargeArr.size() - 1, _chargeArr.data()), "Mu1_eta", "Mu1_pt_deltaMsystUp", "Mu1_charge");
  _h3List.push_back(Mu1_ptdeltaMsystUp);
  auto Mu1_ptdeltaMsystDown = df.Histo3D(TH3D("Mu1_pt_deltaMsystDown", "Mu1_pt_deltaMsystDown", _etaArr.size() - 1, _etaArr.data(), _pTArr.size() - 1, _pTArr.data(), _chargeArr.size() - 1, _chargeArr.data()), "Mu1_eta", "Mu1_pt_deltaMsystDown", "Mu1_charge");
  _h3List.push_back(Mu1_ptdeltaMsystDown);

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
    auto hUp = df.Histo3D(TH3D(ptUp.c_str(), ptUp.c_str(), _etaArr.size() - 1, _etaArr.data(), _pTArr.size() - 1, _pTArr.data(), _chargeArr.size() - 1, _chargeArr.data()), "Mu1_eta", ptUp, "Mu1_charge");
    _h3List.push_back(hUp);
    auto hDown = df.Histo3D(TH3D(ptDown.c_str(), ptDown.c_str(), _etaArr.size() - 1, _etaArr.data(), _pTArr.size() - 1, _pTArr.data(), _chargeArr.size() - 1, _chargeArr.data()), "Mu1_eta", ptDown, "Mu1_charge");
    _h3List.push_back(hDown);
  }
  return df;
}

float rochesterVariations::getCorrfromhisto(std::vector<TH2D *> hvec, float pt, float eta, unsigned int idx)
{
  float cpt = pt * hvec.at(idx)->GetBinContent(hvec.at(idx)->FindBin(eta, pt));
  return cpt;
};
