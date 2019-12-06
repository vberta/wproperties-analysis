import os
import sys
import ROOT
from math import *

from RDFtree import *

sys.path.append('python/')
from utils import *

print "Loading shared library..."
ROOT.gSystem.Load('bin/libAnalysisOnData.so')

pair_f = ROOT.pair('float','float')
pair_s = ROOT.pair('string','string')
era_ratios = pair_f(0.5, 0.5)
vec_s = ROOT.vector('string')

c = 64
		
ROOT.ROOT.EnableImplicitMT(c)

print "Running with {} cores".format(c)

def branch_init(p, systs, start_weight, category):
    weight = copy.deepcopy(start_weight)
    modules = []
    modules.append( ROOT.getLumiWeight(inputFile, 35.9, 61526.7) )
    modules.append( ROOT.getVars("Idx_mu1", "Idx_mu2") )
    for syst in systs:
        modules.append( ROOT.mergeSystWeight(pair_s('Muon1_'+syst+'_BCDEF_SF', 'Muon1_'+syst+'_GH_SF'), era_ratios, 'Muon1_'+syst+'_SF', True) )
        weight += ('*Muon1_'+syst+'_SF')
    modules.append( ROOT.getWeight('weight_'+category+'_nominal', weight) )    
    p.branch(nodeToStart='input', nodeToEnd='defs', modules=modules)
    return start_weight, weight

def branch_muon_nominal(p, start_weight, start_cut, category):
    weight = copy.deepcopy(start_weight)
    modules = []
    modules.append( ROOT.muonHistos(category, start_cut, 'weight_'+category+'_nominal') )
    p.branch(nodeToStart='defs', nodeToEnd=category+'_nominal', modules=modules)
    return start_weight, start_cut, weight

def branch_global_weight(p, var, systs, start_weight, start_cut, category):
    new_weight = copy.deepcopy(start_weight)
    new_weight_name = 'weight_'+category+'_nominal'
    modules = []
    # if var is in start_weight, remove it
    if var in start_weight:
        new_weight = new_weight.replace('*'+var, '')
        new_weight_name = 'weight_'+category+'_nominal_no'+var
        modules.append( ROOT.getWeight(new_weight_name, new_weight) )
    syst_columns = vec_s()
    for syst in systs:
        syst_columns.push_back(var+syst)
    modules.append( ROOT.getSystVar(syst_columns, var+'All', '', True ) )
    modules.append( ROOT.muonHistos(category, start_cut, new_weight_name , syst_columns, var+'All') )
    p.branch(nodeToStart='defs', nodeToEnd=category+'_'+var, modules=modules)
    return start_weight, start_cut, new_weight

def branch_LHE_weight(p, var, systs, start_weight, start_cut, category):
    modules = []
    syst_column_names = vec_s()
    for i in range(systs[0], systs[1]+1):
        syst_column_name = ''
        if var=='LHEScaleWeight':             
            syst_column_name = ROOT.string('LHEScaleWeight_'+str(get_LHEScaleWeight_meaning(i)))
        elif var=='LHEPdfWeight': 
            syst_column_name = ROOT.string('LHEPdfWeight_'+str(get_LHEPdfWeight_meaning(i)))
        syst_column_names.push_back(syst_column_name)
    syst_columns = vec_s()
    syst_columns.push_back(var)
    new_weight = var+'_'+str(systs[0])+'_'+str(systs[1])+'All'
    modules.append( ROOT.getSystWeight(syst_columns, new_weight, ROOT.std.pair('unsigned int','unsigned int')(systs[0], systs[1]) ) )
    modules.append( ROOT.muonHistos(category, start_cut, 'weight_'+category+'_nominal', syst_column_names, new_weight) )
    p.branch(nodeToStart='defs', nodeToEnd=category+'_'+var, modules=modules)
    return start_cut, start_weight, new_weight

def branch_muon_syst_scalefactor(p, systs, start_weight, start_cut, category):
    new_weights = []
    for syst in systs:
        weight = copy.deepcopy(start_weight)
        weight = weight.replace('*Muon1_'+syst+'_SF', '')
        new_weights.append(weight)
        modules = []    
        syst_columns = { 'BCDEF' : vec_s(), 'GH' : vec_s(), 'ALL' : vec_s()  }
        for key,item in syst_columns.items():
            for type in ['statUp', 'statDown', 'systUp', 'systDown']:
                syst_columns[key].push_back( 'Muon_'+syst+'_'+key+'_SF'+type if key!='ALL' else syst+'_'+type)                
            if key=='ALL': continue
            modules.append( ROOT.getSystWeight(syst_columns[key],'Muon1_'+syst+'_'+key+'_SFall', "Idx_mu1") )
        modules.append( ROOT.mergeSystWeight(pair_s('Muon1_'+syst+'_BCDEF_SFall','Muon1_'+syst+'_GH_SFall'), era_ratios, 'Muon1_'+syst+'_SFall', False) )
        modules.append( ROOT.getWeight('weight_'+category+'_nominal_no'+syst, weight) )
        modules.append( ROOT.muonHistos(category, start_cut, "weight_"+category+"_nominal_no"+syst, syst_columns['ALL'], "Muon1_"+syst+"_SFall") )
        p.branch(nodeToStart='defs', nodeToEnd=category+'_'+syst, modules=modules)
    return start_weight, start_cut, new_weights

def branch_muon_syst_variable(p, var, systs, start_cut, start_weight, category):
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

    # reset syst names to contain the actual variations
    syst_columns = vec_s()
    for syst in systs:
        syst_columns.push_back( syst )
            
    # first case: the event cut is changed
    if var in start_cut:
        cut_clean = copy.deepcopy(start_cut)
        cut_clean_split = cut_clean.split(' && ')
        garbage = []
        for i in cut_clean_split:
            if var in i: garbage.append(i)
        for i in garbage:
            cut_clean = cut_clean.replace(i, '1')
        #print('branch_muon_syst_variable(): cut: '+start_cut+' -> '+cut_clean)
        cuts.append(cut_clean)
        weight_columns = vec_s()
        cut = copy.deepcopy(start_cut)
        for syst in systs:
            icut = cut.replace(var, syst)
            newcut = '('+icut+')*('+start_weight+')'
            #print('branch_muon_syst_variable(): '+'cut_'+syst+' = '+newcut)
            modules.append( ROOT.getWeight('cut_'+syst, newcut) )
            weight_columns.push_back('cut_'+syst)
            weights.append('cut_'+syst)
        modules.append( ROOT.getSystVar(weight_columns, 'cut_'+var+'All', '', True) )
        modules.append( ROOT.muonHistos(category, cut_clean, "", syst_columns, "cut_"+var+"All", var, True ) )

    # second case: the event cut is unchanged
    else:
        modules.append( ROOT.muonHistos(category, start_cut, "weight_"+category+"_nominal", syst_columns, "", var, False ) )
    p.branch(nodeToStart='defs', nodeToEnd=category+'_'+var, modules=modules)
    return start_cut, start_weight, cuts, weights

###################################################################################

inputFile = '/scratch/sroychow/NanoAOD2016-V1MCFinal/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/tree.root'

categories = { 
    'SIGNAL': {
        'weight_base' : 'puWeight*lumiweight',
        'cut_base' : 'Vtype==0 ' + \
        '&& HLT_SingleMu24 '+ \
        '&& MET_filters==1 ' + \
        '&& nVetoElectrons==0 ' + \
        '&& Muon1_corrected_pt>25.0 ' + \
        '&& Muon1_corrected_MET_nom_mt>40.0',
    },    
    #'QCD': {
    #    'weight_base' : 'puWeight*lumiweight',
    #    'cut_base' : 'Vtype==1 ' + \
    #    '&& HLT_SingleMu24 '+ \
    #    '&& MET_filters==1 ' + \
    #    '&& nVetoElectrons==0 ' + \
    #    '&& Muon1_corrected_pt>25.0 ' + \
    #    '&& Muon1_corrected_MET_nom_mt>40.0',
    #},
}

p = RDFtree(outputDir = 'test', inputFile = inputFile, outputFile="out.root")

for category,specifics in categories.items():  
    _,  weight_init    = branch_init(p,['ISO', 'ID', 'Trigger'], specifics['weight_base'], category)
    _,_,weight_nominal = branch_muon_nominal(p, weight_init, specifics['cut_base'], category)
    _,_,_              = branch_global_weight(p, 'puWeight', ['Up', 'Down'], weight_nominal, specifics['cut_base'], category)
    _,_,_              = branch_muon_syst_scalefactor(p, ['ISO', 'ID', 'Trigger'],    weight_nominal, specifics['cut_base'], category)
    _,_,_,_            = branch_muon_syst_variable(p, 'corrected', ['correctedUp','correctedDown'], specifics['cut_base'], weight_nominal, category)
    _,_,_,_            = branch_muon_syst_variable(p, 'nom', ['jerUp','jerDown','jesTotalUp','jesTotalDown','unclustEnUp','unclustEnDown'], specifics['cut_base'], weight_nominal, category)
    _,_,_              = branch_LHE_weight(p, 'LHEScaleWeight', [0,8],       weight_nominal, specifics['cut_base'], category)
    _,_,_              = branch_LHE_weight(p, 'LHEPdfWeight',   [0,101],     weight_nominal, specifics['cut_base'], category)


print 'Get output...'
p.getOutput()
#p.saveGraph()


