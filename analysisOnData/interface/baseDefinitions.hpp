#ifndef BASEDEFINITIONS_H
#define BASEDEFINITIONS_H

#include "module.hpp"

class baseDefinitions : public Module
{

private:
    bool _isMC;

public:
    baseDefinitions(bool isMC = 1){
      _isMC = isMC;
    };
    ~baseDefinitions(){};

    RNode run(RNode) override;

};

#endif
