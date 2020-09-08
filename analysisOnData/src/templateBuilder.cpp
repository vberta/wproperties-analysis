#include "interface/THNweightsHelper.hpp"
#include "interface/templateBuilder.hpp"

std::vector<std::string> templateBuilder::stringMultiplication(const std::vector<std::string> &v1, const std::vector<std::string> &v2)
{
  std::vector<std::string> products;
  if (v1.size() == 0) return v2;
  else
  {
    products.reserve(v1.size() * v2.size());
    for (auto e1 : v1)
    {
      for (auto e2 : v2)
      {
        products.push_back(e2 + e1);
      }
    }
    return products;
  }
}

RNode templateBuilder::run(RNode d)
{
  auto d1 = d.Define("weight", _weight);
  if (_hcat == HistoCategory::Nominal)
    return bookNominalhistos(d1);
  if (_hcat == HistoCategory::Weights)
    return bookWeightVariatedhistos(d1);
  else if (_hcat == HistoCategory::Corrected)
    return bookptCorrectedhistos(d1);
  else if (_hcat == HistoCategory::JME)
    return bookJMEvarhistos(d1);
  else
    std::cout << "Warning!! Histocategory undefined!!\n";
  return d1;
}

RNode templateBuilder::bookNominalhistos(RNode d)
//books nominal histos (=nominal + mass variations)
{
  auto d1 = d.Filter("GenV_preFSR_qt<32. && GenV_preFSR_yabs<2.4").Define("harmonicsWeightsMass", vecMultiplication, {"massWeights", "harmonicsWeights"});

  std::vector<std::string> mass = {"_massDown", "", "_massUp"};
  std::vector<std::string> total = stringMultiplication(mass, helXsecs);

  THNweightsHelper helper{"helXsecs",                                        // Name
                          "helXsecs",                                        // Title
                          {nBinsEta, nBinsPt, nBinsY, nBinsQt, nBinsCharge}, // NBins
                          {-2.4, 25., 0., 0., -2},                           // Axes min values
                          {2.4, 55., 2.4, 32., 2},                           // Axes max values
                          total};

  // We book the action: it will be treated during the event loop.
  auto templ = d1.Book<float, float, float, float, float, float, ROOT::VecOps::RVec<float>>(std::move(helper), {"Mu1_eta", "Mu1_pt", "GenV_preFSR_yabs", "GenV_preFSR_qt", "Mu1_charge", "weight", "harmonicsWeightsMass"});
  _hNGroup.push_back(templ);

  return d1;
}

RNode templateBuilder::bookWeightVariatedhistos(RNode d)
{

  auto d1 = d.Filter("GenV_preFSR_qt<32. && GenV_preFSR_yabs<2.4").Define("harmonicsWeightsSyst", vecMultiplication, {_syst_weight, "harmonicsWeights"});

  std::vector<std::string> total = stringMultiplication(_syst_name, helXsecs);

  THNweightsHelper helper{"helXsecs",                                        // Name
                          "helXsecs",                                        // Title
                          {nBinsEta, nBinsPt, nBinsY, nBinsQt, nBinsCharge}, // NBins
                          {-2.4, 25., 0., 0., -2},                           // Axes min values
                          {2.4, 55., 2.4, 32., 2},                           // Axes max values
                          total};

  // We book the action: it will be treated during the event loop.
  auto templ = d1.Book<float, float, float, float, float, float, ROOT::VecOps::RVec<float>>(std::move(helper), {"Mu1_eta", "Mu1_pt", "GenV_preFSR_yabs", "GenV_preFSR_qt", "Mu1_charge", "weight", "harmonicsWeightsSyst"});
  _hNGroup.push_back(templ);

  return d1;
}

RNode templateBuilder::bookptCorrectedhistos(RNode d)

{
  auto d1 = d.Filter("GenV_preFSR_qt<32. && GenV_preFSR_yabs<2.4");
  for (unsigned int i = 0; i < _colvarvec.size(); i++)
  {
    std::vector<std::string> tmp;
    tmp.emplace_back(_colvarvec[i]);
    std::vector<std::string> total = stringMultiplication(tmp, helXsecs);
    THNweightsHelper helper{"helXsecs",                        // Name
                            "helXsecs",                        // Title
                            {nBinsEta, nBinsPt, nBinsY, nBinsQt, nBinsCharge}, // NBins
                            {-2.4, 25., 0., 0., -2},                           // Axes min values
                            {2.4, 55., 2.4, 32., 2},                           // Axes max values
                            total};

    // We book the action: it will be treated during the event loop.
    auto templ = d1.Filter(_filtervec[i]).Book<float, float, float, float, float, float, ROOT::VecOps::RVec<float>>(std::move(helper), {"Mu1_eta", "Mu1_pt" + _colvarvec[i], "GenV_preFSR_yabs", "GenV_preFSR_qt", "Mu1_charge", "weight", "harmonicsWeights"});
    _hNGroup.push_back(templ);
  }
  return d1;
}

RNode templateBuilder::bookJMEvarhistos(RNode d)

{
  auto d1 = d.Filter("GenV_preFSR_qt<32. && GenV_preFSR_yabs<2.4").Define("harmonicsWeightsPt", vecMultiplication, {"massWeights", "harmonicsWeights"});

  for (unsigned int i = 0; i < _colvarvec.size(); i++)
  {
    std::vector<std::string> tmp;
    tmp.emplace_back(_colvarvec[i]);
    std::vector<std::string> total = stringMultiplication(tmp, helXsecs);

    THNweightsHelper helper{"helXsecs",                        // Name
                            "helXsecs",                        // Title
                            {nBinsEta, nBinsPt, nBinsY, nBinsQt, nBinsCharge}, // NBins
                            {-2.4, 25., 0., 0., -2},                           // Axes min values
                            {2.4, 55., 2.4, 32., 2},                           // Axes max values
                            total};

    // We book the action: it will be treated during the event loop.
    auto templ = d1.Filter(_filtervec[i]).Book<float, float, float, float, float, float, ROOT::VecOps::RVec<float>>(std::move(helper), {"Mu1_eta", "Mu1_pt", "GenV_preFSR_yabs", "GenV_preFSR_qt", "Mu1_charge", "weight", "harmonicsWeights"});
    _hNGroup.push_back(templ);
  }
  return d1;
}
