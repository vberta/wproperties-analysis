import os
import sys
import ROOT
from math import *

from RDFtree import *

sys.path.append('python/')

from getLumiWeight import *

ROOT.gSystem.Load('bin/libAnalysisOnData.so')

c=64
		
ROOT.ROOT.EnableImplicitMT(c)

print "running with {} cores".format(c)


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


p.branch(nodeToStart = 'input', nodeToEnd = 'muonHistos', modules = [getLumiWeight(xsec=61526.7, inputFile=inputFile),ROOT.muonHistos(cut, weight)])
p.branch(nodeToStart = 'input', nodeToEnd = 'muonHistos_ISO', modules = [getLumiWeight(xsec=61526.7, inputFile=inputFile),ROOT.getSystWeight(Muon_ISO_BCDEF_SF,"Muon_ISO_syst"),ROOT.muonHistos(cut, weight,Muon_ISO_BCDEF_SF,"Muon_ISO_syst")])
p.getOutput()



