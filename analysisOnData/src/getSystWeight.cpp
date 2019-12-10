#include "interface/getSystWeight.hpp"


RNode getSystWeight::run(RNode d){
    
  auto getRVec_VVVVtoV = [](ROOT::VecOps::RVec<float> statUp, ROOT::VecOps::RVec<float> statDown, ROOT::VecOps::RVec<float> systUp, ROOT::VecOps::RVec<float> systDown, int idx){
    ROOT::VecOps::RVec<float> v;
    v.emplace_back(statUp[idx]);
    v.emplace_back(statDown[idx]);
    v.emplace_back(systUp[idx]);
    v.emplace_back(systDown[idx]);
    return v;
  };

  auto getRVec_VVVVVVtoV = [](ROOT::VecOps::RVec<float> statUp, ROOT::VecOps::RVec<float> statDown, ROOT::VecOps::RVec<float> systUp, ROOT::VecOps::RVec<float> systDown, ROOT::VecOps::RVec<float> syst2Up, ROOT::VecOps::RVec<float> syst2Down, int idx){
    ROOT::VecOps::RVec<float> v;
    v.emplace_back(statUp[idx]);
    v.emplace_back(statDown[idx]);
    v.emplace_back(systUp[idx]);
    v.emplace_back(systDown[idx]);
    v.emplace_back(syst2Up[idx]);
    v.emplace_back(syst2Down[idx]);
    return v;
  };
  
  auto getRVec_VVtoV = [](ROOT::VecOps::RVec<float> statUp, ROOT::VecOps::RVec<float> statDown, int idx){
    ROOT::VecOps::RVec<float> v;
    v.emplace_back(statUp[idx]);
    v.emplace_back(statDown[idx]);
    return v;
  };
  
  auto getRVec_VtoV = [this](ROOT::VecOps::RVec<float> statUp){
    ROOT::VecOps::RVec<float> v;
    for(unsigned int i=_range.first; i<=_range.second ; i++) v.emplace_back(statUp[i]);
    return v;
  };
  
  auto getRVec_FFtoV = [](float statA, float statB){
    ROOT::VecOps::RVec<float> v;
    v.emplace_back(statA);
    v.emplace_back(statB);
    return v;
  };

  auto getRVec_FFFFtoV = [](float statA, float statB, float statC, float statD ){
    ROOT::VecOps::RVec<float> v;
    v.emplace_back(statA);
    v.emplace_back(statB);
    v.emplace_back(statC);
    v.emplace_back(statD);
    return v;
  };

  auto getRVec_FFFFFFtoV = [](float statA, float statB, float statC, float statD, float statE, float statF ){
    ROOT::VecOps::RVec<float> v;
    v.emplace_back(statA);
    v.emplace_back(statB);
    v.emplace_back(statC);
    v.emplace_back(statD);
    v.emplace_back(statE);
    v.emplace_back(statF);
    return v;
  };

  auto getRVec_VVVVtoVnorm = [](ROOT::VecOps::RVec<float> statUp, ROOT::VecOps::RVec<float> statDown, ROOT::VecOps::RVec<float> systUp, ROOT::VecOps::RVec<float> systDown, float nom, int idx){
    ROOT::VecOps::RVec<float> v;
    v.emplace_back(statUp[idx]);
    v.emplace_back(statDown[idx]);
    v.emplace_back(systUp[idx]);
    v.emplace_back(systDown[idx]);
    v /= (nom>0. ? nom : 1.0);
    return v;
  };

  auto getRVec_VVVVVVtoVnorm = [](ROOT::VecOps::RVec<float> statUp, ROOT::VecOps::RVec<float> statDown, ROOT::VecOps::RVec<float> systUp, ROOT::VecOps::RVec<float> systDown, ROOT::VecOps::RVec<float> syst2Up, ROOT::VecOps::RVec<float> syst2Down, float nom, int idx){
    ROOT::VecOps::RVec<float> v;
    v.emplace_back(statUp[idx]);
    v.emplace_back(statDown[idx]);
    v.emplace_back(systUp[idx]);
    v.emplace_back(systDown[idx]);
    v.emplace_back(syst2Up[idx]);
    v.emplace_back(syst2Down[idx]);
    v /= (nom>0. ? nom : 1.0);
    return v;
  };
  
  auto getRVec_VVtoVnorm = [](ROOT::VecOps::RVec<float> statUp, ROOT::VecOps::RVec<float> statDown, float nom, int idx){
    ROOT::VecOps::RVec<float> v;
    v.emplace_back(statUp[idx]);
    v.emplace_back(statDown[idx]);
    v /= (nom>0. ? nom : 1.0);
    return v;
  };
  
  auto getRVec_VtoVnorm = [this](ROOT::VecOps::RVec<float> statUp, float nom){
    ROOT::VecOps::RVec<float> v;        
    for(unsigned int i=_range.first; i<=_range.second ; i++){
      v.emplace_back(statUp[i]);
    }
    v /= (nom>0. ? nom : 1.0);
    return v;
  };
  
  auto getRVec_FFtoVnorm = [](float statA, float statB, float nom){
    ROOT::VecOps::RVec<float> v;
    v.emplace_back(statA);
    v.emplace_back(statB);
    v /= (nom>0. ? nom : 1.0);
    return v;
  };

  auto getRVec_FFFFtoVnorm = [](float statA, float statB, float statC, float statD, float nom ){
    ROOT::VecOps::RVec<float> v;
    v.emplace_back(statA);
    v.emplace_back(statB);
    v.emplace_back(statC);
    v.emplace_back(statD);
    v /= (nom>0. ? nom : 1.0);
    return v;
  };

  auto getRVec_FFFFFFtoVnorm = [](float statA, float statB, float statC, float statD, float statE, float statF, float nom ){
    ROOT::VecOps::RVec<float> v;
    v.emplace_back(statA);
    v.emplace_back(statB);
    v.emplace_back(statC);
    v.emplace_back(statD);
    v.emplace_back(statE);
    v.emplace_back(statF);
    v /= (nom>0. ? nom : 1.0);
    return v;
  };

  
  // group element-i four columns into one new column
  if(_type=="VVVV->V"){
    if(_verbose) std::cout << "getSystWeight::run(): getRVec_VVVVtoV" << std::endl;
    auto d1 = d.Define(_new_syst_column, getRVec_VVVVtoV,{_syst_columns[0], _syst_columns[1], _syst_columns[2], _syst_columns[3], _idx1});
    return d1;
  }
  else if(_type=="VVVVVV->V"){
    if(_verbose) std::cout << "getSystWeight::run(): getRVec_VVVVVVtoV" << std::endl;
    auto d1 = d.Define(_new_syst_column, getRVec_VVVVVVtoV,{_syst_columns[0], _syst_columns[1], _syst_columns[2], _syst_columns[3],  _syst_columns[4], _syst_columns[5],_idx1});
    return d1;
  }
  // group N adjacent elements of one colum into one new column
  else if(_type=="VV->V"){
    if(_verbose) std::cout << "getSystWeight::run(): getRVec_VVtoV" << std::endl;
    auto d1 = d.Define(_new_syst_column, getRVec_VVtoV, {_syst_columns[0], _syst_columns[1], _idx1});
    return d1;
    }
  else if(_type=="V->V"){
    if(_verbose) std::cout << "getSystWeight::run(): getRVec_VtoV" << std::endl;
    auto d1 = d.Define(_new_syst_column, getRVec_VtoV,{_syst_columns[0]});
    return d1;
  }
  else if(_type=="ff->V"){
    if(_verbose) std::cout << "getSystWeight::run(): getRVec_FFtoV" << std::endl;
    auto d1 = d.Define(_new_syst_column, getRVec_FFtoV, {_syst_columns[0], _syst_columns[1]});
    return d1;
  }
  else if(_type=="ffff->V"){
    if(_verbose) std::cout << "getSystWeight::run(): getRVec_FFFFtoV" << std::endl;
    auto d1 = d.Define(_new_syst_column, getRVec_FFFFtoV, {_syst_columns[0], _syst_columns[1], _syst_columns[2], _syst_columns[3]});
    return d1;
  }
  else if(_type=="ffffff->V"){
    if(_verbose) std::cout << "getSystWeight::run(): getRVec_FFFFFFtoV" << std::endl;
    auto d1 = d.Define(_new_syst_column, getRVec_FFFFFFtoV, {_syst_columns[0], _syst_columns[1], _syst_columns[2], _syst_columns[3], _syst_columns[4], _syst_columns[5]});
    return d1;
  }
  else if(_type=="VVVV->Vnorm"){
    if(_verbose) std::cout << "getSystWeight::run(): getRVec_VVVVtoVnorm" << std::endl;
    auto d1 = d.Define(_new_syst_column, getRVec_VVVVtoVnorm,{_syst_columns[0], _syst_columns[1], _syst_columns[2], _syst_columns[3], _nom_column, _idx1});
    return d1;
  }
  else if(_type=="VVVVVV->Vnorm"){
    if(_verbose) std::cout << "getSystWeight::run(): getRVec_VVVVVVtoVnorm" << std::endl;
    auto d1 = d.Define(_new_syst_column, getRVec_VVVVVVtoVnorm,{_syst_columns[0], _syst_columns[1], _syst_columns[2], _syst_columns[3],_syst_columns[4], _syst_columns[5],  _nom_column, _idx1});
    return d1;
  }
  else if(_type=="VV->Vnorm"){
    if(_verbose) std::cout << "getSystWeight::run(): getRVec_VVtoVnorm" << std::endl;
    auto d1 = d.Define(_new_syst_column, getRVec_VVtoVnorm, {_syst_columns[0], _syst_columns[1], _nom_column, _idx1});
    return d1;
    }
  else if(_type=="V->Vnorm"){
    if(_verbose) std::cout << "getSystWeight::run(): getRVec_VtoVnorm" << std::endl;
    auto d1 = d.Define(_new_syst_column, getRVec_VtoVnorm,{_syst_columns[0], _nom_column});
    return d1;
  }
  else if(_type=="ff->Vnorm"){
    if(_verbose) std::cout << "getSystWeight::run(): getRVec_FFtoVnorm" << std::endl;
    auto d1 = d.Define(_new_syst_column, getRVec_FFtoVnorm, {_syst_columns[0], _syst_columns[1], _nom_column});
    return d1;
  }
  else if(_type=="ffff->Vnorm"){
    if(_verbose) std::cout << "getSystWeight::run(): getRVec_FFFFtoVnorm" << std::endl;
    auto d1 = d.Define(_new_syst_column, getRVec_FFFFtoVnorm, {_syst_columns[0], _syst_columns[1], _syst_columns[2], _syst_columns[3], _nom_column});
    return d1;
  }
  else if(_type=="ffffff->Vnorm"){
    if(_verbose) std::cout << "getSystWeight::run(): getRVec_FFFFFFtoV" << std::endl;
    auto d1 = d.Define(_new_syst_column, getRVec_FFFFFFtoVnorm, {_syst_columns[0], _syst_columns[1], _syst_columns[2], _syst_columns[3], _syst_columns[4], _syst_columns[5], _nom_column});
    return d1;
  }
  else{
    if(_verbose) std::cout << "getSystWeight::run(): "<< _type << " option not supported" << std::endl;
    return d;
  }

}

std::vector<ROOT::RDF::RResultPtr<TH1D>> getSystWeight::getTH1(){ 
    return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> getSystWeight::getTH2(){ 
    return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> getSystWeight::getTH3(){ 
    return _h3List;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> getSystWeight::getGroupTH1(){ 
  return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> getSystWeight::getGroupTH2(){ 
  return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> getSystWeight::getGroupTH3(){ 
  return _h3Group;
}

void getSystWeight::reset(){
    _h1List.clear();
    _h2List.clear();
    _h3List.clear();

    _h1Group.clear();
    _h2Group.clear();
    _h3Group.clear();
}
