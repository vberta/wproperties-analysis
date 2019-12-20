#include "interface/functions.hpp"

ROOT::VecOps::RVec<float> dummy(ULong64_t event){
  ROOT::VecOps::RVec<float> v;
  v.emplace_back(1.);
  return v;
}

float getFromIdx(ROOT::VecOps::RVec<float> vec, int index){
  return vec[index];
}

float getIFromIdx(ROOT::VecOps::RVec<int> vec, int index){
  return vec[index];
}

float W_mt(float mu_pt, float mu_phi, float met_pt, float met_phi){
  return mu_pt*mu_phi*TMath::Cos(mu_phi-met_phi);
}

float W_hpt(float mu_pt, float mu_phi, float met_pt, float met_phi){
  float px = mu_pt*TMath::Cos(mu_phi)+met_pt*TMath::Cos(met_phi);
  float py = mu_pt*TMath::Sin(mu_phi)+met_pt*TMath::Sin(met_phi);
  return TMath::Sqrt(px*px + py*py);
}


ROOT::VecOps::RVec<float> getRVec_FFtoV (float statA, float statB){
  ROOT::VecOps::RVec<float> v;
  v.emplace_back(statA);
  v.emplace_back(statB);
  return v;
}

ROOT::VecOps::RVec<float> getRVec_FFFFtoV (float statA, float statB, float statC, float statD ){
  ROOT::VecOps::RVec<float> v;
  v.emplace_back(statA);
  v.emplace_back(statB);
  v.emplace_back(statC);
  v.emplace_back(statD);
  return v;
}

ROOT::VecOps::RVec<float> getRVec_FFFFFFtoV (float statA, float statB, float statC, float statD, float statE, float statF ){
  ROOT::VecOps::RVec<float> v;
  v.emplace_back(statA);
  v.emplace_back(statB);
  v.emplace_back(statC);
  v.emplace_back(statD);
  v.emplace_back(statE);
  v.emplace_back(statF);
  return v;
}
