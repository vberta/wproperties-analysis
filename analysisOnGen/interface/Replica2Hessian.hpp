#ifndef REPLICA2HESSIAN_H
#define REPLICA2HESSIAN_H

//#include "ROOT/RDataFrame.hxx"
//#include "ROOT/RVec.hxx"
//#include "ROOT/RDF/RInterface.hxx"
//#include "TH1D.h"
//#include "TH2D.h"
//#include "TString.h"
//#include "TMath.h"
//#include "interface/PDFWeightsHelper.hpp"
//#include "interface/TH1weightsHelper.hpp"
#include "module.hpp"

using namespace ROOT::VecOps;
using RNode = ROOT::RDF::RNode;
using rvec_f = const RVec<float> &;
using rvec_i = const RVec<int> &;
using rvec_d = const RVec<double> &;

///template <typename T, unsigned int NDIM>
class Replica2Hessian : public Module
{

private:
  //std::vector<ROOT::RDF::RResultPtr<TH1D>> _h1List;
  //std::vector<ROOT::RDF::RResultPtr<TH2D>> _h2List;
  //std::vector<ROOT::RDF::RResultPtr<TH3D>> _h3List;

  // groups of histos
  //std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> _h1Group;
  //std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> _h2Group;
  //std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> _h3Group;

  unsigned int nPdfWeights_ = 100;
  unsigned int nPdfEigWeights_ = 60;
  std::string inFile_ = "NNPDF30_nlo_as_0118_hessian_60.csv";
  PDFWeightsHelper pdfweightshelper_;

  const int nBinsPt_ = 80;
  std::vector<float> ptArr_;
  std::vector<std::string> PDFArrRepl_;
  std::vector<std::string> PDFArrHess_;

public:
  Replica2Hessian() : ptArr_(nBinsPt_ + 1)
  {
    pdfweightshelper_.Init(nPdfWeights_, nPdfEigWeights_, inFile_);
    for (int i = 0; i < nBinsPt_ + 1; i++)
    {
      float binSize = (65. - 25.) / nBinsPt_;
      ptArr_[i] = 25. + i * binSize;
    }
    for (unsigned int i = 0; i < nPdfWeights_; i++)
      PDFArrRepl_.push_back("replica_" + std::to_string(i));
    for (unsigned int i = 0; i < nPdfEigWeights_; i++)
      PDFArrHess_.push_back("hess_" + std::to_string(i));
  };
  ~Replica2Hessian(){};

  RNode run(RNode d) override;
  //std::vector<ROOT::RDF::RResultPtr<TH1D>> getTH1();
  //    std::vector<ROOT::RDF::RResultPtr<TH2D>> getTH2();
  //std::vector<ROOT::RDF::RResultPtr<TH3D>> getTH3();

  //        std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> getGroupTH1();
  //      std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> getGroupTH2();
  //      std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> getGroupTH3();

  //      void reset();
};

#endif
