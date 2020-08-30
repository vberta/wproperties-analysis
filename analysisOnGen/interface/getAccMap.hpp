#ifndef GETACCMAP_H
#define GETACCMAP_H

#include "module.hpp"

class getAccMap : public Module {

    private:

    TFile *_maps;
    TH2D* _mapAccEta;
    TH2D* _mapAcc;
    TH2D* _mapTot;

  public:
    getAccMap(TFile *maps)
    {
      _maps = maps;
      _mapAccEta = (TH2D *)_maps->Get("accMaps/mapAccEta");
      _mapAcc = (TH2D *)_maps->Get("accMaps/mapAcc");
      _mapTot = (TH2D *)_maps->Get("accMaps/mapTot");

      _mapAccEta->Divide(_mapTot);
      _mapAcc->Divide(_mapTot);

    };

    ~getAccMap() {};

    RNode run(RNode) override;

};

#endif