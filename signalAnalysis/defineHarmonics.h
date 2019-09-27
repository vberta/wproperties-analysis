#ifndef DEFINEHARMONICS_H
#define DEFINEHARMONICS_H


#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"
#include "TH1D.h"
#include "TH2D.h"
#include "TString.h"
#include "TMath.h"
#include "../RDFprocessor/framework/module.h"

using RNode = ROOT::RDF::RNode;

class defineHarmonics : public Module {

    private:

    std::vector<ROOT::RDF::RResultPtr<TH1D>> _h1List;
    std::vector<ROOT::RDF::RResultPtr<TH2D>> _h2List;
    std::vector<ROOT::RDF::RResultPtr<TH3D>> _h3List;

    // groups of histos
    std::vector<ROOT::RDF::RResultPtr<std::vector<std::unique_ptr<TH1D>>>> _h1Group;
    std::vector<ROOT::RDF::RResultPtr<std::vector<std::unique_ptr<TH2D>>>> _h2Group;
    std::vector<ROOT::RDF::RResultPtr<std::vector<std::unique_ptr<TH3D>>>> _h3Group;
    
    public:
    
    ~defineHarmonics() {};

    RNode run(RNode) override;
    std::vector<ROOT::RDF::RResultPtr<TH1D>> getTH1() override;
  	std::vector<ROOT::RDF::RResultPtr<TH2D>> getTH2() override;
  	std::vector<ROOT::RDF::RResultPtr<TH3D>> getTH3() override;

    std::vector<ROOT::RDF::RResultPtr<std::vector<std::unique_ptr<TH1D>>>> getGroupTH1() override;
    std::vector<ROOT::RDF::RResultPtr<std::vector<std::unique_ptr<TH2D>>>> getGroupTH2() override;
    std::vector<ROOT::RDF::RResultPtr<std::vector<std::unique_ptr<TH3D>>>> getGroupTH3() override;

    void reset() override;

};

#endif