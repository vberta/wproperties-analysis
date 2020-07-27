#ifndef GETACVALUES_H
#define GETACVALUES_H

#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"
#include "TH1D.h"
#include "TH2D.h"
#include "TString.h"
#include "TMath.h"
#include "interface/module.hpp"
#include "interface/TH2weightsHelper.hpp"

using RNode = ROOT::RDF::RNode;

class getACValues : public Module
{

private:
  std::vector<ROOT::RDF::RResultPtr<TH1D>> _h1List;
  std::vector<ROOT::RDF::RResultPtr<TH2D>> _h2List;
  std::vector<ROOT::RDF::RResultPtr<TH3D>> _h3List;

  // groups of histos
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> _h1Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> _h2Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> _h3Group;

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
  TH2D *_mapTot;
  TFile *_fout;

public:
  getACValues(TFile *AChistos)
  {
    _AChistos = AChistos;
    _hA0 = (TH2D *)_AChistos->Get("AngCoeff/harmonicsA0");
    _hA1 = (TH2D *)_AChistos->Get("AngCoeff/harmonicsA1");
    _hA2 = (TH2D *)_AChistos->Get("AngCoeff/harmonicsA2");
    _hA3 = (TH2D *)_AChistos->Get("AngCoeff/harmonicsA3");
    _hA4 = (TH2D *)_AChistos->Get("AngCoeff/harmonicsA4");
    _hA5 = (TH2D *)_AChistos->Get("AngCoeff/harmonicsA5");
    _hA6 = (TH2D *)_AChistos->Get("AngCoeff/harmonicsA6");
    _hA7 = (TH2D *)_AChistos->Get("AngCoeff/harmonicsA7");
    _hAUL = (TH2D *)_AChistos->Get("AngCoeff/harmonicsAUL");
    _mapTot = (TH2D *)_AChistos->Get("AngCoeff/mapTot");

    getAngCoeff();

    _fout = new TFile("ACvalues.root", "recreate");
    _fout->cd();
    _hA0->Write();
    _hA1->Write();
    _hA2->Write();
    _hA3->Write();
    _hA4->Write();
    _hA5->Write();
    _hA6->Write();
    _hA7->Write();
    _hAUL->Write();
    _mapTot->Write();
  };
  ~getACValues(){
    _fout->Close();
  };

  RNode run(RNode) override;
  std::vector<ROOT::RDF::RResultPtr<TH1D>> getTH1() override;
  std::vector<ROOT::RDF::RResultPtr<TH2D>> getTH2() override;
  std::vector<ROOT::RDF::RResultPtr<TH3D>> getTH3() override;

  std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> getGroupTH1() override;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> getGroupTH2() override;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> getGroupTH3() override;

  void getAngCoeff();

  void reset() override;
};

#endif