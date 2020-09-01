#ifndef TEMPLATEBUILDER_H
#define TEMPLATEBUILDER_H

#include "module.hpp"

using namespace ROOT::VecOps;
using RNode = ROOT::RDF::RNode;
using rvec_f = const RVec<float> &;
using rvec_i = const RVec<int> &;

class templateBuilder : public Module{
  
    private:

    public:
    
    ~templateBuilder() {};
    RNode run(RNode) override;
    std::vector<std::string> stringMultiplication(const std::vector<std::string> &v1, const std::vector<std::string> &v2);
};

#endif
