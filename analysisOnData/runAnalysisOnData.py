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

def branch_defs(p, weight, category, extra_modules, round):
    modules = []
    def_modules = []
    if round==0:
        def_modules.append( ROOT.getLumiWeight(inputFile, 35.9, 61526.7) )
        def_modules.append( ROOT.getVars("Idx_mu1", "Idx_mu2") )
        for syst in ['ISO', 'ID', 'Trigger']:
            def_modules.append( ROOT.mergeSystWeight(pair_s('Muon1_'+syst+'_BCDEF_SF', 'Muon1_'+syst+'_GH_SF'), era_ratios, 'Muon1_'+syst+'_SF', True, False) )
            def_modules.append( ROOT.mergeSystWeight(pair_s('Muon2_'+syst+'_BCDEF_SF', 'Muon2_'+syst+'_GH_SF'), era_ratios, 'Muon2_'+syst+'_SF', True, False) )
    elif round==1:
        def_modules.append( ROOT.getWeight('weight_'+category+'_nominal', weight) )    
    elif round==2:
        def_modules.extend(extra_modules)
        p.branch(nodeToStart='input', nodeToEnd='defs', modules=def_modules)
    return def_modules

def branch_muon_nominal(p, cut, category, round):
    modules = []
    def_modules = []
    if round==0:
        pass
    elif round==1:
        pass
    elif round==2:
        modules.append( ROOT.muonHistos(category, cut, 'weight_'+category+'_nominal') )
        p.branch(nodeToStart='defs', nodeToEnd=category+'_nominal', modules=modules)
    return def_modules

def branch_event_syst_weight(p, var, systs, weight, cut, category, round):
    modules = []
    def_modules = []
    weight_clean = copy.deepcopy(weight) 
    weight_clean_name = 'weight_'+category+'_nominal'
    syst_columns = vec_s()
    for syst in systs: syst_columns.push_back(var+syst)

    if round==0:
        def_modules.append( ROOT.getSystVar(syst_columns, var+'All', '', True ) )
    elif round==1:
        # if var is in start_weight, remove it
        if var in weight:
            weight_clean = weight.replace('*'+var, '')
            weight_clean_name = 'weight_'+category+'_nominal_no'+var        
            def_modules.append( ROOT.getWeight(weight_clean_name, weight_clean) )
    elif round==2:
        modules.append( ROOT.muonHistos(category, cut, weight_clean_name , syst_columns, var+'All') )
        p.branch(nodeToStart='defs', nodeToEnd=category+'_'+var, modules=modules)
    return def_modules

def branch_LHE_weight(p, var, systs, weight, cut, category, round):
    modules = []
    def_modules = []
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
    new_weight_name = var+'_'+str(systs[0])+'_'+str(systs[1])+'All'
    if round==0:
        def_modules.append( ROOT.getSystWeight(syst_columns, new_weight_name, ROOT.std.pair('unsigned int','unsigned int')(systs[0], systs[1]) ) )
    elif round==1:
        pass
    elif round==2:
        modules.append( ROOT.muonHistos(category, cut, 'weight_'+category+'_nominal', syst_column_names, new_weight_name) )
        p.branch(nodeToStart='defs', nodeToEnd=category+'_'+var, modules=modules)
    return def_modules

def branch_muon_syst_scalefactor(p, systs, weight, cut, category, round):
    modules = []
    def_modules = []
    for syst in systs:
        weight_clean = copy.deepcopy(weight)
        weight_clean = weight_clean.replace('*Muon1_'+syst+'_SF', '')
        weight_clean = weight_clean.replace('*Muon2_'+syst+'_SF', '')
        weight_clean_name = 'weight_'+category+'_nominal_no'+syst
        modules = []    
        syst_columns = { 'BCDEF' : vec_s(), 'GH' : vec_s(), 'ALL' : vec_s()  }
        for key,item in syst_columns.items():
            for type in ['statUp', 'statDown', 'systUp', 'systDown']:
                syst_columns[key].push_back( 'Muon_'+syst+'_'+key+'_SF'+type if key!='ALL' else syst+'_'+type)                
            if key=='ALL': continue
            if round==0:
                def_modules.append( ROOT.getSystWeight(syst_columns[key],'Muon1_'+syst+'_'+key+'_SFall', "Idx_mu1") )
                def_modules.append( ROOT.getSystWeight(syst_columns[key],'Muon2_'+syst+'_'+key+'_SFall', "Idx_mu2") )
        if round==0:
            def_modules.append( ROOT.mergeSystWeight(pair_s('Muon1_'+syst+'_BCDEF_SFall','Muon1_'+syst+'_GH_SFall'), era_ratios, 'Muon1_'+syst+'_SFall', False, False) )        
            def_modules.append( ROOT.mergeSystWeight(pair_s('Muon2_'+syst+'_BCDEF_SFall','Muon2_'+syst+'_GH_SFall'), era_ratios, 'Muon2_'+syst+'_SFall', False, False) )                        
            def_modules.append( ROOT.mergeSystWeight(pair_s('Muon1_'+syst+'_SFall','Muon2_'+syst+'_SFall'), pair_f(1.0,1.0), 'Muon12_'+syst+'_SFall', False, True) ) 
        elif round==1:
            def_modules.append( ROOT.getWeight(weight_clean_name, weight_clean) )
        elif round==2:
            if category=='DIMUON':
                modules.append( ROOT.muonHistos(category, cut, weight_clean_name, syst_columns['ALL'], "Muon12_"+syst+"_SFall") )
            else:
                modules.append( ROOT.muonHistos(category, cut, weight_clean_name, syst_columns['ALL'], "Muon1_"+syst+"_SFall") )
            p.branch(nodeToStart='defs', nodeToEnd=category+'_'+syst, modules=modules)
    return def_modules

def branch_muon_syst_column(p, var, systs, cut, weight, category, round):
    modules = []    
    def_modules = []
    if round==0:
        if var=='corrected':
            for col in ['Muon_corrected_pt', 'Muon_corrected_MET_nom_mt', 'Muon_corrected_MET_nom_hpt']:    
                syst_columns = vec_s()
                for syst in systs:
                    syst_columns.push_back( col.replace(var, syst) )            
                def_modules.append( ROOT.getSystVar( syst_columns, col.replace('Muon', 'Muon1').replace(var, var+'All'), 'Idx_mu1', False ) )
                def_modules.append( ROOT.getSystVar( syst_columns, col.replace('Muon', 'Muon2').replace(var, var+'All'), 'Idx_mu2', False ) )
        elif var=='nom':
            for col in ['Muon_corrected_MET_nom_mt', 'Muon_corrected_MET_nom_hpt']:
                syst_columns = vec_s()
                for syst in systs:
                    syst_columns.push_back( col.replace(var, syst) )
                def_modules.append( ROOT.getSystVar( syst_columns, col.replace('Muon', 'Muon1').replace(var, var+'All'), 'Idx_mu1', False ) )
                def_modules.append( ROOT.getSystVar( syst_columns, col.replace('Muon', 'Muon2').replace(var, var+'All'), 'Idx_mu2', False ) )
            for col in ['MET_nom_pt', 'MET_nom_phi']:
                syst_columns = vec_s()
                for syst in systs:
                    syst_columns.push_back( col.replace(var, syst) )
                def_modules.append( ROOT.getSystVar( syst_columns, col.replace(var, var+'All'), '', True ) )
        return def_modules

    # reset syst names to contain the actual variations
    syst_columns = vec_s()
    for syst in systs: syst_columns.push_back( syst )
            
    # first case: the event cut is changed
    if var in cut:
        # remove var-dependent variables from 'cut' -> 'cut_clean'
        cut_clean = copy.deepcopy(cut)
        cut_clean_split = cut_clean.split(' && ')
        garbage = []
        for i in cut_clean_split: 
            if var in i: garbage.append(i)
        for i in garbage: cut_clean = cut_clean.replace(i, '1')
        cut_removed = '1'
        for i in garbage: cut_removed += (' && '+i)
        #print('branch_muon_syst_column(): cut: '+cut+' -> '+cut_clean)
        # create new weights that contain the cut on var-dependent variables * weight
        if round==1:
            weight_columns = vec_s()
            for syst in systs:
                cut_syst = cut_removed.replace(var, syst)
                weight_cut_syst = '('+cut_syst+')*('+weight+')'
                weight_cut_syst_name = 'weight_'+category+'_cut_'+var+'_'+syst
                #print('branch_muon_syst_column(): '+weight_cut_syst_name+' = '+weight_cut_syst)
                def_modules.append( ROOT.getWeight(weight_cut_syst_name, weight_cut_syst) )
                weight_columns.push_back(weight_cut_syst_name)
            def_modules.append( ROOT.getSystVar(weight_columns, 'weight_'+category+'_cut_'+var+'All', '', True) )
            return def_modules
        elif round==2:
            modules.append( ROOT.muonHistos(category, cut_clean, "", syst_columns, 'weight_'+category+'_cut_'+var+'All', var, True ) )
            p.branch(nodeToStart='defs', nodeToEnd=category+'_'+var, modules=modules)

    # second case: the event cut is unchanged
    else:
        if round==1:
            return def_modules
        elif round==2:
            modules.append( ROOT.muonHistos(category, cut, "weight_"+category+"_nominal", syst_columns, "", var, False ) )
            p.branch(nodeToStart='defs', nodeToEnd=category+'_'+var, modules=modules)

    return def_modules

###################################################################################

inputFile = '/scratch/sroychow/NanoAOD2016-V1MCFinal/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext2/tree.root'
#'/scratch/sroychow/NanoAOD2016-V1MCFinal/TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1/tree.root'
#'/scratch/sroychow/NanoAOD2016-V1MCFinal/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/tree.root'

categories = { 
    'SIGNAL': {
        'weight' : 'puWeight*lumiweight*Muon1_ID_SF*Muon1_ISO_SF*Muon1_Trigger_SF',
        'cut' : 'Vtype==0 ' + \
        '&& HLT_SingleMu24 '+ \
        '&& MET_filters==1 ' + \
        '&& nVetoElectrons==0 ' + \
        '&& Muon1_corrected_pt>25.0 ' + \
        '&& Muon1_corrected_MET_nom_mt>40.0 ',
    },    
    'QCD': {
        'weight' : 'puWeight*lumiweight*Muon1_ID_SF*Muon1_ISO_SF*Muon1_Trigger_SF',
        'cut' : 'Vtype==1 ' + \
        '&& HLT_SingleMu24 '+ \
        '&& MET_filters==1 ' + \
        '&& nVetoElectrons==0 ' + \
        '&& Muon1_corrected_pt>25.0 ' + \
        '&& Muon1_corrected_MET_nom_mt<40.0 ',
    },
    'DIMUON': {
        'weight' : 'puWeight*lumiweight*Muon1_ID_SF*Muon1_ISO_SF*Muon1_Trigger_SF*Muon2_ID_SF*Muon2_ISO_SF*Muon2_Trigger_SF',
        'cut' : 'Vtype==2 ' + \
        '&& HLT_SingleMu24 '+ \
        '&& MET_filters==1 ' + \
        '&& nVetoElectrons==0 ' + \
        '&& Muon1_corrected_pt>25.0 ' + \
        '&& Muon2_corrected_pt>25.0 ',
    },
}

p = RDFtree(outputDir = 'test', inputFile = inputFile, outputFile="out.root")

isMC = True
if not isMC:
    for category,specifics in categories.items(): specifics['weight'] = 'Float_t(1.0)'

# FIRST PASS:  collect all GLOBAL defs (run on first category only)
# SECOND PASS: collect all CATEGORY defs        
# THIRD PASS:  run the histograms
def_modules = []
for round in [0,1,2]:
    print "Running pass...", round
    n_cat = 0
    for category,specifics in categories.items():  
        #if category!='SIGNAL': continue
        weight,cut = specifics['weight'], specifics['cut']
        #print "Doing category..."+category
        if round==0 and n_cat>0: continue
        if round<2 or (round==2 and n_cat==0): def_modules.extend(branch_defs(p, weight, category, def_modules, round ))
        def_modules.extend(branch_muon_nominal(p, cut, category, round))
        if not isMC:
            n_cat += 1
            continue
        def_modules.extend(branch_event_syst_weight(p, 'puWeight', ['Up', 'Down'], weight, cut, category, round))
        def_modules.extend(branch_muon_syst_scalefactor(p, ['ISO', 'ID', 'Trigger'], weight, cut, category, round))
        def_modules.extend(branch_muon_syst_column(p, 'corrected', ['correctedUp','correctedDown'], cut, weight, category,round))
        def_modules.extend(branch_muon_syst_column(p, 'nom', ['jerUp','jerDown','jesTotalUp','jesTotalDown','unclustEnUp','unclustEnDown'], cut, weight, category,round))
        def_modules.extend(branch_LHE_weight(p, 'LHEScaleWeight', [0,8], weight, cut, category, round))
        def_modules.extend(branch_LHE_weight(p, 'LHEPdfWeight',   [90,101], weight, cut, category,round))
        n_cat += 1 
    print " ==>", len(def_modules), " defs modules have been loaded..."

print 'Get output...'
p.getOutput()
#p.saveGraph()


