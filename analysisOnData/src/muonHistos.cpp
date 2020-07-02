#include "interface/muonHistos.hpp"
#include "interface/functions.hpp"
RNode muonHistos::run(RNode d)
{
  //for MC part this is a product of few columns// for Data this is just 1.// both are passed from python config
  auto d1 = d.Define("weight", _weight);
  if (_hcat == HistoCategory::Nominal)
    return bookNominalhistos(d1);
  else if (_hcat == HistoCategory::Corrected)
    return bookptCorrectedhistos(d1);
  else if (_hcat == HistoCategory::JME)
    return bookJMEvarhistos(d1);
  else
    std::cout << "Warning!! Histocategory undefined!!\n";
  return d1;
}

RNode muonHistos::bookNominalhistos(RNode df)
{
  TH2weightsHelper helperPt(std::string("Mu1_pt"), std::string(" ; muon p_{T} (Rochester corr.); muon charge"), _pTArr.size() - 1, _pTArr, _chargeArr.size() - 1, _chargeArr, _syst_name);
  auto hpT = df.Filter(_filter).Book<float, float, float, ROOT::VecOps::RVec<float>>(std::move(helperPt), {"Mu1_pt", "Mu1_charge", "weight", _syst_weight});
  _h2Group.emplace_back(hpT);

  TH2weightsHelper helperEta(std::string("Mu1_eta"), std::string(" ; muon #{eta}; muon charge "), _etaArr.size() - 1, _etaArr, _chargeArr.size() - 1, _chargeArr, _syst_name);
  auto heta = df.Filter(_filter).Book<float, float, float, ROOT::VecOps::RVec<float>>(std::move(helperEta), {"Mu1_eta", "Mu1_charge", "weight", _syst_weight});
  _h2Group.emplace_back(heta);

  TH2weightsHelper helperMT(std::string("MT"), std::string(" ; M_{T} (Rochester corr./smear MET); muon charge "), _MTArr.size() -1, _MTArr, _chargeArr.size() - 1, _chargeArr, _syst_name);
  auto hMt = df.Filter(_filter).Book<float, float, float, ROOT::VecOps::RVec<float>>(std::move(helperMT), {"MT", "Mu1_charge", "weight", _syst_weight});
  _h2Group.emplace_back(hMt);

  return df;
}
//muon pt corrections affect both pt and MT
RNode muonHistos::bookptCorrectedhistos(RNode df)
{
  for (unsigned int i = 0; i < _colvarvec.size(); i++)
  {
    TH2weightsHelper helper_Pt(std::string("Mu1_pt_" + _colvarvec[i]), std::string(" ; muon p_{T} (Rochester corr.); muon charge "), 100, _pTArr, _chargeArr.size() - 1, _chargeArr, _syst_name);
    _h2Group.emplace_back(df.Filter(_filtervec[i]).Book<float, float, float, ROOT::VecOps::RVec<float>>(std::move(helper_Pt), {"Mu1_pt_" + _colvarvec[i], "Mu1_charge", "weight", "Nom"}));

    TH2weightsHelper helper_MT(std::string("MT_" + _colvarvec[i]), std::string(" ; M_{T} (Rochester corr./smear MET); muon charge "), 100, _MTArr, _chargeArr.size() - 1, _chargeArr, _syst_name);
    _h2Group.emplace_back(df.Filter(_filtervec[i]).Book<float, float, float, ROOT::VecOps::RVec<float>>(std::move(helper_MT), {"MT_" + _colvarvec[i], "Mu1_charge", "weight", "Nom"}));
  }
  return df;
}

//jme variations affect only MT
RNode muonHistos::bookJMEvarhistos(RNode df)
{
  for (unsigned int i = 0; i < _colvarvec.size(); i++)
  {
    TH2weightsHelper helper_MT(std::string("MT_" + _colvarvec[i]), std::string(" ; M_{T} (Rochester corr./smear MET); muon charge "), 100, _MTArr, _chargeArr.size() - 1, _chargeArr, _syst_name);
    _h2Group.emplace_back(df.Filter(_filtervec[i]).Book<float, float, float, ROOT::VecOps::RVec<float>>(std::move(helper_MT), {"MT_" + _colvarvec[i], "Mu1_charge", "weight", "Nom"}));
  }
  return df;
}

void muonHistos::setAxisarrays()
{
  for (int i = 0; i < 31; i++)
    _pTArr[i] = 25. + i;
  for (int i = 0; i < 49; i++)
    _etaArr[i] = -2.4 + i * (4.8) / 48; //eta -2.4 to 2.4
  for (int i = 0; i < 101; i++)
    _MTArr[i] = i;
  for (int i = 0; i < 3; i++)
    _chargeArr[i] = -2. +  i*2. ; //eta -1.5 to 1.5
}

std::vector<ROOT::RDF::RResultPtr<TH1D>> muonHistos::getTH1()
{
  return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> muonHistos::getTH2()
{
  return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> muonHistos::getTH3()
{
  return _h3List;
}

std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> muonHistos::getGroupTH1()
{
  return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> muonHistos::getGroupTH2()
{
  return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> muonHistos::getGroupTH3()
{
  return _h3Group;
}

void muonHistos::reset()
{

  _h1List.clear();
  _h2List.clear();
  _h3List.clear();

  _h1Group.clear();
  _h2Group.clear();
  _h3Group.clear();
}
