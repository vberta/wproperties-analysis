import os
import sys
import ROOT
import json
import argparse
import subprocess
from RDFtree import RDFtree
sys.path.append('python/')
sys.path.append('data/')
ROOT.gSystem.Load('bin/libAnalysisOnData.so')

#ROOT.ROOT.EnableImplicitMT(128)
#fileScale = ROOT.TFile.Open("data/muscales_extended.root")
#p = RDFtree(outputDir="rochPlots", inputFile='/scratchnvme/wmass/WJetsNoCUT_v2/tree_*_*.root',outputFile="rochPlots.root", pretend=False)
#p.branch(nodeToStart='input', nodeToEnd='rochPlots', modules=[ROOT.baseDefinitions(True, True), ROOT.rochesterVariations(fileScale)])
#p.getOutput()

#fileVars = ROOT.TFile.Open("rochPlots/rochPlots.root")
#hnom = fileVars.Get("rochPlots/Mu1_ptnom")
#print hnom.GetName()
#fout = ROOT.TFile("rochPlots/rochPlotsWeights.root", "recreate")
#fileVarsKey = fileVars.Get('rochPlots')
#for key in fileVarsKey.GetListOfKeys():
#    if "nom" in key.GetName(): continue
#    h = fileVarsKey.Get(key.GetName())
#    hden = hnom.Clone()
#    hden.SetName(h.GetName())
#    hden.Divide(h)
#    fout.cd()
#    hden.Write()

ROOT.ROOT.EnableImplicitMT(128)
fileScale = ROOT.TFile.Open("/scratchnvme/emanca/wproperties-analysis/analysisOnData/rochPlots/rochPlotsWeights.root")
p = RDFtree(outputDir="rochPlots", inputFile='/scratchnvme/wmass/WJetsNoCUT_v2/tree_*_*.root',outputFile="rochPlotsClosure.root", pretend=False)
p.branch(nodeToStart='input', nodeToEnd='rochPlots', modules=[ROOT.baseDefinitions(True, True), ROOT.rochesterWeights(fileScale)])
p.getOutput()

