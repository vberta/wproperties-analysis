#include "AngCoeff.h"


RNode AngCoeff::run(RNode d){
    
    std::vector<float> yArr = {0, 0.4, 0.8, 1.2 ,1.6, 2.0, 2.5, 3.0, 6.0};
    std::vector<float> ptArr = {0., 4., 8., 12., 16., 20., 24., 32., 40., 60., 100., 200.};
    
    int nBinsY = 8;
    int nBinsPt = 11;

    auto multByWeight = [](float a, const ROOT::VecOps::RVec<float> &w){ return a*w;};
    auto multSqByWeight = [](float a, const ROOT::VecOps::RVec<float> &w)-> ROOT::VecOps::RVec<float>{ return a*w*w;};

    auto mapTot = d.Histo2D(TH2D("mapTot", "mapTot", nBinsY, yArr.data(), nBinsPt, ptArr.data()), "Wrap_preFSR_abs", "Wpt_preFSR", "lumiweight");
    auto mapAccEta = d.Filter("fabs(Mueta_preFSR)<2.4").Histo2D(TH2D("mapAccEta", "mapAccEta", nBinsY, yArr.data(), nBinsPt, ptArr.data()), "Wrap_preFSR_abs", "Wpt_preFSR", "lumiweight");
    auto mapAcc = d.Filter("fabs(Mueta_preFSR)<2.4 && Mupt_preFSR>25. && Mupt_preFSR<65.").Histo2D(TH2D("mapAcc", "mapAcc", nBinsY, yArr.data(), nBinsPt, ptArr.data()), "Wrap_preFSR_abs", "Wpt_preFSR", "lumiweight");
    auto sumw = d.Define("genratio", "Generator_weight/genEventSumw").Histo2D(TH2D("sumw", "sumw", nBinsY, yArr.data(), nBinsPt, ptArr.data()), "Wrap_preFSR_abs", "Wpt_preFSR","genratio");

    _h2List.push_back(mapTot);
    _h2List.push_back(mapAccEta);
    _h2List.push_back(mapAcc);
    _h2List.push_back(sumw);

    
    std::vector<std::string> coeff = {"A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "AUL"};
    TH2weightsHelper helper(std::string("harmonics"), std::string("harmonics"), nBinsY, yArr, nBinsPt, ptArr, coeff);

    auto d1 = d.Define("harmonicsVecWeighted", multByWeight, {"lumiweight", "harmonicsVec"})
            .Define("harmonicsVecSqWeighted", multSqByWeight, {"lumiweight", "harmonicsVec"});
    auto helXsecs = d1.Book<float,  float, ROOT::VecOps::RVec<float>>(std::move(helper), {"Wrap_preFSR_abs", "Wpt_preFSR", "harmonicsVecWeighted"});
    
    //auto helXsecsSq = d1.Book<float,  float, float, ROOT::VecOps::RVec<float>>(std::move(helper), {"Wrap_preFSR_abs", "Wpt_preFSR", "harmonicsVecSqWeighted"});

    // this trigger event loop and caches dCache
    std::cout << "Triggering event loop and caching" << std::endl;
    mapTot->GetName();

    // this goes inside a function
    
    int i = 0;
    for(auto it = helXsecs.begin(); it != helXsecs.end()-1; ++it){
          
        (*it)->Divide(&(mapTot.GetValue()));
        
        switch (i)
        {
            case 0: {
                
                for(int xbin = 1; xbin<(*it)->GetNbinsX()+1;xbin++){
                    for(int ybin = 1; ybin<(*it)->GetNbinsY()+1;ybin++){

                        auto content = (*it)->GetBinContent(xbin,ybin);
                        (*it)->SetBinContent(xbin,ybin, 20./3.*(content + 1./10.));

                        }
                    }
                break;
            }
            case 2: {
                (*it)->Scale(20.);
                break;
            }
            case 1: (*it)->Scale(5.);
                break;
            case 5: (*it)->Scale(5.);
                break;
            case 6: (*it)->Scale(5.);
                break;
            default:(*it)->Scale(4.);
                break;
        }
        i++;
    }

    _h2Group.push_back(helXsecs);

    auto getACValues = [helXsecs](float y, float pt)mutable{

        ROOT::VecOps::RVec<float> AngCoeff;
        
        for(auto it = helXsecs.begin(); it != helXsecs.end()-1; ++it){
        
            int bin = (*it)->FindBin(y, pt);
            AngCoeff.push_back((*it)->GetBinContent(bin));

        }
        
        return AngCoeff;

    };

    mapAccEta->Divide(&(mapTot.GetValue()));

    auto fillAccMapEta = [mapTot, mapAccEta](float y, float pt)mutable->float{

        int bin = mapAccEta->FindBin(y, pt);
        return mapAccEta->GetBinContent(bin);

    };

    mapAcc->Divide(&(mapTot.GetValue()));
    auto fillAccMap = [mapTot, mapAcc](float y, float pt)mutable->float{

        int bin = mapAcc->FindBin(y, pt);
        return mapAcc->GetBinContent(bin);

    };

    auto fillTotMap = [mapTot](float y, float pt)mutable->float{

        int bin = mapTot->FindBin(y, pt);
        return mapTot->GetBinContent(bin);

    };

    auto d2 = d1.Define("AngCoeffVec", getACValues, {"Wrap_preFSR_abs", "Wpt_preFSR"}).Define("accMapEta", fillAccMapEta, {"Wrap_preFSR_abs", "Wpt_preFSR"}).Define("accMap", fillAccMap, {"Wrap_preFSR_abs", "Wpt_preFSR"}).Define("totMap", fillTotMap, {"Wrap_preFSR_abs", "Wpt_preFSR"});
    
    return d2;

}

std::vector<ROOT::RDF::RResultPtr<TH1D>> AngCoeff::getTH1(){ 
    return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> AngCoeff::getTH2(){ 
    return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> AngCoeff::getTH3(){ 
    return _h3List;
}

std::vector<ROOT::RDF::RResultPtr<std::vector<std::unique_ptr<TH1D>>>> AngCoeff::getGroupTH1(){ 
  return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<std::unique_ptr<TH2D>>>> AngCoeff::getGroupTH2(){ 
  return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<std::unique_ptr<TH3D>>>> AngCoeff::getGroupTH3(){ 
  return _h3Group;
}

void AngCoeff::reset(){
    
    _h1List.clear();
    _h2List.clear();
    _h3List.clear();

    _h1Group.clear();
    _h2Group.clear();
    _h3Group.clear();

}