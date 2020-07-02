#ifndef REWEIGHTFROMZ_H
#define REWEIGHTFROMZ_H

#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"
#include "TH1D.h"
#include "TH2D.h"
#include "TString.h"
#include "TMath.h"
#include "TFile.h"
#include "interface/module.hpp"

using RNode = ROOT::RDF::RNode;

class reweightFromZ : public Module
{

private:
    std::vector<ROOT::RDF::RResultPtr<TH1D>> _h1List;
    std::vector<ROOT::RDF::RResultPtr<TH2D>> _h2List;
    std::vector<ROOT::RDF::RResultPtr<TH3D>> _h3List;
    
    // groups of histos
    std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> _h1Group;
    std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> _h2Group;
    std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> _h3Group;

    TFile *_Pt;
    TFile *_Y;

    TH1F *_hPt;
    TH1F *_hY;

public:
    reweightFromZ(TFile *Pt, TFile *Y)
    {
        _Pt = Pt;
        _Y = Y;

        _hPt = (TH1F *)_Pt->Get("unfold");
        TH1F *hPtMC = (TH1F *)_Pt->Get("hDDilPtLL");
        _hY = (TH1F *)_Y->Get("unfold");
        TH1F *hYMC = (TH1F *)_Y->Get("hDDilRapLL");

        _hPt->Divide(hPtMC);
        _hPt->Scale(0.979);

        hYMC->Scale(_hY->Integral() / hYMC->Integral());
        _hY->Divide(hYMC);
    };
    ~reweightFromZ(){};

        RNode run(RNode) override;
    std::vector<ROOT::RDF::RResultPtr<TH1D>> getTH1() override;
    std::vector<ROOT::RDF::RResultPtr<TH2D>> getTH2() override;
    std::vector<ROOT::RDF::RResultPtr<TH3D>> getTH3() override;

    std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> getGroupTH1() override;
    std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> getGroupTH2() override;
    std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> getGroupTH3() override;

    void reset() override;
};

#endif
