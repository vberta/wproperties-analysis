import os
import sys
import ROOT
import json
import argparse
import subprocess
from RDFtree import RDFtree
sys.path.append('python/')
sys.path.append('data/')
from systematics import systematics
from selections import selections, selectionVars, selections_bkg

from getLumiWeight import getLumiWeight

ROOT.gSystem.Load('bin/libAnalysisOnData.so')
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 2001;");

def RDFprocessWJetsMC(fvec, outputDir, sample, xsec, fileSF, ncores, pretendJob=True):
    ROOT.ROOT.EnableImplicitMT(ncores)
    print "running with {} cores for sample:{}".format(ncores, sample) 
    wdecayselections = { 
        'WToMu'  : ' && (abs(genVtype) == 14)',
        'WToTau' : ' && (abs(genVtype) == 16)'
    }

    p = RDFtree(outputDir = outputDir, inputFile = fvec, outputFile="{}_plots.root".format(sample), pretend=pretendJob)
    filePt = ROOT.TFile.Open("data/histoUnfoldingSystPt_nsel2_dy3_rebin1_default.root")
    fileY = ROOT.TFile.Open("data/histoUnfoldingSystRap_nsel2_dy3_rebin1_default.root")
    fileAC = ROOT.TFile.Open("../analysisOnGen/genInput.root")
    p.branch(nodeToStart = 'input', nodeToEnd = 'defs', modules = [ROOT.reweightFromZ(filePt,fileY),ROOT.baseDefinitions(),ROOT.weightDefinitions(fileSF),getLumiWeight(xsec=xsec, inputFile=fvec),ROOT.Replica2Hessian()])
    for region,cut in selections_bkg.iteritems():
        if 'aiso' in region:
            weight = 'float(puWeight*lumiweight*weightPt*weightY)'
        else:
            weight = 'float(puWeight*lumiweight*WHSF*weightPt*weightY)'
        
        print weight, "NOMINAL WEIGHT"
        
        nom = ROOT.vector('string')()
        nom.push_back("")
        #last argument refers to histo category - 0 = Nominal, 1 = Pt scale , 2 = MET scale
        print "branching nominal for region:", region 
        wtomu_cut = cut + wdecayselections['WToMu']
        wtotau_cut = cut + wdecayselections['WToTau']
        if region == "Signal":
            print "adding muon histo to graph for Signal region"
            p.branch(nodeToStart = 'defs', nodeToEnd = '{}/prefit_{}/Nominal'.format('WToMu', region), modules = [ROOT.muonHistos(wtomu_cut, weight, nom,"Nom",0)])     
            p.branch(nodeToStart = 'defs', nodeToEnd = '{}/prefit_{}/Nominal'.format('WToTau', region), modules = [ROOT.muonHistos(wtotau_cut, weight, nom,"Nom",0)])     
            
            #reco templates with AC reweighting
            steps = [ROOT.getACValues(fileAC),ROOT.defineHarmonics(),ROOT.getMassWeights(),ROOT.getWeights(),ROOT.templateBuilder(wtomu_cut, weight,nom,"Nom",0)]
            p.branch(nodeToStart = 'defs', nodeToEnd = '{}/templatesAC_{}/Nominal'.format('WToMu', region), modules = steps)
        #Nominal templates
        p.branch(nodeToStart = 'defs', nodeToEnd = '{}/templates_{}/Nominal'.format('WToMu', region), modules = [ROOT.templates(wtomu_cut, weight, nom,"Nom",0)])            
        p.branch(nodeToStart = 'defs', nodeToEnd = '{}/templates_{}/Nominal'.format('WToTau', region), modules = [ROOT.templates(wtotau_cut, weight, nom,"Nom",0)])            
   
        #weight variations
        for s,variations in systematics.iteritems():
            print "branching weight variations", s
            #if "LHEScaleWeight" in s and samples[sample]['systematics'] != 2 :  continue
            if "LHEPdfWeight" in s or "LHEScaleWeight" in s :
                var_weight = weight
                #        if not "LHEScaleWeight" in s :
            else:
                if 'aiso' in region: continue
                var_weight = weight.replace(s, "1.")
            vars_vec = ROOT.vector('string')()
            for var in variations[0]:
                vars_vec.push_back(var)
            print weight,"\t",var_weight, "MODIFIED WEIGHT"
            if region == "Signal": 
                p.branch(nodeToStart = 'defs'.format(region), nodeToEnd = '{}/prefit_{}/{}Vars'.format('WToMu', region,s), modules = [ROOT.muonHistos(wtomu_cut, var_weight,vars_vec,variations[1], 0)])
                p.branch(nodeToStart = 'defs'.format(region), nodeToEnd = '{}/prefit_{}/{}Vars'.format('WToTau', region,s), modules = [ROOT.muonHistos(wtotau_cut, var_weight,vars_vec,variations[1], 0)])
                #reco templates with AC reweighting
                steps = [ROOT.getACValues(fileAC),ROOT.defineHarmonics(),ROOT.getMassWeights(),ROOT.getWeights(),ROOT.templateBuilder(wtomu_cut, var_weight,vars_vec,variations[1], 3)]
                p.branch(nodeToStart = 'defs', nodeToEnd = '{}/templatesAC_{}/{}Vars'.format('WToMu', region, s), modules = steps)
            #Template vars
            p.branch(nodeToStart = 'defs'.format(region), nodeToEnd = '{}/templates_{}/{}Vars'.format('WToMu', region,s), modules = [ROOT.templates(wtomu_cut, var_weight,vars_vec,variations[1], 0)])
            p.branch(nodeToStart = 'defs'.format(region), nodeToEnd = '{}/templates_{}/{}Vars'.format('WToTau', region,s), modules = [ROOT.templates(wtotau_cut, var_weight,vars_vec,variations[1], 0)])

        #column variations#weight will be nominal, cut will vary
        for vartype, vardict in selectionVars.iteritems():
            wtomu_cut_vec = ROOT.vector('string')()
            wtomu_var_vec = ROOT.vector('string')()
            wtotau_cut_vec = ROOT.vector('string')()
            wtotau_var_vec = ROOT.vector('string')()
            for selvar, hcat in vardict.iteritems() :
                wtomu_newcut = wtomu_cut.replace('MT', 'MT'+selvar)
                wtotau_newcut = wtotau_cut.replace('MT', 'MT'+selvar)
                if 'corrected' in selvar:
                    wtomu_newcut = wtomu_newcut.replace('Mu1_pt', 'Mu1_pt'+selvar)
                    wtotau_newcut = wtotau_newcut.replace('Mu1_pt', 'Mu1_pt'+selvar)
                wtomu_cut_vec.push_back(wtomu_newcut)
                wtomu_var_vec.push_back(selvar)
                wtotau_cut_vec.push_back(wtotau_newcut)
                wtotau_var_vec.push_back(selvar)
                print "branching column variations:", vartype, " for region:", region, "\tvariations:", wtomu_var_vec
            if region == "Signal": 
                p.branch(nodeToStart = 'defs', nodeToEnd = '{}/prefit_{}/{}Vars'.format('WToMu', region,vartype), modules = [ROOT.muonHistos(wtomu_cut_vec, weight, nom,"Nom",hcat,wtomu_var_vec)])  
                p.branch(nodeToStart = 'defs', nodeToEnd = '{}/prefit_{}/{}Vars'.format('WToTau', region,vartype), modules = [ROOT.muonHistos(wtotau_cut_vec, weight, nom,"Nom",hcat,wtotau_var_vec)])
                #reco templates with AC reweighting
                steps = [ROOT.getACValues(fileAC),ROOT.defineHarmonics(),ROOT.getMassWeights(),ROOT.getWeights(),ROOT.templateBuilder(wtomu_cut_vec, weight, nom,"Nom",hcat,wtomu_var_vec)]
                p.branch(nodeToStart = 'defs', nodeToEnd = '{}/templatesAC_{}/{}Vars'.format('WToMu', region, vartype), modules = steps)
            #templates 
            p.branch(nodeToStart = 'defs', nodeToEnd = '{}/templates_{}/{}Vars'.format('WToMu', region,vartype), modules = [ROOT.templates(wtomu_cut_vec, weight, nom,"Nom",hcat,wtomu_var_vec)])  
            p.branch(nodeToStart = 'defs', nodeToEnd = '{}/templates_{}/{}Vars'.format('WToTau', region,vartype), modules = [ROOT.templates(wtotau_cut_vec, weight, nom,"Nom",hcat,wtotau_var_vec)])  

    p.getOutput()
    p.saveGraph()
   
    #if not pretendJob:
    #split the output file into decay modes
    os.chdir(outputDir)
    os.system("ls -ltrh")
    os.system("root -b -q ../python/splitWJets.C")
    os.chdir("../")


def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument('-p', '--pretend',type=int, default=False, help="run over a small number of event")
    parser.add_argument('-c', '--ncores',type=int, default=64, help="number of cores used")
    parser.add_argument('-o', '--outputDir',type=str, default='./output/', help="output dir name")
    parser.add_argument('-i', '--inputDir',type=str, default='/scratch/wmass/NanoAOD2016-V2/', help="input dir name")
    args = parser.parse_args()
    pretendJob = args.pretend
    ncores = args.ncores
    outputDir = args.outputDir
    inDir = args.inputDir
    if pretendJob:
        print "Running a test job over a few events"
    else:
        print "Running on full dataset"
    samples={}
    with open('data/samples_2016.json') as f:
        samples = json.load(f)
    sample='WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'
    print sample
    direc = samples[sample]['dir']
    xsec = samples[sample]['xsec']
    fvec=ROOT.vector('string')()
    for dirname,fname in direc.iteritems():
        ##check if file exists or not
        inputFile = '{}/{}/tree.root'.format(inDir, dirname)
        isFile = os.path.isfile(inputFile)  
        if not isFile:
            print inputFile, " does not exist"
            continue
        fvec.push_back(inputFile)
    if fvec.empty():
        print "No files found for directory:", samples[sample], " SKIPPING processing"
        sys.exit(1)
    print fvec 

    fileSF = ROOT.TFile.Open("data/ScaleFactors_OnTheFly.root")
    RDFprocessWJetsMC(fvec, outputDir, sample, xsec, fileSF, ncores, pretendJob)


if __name__ == "__main__":
    main()
