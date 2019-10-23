#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"

ROOT::VecOps::RVec<float> dummy(ULong64_t event);
float getFromIdx(ROOT::VecOps::RVec<float> vec, int index);
