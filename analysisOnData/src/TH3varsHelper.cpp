#include "interface/TH3varsHelper.hpp"
   /// This constructor takes all the parameters necessary to build the THnTs. In addition, it requires the names of
   /// the columns which will be used.
TH3varsHelper::TH3varsHelper(std::string category, std::string name, std::string title, 
			     int nbinsX, std::vector<float> xbins,			     
			     int nbinsY, std::vector<float> ybins,			     
			     int nbinsZ, std::vector<float> zbins,			     
			     std::vector<std::string> weightNames
			     ){
  _category = category;
  _name = name;
  _nbinsX = nbinsX;
  _xbins = xbins;
  _nbinsY = nbinsY;
  _ybins = ybins;
  _nbinsZ = nbinsZ;
  _zbins = zbins;
  _weightNames = weightNames;
  
  const auto nSlots = ROOT::IsImplicitMTEnabled() ? ROOT::GetImplicitMTPoolSize() : 1;
  for (auto slot : ROOT::TSeqU(nSlots)) {
    fHistos.emplace_back(std::make_shared<std::vector<TH3D>>());
    (void)slot;
    
    std::vector<TH3D>& histos = *fHistos[slot];
    auto n_histos = _weightNames.size();
    
    std::string slotnum = "";
    slotnum = slot>0 ? std::to_string(slot):"";
    
    for (unsigned int i = 0; i < n_histos; ++i){
      
      histos.emplace_back(TH3D(std::string(_category+"__"+_name+"__"+_weightNames[i]+slotnum).c_str(), 
			       std::string(_category+"__"+_name+"__"+_weightNames[i]+slotnum).c_str(), 
			       _nbinsX, _xbins.data(), _nbinsY, _ybins.data(), _nbinsZ, _zbins.data()));	 
      histos.back().SetDirectory(nullptr);
    }
    
  }
}

std::shared_ptr<std::vector<TH3D>> TH3varsHelper::GetResultPtr() const { return fHistos[0]; }
void TH3varsHelper::Initialize() {}
void TH3varsHelper::InitTask(TTreeReader *, unsigned int) {}
/// This is a method executed at every entry

void TH3varsHelper::Exec(unsigned int slot, const ROOT::VecOps::RVec<float> &vars1, const ROOT::VecOps::RVec<float> &vars2, const ROOT::VecOps::RVec<float> &vars3, const  ROOT::VecOps::RVec<float> &weights)
{
  auto& histos = *fHistos[slot];
  const auto n_histos = histos.size();
  for (unsigned int i = 0; i < n_histos; ++i)
    histos[i].Fill(vars1[i], vars2[i], vars3[i], weights[i]);
}

void TH3varsHelper::Exec(unsigned int slot, const ROOT::VecOps::RVec<float> &vars1, const float &vars2, const ROOT::VecOps::RVec<float> &vars3, const  ROOT::VecOps::RVec<float> &weights)
{
  auto& histos = *fHistos[slot];
  const auto n_histos = histos.size();
  for (unsigned int i = 0; i < n_histos; ++i)
    histos[i].Fill(vars1[i], vars2, vars3[i], weights[i]);
}

void TH3varsHelper::Exec(unsigned int slot, const float &vars1, const ROOT::VecOps::RVec<float> &vars2, const ROOT::VecOps::RVec<float> &vars3, const  ROOT::VecOps::RVec<float> &weights)
{
  auto& histos = *fHistos[slot];
  const auto n_histos = histos.size();
  for (unsigned int i = 0; i < n_histos; ++i)
    histos[i].Fill(vars1, vars2[i], vars3[i], weights[i]);
}

void TH3varsHelper::Exec(unsigned int slot, const float& var1, const float& var2,  const ROOT::VecOps::RVec<float> &vars3, const  ROOT::VecOps::RVec<float> &weights)
{
  auto& histos = *fHistos[slot];
  const auto n_histos = histos.size();
  for (unsigned int i = 0; i < n_histos; ++i){
    histos[i].Fill(var1, var2, vars3[i], weights[i]);
  }
}

void TH3varsHelper::Exec(unsigned int slot, const ROOT::VecOps::RVec<float> &vars1,  const ROOT::VecOps::RVec<float> &vars2, const ROOT::VecOps::RVec<float> &vars3, const float &weight)
{
  auto& histos = *fHistos[slot];
  const auto n_histos = histos.size();
  for (unsigned int i = 0; i < n_histos; ++i)
    histos[i].Fill(vars1[i], vars2[i], vars3[i], weight);
}

void TH3varsHelper::Exec(unsigned int slot, const ROOT::VecOps::RVec<float> &vars1,  const float &vars2, const ROOT::VecOps::RVec<float> &vars3, const float &weight)
{
  auto& histos = *fHistos[slot];
  const auto n_histos = histos.size();
  for (unsigned int i = 0; i < n_histos; ++i)
    histos[i].Fill(vars1[i], vars2, vars3[i], weight);
}

void TH3varsHelper::Exec(unsigned int slot, const float &vars1,  const ROOT::VecOps::RVec<float> &vars2, const ROOT::VecOps::RVec<float> &vars3, const float &weight)
{
  auto& histos = *fHistos[slot];
  const auto n_histos = histos.size();
  for (unsigned int i = 0; i < n_histos; ++i)
    histos[i].Fill(vars1, vars2[i], vars3[i], weight);
}

void TH3varsHelper::Exec(unsigned int slot, const float& var1, const float& var2, const ROOT::VecOps::RVec<float> &vars3, const float &weight)
{
  auto& histos = *fHistos[slot];
  const auto n_histos = histos.size();
  for (unsigned int i = 0; i < n_histos; ++i)
    histos[i].Fill(var1, var2, vars3[i], weight);
}

//////

void TH3varsHelper::Exec(unsigned int slot, const ROOT::VecOps::RVec<float> &vars1, const ROOT::VecOps::RVec<float> &vars2, const float& var3, const  ROOT::VecOps::RVec<float> &weights)
{
  auto& histos = *fHistos[slot];
  const auto n_histos = histos.size();
  for (unsigned int i = 0; i < n_histos; ++i)
    histos[i].Fill(vars1[i], vars2[i], var3, weights[i]);
}

void TH3varsHelper::Exec(unsigned int slot, const ROOT::VecOps::RVec<float> &vars1, const float &vars2, const float& var3, const  ROOT::VecOps::RVec<float> &weights)
{
  auto& histos = *fHistos[slot];
  const auto n_histos = histos.size();
  for (unsigned int i = 0; i < n_histos; ++i)
    histos[i].Fill(vars1[i], vars2, var3, weights[i]);
}

void TH3varsHelper::Exec(unsigned int slot, const float &vars1, const ROOT::VecOps::RVec<float> &vars2, const float& var3, const  ROOT::VecOps::RVec<float> &weights)
{
  auto& histos = *fHistos[slot];
  const auto n_histos = histos.size();
  for (unsigned int i = 0; i < n_histos; ++i)
    histos[i].Fill(vars1, vars2[i], var3, weights[i]);
}

void TH3varsHelper::Exec(unsigned int slot, const float& var1, const float& var2,  const float& var3, const  ROOT::VecOps::RVec<float> &weights)
{
  auto& histos = *fHistos[slot];
  const auto n_histos = histos.size();
  for (unsigned int i = 0; i < n_histos; ++i){
    histos[i].Fill(var1, var2, var3, weights[i]);
  }
}

void TH3varsHelper::Exec(unsigned int slot, const ROOT::VecOps::RVec<float> &vars1,  const ROOT::VecOps::RVec<float> &vars2, const float& var3, const float &weight)
{
  auto& histos = *fHistos[slot];
  const auto n_histos = histos.size();
  for (unsigned int i = 0; i < n_histos; ++i)
    histos[i].Fill(vars1[i], vars2[i], var3, weight);
}

void TH3varsHelper::Exec(unsigned int slot, const ROOT::VecOps::RVec<float> &vars1,  const float &vars2, const float& var3, const float &weight)
{
  auto& histos = *fHistos[slot];
  const auto n_histos = histos.size();
  for (unsigned int i = 0; i < n_histos; ++i)
    histos[i].Fill(vars1[i], vars2, var3, weight);
}

void TH3varsHelper::Exec(unsigned int slot, const float &vars1,  const ROOT::VecOps::RVec<float> &vars2, const float& var3, const float &weight)
{
  auto& histos = *fHistos[slot];
  const auto n_histos = histos.size();
  for (unsigned int i = 0; i < n_histos; ++i)
    histos[i].Fill(vars1, vars2[i], var3, weight);
}

void TH3varsHelper::Exec(unsigned int slot, const float& var1, const float& var2, const float& var3, const float &weight)
{
  auto& histos = *fHistos[slot];
  const auto n_histos = histos.size();
  for (unsigned int i = 0; i < n_histos; ++i)
    histos[i].Fill(var1, var2, var3, weight);
}

/// This method is called at the end of the event loop. It is used to merge all the internal THnTs which
/// were used in each of the data processing slots.
void TH3varsHelper::Finalize()
{
  auto &res_vec = *fHistos[0];
  for (auto slot : ROOT::TSeqU(1, fHistos.size())) {
    auto& histo_vec = *fHistos[slot];
    for (auto i : ROOT::TSeqU(0, res_vec.size()))
      res_vec[i].Add(&histo_vec[i]);
  }
}
std::string TH3varsHelper::GetActionName(){
  return "TH3varsHelper";
}