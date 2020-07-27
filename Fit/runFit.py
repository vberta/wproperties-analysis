import ROOT
from termcolor import colored
import math 
from fitUtils import fitUtils
import os


f = fitUtils(fIn='/scratchssd/emanca/wproperties-analysis/signalAnalysis/TEST/templates.root', fMap='/scratchssd/emanca/wproperties-analysis/signalAnalysis/ACvalues.root',fileMap='/scratchssd/emanca/wproperties-analysis/signalAnalysis/TEST/AC.root', shapeFile='testfit')

for key in f.file.GetListOfKeys():

    if not 'TH3' in key.GetClassName(): continue
    print key.GetName()
                
    th3=ROOT.TH3D

    th3 = f.file.Get(key.GetName())

    f.project3Dto2D(th3)
                
f.fillSignalList()
f.fillHelGroup()
f.xsecMap()
f.writeShapeFile()
f.fillShapeMap()
f.makeDatacard()

#assert(0)

text2hd5f = 'text2hdf5.py --allowNegativeExpectation --maskedChan=Wplus {}.pkl'.format(f.shapeFile)
print 'executing', text2hd5f 
os.system(text2hd5f)

combinetf = 'combinetf.py --allowNegativePOI -t-1 {}.pkl.hdf5 -o {}.root'.format(f.shapeFile, f.shapeFile)
print 'executing', combinetf
os.system(combinetf)
