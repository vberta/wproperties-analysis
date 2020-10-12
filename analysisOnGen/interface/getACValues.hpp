#ifndef GETACVALUES_H
#define GETACVALUES_H

#include "interface/module.hpp"

using RNode = ROOT::RDF::RNode;

class getACValues : public Module
{

private:

  TFile *_AChistos;
  TH2D* _hA0;
  TH2D *_hA1;
  TH2D *_hA2;
  TH2D *_hA3;
  TH2D *_hA4;
  TH2D *_hA5;
  TH2D *_hA6;
  TH2D *_hA7;
  TH2D *_hAUL;

public:
  getACValues(TFile *AChistos)
  {
    _AChistos = AChistos;
    _hA0 = (TH2D *)_AChistos->Get("angularCoefficients/harmonicsA0");
    _hA1 = (TH2D *)_AChistos->Get("angularCoefficients/harmonicsA1");
    _hA2 = (TH2D *)_AChistos->Get("angularCoefficients/harmonicsA2");
    _hA3 = (TH2D *)_AChistos->Get("angularCoefficients/harmonicsA3");
    _hA4 = (TH2D *)_AChistos->Get("angularCoefficients/harmonicsA4");
    _hA5 = (TH2D *)_AChistos->Get("angularCoefficients/harmonicsA5");
    _hA6 = (TH2D *)_AChistos->Get("angularCoefficients/harmonicsA6");
    _hA7 = (TH2D *)_AChistos->Get("angularCoefficients/harmonicsA7");
    _hAUL = (TH2D *)_AChistos->Get("angularCoefficients/harmonicsAUL");
  };
  
  ~getACValues(){};

  RNode run(RNode) override;
  void getAngCoeff();
};

#endif
