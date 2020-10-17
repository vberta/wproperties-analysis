#ifndef GETACVALUES_H
#define GETACVALUES_H

#include "module.hpp"

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
  TH2D *_htotMap;

public:
  getACValues(TFile *AChistos)
  {
    _AChistos = AChistos;
    _hA0 = (TH2D *)_AChistos->Get("angularCoefficients/harmonicsA0_nom_nom");
    _hA1 = (TH2D *)_AChistos->Get("angularCoefficients/harmonicsA1_nom_nom");
    _hA2 = (TH2D *)_AChistos->Get("angularCoefficients/harmonicsA2_nom_nom");
    _hA3 = (TH2D *)_AChistos->Get("angularCoefficients/harmonicsA3_nom_nom");
    _hA4 = (TH2D *)_AChistos->Get("angularCoefficients/harmonicsA4_nom_nom");
    _hA5 = (TH2D *)_AChistos->Get("angularCoefficients/harmonicsA5_nom_nom");
    _hA6 = (TH2D *)_AChistos->Get("angularCoefficients/harmonicsA6_nom_nom");
    _hA7 = (TH2D *)_AChistos->Get("angularCoefficients/harmonicsA7_nom_nom");
    _hAUL = (TH2D *)_AChistos->Get("angularCoefficients/harmonicsAUL_nom_nom");
    _htotMap = (TH2D *)_AChistos->Get("accMaps/mapTot");
  };
  
  ~getACValues(){};

  RNode run(RNode) override;
  void getAngCoeff();
};

#endif
