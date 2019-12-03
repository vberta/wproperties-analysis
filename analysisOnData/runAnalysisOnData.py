import os
import sys
import ROOT
from math import *

from RDFtree import *

sys.path.append('python/')

from getLumiWeight import *

print "Loading"
ROOT.gSystem.Load('bin/libAnalysisOnData.so')

c=64
		
ROOT.ROOT.EnableImplicitMT(c)

print "Running with {} cores".format(c)

inputFile = '/scratch/sroychow/NanoAOD2016-V1MCFinal/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/tree.root'

muon = '_corrected'
met = '_nom'

cut = 'Vtype==0 && ' + \
      'HLT_SingleMu24 && '+ \
      ('Muon%s_pt[Idx_mu1]>25. && ' % muon) + \
      ('Muon%s_MET%s_mt[Idx_mu1]>0. && ' % (muon, met) ) + \
      'MET_filters==1 && ' + \
      'nVetoElectrons==0'

weight = 'puWeight*' + \
         'lumiweight*' + \
         'Muon_Trigger_BCDEF_SF[Idx_mu1]*' + \
         'Muon_ID_BCDEF_SF[Idx_mu1]*' + \
         'Muon_ISO_BCDEF_SF[Idx_mu1]'

p = RDFtree(outputDir = 'TEST', inputFile = inputFile, outputFile="test.root")

Muon_ISO_BCDEF_SF = ROOT.vector('string')()
Muon_ISO_BCDEF_SF.push_back('Muon_ISO_BCDEF_SFstatUp')
Muon_ISO_BCDEF_SF.push_back('Muon_ISO_BCDEF_SFstatDown')
Muon_ISO_BCDEF_SF.push_back('Muon_ISO_BCDEF_SFsystUp')
Muon_ISO_BCDEF_SF.push_back('Muon_ISO_BCDEF_SFsystDown')

hmap = ROOT.TH2F('hmap','',10,-2.5,2.5,101,25,65)
for i in range(10):
    for j in range(101):
        hmap.SetBinContent(i,j,0.9)


#p.branch(nodeToStart = 'input', nodeToEnd = 'fakeRate',    modules = [getLumiWeight(xsec=61526.7, inputFile=inputFile), 
#                                                                        ROOT.fakeRate( hmap )])
    
p.branch(nodeToStart = 'input', nodeToEnd = 'muonHistos',    modules = [ROOT.getLumiWeight(inputFile, 35.9, 61526.7), 
                                                                        ROOT.getSystWeight(Muon_ISO_BCDEF_SF,"Muon_ISO_syst"),
                                                                        ROOT.muonHistos(cut, weight, Muon_ISO_BCDEF_SF,"Muon_ISO_syst")])

#p.branch(nodeToStart = 'fakeRate', nodeToEnd = 'muonHistos_ISO', modules = [ROOT.getSystWeight(Muon_ISO_BCDEF_SF,"Muon_ISO_syst"), 
#                                                                            ROOT.muonHistos(cut, weight+'*FakeRate', Muon_ISO_BCDEF_SF,"Muon_ISO_syst")])

print "Get output..."
p.getOutput()
#p.saveGraph()


