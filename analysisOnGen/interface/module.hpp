#ifndef MODULE_H
#define MODULE_H

//#include "ROOT/RDataFrame.hxx"
//#include "ROOT/RVec.hxx"
//#include "ROOT/RDF/RInterface.hxx"
//#include "THn.h"

using namespace ROOT::VecOps;
using RNode = ROOT::RDF::RNode;
using rvec_f = const RVec<float> &;
using rvec_i = const RVec<int> &;

class Module
{

private:
  std::vector<ROOT::RDF::RResultPtr<TH1D>> _h1List;
  std::vector<ROOT::RDF::RResultPtr<TH2D>> _h2List;
  std::vector<ROOT::RDF::RResultPtr<TH3D>> _h3List;

  // groups of histos
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> _h1Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> _h2Group;
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> _h3Group;
  
  // template <typename T, unsigned int NDIM>
  //using THn_t = THnT<float>;
  //std::vector<ROOT::RDF::RResultPtr<std::vector<THn_t>>> _hNGroup;

public:
  virtual ~Module(){};
  virtual RNode run(RNode d) = 0;
  std::vector<ROOT::RDF::RResultPtr<TH1D>> getTH1();
  std::vector<ROOT::RDF::RResultPtr<TH2D>> getTH2();
  std::vector<ROOT::RDF::RResultPtr<TH3D>> getTH3();

  std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> getGroupTH1();
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> getGroupTH2();
  std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> getGroupTH3();
  //std::vector<ROOT::RDF::RResultPtr<std::vector<THn_t>>> getGroupTHN();

  void reset();
};

#endif






  
