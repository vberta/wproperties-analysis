import os
import sys
import ROOT
import json

from RDFtree import RDFtree
sys.path.append('python/')
sys.path.append('data/')
from systematics import systematics

from selections import selections, selections_bkg, selections_fakes, selectionVars
from getLumiWeight import getLumiWeight

ROOT.gSystem.Load('bin/libAnalysisOnData.so')

pretendJob = True if int(sys.argv[2]) == 1 else False
if pretendJob:
    print "Running a test job over a few events"
else:
    print "Running on full dataset"

runBKG = True if int(sys.argv[1]) == 1 else False 
outF="SingleMuonData_plots.root"
if runBKG:
    selections = selections_bkg
    outF="SingleMuonData_bkginput_plots.root"
    print "Running job for preparing inputs of background study"

fvec=ROOT.vector('string')()

samples={}
with open('data/samples_2016.json') as f:
  samples = json.load(f)
for sample in samples:
    if not samples[sample]['datatype']=='DATA': continue
    #print sample
    direc = samples[sample]['dir']
    for dirname,fname in direc.iteritems():
        ##check if file exists or not
        inputFile = '/scratchssd/sroychow/NanoAOD2016-V2/{}/tree.root'.format(dirname)
        isFile = os.path.isfile(inputFile)  
        if not isFile:
            print inputFile, " does not exist"
            continue
        fvec.push_back(inputFile)
        #print inputFile

if fvec.empty():
    print "No files found for json provided\n"
    sys.exit(1)
    
print fvec
c = 64		
ROOT.ROOT.EnableImplicitMT(c)
print "running with {} cores".format(c)

weight = 'float(1)'
p = RDFtree(outputDir = './output/', inputFile = fvec, outputFile=outF, pretend=pretendJob)
p.branch(nodeToStart = 'input', nodeToEnd = 'defs', modules = [ROOT.baseDefinitions(0)])

for region,cut in selections.iteritems():    
    print region       
    nom = ROOT.vector('string')()
    nom.push_back("")
    #last argument refers to histo category - 0 = Nominal, 1 = Pt scale , 2 = MET scale
    print "branching nominal"
    p.branch(nodeToStart = 'defs', nodeToEnd = 'prefit_{}/Nominal'.format(region), modules = [ROOT.muonHistos(cut, weight, nom,"Nom",0)]) 
    p.branch(nodeToStart = 'defs', nodeToEnd = 'templates_{}/Nominal'.format(region), modules = [ROOT.templates(cut, weight, nom,"Nom",0)])       

if not runBKG:
    FR = ROOT.TFile.Open("/scratch/bertacch/wmass/wproperties-analysis/bkgAnalysis/BKG_syst_WHSF_20July/bkg_parameters_CFstatAna.root")
    for region,cut in selections_fakes.iteritems():    
        print region       
        nom = ROOT.vector('string')()
        nom.push_back("")
        weight = "float(fakeRate)"
        #last argument refers to histo category - 0 = Nominal, 1 = Pt scale , 2 = MET scale
        print "branching nominal"
        p.branch(nodeToStart = 'defs', nodeToEnd = 'prefit_{}/Nominal'.format(region), modules = [ROOT.fakeRate(FR),ROOT.muonHistos(cut, weight, nom,"Nom",0)]) 
        p.branch(nodeToStart = 'defs', nodeToEnd = 'templates_{}/Nominal'.format(region), modules = [ROOT.fakeRate(FR),ROOT.templates(cut, weight, nom,"Nom",0)])       

        #now add fake variations
        for s,variations in systematics.iteritems():
            print "branching weight variations", s
            weight = 'float(1)'

            vars_vec = ROOT.vector('string')()
            for var in variations[0]:
                vars_vec.push_back(var)

            if not runBKG: p.branch(nodeToStart = 'defs'.format(region), nodeToEnd = 'prefit_{}/{}Vars'.format(region,s), modules = [ROOT.muonHistos(cut,weight,vars_vec,"fakeRate_"+variations[1], 0)])
            p.branch(nodeToStart = 'defs'.format(region), nodeToEnd = 'templates_{}/{}Vars'.format(region,s), modules = [ROOT.templates(cut,weight,vars_vec,"fakeRate_"+variations[1], 0)])
        
        #column variations#weight will be nominal, cut will vary
        for vartype, vardict in selectionVars.iteritems():
            cut_vec = ROOT.vector('string')()
            var_vec = ROOT.vector('string')()
            for selvar, hcat in vardict.iteritems() :
                newcut = cut.replace('MT', 'MT_'+selvar)
                if 'corrected' in selvar:
                    newcut = newcut.replace('Mu1_pt', 'Mu1_pt_'+selvar)
                
                weight = "float(fakeRate"+"_{})".format(selvar)

                cut_vec.push_back(newcut)
                var_vec.push_back(selvar)

            if not runBKG: p.branch(nodeToStart = 'defs', nodeToEnd = 'prefit_{}/{}Vars'.format(region,vartype), modules = [ROOT.muonHistos(cut_vec, weight, nom,"Nom",hcat,var_vec)])  
            p.branch(nodeToStart = 'defs', nodeToEnd = 'templates_{}/{}Vars'.format(region,vartype), modules = [ROOT.templates(cut_vec, weight, nom,"Nom",hcat,var_vec)])  

p.getOutput()
p.saveGraph()



