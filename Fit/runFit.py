import ROOT
from termcolor import colored
import math 
from fitUtils import fitUtils
import os

charges = ["Wplus","Wminus"]
for charge in charges:
    fmap = '/scratchnvme/emanca/wproperties-analysis/analysisOnGen/genInput_{}.root'.format(charge) 
    f = fitUtils(fmap, channel=charge+"_reco", doSyst=True)
    f.fillProcessList()
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
