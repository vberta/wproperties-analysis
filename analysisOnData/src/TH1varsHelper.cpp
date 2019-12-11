#include "interface/TH1varsHelper.hpp"
   /// This constructor takes all the parameters necessary to build the THnTs. In addition, it requires the names of
   /// the columns which will be used.
TH1varsHelper::TH1varsHelper(std::string category, std::string name, std::string title, 
                    int nbinsX, std::vector<float> xbins,
                    std::vector<std::string> weightNames
                    ){
  _category = category;
  _name = name;
  _nbinsX = nbinsX;
  _xbins = xbins;
  _weightNames = weightNames;
  
  const auto nSlots = ROOT::IsImplicitMTEnabled() ? ROOT::GetImplicitMTPoolSize() : 1;
  for (auto slot : ROOT::TSeqU(nSlots)) {
    fHistos.emplace_back(std::make_shared<std::vector<TH1D>>());
    (void)slot;
    
    std::vector<TH1D>& histos = *fHistos[slot];
    auto n_histos = _weightNames.size();
    
    std::string slotnum = "";
    slotnum = slot>0 ? std::to_string(slot):"";
    
    for (unsigned int i = 0; i < n_histos; ++i){
      
      histos.emplace_back(TH1D(std::string(_category+"__"+_name+"__"+_weightNames[i]+slotnum).c_str(), 
			       std::string(_category+"__"+_name+"__"+_weightNames[i]+slotnum).c_str(), 
			       _nbinsX, _xbins.data()));	 
      histos.back().SetDirectory(nullptr);
    }
    
  }
}

std::shared_ptr<std::vector<TH1D>> TH1varsHelper::GetResultPtr() const { return fHistos[0]; }
void TH1varsHelper::Initialize() {}
void TH1varsHelper::InitTask(TTreeReader *, unsigned int) {}
/// This is a method executed at every entry

void TH1varsHelper::Exec(unsigned int slot, const ROOT::VecOps::RVec<float> &vars, const  ROOT::VecOps::RVec<float> &weights)
{
  auto& histos = *fHistos[slot];
  const auto n_histos = histos.size();
  for (unsigned int i = 0; i < n_histos; ++i)
    histos[i].Fill(vars[i], weights[i]);
}

void TH1varsHelper::Exec(unsigned int slot, const float& var, const  ROOT::VecOps::RVec<float> &weights)
{
  auto& histos = *fHistos[slot];
  const auto n_histos = histos.size();
  for (unsigned int i = 0; i < n_histos; ++i){
    histos[i].Fill(var, weights[i]);
  }
}

void TH1varsHelper::Exec(unsigned int slot, const ROOT::VecOps::RVec<float> &vars, const float &weight)
{
  auto& histos = *fHistos[slot];
  const auto n_histos = histos.size();
  for (unsigned int i = 0; i < n_histos; ++i)
    histos[i].Fill(vars[i], weight);
}

void TH1varsHelper::Exec(unsigned int slot, const float& var, const float &weight)
{
  auto& histos = *fHistos[slot];
  const auto n_histos = histos.size();
  for (unsigned int i = 0; i < n_histos; ++i)
    histos[i].Fill(var, weight);
}

/// This method is called at the end of the event loop. It is used to merge all the internal THnTs which
/// were used in each of the data processing slots.
void TH1varsHelper::Finalize()
{
  auto &res_vec = *fHistos[0];
  for (auto slot : ROOT::TSeqU(1, fHistos.size())) {
    auto& histo_vec = *fHistos[slot];
    for (auto i : ROOT::TSeqU(0, res_vec.size()))
      res_vec[i].Add(&histo_vec[i]);
  }
}
std::string TH1varsHelper::GetActionName(){
  return "TH1varsHelper";
}
