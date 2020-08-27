#include "interface/getMassWeights.hpp"

RNode getMassWeights::run(RNode d)
{

  auto BreitWigner = [](float Q2, float M2, float G2) -> float {
    return 1. / ((Q2 - M2) * (Q2 - M2) + M2 * G2);
  };

  auto getBWVec = [&](float Q) {
    ROOT::VecOps::RVec<float> v;

    float w1 = BreitWigner(Q * Q, 80.419002 * 80.419002, 2.0476 * 2.0476) /
         BreitWigner(Q * Q, 80.319002 * 80.319002, 2.0476 * 2.0476);
    v.emplace_back(w1);
    v.emplace_back(1.);
    float w2 = BreitWigner(Q * Q, 80.419002 * 80.419002, 2.0476 * 2.0476) /
         BreitWigner(Q * Q, 80.519002 * 80.519002, 2.0476 * 2.0476);
    v.emplace_back(w2);
    
    return v;
  };

  auto d1 = d.Define("massWeights", getBWVec, {"Wmass_preFSR"});
  return d1;
}

std::vector<ROOT::RDF::RResultPtr<TH1D>> getMassWeights::getTH1()
{
  return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> getMassWeights::getTH2()
{
  return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> getMassWeights::getTH3()
{
  return _h3List;
}

std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> getMassWeights::getGroupTH1()
{
  return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> getMassWeights::getGroupTH2()
{
  return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> getMassWeights::getGroupTH3()
{
  return _h3Group;
}

void getMassWeights::reset()
{

  _h1List.clear();
  _h2List.clear();
  _h3List.clear();

  _h1Group.clear();
  _h2Group.clear();
  _h3Group.clear();
}