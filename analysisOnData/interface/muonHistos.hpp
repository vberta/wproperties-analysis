#ifndef MUONHISTOS_H
#define MUONHISTOS_H


#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"
#include "TH1D.h"
#include "TH2D.h"
#include "TString.h"
#include "TMath.h"
#include "interface/module.hpp"
#include "interface/TH1weightsHelper.hpp"
#include "interface/TH2weightsHelper.hpp"
#include "interface/functions.hpp"
#include<map>
#include<vector>

using RNode = ROOT::RDF::RNode;
enum HistoCategory {
    Nominal=0, Corrected, JME
};
class muonHistos : public Module {

    private:

    std::vector<ROOT::RDF::RResultPtr<TH1D>> _h1List;
    std::vector<ROOT::RDF::RResultPtr<TH2D>> _h2List;
    std::vector<ROOT::RDF::RResultPtr<TH3D>> _h3List;

    // groups of histos
    std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> _h1Group;
    std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> _h2Group;
    std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> _h3Group;

    std::vector<std::string> _syst_name;
    std::string _syst_weight;

    std::string _filter;
    std::string _weight;
    HistoCategory _hcat;
    
    std::vector<float> _pTArr = std::vector<float>(101);
    std::vector<float> _etaArr = std::vector<float>(49);
    std::vector<float> _MTArr = std::vector<float>(101);

    public:
    
    muonHistos(std::string filter, std::string weight, std::vector<std::string> syst_name, std::string syst_weight, HistoCategory hcat){
        
        _filter = filter;
        _weight = weight;
        _syst_name = syst_name;
        _syst_weight = syst_weight;
        _hcat = hcat;

        for(int i=0; i<101; i++) 
          _pTArr[i] = 25. + i*(65.-25.)/100;
        for(int i=0; i<49; i++) 
          _etaArr[i] = -2.4 + i*(4.8)/48;//eta -2.4 to 2.4
        for(int i=0; i<101; i++) 
          _MTArr[i] = i;

    };

    ~muonHistos() {};
    RNode bookNominalhistos(RNode);
    RNode bookptCorrectedhistos(RNode);
    RNode bookJMEvarhistos(RNode);


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
