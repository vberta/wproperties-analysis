import os
import sys
import ROOT
import json

from RDFtree import RDFtree
sys.path.append('python/')
sys.path.append('data/')
from systematics import systematics
from selections import selections, selectionVars

ROOT.gSystem.Load('bin/libAnalysisOnData.so')


fvec=ROOT.vector('string')()
samples={}
with open('data/samples_2016.json') as f:
  samples = json.load(f)
for sample in samples:
    if not samples[sample]['datatype']=='DATA': continue
    print sample
    c = 64		
    ROOT.ROOT.EnableImplicitMT(c)

    print "running with {} cores".format(c)
    direc = samples[sample]['dir']
    for dirname,fname in direc.iteritems():
        ##check if file exists or not
        inputFile = '/scratchssd/sroychow/NanoAOD2016-V2/{}/tree.root'.format(dirname)
        isFile = os.path.isfile(inputFile)  
        if not isFile:
            print inputFile, " does not exist"
            continue
        fvec.push_back(inputFile)
        print inputFile

if fvec.empty():
    print "No files found for json provided\n"
    sys.exit(1)
    
print fvec
weight = 'float(1)'
p = RDFtree(outputDir = './output/', inputFile = fvec, outputFile="SingleMuonData_plots.root".format(sample), pretend=True)
p.branch(nodeToStart = 'input', nodeToEnd = 'defs', modules = [ROOT.baseDefinitions(0)])
for region,cut in selections.iteritems():
    print region       
    nom = ROOT.vector('string')()
    nom.push_back("")
    #last argument refers to histo category - 0 = Nominal, 1 = Pt scale , 2 = MET scale
    print "branching nominal"
    p.branch(nodeToStart = 'defs', nodeToEnd = 'prefit_{}/Nominal'.format(region), modules = [ROOT.muonHistos(cut, weight, nom,"Nom",0)])    
    p.getOutput()
    #p.saveGraph()


