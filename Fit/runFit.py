import ROOT
from termcolor import colored
import math 
from fitUtils import fitUtils
import os

ftemplates = '/scratch/emanca/wproperties-analysis/analysisOnGen/GenInfo/genInfo.root'
fmap = '/scratch/emanca/wproperties-analysis/analysisOnGen/genInput.root'
fbkg = '/scratchssd/sroychow/wproperties-sroychow/analysisOnData/output/hadded/'
fbkg_list = []
#fbkg_list.append(fbkg+'TTJets_plots.root')
#fbkg_list.append(fbkg+'DYJets_plots.root')
#fbkg_list.append(fbkg+'Diboson_plots.root')
#fbkg_list.append(fbkg+'FakeFromData_plots.root')
#fbkg_list.append(fbkg+'WToTau_plots.root')

f = fitUtils(ftemplates, fmap, fbkg_list)

#f.project3Dto2D()
#f.symmetrisePDF()
#f.unrollTemplates()
#f.fillHelGroup()
#f.fillSumGroup()
#f.fillHelMetaGroup()
#f.xsecMap()
#f.makeDatacard()

#assert(0)

text2hd5f = 'text2hdf5.py --allowNegativeExpectation --maskedChan=Wplus {}.pkl'.format(f.shapeFile)
print 'executing', text2hd5f 
#os.system(text2hd5f)

combinetf = 'combinetf.py --allowNegativePOI --binByBinStat --correlateXsecStat --doImpacts -t-1 {}.pkl.hdf5 -o fit_{}.root'.format(f.shapeFile, f.shapeFile)
print 'executing', combinetf
os.system(combinetf)
