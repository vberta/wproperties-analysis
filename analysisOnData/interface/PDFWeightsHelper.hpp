#ifndef PhysicsTools_HepMCCandAlgos_PDFWeightsHelper_h
#define PhysicsTools_HepMCCandAlgos_PDFWeightsHelper_h

#include <Eigen/Dense>
#include <iostream>


class PDFWeightsHelper {
  
public:
  
  PDFWeightsHelper();
  
  void Init(unsigned int nreplicas, unsigned int neigenvectors, const std::string inFile);
  void DoMC2Hessian(float nomweight, const float *inweights, float *outweights) const;
  
  unsigned int neigenvectors() const { return transformation_.cols(); }
  
protected:
  
  Eigen::MatrixXd transformation_;  

};
#endif