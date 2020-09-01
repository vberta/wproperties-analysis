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

public:
    ~templateBuilder(){};
    templates(std::string filter, std::string weight, std::vector<std::string> syst_name, std::string syst_weight, HistoCategory hcat, std::string colvar = "")
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
    RNode run(RNode) override;
    std::vector<std::string> stringMultiplication(const std::vector<std::string> &v1, const std::vector<std::string> &v2);
};

#endif
