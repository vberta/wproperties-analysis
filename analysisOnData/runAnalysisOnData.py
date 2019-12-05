import os
import sys
import ROOT
from math import *

from RDFtree import *

sys.path.append('python/')

#from getLumiWeight import *

print "Loading shared library..."
ROOT.gSystem.Load('bin/libAnalysisOnData.so')

c=64
		
ROOT.ROOT.EnableImplicitMT(c)

print "Running with {} cores".format(c)

inputFile = '/scratch/sroychow/NanoAOD2016-V1MCFinal/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/tree.root'

cut_base = 'Vtype==0 ' + \
      '&& HLT_SingleMu24 '+ \
      '&& MET_filters==1 ' + \
      '&& nVetoElectrons==0 ' + \
      '&& Muon1_corrected_pt>25.0 ' + \
      '&& Muon1_corrected_MET_nom_mt>40.0'


weight_base = 'puWeight' + \
              '*lumiweight'
              #'Muon_Trigger_BCDEF_SF[Idx_mu1]*' + \
              #'Muon_ID_BCDEF_SF[Idx_mu1]*' + \
              #'Muon_ISO_BCDEF_SF[Idx_mu1]'

p = RDFtree(outputDir = 'TEST', inputFile = inputFile, outputFile="test.root")

pair_f = ROOT.pair('float','float')
pair_s = ROOT.pair('string','string')
era_ratios = pair_f(0.5, 0.5)
vec_s = ROOT.vector('string')

def branch_init(p, systs, start_weight):
    weight = copy.deepcopy(start_weight)
    modules = []
    modules.append( ROOT.getLumiWeight(inputFile, 35.9, 61526.7) )
    modules.append( ROOT.getVars("Idx_mu1", "Idx_mu2") )
    for syst in systs:
        modules.append( ROOT.mergeSystWeight(pair_s('Muon1_'+syst+'_BCDEF_SF', 'Muon1_'+syst+'_GH_SF'), era_ratios, 'Muon1_'+syst+'_SF', True) )
        weight += ('*Muon1_'+syst+'_SF')
    modules.append( ROOT.getWeight('weight_nominal', weight) )    
    p.branch(nodeToStart='input', nodeToEnd='defs', modules=modules)
    return start_weight, weight

def branch_Muon_nominal(p, start_weight):
    weight = copy.deepcopy(start_weight)
    modules = []
    modules.append( ROOT.muonHistos(cut_base, 'weight_nominal') )
    p.branch(nodeToStart='defs', nodeToEnd='muonHistos_nominal', modules=modules)
    return start_weight, weight

def branch_Muon_syst_SF(p, systs, start_weight):
    weights = []
    for syst in systs:
        weight = copy.deepcopy(start_weight)
        weight = weight.replace('*Muon1_'+syst+'_SF', '')
        weights.append(weight)
        modules = []    
        syst_columns = { 'BCDEF' : vec_s(), 'GH' : vec_s(), 'ALL' : vec_s()  }
        for key,item in syst_columns.items():
            for type in ['statUp', 'statDown', 'systUp', 'systDown']:
                syst_columns[key].push_back('Muon_'+syst+('_'+key if key!='ALL' else '')+'_SF'+type)                
            if key=='ALL': continue
            modules.append( ROOT.getSystWeight(syst_columns[key],'Muon1_'+syst+'_'+key+'_SFall') )
        modules.append( ROOT.mergeSystWeight(pair_s('Muon1_'+syst+'_BCDEF_SFall','Muon1_'+syst+'_GH_SFall'), era_ratios, 'Muon1_'+syst+'_SFall', False) )
        modules.append( ROOT.getWeight('weight_nominal_no'+syst, weight) )
        modules.append( ROOT.muonHistos(cut_base, 'weight_nominal_no'+syst, syst_columns['ALL'], 'Muon1_'+syst+'_SFall') )
        p.branch(nodeToStart='defs', nodeToEnd='muonHistos_'+syst, modules=modules)
    return start_weight, weights

def branch_Muon_syst_variable(p, var, systs, start_cut, start_weight):
    cuts = []
    weights = []
    modules = []    

    # these columns have to be created before running muonHistos
    if var=='corrected':
        for col in ['Muon_corrected_pt', 'Muon_corrected_MET_nom_mt', 'Muon_corrected_MET_nom_hpt']:    
            syst_columns = vec_s()
            for syst in systs:
                syst_columns.push_back( col.replace(var, syst) )
            modules.append( ROOT.getSystVar( syst_columns, col.replace('Muon', 'Muon1').replace(var, var+'All'), 'Idx_mu1', False ) )
    elif var=='nom':
        for col in ['Muon_corrected_MET_nom_mt', 'Muon_corrected_MET_nom_hpt']:
            syst_columns = vec_s()
            for syst in systs:
                syst_columns.push_back( col.replace(var, syst) )
            modules.append( ROOT.getSystVar( syst_columns, col.replace('Muon', 'Muon1').replace(var, var+'All'), 'Idx_mu1', False ) )
        for col in ['MET_nom_pt', 'MET_nom_phi']:
            syst_columns = vec_s()
            for syst in systs:
                syst_columns.push_back( col.replace(var, syst) )
            modules.append( ROOT.getSystVar( syst_columns, col.replace(var, var+'All'), '', True ) )
            
    # first case: the event cut is changed
    if var in start_cut:
        cut_clean = copy.deepcopy(start_cut)
        cut_clean_split = cut_clean.split(' && ')
        garbage = []
        for i in cut_clean_split:
            if var in i: garbage.append(i)
        for i in garbage:
            cut_clean = cut_clean.replace(i, '1')
        print('branch_Muon_syst_variable(): cut: '+start_cut+' -> '+cut_clean)
        cuts.append(cut_clean)
        weight_columns = vec_s()
        cut = copy.deepcopy(start_cut)
        for syst in systs:
            icut = cut.replace(var, syst)
            newcut = '('+icut+')*('+start_weight+')'
            print('branch_Muon_syst_variable(): '+'cut_'+syst+' = '+newcut)
            modules.append( ROOT.getWeight('cut_'+syst, newcut) )
            weight_columns.push_back('cut_'+syst)
            weights.append('cut_'+syst)
        modules.append( ROOT.getSystVar(weight_columns, 'cut_'+var+'All', '', True) )
        modules.append( ROOT.muonHistos( cut_clean, '', syst_columns, 'cut_'+var+'All', var, True ) )
    # second case: the event cut is unchanged
    else:
        modules.append( ROOT.muonHistos( start_cut, 'weight_nominal', syst_columns, '', var, False ) )

    p.branch(nodeToStart='defs', nodeToEnd='muonHistos_'+var, modules=modules)
    return start_cut, start_weight, cuts, weights

_, weight_init    = branch_init(p,['ISO', 'ID', 'Trigger'], weight_base)
_, weight_nominal = branch_Muon_nominal(p, weight_init)
_, weights_syst   = branch_Muon_syst_SF(p, ['ISO', 'ID', 'Trigger'], weight_nominal)
_, _, _, _        = branch_Muon_syst_variable(p, 'corrected', ['correctedUp','correctedDown'], cut_base, weight_nominal)
_, _, _, _        = branch_Muon_syst_variable(p, 'nom', ['jerUp','jerDown'], cut_base, weight_nominal)

#p.branch(nodeToStart = 'fakeRate', nodeToEnd = 'muonHistos_ISO', modules = [ROOT.getSystWeight(Muon_ISO_BCDEF_SF,'Muon_ISO_syst'), 
#                                                                            ROOT.muonHistos(cut, weight+'*FakeRate', Muon_ISO_BCDEF_SF,'Muon_ISO_syst')])

print 'Get output...'
p.getOutput()
#p.saveGraph()


