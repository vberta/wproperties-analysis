#ifndef TH3VARSHELPER_H
#define TH3VARSHELPER_H

#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"

class TH3varsHelper : public ROOT::Detail::RDF::RActionImpl<TH3varsHelper> {

public:
  /// This type is a requirement for every helper.
  using Result_t = std::vector<TH3D>;
private:
  std::vector<std::shared_ptr<std::vector<TH3D>>> fHistos; // one per data processing slot
  std::string _category, _name;
  int _nbinsX, _nbinsY, _nbinsZ;
  std::vector<float> _xbins, _ybins, _zbins;
  std::vector<std::string> _weightNames;
  

public:
   /// This constructor takes all the parameters necessary to build the THnTs. In addition, it requires the names of
   /// the columns which will be used.
  TH3varsHelper(std::string category, std::string name, std::string title, 
		int nbinsX, std::vector<float> xbins,
		int nbinsY, std::vector<float> ybins,
		int nbinsZ, std::vector<float> zbins,
		std::vector<std::string> weightNames
		);
  
   TH3varsHelper(TH3varsHelper &&) = default;
   TH3varsHelper(const TH3varsHelper &) = delete;
   std::shared_ptr<std::vector<TH3D>> GetResultPtr() const;
   void Initialize();
   void InitTask(TTreeReader *, unsigned int);
   /// This is a method executed at every entry

  void Exec(unsigned int, const ROOT::VecOps::RVec<float>&, const ROOT::VecOps::RVec<float>&, const ROOT::VecOps::RVec<float>&, const  ROOT::VecOps::RVec<float>&);
  void Exec(unsigned int, const ROOT::VecOps::RVec<float>&, const float&, const ROOT::VecOps::RVec<float>&, const  ROOT::VecOps::RVec<float>&);
  void Exec(unsigned int, const float&, const  ROOT::VecOps::RVec<float>&, const ROOT::VecOps::RVec<float>&, const  ROOT::VecOps::RVec<float>&);
  void Exec(unsigned int, const float&, const float&, const ROOT::VecOps::RVec<float>&, const  ROOT::VecOps::RVec<float>&);
  void Exec(unsigned int, const ROOT::VecOps::RVec<float> &, const ROOT::VecOps::RVec<float> &, const ROOT::VecOps::RVec<float>&, const float&);
  void Exec(unsigned int, const ROOT::VecOps::RVec<float> &, const float &, const ROOT::VecOps::RVec<float>&, const float&);
  void Exec(unsigned int, const float&, const ROOT::VecOps::RVec<float> &, const ROOT::VecOps::RVec<float>&, const float&);
  void Exec(unsigned int, const float&, const float&, const ROOT::VecOps::RVec<float>&, const float&);
  /////
  void Exec(unsigned int, const ROOT::VecOps::RVec<float>&, const ROOT::VecOps::RVec<float>&, const float&, const  ROOT::VecOps::RVec<float>&);
  void Exec(unsigned int, const ROOT::VecOps::RVec<float>&, const float&, const float&, const  ROOT::VecOps::RVec<float>&);
  void Exec(unsigned int, const float&, const  ROOT::VecOps::RVec<float>&, const float&, const  ROOT::VecOps::RVec<float>&);
  void Exec(unsigned int, const float&, const float&, const float&, const  ROOT::VecOps::RVec<float>&);
  void Exec(unsigned int, const ROOT::VecOps::RVec<float> &, const ROOT::VecOps::RVec<float> &, const float&, const float&);
  void Exec(unsigned int, const ROOT::VecOps::RVec<float> &, const float &, const float&, const float&);
  void Exec(unsigned int, const float&, const ROOT::VecOps::RVec<float> &, const float&, const float&);
  void Exec(unsigned int, const float&, const float&, const float&, const float&);

  void Finalize();
  std::string GetActionName();
};

#endif

