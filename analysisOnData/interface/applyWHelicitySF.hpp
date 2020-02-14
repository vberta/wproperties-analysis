#ifndef APPLYWHELICITYSF_H
#define APPLYWHELICITYSF_H


#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"
#include "TH1D.h"
#include "TH2D.h"
#include "TFile.h"
#include "TString.h"
#include "TMath.h"
#include "TMatrixDSym.h"
#include "TMatrixD.h"
#include "TVectorD.h"

#include "interface/module.hpp"
#include "interface/functions.hpp"

using RNode = ROOT::RDF::RNode;

class applyWHelicitySF : public Module {

 private:

  std::vector<ROOT::RDF::RResultPtr<TH1D>> _h1List;
  std::vector<ROOT::RDF::RResultPtr<TH2D>> _h2List;
  std::vector<ROOT::RDF::RResultPtr<TH3D>> _h3List;

    // groups of histos
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> _h1Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> _h2Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> _h3Group;

  std::map<std::string, TFile*> _fmap;
  std::string _idx2;
  std::vector<std::string> _syst_columns_trigger;
  std::vector<std::string> _syst_columns_reco;
  std::map<std::string, TH2D*> _hmap;

 public:
    
  applyWHelicitySF(std::string fname_trigger_plus, std::string fname_trigger_minus, std::string fname_reco, std::string idx2, 
		   std::vector<std::string> syst_columns_trigger, std::vector<std::string> syst_columns_reco) : 
    _idx2(idx2), _syst_columns_trigger(syst_columns_trigger), _syst_columns_reco(syst_columns_reco){

    _fmap.insert( std::pair<std::string, TFile*>("trigger_plus",  TFile::Open(fname_trigger_plus.c_str(),   "READ")) );
    _fmap.insert( std::pair<std::string, TFile*>("trigger_minus", TFile::Open(fname_trigger_minus.c_str(),  "READ")) );
    _fmap.insert( std::pair<std::string, TFile*>("reco",          TFile::Open(fname_reco.c_str(),  "READ")) );
    
    _hmap.insert( std::pair<std::string, TH2D*>("trigger_plus",  (TH2D*)_fmap.at("trigger_plus")->Get("scaleFactor") ) );
    _hmap.insert( std::pair<std::string, TH2D*>("trigger_minus", (TH2D*)_fmap.at("trigger_minus")->Get("scaleFactor") ) );
    _hmap.insert( std::pair<std::string, TH2D*>("reco",          (TH2D*)_fmap.at("reco")->Get("scaleFactor") ) );    

    if(syst_columns_trigger.size()>0 || syst_columns_reco.size()>0){

      std::vector<std::string> systs   = {"trigger", "reco"};
      std::vector<std::string> data    = {"mc","data"};
      std::vector<std::string> charges = {"plus","minus"};
      std::vector<std::string> vars    = {"Up","Down"};

      std::map<std::string, TH3D*> cmap;
      std::map<std::string, TH2D*> vmap;      
      for(auto s : systs){
	for(auto d : data){
	  for(auto c : charges){
	    std::string c_name = (s!="reco") ? "_"+c : "";
	    if(s=="reco" && c!=charges[0]) continue;	    	    
	    cmap.insert( std::pair<std::string, TH3D*>(s+"_cov_"+d+c_name,   (TH3D*)_fmap.at(s+c_name)->Get(("hist_ErfCovMatrix_vs_eta_"+d).c_str())));
	    vmap.insert( std::pair<std::string, TH2D*>(s+"_val_"+d+c_name,   (TH2D*)_fmap.at(s+c_name)->Get(("hist_ErfParam_vs_eta_"+d).c_str())));
	  }
	}
      }

      for(auto s : systs){
	for(auto d : data){
	  for(auto c : charges){	    

	    std::string c_name = (s!="reco") ? "_"+c : "";
	    if(s=="reco" && c!=charges[0]) continue;

	    TH3D* cov = cmap.at(s+"_cov_"+d+c_name);
	    TH2D* val = vmap.at(s+"_val_"+d+c_name);
	    for(int e = 0 ; e<3 ; e++ ){
	      for(auto v : vars ){
		std::string mapname = s+"_"+d+"_eigen"+std::to_string(e)+v+c_name;
		std::string mapname_nocharge = s+"_"+d+"_eigen"+std::to_string(e)+v;
		
		//std::cout << "applyWHelicitySF: find a match for " <<  mapname_nocharge <<  std::endl;
		if( s=="trigger" && std::find(syst_columns_trigger.begin(), syst_columns_trigger.end(), mapname_nocharge)==syst_columns_trigger.end() ) continue;
		if( s=="reco"    && std::find(syst_columns_reco.begin(), syst_columns_reco.end(), mapname_nocharge)==syst_columns_reco.end() ) continue;

		std::cout << "applyWHelicitySF(): Adding histo to map with name: " << mapname << std::endl;
		TH2D* h = (TH2D*)_hmap.at(s+c_name)->Clone(mapname.c_str());
		h->Reset();
		_hmap.insert( std::pair<std::string, TH2D*>(mapname, h) );
	      }
	    }

	    int nbins_eta = cov->GetXaxis()->GetNbins();
	    for( int ieta = 1; ieta<=nbins_eta; ieta++ ){
	      //double eta = cov->GetXaxis()->GetBinCenter(ieta);
	      cov->GetXaxis()->SetRange(ieta,ieta);
	      TH2D* icov = (TH2D*)((TH2D*)cov->Project3D("yz"))->Clone((s+"_"+d+c_name+"_"+std::to_string(ieta)).c_str());
	      int nbins_cov= icov->GetXaxis()->GetNbins();
	      double data[9];
	      for(int j = 0; j < nbins_cov; j++ ){
		for(int k = 0; k < nbins_cov; k++ ){
		  data[j*nbins_cov+k] = icov->GetBinContent(j+1,k+1);
		}
	      }
	      TMatrixDSym Cov(3, data);
	      TVectorD eigvals(3);
	      TMatrixD U = Cov.EigenVectors(eigvals);
	      TMatrixD Uinv = U.InvertFast();
	      TMatrixD dummy = U.InvertFast();
	      //(Uinv*Cov*U).Print();
	      //eigvals.Print();
	      //U.Print();
	      //std::cout << v << std::to_string(ieta) << std::endl;
	      //Cov.Print();
	      TVectorD coeffs(3);
	      coeffs[0] = val->GetBinContent(ieta,1);
	      coeffs[1] = val->GetBinContent(ieta,2);
	      coeffs[2] = val->GetBinContent(ieta,3);
	      TVectorD eigen_coeffs = Uinv*coeffs;
	      for(int e = 0 ; e<3 ; e++ ){
		for(auto v : vars ){

		  std::string mapname = s+"_"+d+"_eigen"+std::to_string(e)+v+c_name;
		  std::string mapname_nocharge = s+"_"+d+"_eigen"+std::to_string(e)+v;
		  if( s=="trigger" && std::find(syst_columns_trigger.begin(), syst_columns_trigger.end(), mapname_nocharge)==syst_columns_trigger.end() ) continue;
		  if( s=="reco"    && std::find(syst_columns_reco.begin(), syst_columns_reco.end(), mapname_nocharge)==syst_columns_reco.end() ) continue;

		  TVectorD eigen_coeffs_mod(eigen_coeffs);
		  eigen_coeffs_mod[e] += (v=="Up"? 1.0 :-1.0)*TMath::Sqrt(eigvals[e]);
		  TVectorD coeffs_shift = U*eigen_coeffs_mod;
		  //cout << "Eig[" << e << "] --> " << coeffs_shift[0] << "," << coeffs_shift[1] << "," << coeffs_shift[2] << std::endl;
		  //cout << "Eig[" << e << "] + 1sigma : " << eff_shift << "/" << eff_nominal << " = " << eff_shift/eff_nominal <<  endl;		  
		  TH2D* h = _hmap.at(mapname);
		  //std::cout << "Filling "+mapname+" with SFsyst" << std::endl;
		  for(int ipt=1; ipt<=h->GetYaxis()->GetNbins(); ipt++){
		    double pt = h->GetYaxis()->GetBinCenter(ipt);
		    double eff_nominal = coeffs[0]*TMath::Erf(( pt - coeffs[1])/coeffs[2]);
		    double eff_shift   = coeffs_shift[0]*TMath::Erf((pt - coeffs_shift[1])/coeffs_shift[2]);
		    //double old = h->GetBinContent(ieta,ipt);
		    double sf =  eff_nominal>0. ? eff_shift/eff_nominal : 1.0;
		    if(d=="mc" && sf>0.) sf = 1./sf;
		    h->SetBinContent(ieta,ipt, sf);
		    //std::cout << mapname+" eig[" << e << "] "+v+" at (" << eta << "," << pt << ") : " << std::setprecision(9) << h->GetBinContent(ieta,ipt) <<  std::endl;
		  }
		}
	      }
	    }
	  }
	}
      }
    }
  }

  ~applyWHelicitySF() {
    for(auto const& f : _fmap) (f.second)->Close();
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
