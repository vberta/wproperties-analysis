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
  std::vector<TH2D *> _histos;
  TFile *_fout;

public:
  getACValues(TFile *AChistos)
  {
    _AChistos = AChistos;
    TH2D *hA0 = (TH2D *)_AChistos->Get("AngCoeff/harmonicsA0");
    _histos.push_back(hA0);
    TH2D *hA1 = (TH2D *)_AChistos->Get("AngCoeff/harmonicsA1");
    _histos.push_back(hA1);
    TH2D *hA2 = (TH2D *)_AChistos->Get("AngCoeff/harmonicsA2");
    _histos.push_back(hA2);
    TH2D *hA3 = (TH2D *)_AChistos->Get("AngCoeff/harmonicsA3");
    _histos.push_back(hA3);
    TH2D *hA4 = (TH2D *)_AChistos->Get("AngCoeff/harmonicsA4");
    _histos.push_back(hA4);
    TH2D *hA5 = (TH2D *)_AChistos->Get("AngCoeff/harmonicsA5");
    _histos.push_back(hA5);
    TH2D *hA6 = (TH2D *)_AChistos->Get("AngCoeff/harmonicsA6");
    _histos.push_back(hA6);
    TH2D *hA7 = (TH2D *)_AChistos->Get("AngCoeff/harmonicsA7");
    _histos.push_back(hA7);
    TH2D *hAUL = (TH2D *)_AChistos->Get("AngCoeff/harmonicsAUL");
    _histos.push_back(hAUL);

    getAngCoeff(_histos);

    _fout = new TFile("ACvalues.root", "recreate");
    _fout->cd();
    for (auto &h : _histos) h->Write();
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

  void getAngCoeff(std::vector<TH2D*>);

  void reset() override;
};

#endif