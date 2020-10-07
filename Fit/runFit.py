import ROOT
from termcolor import colored
import math 
from fitUtils import fitUtils
import os

basepath = '/scratchnvme/emanca/wproperties-analysis/analysisOnData/python/templates2D/'
fsig = basepath+'WPlus_2D_ACTemplates.root'
fmap = '/scratchnvme/emanca/wproperties-analysis/analysisOnGen/genInput.root'

samples = ["DY","Diboson","Top","Fake","Tau","LowAcc","data_obs"]

fbkg = basepath
fbkg_dict = {}
fbkg_dict["Top"]=fbkg+'TTbar_templates2Dplus.root'
fbkg_dict["DY"]=fbkg+'DYJets_templates2Dplus.root'
fbkg_dict["Diboson"]=fbkg+'DiBoson_templates2Dplus.root'
fbkg_dict["Fake"]=fbkg+'Fake_templates2Dplus.root'
fbkg_dict["Tau"]=fbkg+'WtoTau_templates2Dplus.root'
fbkg_dict["LowAcc"]=fbkg+'LowAcc_templates2Dplus.root'
fbkg_dict["data_obs"]=fbkg+'WToMu_templates2Dplus.root' #placeholder for data

f = fitUtils(fsig, fmap, fbkg_dict, "Wplus_reco")
f.getTemplates()
f.shapeFile()
f.fillHelGroup()
f.fillSumGroup()
f.fillHelMetaGroup()
f.makeDatacard()

#assert(0)

text2hd5f = 'text2hdf5.py --allowNegativeExpectation --maskedChan={}_xsec {}.pkl'.format(f.channel,f.channel)
print 'executing', text2hd5f 
os.system(text2hd5f)

combinetf = 'combinetf.py --allowNegativePOI --binByBinStat --correlateXsecStat --doImpacts -t-1 {}.pkl.hdf5 -o fit_{}.root'.format(f.channel, f.channel)
print 'executing', combinetf
os.system(combinetf)
