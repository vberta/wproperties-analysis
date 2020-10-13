#ifndef ROCHESTERVARIATIONS_H
#define ROCHESTERVARIATIONS_H

#include "module.hpp"
#include<string>
#include "TH2D.h"
#include "TFile.h"
/*
-------------------------------------------------------------------------------------
Following variations are provided to estimate uncertainties. 
-------------------------------------------------------------------------------------
set        nmemberscomment
Default  0    1default, reference based on madgraph sample, with adhoc ewk (sw2eff and Z width) and Z pt (to match data) weights. 
Stat     1          100         pre-generated stat. replicas; 
Zpt      2          1           derived without reweighting reference pt to data. 
Ewk      3          1           derived without applying ad-hoc ewk weights 
deltaM   4          1           one representative set for alternative profile deltaM mass window 
Ewk2     5          1           weight reference from constant to s-dependent Z width 
*/
class rochesterVariations : public Module
{

private:
  TFile* _corrF;
  std::vector<TH2D*> _Zptcorv;
  std::vector<TH2D*> _Ewkcorv;
  std::vector<TH2D*> _deltaMcorv;
  std::vector<TH2D*> _Ewk2corv;
  std::vector<TH2D*> _statEigenplusv;
  std::vector<TH2D*> _statEigenminusv;
  float getCorrfromhisto(std::vector<TH2D*> hvec, float pt, float eta, unsigned int idx);

public:
  rochesterVariations(TFile* cf){
    _corrF = cf;
    _Zptcorv.emplace_back(static_cast<TH2D*>(_corrF->Get("systhist_plus_2")));
    _Zptcorv.emplace_back(static_cast<TH2D*>(_corrF->Get("systhist_minus_2")));

    _Ewkcorv.emplace_back(static_cast<TH2D*>(_corrF->Get("systhist_plus_3")));
    _Ewkcorv.emplace_back(static_cast<TH2D*>(_corrF->Get("systhist_minus_3")));

    _deltaMcorv.emplace_back(static_cast<TH2D*>(_corrF->Get("systhist_plus_4")));
    _deltaMcorv.emplace_back(static_cast<TH2D*>(_corrF->Get("systhist_minus_4")));

    _Ewk2corv.emplace_back(static_cast<TH2D*>(_corrF->Get("systhist_plus_5")));
    _Ewk2corv.emplace_back(static_cast<TH2D*>(_corrF->Get("systhist_minus_5")));

    for(unsigned int idx = 0; idx < 99; idx++) {
      std::string up = "stathis_eig_plus_" + std::to_string(idx);
      TH2D* hup = static_cast<TH2D*>(_corrF->Get(up.c_str()));
      if(hup) _statEigenplusv.emplace_back(hup);

      std::string down = "stathis_eig_minus_" + std::to_string(idx);
      TH2D* hdown = static_cast<TH2D*>(_corrF->Get(down.c_str()));
      if(hdown) _statEigenminusv.emplace_back(hdown);
    }
    // std::cout << "Eigen plus size:" << _statEigenplusv.size() << std::endl;
    //std::cout << "Eigen minus size:" << _statEigenminusv.size() << std::endl;
  }

  
  ~rochesterVariations(){
    _corrF->Close();    
  }
  
  RNode run(RNode) override;
  

};

#endif
