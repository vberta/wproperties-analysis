#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"
#include "TMath.h"

ROOT::VecOps::RVec<float> dummy(ULong64_t);

float castToFloat(int);

float getFromIdx(ROOT::VecOps::RVec<float>, int);

float getIFromIdx(ROOT::VecOps::RVec<int>,int);

//bool getBFromIdx(ROOT::VecOps::RVec<bool>,int);

ROOT::VecOps::RVec<float> getRVec_FFtoV(float,float);
ROOT::VecOps::RVec<float> getRVec_FFFFtoV(float,float,float,float);
ROOT::VecOps::RVec<float> getRVec_FFFFFFtoV(float,float,float,float,float,float);

float W_mt(float,float,float,float);
float W_hpt(float,float,float,float);
float Z_qt(float,float,float,float);
float Z_mass(float,float,float,float,float,float);
float Z_y(float,float,float,float);
