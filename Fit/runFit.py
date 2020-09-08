import ROOT
from termcolor import colored
import math 
from fitUtils import fitUtils
import os

basepath = '/scratch/emanca/wproperties-analysis/analysisOnData/python/templates2D/'
fsig = basepath+'WPlus_2D_ACTemplates.root'
fmap = '/scratch/emanca/wproperties-analysis/analysisOnGen/genInput.root'

samples = ["DY","Diboson","Top","Fake","Tau","LowAcc"]
fbkg = basepath
fbkg_dict = {}
fbkg_dict["Top"]=fbkg+'TTJets_templates2Dplus.root'
fbkg_dict["DY"]=fbkg+'DYJets_templates2Dplus.root'
fbkg_dict["Diboson"]=fbkg+'Diboson_templates2Dplus.root'
fbkg_dict["Fake"]=fbkg+'FakeFromData_templates2Dplus.root'
fbkg_dict["Tau"]=fbkg+'WToTau_templates2Dplus.root'
fbkg_dict["LowAcc"]=fbkg+'WToMu_templates2Dplus.root'

f = fitUtils(fsig, fmap, fbkg, "Wplus")
f.getTemplates()

#f.unrollTemplates()
#f.fillHelGroup()
#f.fillSumGroup()
#f.fillHelMetaGroup()
#f.xsecMap()
#f.makeDatacard()

#assert(0)

text2hd5f = 'text2hdf5.py --allowNegativeExpectation --maskedChan=Wplus {}.pkl'.format(f.shapeFile)
print 'executing', text2hd5f 
os.system(text2hd5f)

combinetf = 'combinetf.py --allowNegativePOI --binByBinStat --correlateXsecStat --doImpacts -t-1 {}.pkl.hdf5 -o fit_{}.root'.format(f.shapeFile, f.shapeFile)
print 'executing', combinetf
os.system(combinetf)
