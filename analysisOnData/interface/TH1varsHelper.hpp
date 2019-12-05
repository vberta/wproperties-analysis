#ifndef TH1VARSHELPER_H
#define TH1VARSHELPER_H

#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"

class TH1varsHelper : public ROOT::Detail::RDF::RActionImpl<TH1varsHelper> {

public:
   /// This type is a requirement for every helper.
   using Result_t = std::vector<TH1D>;
private:
   std::vector<std::shared_ptr<std::vector<TH1D>>> fHistos; // one per data processing slot
   std::string _name;
   int _nbinsX;
   std::vector<float> _xbins;
   std::vector<std::string> _weightNames;
  

public:
   /// This constructor takes all the parameters necessary to build the THnTs. In addition, it requires the names of
   /// the columns which will be used.
   TH1varsHelper(std::string name, std::string title, 
                    int nbinsX, std::vector<float> xbins,
                    std::vector<std::string> weightNames
                    );

   TH1varsHelper(TH1varsHelper &&) = default;
   TH1varsHelper(const TH1varsHelper &) = delete;
   std::shared_ptr<std::vector<TH1D>> GetResultPtr() const;
   void Initialize();
   void InitTask(TTreeReader *, unsigned int);
   /// This is a method executed at every entry

  void Exec(unsigned int, const ROOT::VecOps::RVec<float>&, const  ROOT::VecOps::RVec<float>&);
  void Exec(unsigned int, const float&, const  ROOT::VecOps::RVec<float>&);
  void Exec(unsigned int, const ROOT::VecOps::RVec<float> &, const float&);
  void Exec(unsigned int, const float&, const float&);
  void Finalize();
  std::string GetActionName();
};

#endif

