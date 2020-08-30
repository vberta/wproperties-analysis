#ifndef DATAOBS_H
#define DATAOBS_H

#include "module.hpp"

class dataObs : public Module {

private:

    std::vector<std::string> _syst_name;
    std::string _syst_weight;

public:

    dataObs() {
        _syst_weight = "";
    };
    dataObs(std::vector<std::string> syst_name, std::string syst_weight) {
        TH3::SetDefaultSumw2(true);
        TH2::SetDefaultSumw2(true);
        _syst_name = syst_name;
        _syst_weight = syst_weight;
    };

    ~dataObs() {};
    RNode run(RNode) override;
};

#endif






