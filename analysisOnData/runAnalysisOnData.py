import os
import sys
import ROOT
import json
import argparse

from RDFtree import RDFtree
sys.path.append('python/')
sys.path.append('data/')
from systematics import systematics
from selections import selections, selections_bkg, selections_fakes, selectionVars
from getLumiWeight import getLumiWeight
ROOT.gSystem.Load('bin/libAnalysisOnData.so')

#produces templates for all regions and prefit for signal
def RDFprocessData(fvec, outputDir, ncores, pretendJob=True, SBana=False, outF="SingleMuonData_plots.root"):
    ROOT.ROOT.EnableImplicitMT(ncores)
    print "running with {} cores".format(ncores)
    weight = 'float(1)'
    outF="SingleMuonData_plots.root"
    p = RDFtree(outputDir = outputDir, inputFile = fvec, outputFile=outF, pretend=pretendJob)
    p.branch(nodeToStart = 'input', nodeToEnd = 'defs', modules = [ROOT.baseDefinitions(0)])
    for region,cut in selections_bkg.iteritems():    
        print region       
        nom = ROOT.vector('string')()
        nom.push_back("")
        #last argument refers to histo category - 0 = Nominal, 1 = Pt scale , 2 = MET scale
        print "branching nominal"
        #if region == "Signal" or (region=='Sideband' and SBana):
        #    p.branch(nodeToStart = 'defs', nodeToEnd = 'prefit_{}/Nominal'.format(region), modules = [ROOT.muonHistos(cut, weight, nom,"Nom",0)]) 
        #nominal templates
        p.branch(nodeToStart = 'defs', nodeToEnd = 'templates_{}/Nominal'.format(region), modules = [ROOT.templates(cut, weight, nom,"Nom",0)])       
    p.getOutput()
    p.saveGraph()

#produces Fake contribution to prefit plots computed from data 
def RDFprocessfakefromData(fvec, outputDir, bkgFile, ncores, pretendJob=True, SBana=False, outF="FakeFromData_plots.root"):
    ROOT.ROOT.EnableImplicitMT(ncores)
    print "running with {} cores".format(ncores)
    weight = 'float(1)'
    #in case we want pdf variations for fakes
    #systematics.update({ "LHEPdfWeight" : ( ["_LHEPdfWeight" + str(i)  for i in range(0, 100)], "LHEPdfWeight" ) } )
    #print systematics
    p = RDFtree(outputDir = outputDir, inputFile = fvec, outputFile=outF, pretend=pretendJob)
    for region,cut in selections_fakes.iteritems(): 
        if 'SideBand' in region and (not SBana) : continue 
        if 'SideBand' in region : bkgFile_mod = bkgFile.replace('.root','SideBand.root') 
        else :  bkgFile_mod=bkgFile
        FR=ROOT.TFile.Open(bkgFile_mod)
        p.branch(nodeToStart = 'input', nodeToEnd = 'defs', modules = [ROOT.baseDefinitions(0),ROOT.fakeRate(FR)]) 
        print region       
        nom = ROOT.vector('string')()
        nom.push_back("")
        weight = "float(fakeRate_Nominal_)"
        #last argument refers to histo category - 0 = Nominal, 1 = Pt scale , 2 = MET scale
        print "branching nominal"
        p.branch(nodeToStart = 'defs', nodeToEnd = 'prefit_{}/Nominal'.format(region), modules = [ROOT.muonHistos(cut, weight, nom,"Nom",0)]) 
        p.branch(nodeToStart = 'defs', nodeToEnd = 'templates_{}/Nominal'.format(region), modules = [ROOT.templates(cut, weight, nom,"Nom",0)])       

        #now add fake variations
        for s,variations in systematics.iteritems():
            #only required systs
            if "LHEPdfWeight" not in s and "LHEScaleWeight" not in s: continue
            print "branching weight variations", s
            vars_vec = ROOT.vector('string')()
            for var in variations[0]:
                vars_vec.push_back(var)
                weight="float(1)"
            print "fakeRate_"+variations[1]
            print vars_vec
            p.branch(nodeToStart = 'defs'.format(region), nodeToEnd = 'prefit_{}/{}'.format(region,s), modules = [ROOT.muonHistos(cut,weight,vars_vec,"fakeRate_"+variations[1], 0)])
            p.branch(nodeToStart = 'defs'.format(region), nodeToEnd = 'templates_{}/{}'.format(region,s), modules = [ROOT.templates(cut,weight,vars_vec,"fakeRate_"+variations[1], 0)])
        
        #fake column variations since the cut won't change in data
        for vartype, vardict in selectionVars.iteritems():
            if vartype != 'jme' : continue
            vars_vec = ROOT.vector('string')()
            for selvar, hcat in vardict.iteritems() :
                vars_vec.push_back(selvar)
            print "branching fake column variations", vartype
            p.branch(nodeToStart = 'defs'.format(region), nodeToEnd = 'prefit_{}/{}'.format(region,vartype), modules = [ROOT.muonHistos(cut,weight,vars_vec,"fakeRate_"+vartype, 0)])
            p.branch(nodeToStart = 'defs'.format(region), nodeToEnd = 'templates_{}/{}'.format(region,vartype), modules = [ROOT.templates(cut,weight,vars_vec,"fakeRate_"+vartype, 0)])

    #save output
    p.getOutput()
    p.saveGraph()

def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument('-p', '--pretend',type=bool, default=False, help="run over a small number of event")
    parser.add_argument('-b', '--runBKG',type=bool, default=False, help="prepare the input of the bkg analysis, if =false run the prefit Plots")
    parser.add_argument('-c', '--ncores',type=int, default=64, help="number of cores used")
    parser.add_argument('-o', '--outputDir',type=str, default='./output/', help="output dir name")
    parser.add_argument('-f', '--bkgFile',type=str, default='/scratch/bertacch/wmass/wproperties-analysis/bkgAnalysis/TEST_runTheMatrix/bkg_parameters_CFstatAna.root', help="bkg parameters file path/name.root")
    parser.add_argument('-i', '--inputDir',type=str, default='/scratchssd/sroychow/NanoAOD2016-V2/', help="input dir name")
    parser.add_argument('-s', '--SBana',type=bool, default=False, help="run also on the sideband (clousure test)")

    args = parser.parse_args()
    pretendJob = args.pretend
    runBKG = args.runBKG
    ncores = args.ncores
    outputDir = args.outputDir
    bkgFile = args.bkgFile
    inDir = args.inputDir
    SBana = args.SBana
    if pretendJob:
        print "Running a test job over a few events"
    else:
        print "Running on full dataset"
    fvec=ROOT.vector('string')()
    samples={}
    with open('data/samples_2016.json') as f:
        samples = json.load(f)
    for sample in samples:
        if not samples[sample]['datatype']=='DATA': continue
        direc = samples[sample]['dir']
        for dirname,fname in direc.iteritems():
            ##check if file exists or not
            inputFile = '{}/{}/tree.root'.format(inDir, dirname)
            isFile = os.path.isfile(inputFile)  
            if not isFile:
                print inputFile, " does not exist"
                continue
            fvec.push_back(inputFile)
        
    if fvec.empty():
        print "No files found for json provided\n"
        sys.exit(1)
    print fvec
    if runBKG : #produces templates for all regions and prefit for signal
        RDFprocessData(fvec, outputDir, ncores, pretendJob,SBana)
    else : #produces Fake contribution to prefit plots computed from data 
        RDFprocessfakefromData(fvec, outputDir, bkgFile, ncores, pretendJob,SBana)

if __name__ == "__main__":
    main()
