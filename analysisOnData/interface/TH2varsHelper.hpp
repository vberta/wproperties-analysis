#ifndef TH2VARSHELPER_H
#define TH2VARSHELPER_H

#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"

class TH2varsHelper : public ROOT::Detail::RDF::RActionImpl<TH2varsHelper> {

public:
  /// This type is a requirement for every helper.
  using Result_t = std::vector<TH2D>;
private:
  std::vector<std::shared_ptr<std::vector<TH2D>>> fHistos; // one per data processing slot
  std::string _category, _name;
  int _nbinsX, _nbinsY;
  std::vector<float> _xbins, _ybins;
  std::vector<std::string> _weightNames;
  

public:
   /// This constructor takes all the parameters necessary to build the THnTs. In addition, it requires the names of
   /// the columns which will be used.
  TH2varsHelper(std::string category, std::string name, std::string title, 
		int nbinsX, std::vector<float> xbins,
		int nbinsY, std::vector<float> ybins,
		std::vector<std::string> weightNames
		);
  
   TH2varsHelper(TH2varsHelper &&) = default;
   TH2varsHelper(const TH2varsHelper &) = delete;
   std::shared_ptr<std::vector<TH2D>> GetResultPtr() const;
   void Initialize();
   void InitTask(TTreeReader *, unsigned int);
   /// This is a method executed at every entry

  void Exec(unsigned int, const ROOT::VecOps::RVec<float>&, const ROOT::VecOps::RVec<float>&, const  ROOT::VecOps::RVec<float>&);
  void Exec(unsigned int, const ROOT::VecOps::RVec<float>&, const float&, const  ROOT::VecOps::RVec<float>&);
  void Exec(unsigned int, const float&, const  ROOT::VecOps::RVec<float>&, const  ROOT::VecOps::RVec<float>&);
  void Exec(unsigned int, const float&, const float&, const  ROOT::VecOps::RVec<float>&);
  void Exec(unsigned int, const ROOT::VecOps::RVec<float> &, const ROOT::VecOps::RVec<float> &, const float&);
  void Exec(unsigned int, const ROOT::VecOps::RVec<float> &, const float &, const float&);
  void Exec(unsigned int, const float&, const ROOT::VecOps::RVec<float> &, const float&);
  void Exec(unsigned int, const float&, const float&, const float&);
  void Finalize();
  std::string GetActionName();
};

#endif

