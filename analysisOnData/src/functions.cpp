#include "interface/functions.hpp"

ROOT::VecOps::RVec<float> dummy(ULong64_t event){

	ROOT::VecOps::RVec<float> v;
	v.emplace_back(1.);
	return v;
}
float getFromIdx(ROOT::VecOps::RVec<float> vec, int index){

	return vec[index];
}
