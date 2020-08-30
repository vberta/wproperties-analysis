#ifndef DEFINEHARMONICS_H
#define DEFINEHARMONICS_H

#include "module.hpp"

class defineHarmonics : public Module
{

private:
public:
  ~defineHarmonics(){};

  RNode run(RNode) override;
};

#endif