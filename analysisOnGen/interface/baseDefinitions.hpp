#ifndef BASEDEFINITIONS_H
#define BASEDEFINITIONS_H

#include "module.hpp"

class baseDefinitions : public Module
{

private:

public:

    ~baseDefinitions(){};

    RNode run(RNode) override;
#endif
