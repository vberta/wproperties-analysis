#ifndef BASEDEFINITIONS_H
#define BASEDEFINITIONS_H

#include "module.hpp"

class baseDefinitions : public Module
{

private:
    bool _isMC;
    bool _isWjets;

public:
    baseDefinitions(bool isMC = 1, bool isWjets = 0){
      _isMC = isMC;
      _isWjets = isWjets;
    };
    ~baseDefinitions(){};

    RNode run(RNode) override;

};

#endif
