import os
import sys
import ROOT
from math import *

from RDFtree import *

sys.path.append('python/')

from getLumiWeight import *

print "Loading"
ROOT.gSystem.Load('bin/libAnalysisOnData.so')

def runRDFForaSample(nCores, sampleKey, inputFiles, xSec ="1.", dataType = "MC", cutMap = {}, systCategory = 0, weightVarDict = {}):
    if nCores:
        ROOT.ROOT.EnableImplicitMT(nCores)
        print "Running with {} cores".format(nCores)
    else:
        print "Running in single thread"

    print cutMap
     
    nomweight = 'puWeight*' + \
                'lumiweight*' + \
                'Muon_Trigger_BCDEF_SF[Idx_mu1]*' + \
                'Muon_ID_BCDEF_SF[Idx_mu1]*' + \
                'Muon_ISO_BCDEF_SF[Idx_mu1]'  if dataType == "MC" else 'float(1.)'
    
    print "printing from runAnalysis:\n", inputFiles
    p = RDFtree(outputDir = 'TEST', inputFile = inputFiles, outputFile= sampleKey + "_output.root")
    
    Muon_ISO_BCDEF_SF = ROOT.vector('string')()
    Muon_ISO_BCDEF_SF.push_back('Muon_ISO_BCDEF_SFstatUp')
    Muon_ISO_BCDEF_SF.push_back('Muon_ISO_BCDEF_SFstatDown')
    Muon_ISO_BCDEF_SF.push_back('Muon_ISO_BCDEF_SFsystUp')
    Muon_ISO_BCDEF_SF.push_back('Muon_ISO_BCDEF_SFsystDown')
    
    genweightvec = ROOT.vector('string')()
    for i in range(0, 99):
        genweightvec.push_back(ROOT.std.string("LHEPdfWeight" + str(i)))  

    nodeweightDict = {}
    for wt, systs in weightVarDict.items():
        wvec = ROOT.std.vector(ROOT.std.string)()
        for syst in systs:
            wvec.push_back(ROOT.std.string(syst))
        nodeweightDict['muonHistos_' + wt]  = wvec

    print nodeweightDict

    hmap = ROOT.TH2F('hmap','',10,-2.5,2.5,101,25,65)
    for i in range(10):
        for j in range(101):
            hmap.SetBinContent(i,j,0.9)
            
    if dataType == 'MC':        
        p.branch(nodeToStart = 'input', nodeToEnd = 'inputwLumi',    modules =[getLumiWeight(xsec=xSec, inputFile=inputFiles)])
        for region, cut in cutMap.items():
            p.branch(nodeToStart = 'inputwLumi', nodeToEnd = region,    modules =[ ROOT.baseDefinitions( hmap, ROOT.std.string(cut) )])
            #nominal histos
            p.branch(nodeToStart = region, nodeToEnd = region + '/muonHistos',    modules = [ROOT.muonHistos(ROOT.std.string(cut), nomweight)])
            #is 2 only for Signal and TTbar samples
            if systCategory == 2:
                p.branch(nodeToStart = region, nodeToEnd = region +  '/muonHisots_pdfweight',    modules = [ROOT.muonHistos(ROOT.std.string(cut), nomweight, genweightvec, 'LHEPdfWeight')])
            #weight systematics  
            for en, wtvec in nodeweightDict.items():
                ecol = region + "_" + en
                p.branch(nodeToStart = region, nodeToEnd =  region + "/" + en, modules = [ROOT.getSystWeight(wtvec, ROOT.std.string(ecol) ), ROOT.muonHistos(cut, nomweight, wtvec, ROOT.std.string(ecol) )])

    else:
        for region, cut in cutMap.items():
            p.branch(nodeToStart = 'input', nodeToEnd = region,    modules =[ ROOT.baseDefinitions( hmap, ROOT.std.string(cut) )])
            #nominal histos
            p.branch(nodeToStart = region, nodeToEnd = region + '/muonHistos',    modules = [ROOT.muonHistos(ROOT.std.string(cut), nomweight)])

    print "Get output..."
    p.getOutput()
    p.saveGraph()

