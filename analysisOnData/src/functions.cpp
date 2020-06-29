#include "interface/functions.hpp"
#include "TMath.h"

float getFromIdx(ROOT::VecOps::RVec<float> vec, int index){
	return vec[index];
}
float getCharge(ROOT::VecOps::RVec<int> vec, int index)
{
  return float(vec[index]);
}

float W_mt(float mu_pt, float mu_phi, float met_pt, float met_phi){
  return TMath::Sqrt(2*mu_pt*met_pt*(1.0-TMath::Cos(mu_phi-met_phi)));
}

float Wlike_mt(float mu1_pt, float mu1_phi, float mu2_pt, float mu2_phi, float met_pt, float met_phi){
  float newmet_px = met_pt*TMath::Cos(met_phi) + mu2_pt*TMath::Cos(mu2_phi);
  float newmet_py = met_pt*TMath::Sin(met_phi) + mu2_pt*TMath::Sin(mu2_phi);
  float newmet_pt = TMath::Sqrt(newmet_px*newmet_px+newmet_py*newmet_py);
  float newmet_phi = TMath::ATan2(newmet_py,newmet_px);
  return TMath::Sqrt(2*mu1_pt*newmet_pt*(1.0-TMath::Cos(mu1_phi-newmet_phi)))*(80.379/91.1876);
}

float W_hpt(float mu_pt, float mu_phi, float met_pt, float met_phi){
  float px = mu_pt*TMath::Cos(mu_phi)+met_pt*TMath::Cos(met_phi);
  float py = mu_pt*TMath::Sin(mu_phi)+met_pt*TMath::Sin(met_phi);
  return TMath::Sqrt(px*px + py*py);
}

float Z_qt(float mu1_pt, float mu1_phi, float mu2_pt, float mu2_phi){
  float px = mu1_pt*TMath::Cos(mu1_phi)+mu2_pt*TMath::Cos(mu2_phi);
  float py = mu1_pt*TMath::Sin(mu1_phi)+mu2_pt*TMath::Sin(mu2_phi);
  return TMath::Sqrt(px*px + py*py);
}

float Z_mass(float mu1_pt, float mu1_eta, float mu1_phi, float mu2_pt, float mu2_eta, float mu2_phi){
  float e  = mu1_pt*TMath::CosH(mu1_eta) + mu2_pt*TMath::CosH(mu2_eta);
  float px = mu1_pt*TMath::Cos(mu1_phi)  + mu2_pt*TMath::Cos(mu2_phi);
  float py = mu1_pt*TMath::Sin(mu1_phi)  + mu2_pt*TMath::Sin(mu2_phi);
  float pz = mu1_pt*TMath::SinH(mu1_eta) + mu2_pt*TMath::SinH(mu2_eta);
  return TMath::Sqrt(e*e - px*px - py*py - pz*pz);
}

float Z_y(float mu1_pt, float mu1_eta, float mu2_pt, float mu2_eta){
  float e  = mu1_pt*TMath::CosH(mu1_eta) + mu2_pt*TMath::CosH(mu2_eta);
  float pz = mu1_pt*TMath::SinH(mu1_eta) + mu2_pt*TMath::SinH(mu2_eta);
  return 0.5*TMath::Log((e+pz)/(e-pz));
}
