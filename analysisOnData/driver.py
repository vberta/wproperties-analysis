import os
import sys
import ROOT
from math import *

sys.path.append('python/')
from configRDF import *

print "Loading shared library..."
ROOT.gSystem.Load('bin/libAnalysisOnData.so')

c = 64		

ROOT.ROOT.EnableImplicitMT(c)

print "Running with {} cores".format(c)

inputFile   = '/scratch/sroychow/NanoAOD2016-V1MCFinal/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/tree.root'
inputSample = 'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'

#inputFile   = '/scratch/sroychow/NanoAOD2016-V1MCFinal/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext2/tree.root'
#inputSample = 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext2'

config = ConfigRDF(inputFile, 'test', inputSample+'.root')
config.set_sample_specifics(isMC=True, lumi=35.9, xsec=61526.7, dataYear='2016', era_ratios=[0.5,0.5])

categories = { 
    'SIGNAL': {
        'weight' : 'puWeight*lumiweight*SelMuon1_ID_SF*SelMuon1_ISO_SF*SelMuon1_Trigger_SF',
        'cut' : 'Vtype==0 ' + \
        '&& HLT_SingleMu24 '+ \
        '&& MET_filters==1 ' + \
        '&& nVetoElectrons==0 ' + \
        '&& SelMuon1_corrected_pt>25.0 ' + \
        '&& SelMuon1_corrected_MET_nom_mt>40.0 ',
        'modules' : {
            'muon_nominal' : [],
            'event_syst_puWeight' : ['Up', 'Down'],
            'muon_syst_scalefactor_ID' : [],
            'muon_syst_scalefactor_ISO' : [],
            'muon_syst_scalefactor_Trigger' : [],
            'muon_syst_column_corrected' : ['correctedUp','correctedDown'],
            'muon_syst_column_nom' : ['jerUp','jerDown','jesTotalUp','jesTotalDown','unclustEnUp','unclustEnDown'],
            'event_syst_LHEScaleWeight' : [0,8],
            'event_syst_LHEPdfWeight' : [98,101],
            },
    },    
    'QCD': {
        'weight' : 'puWeight*lumiweight*SelMuon1_ID_SF*SelMuon1_ISO_SF*SelMuon1_Trigger_SF',
        'cut' : 'Vtype==1 ' + \
        '&& HLT_SingleMu24 '+ \
        '&& MET_filters==1 ' + \
        '&& nVetoElectrons==0 ' + \
        '&& SelMuon1_corrected_pt>25.0 ' + \
        '&& SelMuon1_corrected_MET_nom_mt<40.0 ',
        'modules' : {
            'muon_nominal' : [],
            'event_syst_puWeight' : ['Up', 'Down'],
            'muon_syst_scalefactor_ID' : [],
            'muon_syst_scalefactor_ISO' : [],
            'muon_syst_scalefactor_Trigger' : [],
            'muon_syst_column_corrected' : ['correctedUp','correctedDown'],
            'muon_syst_column_nom' : ['jerUp','jerDown','jesTotalUp','jesTotalDown','unclustEnUp','unclustEnDown'],
            },
    },
    'DIMUON': {
        'weight' : 'puWeight*lumiweight*SelMuon1_ID_SF*SelMuon1_ISO_SF*SelMuon1_Trigger_SF*SelMuon2_ID_SF*SelMuon2_ISO_SF*SelMuon2_Trigger_SF',
        'cut' : 'Vtype==2 ' + \
        '&& HLT_SingleMu24 '+ \
        '&& MET_filters==1 ' + \
        '&& nVetoElectrons==0 ' + \
        '&& SelMuon1_corrected_pt>25.0 ' + \
        '&& SelMuon2_corrected_pt>25.0 ',
        'modules' : {
            'muon_nominal' : [],
            'event_syst_puWeight' : ['Up', 'Down'],
            'muon_syst_scalefactor_ID' : [],
            'muon_syst_scalefactor_ISO' : [],
            'muon_syst_scalefactor_Trigger' : [],
            'muon_syst_column_corrected' : ['correctedUp','correctedDown'],
            'muon_syst_column_nom' : ['jerUp','jerDown','jesTotalUp','jesTotalDown','unclustEnUp','unclustEnDown'],
            },
        },
    }

categories['SIGNAL']['modules'] = {'muon_nominal':[]}
del categories['DIMUON']
del categories['QCD']
print categories

config.run( categories )
