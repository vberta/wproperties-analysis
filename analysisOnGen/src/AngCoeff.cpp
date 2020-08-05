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
        auto d1 = d.Define(Form("%sharmonicsVec", _syst_weight.c_str()), vecMultiplication, {_syst_weight, "harmonicsVec"});

        TH2weightsHelper helper(std::string("harmonics"), std::string("harmonics"), _nBinsY, _yArr, _nBinsPt, _ptArr, total);
        auto helXsecs = d1.Book<float, float, float, ROOT::VecOps::RVec<float>>(std::move(helper), {"Wrap_preFSR_abs", "Wpt_preFSR", "lumiweight", Form("%sharmonicsVec", _syst_weight.c_str())});
        _h2Group.push_back(helXsecs);
        
        TH2weightsHelper mapTothelper(std::string("mapTot"), std::string("mapTot"), _nBinsY, _yArr, _nBinsPt, _ptArr, _syst_name);
        auto mapTot = d1.Book<float, float, float, ROOT::VecOps::RVec<float>>(std::move(mapTothelper), { "Wrap_preFSR_abs", "Wpt_preFSR", "lumiweight", _syst_weight});
        _h2Group.push_back(mapTot);
    }
    else
    {
        TH2weightsHelper helper(std::string("harmonics"), std::string("harmonics"), _nBinsY, _yArr, _nBinsPt, _ptArr, total);
        auto helXsecs = d.Book<float, float, float, ROOT::VecOps::RVec<float>>(std::move(helper), {"Wrap_preFSR_abs", "Wpt_preFSR", "lumiweight", Form("%sharmonicsVec", _syst_weight.c_str())});
        _h2Group.push_back(helXsecs);
        auto mapTot = d.Histo2D(TH2D("mapTot", "mapTot", _nBinsY, _yArr.data(), _nBinsPt, _ptArr.data()), "Wrap_preFSR_abs", "Wpt_preFSR", "lumiweight");
        _h2List.push_back(mapTot);
    }


    return d;
}

std::vector<ROOT::RDF::RResultPtr<TH1D>> AngCoeff::getTH1()
{
    return _h1List;
}
std::vector<ROOT::RDF::RResultPtr<TH2D>> AngCoeff::getTH2()
{
    return _h2List;
}
std::vector<ROOT::RDF::RResultPtr<TH3D>> AngCoeff::getTH3()
{
    return _h3List;
}

std::vector<ROOT::RDF::RResultPtr<std::vector<TH1D>>> AngCoeff::getGroupTH1()
{
    return _h1Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH2D>>> AngCoeff::getGroupTH2()
{
    return _h2Group;
}
std::vector<ROOT::RDF::RResultPtr<std::vector<TH3D>>> AngCoeff::getGroupTH3()
{
    return _h3Group;
}

void AngCoeff::reset()
{

    _h1List.clear();
    _h2List.clear();
    _h3List.clear();

    _h1Group.clear();
    _h2Group.clear();
    _h3Group.clear();
}