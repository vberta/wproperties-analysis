#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"

ROOT::VecOps::RVec<float> dummy(ULong64_t event);
float getFromIdx(ROOT::VecOps::RVec<float> vec, int index);
float getCharge(ROOT::VecOps::RVec<int> vec, int idx);
float W_mt(float,float,float,float);
float Wlike_mt(float,float,float,float,float,float);
float W_hpt(float,float,float,float);
float Z_qt(float,float,float,float);
float Z_mass(float,float,float,float,float,float);
float Z_y(float,float,float,float);
