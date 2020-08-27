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

RNode templateBuilder::run(RNode d){

  TH3::SetDefaultSumw2(true);
  TH2::SetDefaultSumw2(true);

  std::vector<float> yArr = {0, 0.4, 0.8, 1.2 ,1.6, 2.0, 2.4};
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
  std::vector<std::string> mass = {"Up", "", "Down"};
  std::vector<std::string> total = stringMultiplication(helXsecs, mass);

  // first the templates for the fit
  auto h = new TH2F("h", "h", nBinsY, yArr.data(), nBinsQt, qtArr.data());

  for(int j=1; j<h->GetNbinsY()+1; j++){ // for each W pt bin

    float lowEdgePt = h->GetYaxis()->GetBinLowEdge(j);
    float upEdgePt = h->GetYaxis()->GetBinUpEdge(j);

    auto sel = [lowEdgePt, upEdgePt](float pt) { return (pt >lowEdgePt && pt<upEdgePt);};

    TH3weightsHelper helperHelXsecs(std::string("pt_")+std::to_string(j)+std::string("_helXsecs_"), std::string("pt_")+std::to_string(j)+std::string("_helXsecs_"), nBinsEta, etaArr, nBinsPt, ptArr, nBinsY, yArr, total);
    auto htmp = dFit.Filter(sel, {"Wpt_preFSR"}).Book<float, float, float, float, ROOT::VecOps::RVec<float>>(std::move(helperHelXsecs), {"Mueta_preFSR", "Mupt_preFSR", "Wrap_preFSR_abs", "lumiweight", "harmonicsWeightsMass"});
    _h3Group.push_back(htmp);

  }

  return dFit;
  
  }

std::vector<ROOT::RDF::RResultPtr<TH1D>> templateBuilder::getTH1(){ 
    return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> templateBuilder::getTH2(){ 
    return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> templateBuilder::getTH3(){ 
    return _h3List;
}

std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> templateBuilder::getGroupTH1(){ 
  return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> templateBuilder::getGroupTH2(){ 
  return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> templateBuilder::getGroupTH3(){ 
  return _h3Group;
}

void templateBuilder::reset(){
    
    _h1List.clear();
    _h2List.clear();
    _h3List.clear();

    _h1Group.clear();
    _h2Group.clear();
    _h3Group.clear();

}
