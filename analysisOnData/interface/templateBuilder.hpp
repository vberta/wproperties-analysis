#ifndef TEMPLATEBUILDER_H
#define TEMPLATEBUILDER_H

#include "module.hpp"

class templateBuilder : public Module
{

private:
    std::vector<std::string> _syst_name;
    std::string _syst_weight;
    std::string _filter;
    std::vector<std::string> _filtervec;
    std::string _weight;
    std::string _colvar;
    std::vector<std::string> _colvarvec;
    HistoCategory _hcat;

  std::vector<std::string> helXsecs = {"L", "I", "T", "A", "P", "7", "8", "9", "UL"};
  
  const int nBinsY = 6;
  const int nBinsQt = 8;
  const int nBinsEta = 48;
  const int nBinsPt = 60;
  const int nBinsCharge = 2;
  std::vector<float> _pTArr = std::vector<float>(61);
  std::vector<float> _etaArr = std::vector<float>(49);
  std::vector<float> _yArr = std::vector<float>(7);

public:
  templateBuilder(std::string filter, std::string weight, std::vector<std::string> syst_name, std::string syst_weight, HistoCategory hcat, std::string colvar = "")
    {

        _filter = filter;
        _weight = weight;
        _syst_name = syst_name;
        _syst_weight = syst_weight;
        _hcat = hcat;
        _colvar = colvar;
        setAxisarrays();
    };

    templateBuilder(std::vector<std::string> filtervec, std::string weight, std::vector<std::string> syst_name, std::string syst_weight, HistoCategory hcat, std::vector<std::string> colvarvec)
    {

        _filtervec = filtervec;
        _weight = weight;
        _syst_name = syst_name;
        _syst_weight = syst_weight;
        _hcat = hcat;
        _colvarvec = colvarvec;
        setAxisarrays();
    };

  ~templateBuilder(){};
  RNode bookNominalhistos(RNode);
  RNode bookptCorrectedhistos(RNode);
  RNode bookJMEvarhistos(RNode);
  RNode bookWeightVariatedhistos(RNode d);
  RNode run(RNode) override;
  void setAxisarrays();
  std::vector<std::string> stringMultiplication(const std::vector<std::string> &v1, const std::vector<std::string> &v2);
  static ROOT::VecOps::RVec<float> vecMultiplication(const ROOT::VecOps::RVec<float> &v1, const ROOT::VecOps::RVec<float> &v2) {
    ROOT::VecOps::RVec<float> products;
    
    products.reserve(v1.size() * v2.size());
    for (auto e1 : v1)
      for (auto e2 : v2)
	products.push_back(e1 * e2);

    return products;
  
  }
};

#endif
