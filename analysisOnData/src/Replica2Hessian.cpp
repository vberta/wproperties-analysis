#include "interface/Replica2Hessian.hpp"

RNode Replica2Hessian::run(RNode d)
{

  auto newPDFweights = [this](rvec_f replicas, float lhenom, unsigned long long ev) {
    std::vector<float> raw_weights;

    for (unsigned int i = 0; i < nPdfWeights_; i++)
    {
      raw_weights.push_back(replicas[i] * lhenom);
    }
    std::vector<float> raw_Hessweights;
    raw_Hessweights.resize(nPdfEigWeights_);

    pdfweightshelper_.DoMC2Hessian(lhenom, raw_weights.data(), raw_Hessweights.data());

    for (unsigned int i = 0; i < nPdfEigWeights_; i++)
    {
      raw_Hessweights[i] = raw_Hessweights[i] / lhenom;
    }
    return ROOT::VecOps::RVec<float>(raw_Hessweights);
  };

  auto d1 = d.Define("nLHEPdfWeightHess", [this]() { return nPdfEigWeights_ - 1; }).Define("LHEPdfWeightHess", newPDFweights, {"LHEPdfWeight", "LHEWeight_originalXWGTUP", "event"});

  return d1;
}