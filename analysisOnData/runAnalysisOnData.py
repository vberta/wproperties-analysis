import os
import sys
import ROOT

from RDFtree import RDFtree

sys.path.append('python/')
sys.path.append('data/')
from systematics import systematics

from getLumiWeight import getLumiWeight

ROOT.gSystem.Load('bin/libAnalysisOnData.so')

c=64
		
ROOT.ROOT.EnableImplicitMT(c)

print "running with {} cores".format(c)

inputFile = '/scratchssd/sroychow/NanoAOD2016-V2/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/tree.root'

cutSignal = 'Vtype==0 && HLT_SingleMu24 && Mu1_pt>25. && MT>0. && MET_filters==1 && nVetoElectrons==0' 
regions = {}
regions['signal'] = cutSignal

weight = 'float(puWeight*lumiweight*TriggerSF*RecoSF)'

fileSF = ROOT.TFile.Open("/scratch/bertacch/wmass/wproperties-analysis/bkgAnalysis/ScaleFactors.root")

p = RDFtree(outputDir = 'TEST', inputFile = inputFile, outputFile="test.root", pretend=True)

p.branch(nodeToStart = 'input', nodeToEnd = 'defs', modules = [ROOT.baseDefinitions(),ROOT.weightDefinitions(fileSF),getLumiWeight(xsec=61526.7, inputFile=inputFile)])

for region,cut in regions.iteritems():

    nom = ROOT.vector('string')()
    nom.push_back("Nom")

    p.branch(nodeToStart = 'defs', nodeToEnd = 'prefit_{}'.format(region), modules = [ROOT.muonHistos(cut, weight, nom,"Nom")])
    
    for s,variations in systematics.iteritems():
        weight.replace(s, "1.")
        vars_vec = ROOT.vector('string')()
        for var in variations[0]:
            vars_vec.push_back(var)

        p.branch(nodeToStart = 'defs', nodeToEnd = 'prefit_{}_{}Vars'.format(region,s), modules = [ROOT.muonHistos(cut, weight,vars_vec,variations[1])])

p.getOutput()
p.saveGraph()




