#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"
#include "interface/TH2weightsHelper.hpp"
#include "interface/AngCoeff.hpp"

std::vector<std::string> AngCoeff::stringMultiplication(const std::vector<std::string> &v1, const std::vector<std::string> &v2)
{

    std::vector<std::string> products;

    if (v1.size() == 0)
        return v2;

    else
    {

        products.reserve(v1.size() * v2.size());
        for (auto e1 : v1)
        {
            for (auto e2 : v2)
            {
                products.push_back(e2 + e1);
            }
        }

        return products;
    }
}

RNode AngCoeff::run(RNode d)
{

    std::vector<std::string> total = stringMultiplication(_syst_name, _coeff);

    auto vecMultiplication = [](const ROOT::VecOps::RVec<float> &v1, const ROOT::VecOps::RVec<float> &v2) {
        ROOT::VecOps::RVec<float> products;

        products.reserve(v1.size() * v2.size());
        for (auto e1 : v1)
            for (auto e2 : v2)
                products.push_back(e1 * e2);

        return products;
    };

    if (_syst_name.size() > 0)
    {
        auto d1 = d.Define("weight", "lumiweight*weightPt*weightY").Define(Form("%sharmonicsVec", _syst_weight.c_str()), vecMultiplication, {_syst_weight, "harmonicsVec"});

        TH2weightsHelper helper(std::string("harmonics"), std::string("harmonics"), _nBinsY, _yArr, _nBinsPt, _ptArr, total);
        auto helXsecs = d1.Book<float, float, float, ROOT::VecOps::RVec<float>>(std::move(helper), { "Wrap_preFSR_abs", "Wpt_preFSR", "weight", Form("%sharmonicsVec", _syst_weight.c_str()) });
        _h2Group.push_back(helXsecs);
	
	TH2weightsHelper mapTothelper(std::string("mapTot"), std::string("mapTot"), _nBinsY, _yArr, _nBinsPt, _ptArr, _syst_name);
        auto mapTot = d1.Book<float, float, float, ROOT::VecOps::RVec<float>>(std::move(mapTothelper), { "Wrap_preFSR_abs", "Wpt_preFSR", "weight", _syst_weight });
        _h2Group.push_back(mapTot);

        //TH1weightsHelper helperPt(std::string("harmonicsPt"), std::string("harmonicsPt"), _nBinsPt, _ptArr, total);
        //auto helXsecsPt = d1.Book<float, float, ROOT::VecOps::RVec<float>>(std::move(helperPt), { "Wpt_preFSR", "weight", Form("%sharmonicsVec", _syst_weight.c_str()) });
        //_h1Group.push_back(helXsecsPt);

        //TH1weightsHelper helperY(std::string("harmonicsY"), std::string("harmonicsY"), _nBinsY, _yArr, total);
        //auto helXsecsY = d1.Book<float, float, ROOT::VecOps::RVec<float>>(std::move(helperY), { "Wrap_preFSR_abs", "weight", Form("%sharmonicsVec", _syst_weight.c_str()) });
        //_h1Group.push_back(helXsecsY);

        //TH1weightsHelper Pthelper(std::string("Pt"), std::string("Pt"), _nBinsPt, _ptArr, _syst_name);
        //auto Pt = d1.Book<float, float, ROOT::VecOps::RVec<float>>(std::move(Pthelper), { "Wpt_preFSR", "weight", _syst_weight });
        //_h1Group.push_back(Pt);

        //TH1weightsHelper Yhelper(std::string("Y"), std::string("Y"), _nBinsY, _yArr, _syst_name);
        //auto Y = d1.Book<float, float, ROOT::VecOps::RVec<float>>(std::move(Yhelper), { "Wrap_preFSR_abs", "weight", _syst_weight });
        //_h1Group.push_back(Y);

    }
    else
    {
        TH2weightsHelper helper(std::string("harmonics"), std::string("harmonics"), _nBinsY, _yArr, _nBinsPt, _ptArr, total);
        auto helXsecs = d.Define("weight", "lumiweight*weightPt*weightY").Book<float, float, float, ROOT::VecOps::RVec<float>>(std::move(helper), {"Wrap_preFSR_abs", "Wpt_preFSR", "weight", Form("%sharmonicsVec", _syst_weight.c_str())});
        _h2Group.push_back(helXsecs);

        auto mapTot = d.Define("weight", "lumiweight*weightPt*weightY").Histo2D(TH2D("mapTot", "mapTot", _nBinsY, _yArr.data(), _nBinsPt, _ptArr.data()), "Wrap_preFSR_abs", "Wpt_preFSR", "weight");
        _h2List.push_back(mapTot);

        //TH1weightsHelper helperPt(std::string("harmonicsPt"), std::string("harmonicsPt"), _nBinsPt, _ptArr, total);
        //auto helXsecsPt = d.Book<float, float, ROOT::VecOps::RVec<float>>(std::move(helperPt), { "Wpt_preFSR", "weight", Form("%sharmonicsVec", _syst_weight.c_str()) });
        //_h1Group.push_back(helXsecsPt);

        //TH1weightsHelper helperY(std::string("harmonicsY"), std::string("harmonicsY"), _nBinsY, _yArr, total);
        //auto helXsecsY = d.Book<float, float, ROOT::VecOps::RVec<float>>(std::move(helperY), { "Wrap_preFSR_abs", "weight", Form("%sharmonicsVec", _syst_weight.c_str()) });
        //_h1Group.push_back(helXsecsY);

        //auto Pt = d.Histo1D(TH1D("Pt", "Pt", _nBinsPt, _ptArr.data()), "Wpt_preFSR", "weight");
        //_h1List.push_back(Pt);

        //auto Y = d.Histo1D(TH1D("Y", "Y", _nBinsY, _yArr.data()), "Wrap_preFSR_abs", "weight");
        //_h1List.push_back(Y);

    }


    return d;
}