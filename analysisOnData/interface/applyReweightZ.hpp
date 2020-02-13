#ifndef APPLYREWEIGHTZ_H
#define APPLYREWEIGHTZ_H


#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"
#include "TH1D.h"
#include "TH2D.h"
#include "TFile.h"
#include "TString.h"
#include "TMath.h"
#include "interface/module.hpp"
#include "interface/functions.hpp"
#include <algorithm>

using RNode = ROOT::RDF::RNode;

class applyReweightZ : public Module {

 private:

  std::vector<ROOT::RDF::RResultPtr<TH1D>> _h1List;
  std::vector<ROOT::RDF::RResultPtr<TH2D>> _h2List;
  std::vector<ROOT::RDF::RResultPtr<TH3D>> _h3List;

    // groups of histos
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> _h1Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> _h2Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> _h3Group;

  std::string _genV;
  std::string _leptonType;
  TFile* _fileQt;
  TFile* _fileY;
  TH1F* _hQt;
  TH1F* _hY;
  int _lastBinQt;
  int _lastBinY;
  
 public:

  applyReweightZ(std::string genV, std::string fnameQt, std::string fnameY, std::string leptonType, float scaleFactor) : _genV(genV), _leptonType(leptonType) {
    bool rescaled_once_internal = false;

    if( fnameQt!="" ){
      _fileQt = TFile::Open(fnameQt.c_str(), "READ");
      std::cout << "applyReweightZ(): Opening file " << fnameQt << std::endl;
      _fileQt->cd();
      _hQt = (TH1F*)gDirectory->Get("unfold");
      _lastBinQt = _hQt->GetNbinsX();
      TH1F* hMC = (TH1F*)gDirectory->Get("hDDilPtLL");
      if(rescaled_once_internal){
	hMC->Scale(_hQt->Integral()/hMC->Integral());
	std::cout << "applyReweightZ: rescaling qt unfolded to MC" << std::endl;
      }
      _hQt->Divide(hMC);
      rescaled_once_internal = true;
      if(scaleFactor>0.){
	_hQt->Scale(scaleFactor);
	std::cout << "applyReweightZ(): rescaling qt unfolded by " << scaleFactor << std::endl;
      }
    }
    else{
      _fileQt = nullptr;
      _hQt = nullptr;
    }
    if( fnameY!="" ){
      _fileY = TFile::Open(fnameY.c_str(), "READ");
      std::cout << "applyReweightZ(): Opening file " << fnameY << std::endl;
      _fileY->cd();
      _hY = (TH1F*)gDirectory->Get("unfold");
      _lastBinY = _hY->GetNbinsX();
      TH1F* hMC = (TH1F*)gDirectory->Get("hDDilRapLL");
      // do not rescale twice
      if(rescaled_once_internal){
	hMC->Scale(_hY->Integral()/hMC->Integral());
	std::cout << "applyReweightZ(): rescaling |y| unfolded to MC" << std::endl;
      }
      _hY->Divide(hMC);
    }
    else{
      _fileY = nullptr;
      _hY = nullptr;
    }
  }

  ~applyReweightZ() {
    if(_fileQt!=nullptr) _fileQt->Close();
    if(_fileY!=nullptr) _fileY->Close();
  };
  
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
