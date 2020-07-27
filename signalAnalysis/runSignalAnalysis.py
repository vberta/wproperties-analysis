import os
import sys
import ROOT

from RDFtree import RDFtree
sys.path.append('python/')

from getLumiWeight import getLumiWeight

ROOT.gSystem.Load('bin/libSignalAnalysis.so')

c=64

ROOT.ROOT.EnableImplicitMT(c)

print "running with {} cores".format(c)


inputFile = '/scratchssd/sroychow/NanoAOD2016-V2/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_GEN/test_tree_*.root'

p = RDFtree(outputDir = 'TEST', inputFile = inputFile, outputFile="AC.root")
p.branch(nodeToStart = 'input', nodeToEnd = 'basicSelection', modules = [getLumiWeight(xsec=61526.7, inputFile=inputFile), ROOT.baseDefinitions(),ROOT.defineHarmonics()])
p.branch(nodeToStart = 'basicSelection', nodeToEnd = 'AngCoeff', modules = [ROOT.AngCoeff()])
p.getOutput()

p = RDFtree(outputDir = 'TEST', inputFile = inputFile, outputFile="templates.root")
p.branch(nodeToStart = 'input', nodeToEnd = 'basicSelection', modules = [getLumiWeight(xsec=61526.7, inputFile=inputFile), ROOT.baseDefinitions(),ROOT.defineHarmonics()])
fileAC = ROOT.TFile.Open("TEST/AC.root")
p.branch(nodeToStart = 'basicSelection', nodeToEnd = 'AngCoeff2',modules = [ROOT.getACValues(fileAC)])
p.branch(nodeToStart = 'AngCoeff2', nodeToEnd = 'accMap', modules =[ROOT.getAccMap(fileAC)])
p.branch(nodeToStart = 'accMap', nodeToEnd = 'templates', modules =[ROOT.getWeights(), ROOT.templateBuilder()])
p.branch(nodeToStart = 'accMap', nodeToEnd = 'dataObs', modules =[ROOT.dataObs()])

p.getOutput()
p.saveGraph()


"""
pdf = ROOT.vector('string')()
for i in range(1,102):
	pdf.push_back('replica{}'.format(i))

p.branch(nodeToStart = 'basicSelection', nodeToEnd = 'AngCoeffPDF', modules = [ROOT.defineSystWeight("LHEPdfWeight"),ROOT.AngCoeff(pdf,"LHEPdfWeight")])

p.getOutput()


#p.branch(nodeToStart = 'AngCoeffPDF', nodeToEnd = 'AngCoeffPDF2',modules = [ROOT.getACValues([h for h in p.getObjects('AngCoeff') if 'vector' in h.__cppname__][0])])

maps = ROOT.vector(ROOT.RDF.RResultPtr('TH2D'))()
for i in range(0,3):
	maps.push_back([h for h in p.getObjects('AngCoeff') if not 'vector' in h.__cppname__][i])

p.branch(nodeToStart = 'AngCoeff2', nodeToEnd = 'accMap', modules =[ROOT.getAccMap(maps)])
p.branch(nodeToStart = 'accMap', nodeToEnd = 'templates', modules =[ROOT.getWeights(), ROOT.templateBuilder()])
p.branch(nodeToStart = 'accMap', nodeToEnd = 'dataObs', modules =[ROOT.dataObs()])

p.getOutput()
#p.saveGraph()
"""		



