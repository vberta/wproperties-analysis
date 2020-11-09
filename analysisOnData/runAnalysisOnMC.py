import os
import sys
import ROOT
import json
import argparse
import copy
import time
from RDFtree import RDFtree

sys.path.append('data/')
from systematics import systematics
from selections import selections, selectionVars, selections_bkg
sys.path.append('python/')
from getLumiWeight import getLumiWeight

ROOT.gSystem.Load('bin/libAnalysisOnData.so')
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 2001;")

def RDFprocess(fvec, outputDir, sample, xsec, fileSF, systType, pretendJob,SBana=False):

    p = RDFtree(outputDir = outputDir, inputFile = fvec, outputFile="{}_plots.root".format(sample), pretend=pretendJob)
    
    if systType == 0: #this is data
        p.branch(nodeToStart='input', nodeToEnd='defs', modules=[ROOT.baseDefinitions(False, False)])
    elif systType < 2: #this is MC with no PDF variations
        p.branch(nodeToStart = 'input', nodeToEnd = 'defs', modules = [ROOT.baseDefinitions(True, False),ROOT.weightDefinitions(fileSF),getLumiWeight(xsec=xsec, inputFile=fvec)])
    else:
        p.branch(nodeToStart = 'input', nodeToEnd = 'defs', modules = [ROOT.baseDefinitions(True, False),ROOT.weightDefinitions(fileSF),getLumiWeight(xsec=xsec, inputFile=fvec),ROOT.Replica2Hessian()])
    #selections bkg also includes Signal
    for region,cut in list(selections_bkg.items()):
        print("running in region {}".format(region))
        #drop SF evaluation in anti-isolated region
        if 'aiso' in region:
            weight = 'float(puWeight*PrefireWeight*lumiweight)'
        else:
            weight = 'float(puWeight*PrefireWeight*lumiweight*WHSF)'
        if systType == 0:
            weight = "float(1.)"
        
        #nominal part of the analysis
        nom = ROOT.vector('string')()
        nom.push_back("")
        #last argument refers to histo category - 0 = Nominal, 1 = Pt scale , 2 = MET scale

        if region == "Signal" or (region=='Sideband' and SBana):
            p.branch(nodeToStart = 'defs', nodeToEnd = 'prefit_{}/Nominal'.format(region), modules = [ROOT.muonHistos(cut, weight, nom,"Nom",0)])  
        p.branch(nodeToStart = 'defs', nodeToEnd = 'templates_{}/Nominal'.format(region), modules = [ROOT.templates(cut, weight, nom,"Nom",0)])    
        if systType == 0: #stop data here
            continue
        #sample specific systematics
        #weight variations
        for s,variations in list(systematics.items()):
            if "LHEScaleWeight" in s and systType != 2 :  continue
            if "LHEPdfWeight"   in s and systType != 2 :  continue
            if "alphaS"         in s and systType != 2 :  continue

            if 'aiso' in region: continue
            var_weight = weight.replace(s, "1.")

            vars_vec = ROOT.vector('string')()
            for var in variations[0]:
                vars_vec.push_back(var)
            
            if region == "Signal" or (region=='Sideband' and SBana): 
                p.branch(nodeToStart = 'defs'.format(region), nodeToEnd = 'prefit_{}/{}'.format(region,s), modules = [ROOT.muonHistos(cut,var_weight,vars_vec,variations[1], 0)])
            p.branch(nodeToStart = 'defs'.format(region), nodeToEnd = 'templates_{}/{}'.format(region,s), modules = [ROOT.templates(cut,var_weight,vars_vec,variations[1], 0)])

        #column variations
        #weight will be nominal, cut will vary
        for vartype, vardict in list(selectionVars.items()):
            cut_vec = ROOT.vector('string')()
            var_vec = ROOT.vector('string')()
            for selvar, hcat in list(vardict.items()) :
                newcut = cut.replace('MT', 'MT'+selvar)
                if 'corrected' in selvar:
                    newcut = newcut.replace('Mu1_pt', 'Mu1_pt'+selvar)
                cut_vec.push_back(newcut)
                var_vec.push_back(selvar)
            if region == "Signal" or (region=='Sideband' and SBana):
                p.branch(nodeToStart = 'defs', nodeToEnd = 'prefit_{}/{}'.format(region,vartype), modules = [ROOT.muonHistos(cut_vec, weight, nom,"Nom",hcat,var_vec)])  
            p.branch(nodeToStart = 'defs', nodeToEnd = 'templates_{}/{}'.format(region,vartype), modules = [ROOT.templates(cut_vec, weight, nom,"Nom",hcat,var_vec)])  
    return p
def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument('-p', '--pretend',type=bool, default=False, help="run over a small number of event")
    parser.add_argument('-o', '--outputDir',type=str, default='./output/', help="output dir name")
    parser.add_argument('-i', '--inputDir',type=str, default='/scratchnvme/wmass/NanoAOD2016-V2/', help="input dir name")    
    parser.add_argument('-s', '--SBana',type=bool, default=False, help="run also on the sideband (clousure test)")

    args = parser.parse_args()
    pretendJob = args.pretend
    outputDir = args.outputDir
    inDir = args.inputDir
    SBana = args.SBana

    if pretendJob:
        print("Running a test job over a few events")
    else:
        print("Running on full dataset")
    ROOT.ROOT.EnableImplicitMT(64)
    RDFtrees = {}
    samples={}
    with open('data/samples_2016.json') as f:
        samples = json.load(f)
    for sample in samples:
        print('analysing sample: %s'%sample)
        direc = samples[sample]['dir']
        xsec = samples[sample]['xsec']
        fvec=ROOT.vector('string')()
        for dirname,fname in list(direc.items()):
            ##check if file exists or not
            inputFile = '{}/{}/tree.root'.format(inDir, dirname)
            isFile = os.path.isfile(inputFile)  
            if not isFile:
                print(inputFile, " does not exist")
                continue
            fvec.push_back(inputFile)

        if fvec.empty():
            print("No files found for directory:", samples[sample], " SKIPPING processing")
            continue
        print(fvec) 
        fileSF = ROOT.TFile.Open("data/ScaleFactors_OnTheFly.root")
        systType = samples[sample]['systematics']
        RDFtrees[sample] = RDFprocess(fvec, outputDir, sample, xsec, fileSF, systType, pretendJob, SBana)

    #now trigger all the event loops at the same time:
    objList = []
    for sample in samples:
        RDFtreeDict = RDFtrees[sample].getObjects()
        for node in RDFtreeDict:
            objList.extend(RDFtreeDict[node])
    #magic happens here
    start = time.time()
    ROOT.RDF.RunGraphs(objList)
    #now write the histograms:
    
    for sample in samples:
        RDFtrees[sample].getOutput()
    print('all samples processed in {} s'.format(time.time()-start))
if __name__ == "__main__":
    main()
