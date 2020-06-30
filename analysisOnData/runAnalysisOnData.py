import os
import sys
import ROOT
import json

from RDFtree import RDFtree
sys.path.append('python/')
sys.path.append('data/')
from systematics import systematics
from selections import selections, selections_bkg, selectionVars

from getLumiWeight import getLumiWeight

ROOT.gSystem.Load('bin/libAnalysisOnData.so')

runBKG = False ###please make this an option

samples={}
with open('data/samples_2016.json') as f:
  samples = json.load(f)
for sample in samples:

    if not samples[sample]['datatype']=='MC': continue
    print sample
    direc = samples[sample]['dir']
    xsec = samples[sample]['xsec']

    c = 64		
    #ROOT.ROOT.EnableImplicitMT(c)

    print "running with {} cores".format(c)

    fvec=ROOT.vector('string')()
    for dirname,fname in direc.iteritems():
        ##check if file exists or not
        inputFile = '/scratchssd/sroychow/NanoAOD2016-V2/{}/tree.root'.format(dirname)
        #inputFile = "/scratchssd/sroychow/forElisabetta/testtree.root"
        isFile = os.path.isfile(inputFile)  
        if not isFile:
            print inputFile, " does not exist"
            continue
        fvec.push_back(inputFile)
        print inputFile
        WJets = False
        if "WJetsToLNu" in inputFile: WJets = True
    if fvec.empty():
        print "No files found for directory:", samples[sample], " SKIPPING processing"
        continue

    weight = 'float(puWeight*lumiweight*TriggerSF*RecoSF'
    if WJets: weight+="*weightPt*weightY"
    weight+=")"

    fileSF = ROOT.TFile.Open("data/ScaleFactors.root")

    p = RDFtree(outputDir = './output/', inputFile = inputFile, outputFile="{}_plots.root".format(sample), pretend=True)
    if WJets:
        filePt = ROOT.TFile.Open("data/histoUnfoldingSystPt_nsel2_dy3_rebin1_default.root")
        fileY = ROOT.TFile.Open("data/histoUnfoldingSystRap_nsel2_dy3_rebin1_default.root")
        p.branch(nodeToStart = 'input', nodeToEnd = 'defs', modules = [ROOT.reweightFromZ(filePt,fileY),ROOT.baseDefinitions(),ROOT.weightDefinitions(fileSF),getLumiWeight(xsec=xsec, inputFile=inputFile)])
    else:
        p.branch(nodeToStart = 'input', nodeToEnd = 'defs', modules = [ROOT.baseDefinitions(),ROOT.weightDefinitions(fileSF),getLumiWeight(xsec=xsec, inputFile=inputFile)])

    if runBKG: selections = selections_bkg

    for region,cut in selections.iteritems():
        nom = ROOT.vector('string')()
        nom.push_back("")
        #last argument refers to histo category - 0 = Nominal, 1 = Pt scale , 2 = MET scale
        print "branching nominal"

        if not (runBKG): p.branch(nodeToStart = 'defs', nodeToEnd = 'prefit_{}/Nominal'.format(region), modules = [ROOT.muonHistos(cut, weight, nom,"Nom",0)])  
        p.branch(nodeToStart = 'defs', nodeToEnd = 'templates_{}/Nominal'.format(region), modules = [ROOT.templates(cut, weight, nom,"Nom",0)])    
  
        #weight variations
        for s,variations in systematics.iteritems():
            if not "LHEScaleWeight" in s:
                weight.replace(s, "1.")
            else: 
                if not "WJets" in sample and not "TTJets" in sample and not "DY" in sample and not "ST" in sample: continue 
            vars_vec = ROOT.vector('string')()
            for var in variations[0]:
                vars_vec.push_back(var)
            print "branching weight variations", region, s

            if not (runBKG): p.branch(nodeToStart = 'defs'.format(region), nodeToEnd = 'prefit_{}/{}Vars'.format(region,s), modules = [ROOT.muonHistos(cut, weight,vars_vec,variations[1], 0)])
            p.branch(nodeToStart = 'defs'.format(region), nodeToEnd = 'templates_{}/{}Vars'.format(region,s), modules = [ROOT.templates(cut, weight,vars_vec,variations[1], 0)])

        #column variations#weight will be nominal, cut will vary
        for vartype, vardict in selectionVars.iteritems():
            cut_vec = ROOT.vector('string')()
            var_vec = ROOT.vector('string')()
            for selvar, hcat in vardict.iteritems() :
                newcut = cut.replace('MT', 'MT_'+selvar)

                if 'corrected' in selvar:
                    newcut = newcut.replace('Mu1_pt', 'Mu1_pt_'+selvar)

                cut_vec.push_back(newcut)
                var_vec.push_back(selvar)

            if not (runBKG): p.branch(nodeToStart = 'defs', nodeToEnd = 'prefit_{}/{}Vars'.format(region,vartype), modules = [ROOT.muonHistos(cut_vec, weight, nom,"Nom",hcat,var_vec)])  
            p.branch(nodeToStart = 'defs', nodeToEnd = 'templates_{}/{}Vars'.format(region,vartype), modules = [ROOT.templates(cut_vec, weight, nom,"Nom",hcat,var_vec)])  

    p.getOutput()
    #p.saveGraph()
assert(0)
for sample in samples:

    if not samples[sample]['datatype']=='DATA': continue
    print sample
    direc = samples[sample]['dir']

    c = 64		
    #ROOT.ROOT.EnableImplicitMT(c)

    print "running with {} cores".format(c)

    fvec=ROOT.vector('string')()
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
        print "No files found for directory:", samples[sample], " SKIPPING processing"
        continue

    weight = '1.'

    p = RDFtree(outputDir = './output/', inputFile = inputFile, outputFile="{}_plots.root".format(sample), pretend=True)

    p.branch(nodeToStart = 'input', nodeToEnd = 'defs', modules = [ROOT.baseDefinitions()])

    if runBKG: selections = selections_bkg

    for region,cut in selections.iteritems():
        nom = ROOT.vector('string')()
        nom.push_back("")
        #last argument refers to histo category - 0 = Nominal, 1 = Pt scale , 2 = MET scale
        print "branching nominal"

        if not (runBKG): p.branch(nodeToStart = 'defs', nodeToEnd = 'prefit_{}/Nominal'.format(region), modules = [ROOT.muonHistos(cut, weight, nom,"Nom",0)])  
        p.branch(nodeToStart = 'defs', nodeToEnd = 'templates_{}/Nominal'.format(region), modules = [ROOT.templates(cut, weight, nom,"Nom",0)])

    p.getOutput()




