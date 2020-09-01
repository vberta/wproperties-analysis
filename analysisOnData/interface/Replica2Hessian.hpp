#ifndef REPLICA2HESSIAN_H
#define REPLICA2HESSIAN_H

#include "module.hpp"
#include "PDFWeightsHelper.hpp"

class Replica2Hessian : public Module
{

private:
  
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

};

#endif
