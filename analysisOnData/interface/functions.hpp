#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"

ROOT::VecOps::RVec<float> dummy(ULong64_t event);

float getFromIdx(ROOT::VecOps::RVec<float> vec, int index);

float getIFromIdx(ROOT::VecOps::RVec<int> vec, int index);

ROOT::VecOps::RVec<float> getRVec_FFtoV(float,float);
ROOT::VecOps::RVec<float> getRVec_FFFFtoV(float,float,float,float);
ROOT::VecOps::RVec<float> getRVec_FFFFFFtoV(float,float,float,float,float,float);

float W_mt(float mu_pt, float mu_phi, float met_pt, float met_phi);
float W_hpt(float mu_pt, float mu_phi, float met_pt, float met_phi);
