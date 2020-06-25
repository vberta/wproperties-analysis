import os
import sys
import ROOT

from RDFtree import RDFtree

sys.path.append('python/')

from getLumiWeight import getLumiWeight

ROOT.gSystem.Load('bin/libAnalysisOnData.so')

c=64
		
ROOT.ROOT.EnableImplicitMT(c)

print "running with {} cores".format(c)

inputFile = '/scratch/sroychow/NanoAOD2016-V2/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/tree.root'

cutSignal = 'Vtype==0 && HLT_SingleMu24 && muon_pt>25. && mt>0. && MET_filters==1 && nVetoElectrons==0' 
cut2 = '1.' 
cut3 = '1.' 
cut4 = '1.' 

p = RDFtree(outputDir = 'TEST', inputFile = inputFile, outputFile="test.root")

p.branch(nodeToStart = 'input', nodeToEnd = 'defs', modules = [ROOT.baseDefinitions(),ROOT.weightDefinitions(),getLumiWeight(xsec=61526.7, inputFile=inputFile)])

for r in regions concerning prefit plots:

    p.branch(nodeToStart = 'defs', nodeToEnd = 'muonHistos_r', modules = [ROOT.muonHistos(cut, weight)])
    
    for variations concerning prefit plots:

        p.branch(nodeToStart = 'defs', nodeToEnd = 'muonHistos_r_var1', modules = [ROOT.muonHistos(cut, weight,Muon_ISO_BCDEF_SF,"Muon_ISO_syst")])

for r in regions concerning bkg plots:

    p.branch(nodeToStart = 'defs', nodeToEnd = 'bkgHistos_r', modules = [ROOT.bkgHistos(cut, weight)])

    for variations concerning prefit plots:

        p.branch(nodeToStart = 'defs', nodeToEnd = 'bkgHistos_r_var1', modules = [ROOT.bkgHistos(cut, weight)])


p.getOutput()



