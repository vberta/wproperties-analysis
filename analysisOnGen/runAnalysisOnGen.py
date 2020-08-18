import os
import sys
import ROOT
import argparse

from RDFtree import RDFtree
sys.path.append('python/')
sys.path.append('utils/')

from systematics import systematics
from getLumiWeight import getLumiWeight

ROOT.gSystem.Load('bin/libSignalAnalysis.so')

c=128

ROOT.ROOT.EnableImplicitMT(c)

print "running with {} cores".format(c)


parser = argparse.ArgumentParser('')
parser.add_argument('-runAC', '--runAC', default=False, action='store_true', help='Use to run the Angular Coefficients with all the variations')
parser.add_argument('-runTemplates', '--runTemplates', default=False, action='store_true', help='Use to run the templates')
args = parser.parse_args()
runAC = args.runAC
runTemplates = args.runTemplates

inputFile = 'test_tree_*.root'

p = RDFtree(outputDir = 'GenInfo', inputFile = inputFile, outputFile="genInfo.root")
p.branch(nodeToStart = 'input', nodeToEnd = 'basicSelection', modules = [getLumiWeight(xsec=61526.7, inputFile=inputFile), ROOT.baseDefinitions(),ROOT.defineHarmonics(),ROOT.Replica2Hessian(),ROOT.accMap()])

if runAC:
    p.branch(nodeToStart = 'basicSelection', nodeToEnd = 'angularCoefficients', modules = [ROOT.AngCoeff()])
    """
    #weight variations
    for s,variations in systematics.iteritems():
        print "branching weight variations", s
        vars_vec = ROOT.vector('string')()
        for var in variations[0]:
            vars_vec.push_back(var)
        
        p.branch(nodeToStart = 'basicSelection', nodeToEnd = 'angularCoefficients_{}'.format(s), modules = [ROOT.AngCoeff(vars_vec,variations[1])])
    """
    p.getOutput()

if runTemplates:
    
    nom = ROOT.vector('string')()
    nom.push_back("")

    fileAC = ROOT.TFile.Open("genInput.root")
    p.branch(nodeToStart = 'basicSelection', nodeToEnd = 'harmonicsWeights',modules = [ROOT.getACValues(fileAC)])
    p.branch(nodeToStart = 'harmonicsWeights', nodeToEnd = 'accMap', modules =[ROOT.getAccMap(fileAC)])
    p.branch(nodeToStart = 'accMap', nodeToEnd = 'templates', modules =[ROOT.getWeights(), ROOT.templateBuilder()])
    p.branch(nodeToStart = 'accMap', nodeToEnd = 'dataObs', modules =[ROOT.dataObs(nom,"Nom")])

    #weight variations
    for s,variations in systematics.iteritems():
        print "branching weight variations", s
        vars_vec = ROOT.vector('string')()
        for var in variations[0]:
            vars_vec.push_back(var)
        p.branch(nodeToStart = 'accMap', nodeToEnd = 'dataObs_{}'.format(s), modules =[ROOT.dataObs(vars_vec,variations[1])])

    p.getOutput()
    p.saveGraph()
