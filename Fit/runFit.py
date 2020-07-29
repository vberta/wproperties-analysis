import ROOT
from termcolor import colored
import math 
from fitUtils import fitUtils
import os

ftemplates = '/scratchssd/emanca/wproperties-analysis/signalAnalysis/TEST/templates.root'
fmap = '/scratchssd/emanca/wproperties-analysis/signalAnalysis/ACvalues.root'
fbkg = ''
f = fitUtils(ftemplates, fmap, fbkg)

f.project3Dto2D()
f.unrollTemplates()         
f.fillSignalList()
f.fillHelGroup()
f.xsecMap()
f.fillShapeMap()
f.makeDatacard()

#assert(0)

text2hd5f = 'text2hdf5.py --allowNegativeExpectation --maskedChan=Wplus {}.pkl'.format(f.shapeFile)
print 'executing', text2hd5f 
os.system(text2hd5f)

combinetf = 'combinetf.py --allowNegativePOI -t-1 {}.pkl.hdf5 -o {}.root'.format(f.shapeFile, f.shapeFile)
print 'executing', combinetf
os.system(combinetf)
