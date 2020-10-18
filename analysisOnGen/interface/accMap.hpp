#ifndef ACCMAP_H
#define ACCMAP_H

#include "module.hpp"

class accMap : public Module
{
private:
  std::vector<float> _yArr = {0, 0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 3.0, 6.0};
  std::vector<float> _ptArr = {0., 4., 8., 12., 16., 20., 24., 28., 32., 40., 60., 100., 200.};

  int _nBinsY = 8;
  int _nBinsPt = 12;
  std::string _filter;
public:
  
  accMap(std::string filter){
    _filter = filter;
  };
  ~accMap(){};

  RNode run(RNode) override;
  
};

#endif
