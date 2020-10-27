#ifndef ROCHESTERWEIGHTS_H
#define ROCHESTERWEIGHTS_H

#include "module.hpp"
#include <string>
#include "TH3D.h"
#include "TFile.h"
#include "TKey.h"
#include <vector>

class rochesterWeights : public Module
{

private:
  TFile *_corrF;
  std::vector<TH3D *> _weights;

public:
  rochesterWeights(TFile *cf)
  {

    _corrF = cf;
    _weights.emplace_back((TH3D *)_corrF->Get("Mu1_pt_zptsystUp"));
    _weights.emplace_back((TH3D *)_corrF->Get("Mu1_pt_zptsystDown"));

    _weights.emplace_back((TH3D *)_corrF->Get("Mu1_pt_EwksystUp"));
    _weights.emplace_back((TH3D *)_corrF->Get("Mu1_pt_EwksystDown"));

    _weights.emplace_back((TH3D *)_corrF->Get("Mu1_pt_deltaMsystUp"));
    _weights.emplace_back((TH3D *)_corrF->Get("Mu1_pt_deltaMsystDown"));

    _weights.emplace_back((TH3D *)_corrF->Get("Mu1_pt_Ewk2systUp"));
    _weights.emplace_back((TH3D *)_corrF->Get("Mu1_pt_Ewk2systDown"));

    for (unsigned int i = 0; i < 99; i++)
    {
      _weights.emplace_back((TH3D *)_corrF->Get(Form("Mu1_pt_stateig%dUp", i)));
      _weights.emplace_back((TH3D *)_corrF->Get(Form("Mu1_pt_stateig%dDown", i)));
    }
  }

  ~rochesterWeights() {}
  RNode run(RNode) override;
};

#endif
