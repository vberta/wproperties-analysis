#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"
#include "interface/templateBuilder.hpp"

std::vector<std::string> templateBuilder::stringMultiplication(const std::vector<std::string> &v1, const std::vector<std::string> &v2)
{

  std::vector<std::string> products;

  if (v1.size() == 0)
    return v2;

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

  TH3::SetDefaultSumw2(true);
  TH2::SetDefaultSumw2(true);

  std::vector<float> yArr = {0, 0.4, 0.8, 1.2, 1.6, 2.0, 2.4};
  std::vector<float> qtArr = {0., 4., 8., 12., 16., 20., 24., 28., 32.};

  const int nBinsY = 6;
  const int nBinsQt = 8;

  // whelicity binning
  // const int nBinsEta = 48;
  // const int nBinsPt = 29;

  // std::vector<float> etaArr(nBinsEta + 1);
  // std::vector<float> ptArr(nBinsPt + 1);

  // for (unsigned int i = 0; i < 30; i++)
  //   ptArr[i] = 26. + i;
  // for (unsigned int i = 0; i < 49; i++)
  //   etaArr[i] = -2.4 + i * (4.8) / 48; //eta -2.4 to 2.4

  const int nBinsEta = 100;
  const int nBinsPt = 80;

  std::vector<float> etaArr(nBinsEta + 1);
  std::vector<float> ptArr(nBinsPt + 1);

  for (int i = 0; i < nBinsEta + 1; i++)
  {

    float binSize = 5.0 / nBinsEta;
    etaArr[i] = -2.5 + i * binSize;
  }

  for (int i = 0; i < nBinsPt + 1; i++)
  {

    float binSize = (65. - 25.) / nBinsPt;
    ptArr[i] = 25. + i * binSize;
  }

  auto vecMultiplication = [](const ROOT::VecOps::RVec<float> &v1, const ROOT::VecOps::RVec<float> &v2) {
    ROOT::VecOps::RVec<float> products;

    products.reserve(v1.size() * v2.size());
    for (auto e1 : v1)
      for (auto e2 : v2)
        products.push_back(e1 * e2);

    return products;
  };

  auto dFit = d.Filter("Wpt_preFSR<32. && Wrap_preFSR_abs<2.4").Define("harmonicsWeightsMass", vecMultiplication, {"massWeights", "harmonicsWeights"});

  // auto cut1 = [](float map){ return map > 0.4;};
  // auto cut2 = [](float map){ return map < 0.4;};

  // auto dFit = d.Filter("fabs(Mueta_preFSR)<2.4 && Mupt_preFSR>25. && Mupt_preFSR<65.").Filter(cut1, {"accMapEta"}, "accMapEta fit");
  // auto cutReport1 = dFit.Report();

  // auto dFix = d.Filter("fabs(Mueta_preFSR)<2.4 && Mupt_preFSR>25. && Mupt_preFSR<65.").Filter(cut2, {"accMapEta"}, "accMapEta fix");
  // auto cutReport2 = dFix.Report();

  // cutReport1->Print();
  // cutReport2->Print();

  std::vector<std::string> helXsecs = {"L", "I", "T", "A", "P", "7", "8", "9", "UL"};
  std::vector<std::string> mass = {"_massDown", "", "_massUp"};
  std::vector<std::string> total = stringMultiplication(mass, helXsecs);

  // templates for the fit
  // auto h = new TH2F("h", "h", nBinsY, yArr.data(), nBinsQt, qtArr.data());

  // for(int j=1; j<h->GetNbinsY()+1; j++){ // for each W pt bin

  //   float lowEdgePt = h->GetYaxis()->GetBinLowEdge(j);
  //   float upEdgePt = h->GetYaxis()->GetBinUpEdge(j);

  //   auto sel = [lowEdgePt, upEdgePt](float pt) { return (pt >lowEdgePt && pt<upEdgePt);};

  //   TH3weightsHelper helperHelXsecs(std::string("pt_")+std::to_string(j)+std::string("_helXsecs_"), std::string("pt_")+std::to_string(j)+std::string("_helXsecs_"), nBinsEta, etaArr, nBinsPt, ptArr, nBinsY, yArr, total);
  //   auto htmp = dFit.Filter(sel, {"Wpt_preFSR"}).Book<float, float, float, float, ROOT::VecOps::RVec<float>>(std::move(helperHelXsecs), {"Mueta_preFSR", "Mupt_preFSR", "Wrap_preFSR_abs", "lumiweight", "harmonicsWeightsMass"});
  //   _h3Group.push_back(htmp);

  // }

  // Our Helper type: templated on the internal THnT type, the size, the types of the columns
  // we'll use to fill.
  using Helper_t = THnHelper<float, 4>;

  Helper_t helper{"helXsecs",                           // Name
                  "helXsecs",                           // Title
                  {nBinsEta, nBinsPt, nBinsY, nBinsQt}, // NBins
                  {-2.4, 25., 0., 0.},                  // Axes min values
                  {2.4, 65., 2.4, 32.},
                  total}; // Axes max values

  // We book the action: it will be treated during the event loop.
  auto templ = dFit.Book<float, float, float, float, float, ROOT::VecOps::RVec<float>>(std::move(helper), {"Mueta_preFSR", "Mupt_preFSR", "Wrap_preFSR_abs", "Wpt_preFSR", "lumiweight", "harmonicsWeightsMass"});
  _hNGroup.push_back(templ);

  return dFit;
}