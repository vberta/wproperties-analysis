import os
import sys
import ROOT
from math import *

from RDFtree import *

sys.path.append('python/')
from utils import *

print "Loading shared library..."
ROOT.gSystem.Load('bin/libAnalysisOnData.so')

pair_f  = ROOT.pair('float','float')
pair_s  = ROOT.pair('string','string')
pair_ui = ROOT.std.pair('unsigned int','unsigned int')
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
            def_modules.append( ROOT.mergeSystWeight(pair_s('Muon1_'+syst+'_BCDEF_SF', 'Muon1_'+syst+'_GH_SF'), 
                                                     era_ratios, 'Muon1_'+syst+'_SF', "f,f->af+bf") )
            def_modules.append( ROOT.mergeSystWeight(pair_s('Muon2_'+syst+'_BCDEF_SF', 'Muon2_'+syst+'_GH_SF'), 
                                                     era_ratios, 'Muon2_'+syst+'_SF', "f,f->af+bf") )
    elif round==1:
        def_modules.append( ROOT.getWeight('weight_'+category+'_nominal', weight) )    
    elif round==2:
        def_modules.extend(extra_modules)
        p.branch(nodeToStart='input', nodeToEnd='defs', modules=def_modules)
        def_modules = []
    return def_modules

def branch_muon_nominal(p, cut, category, round):
    modules = []
    def_modules = []
    if round==0:
        pass
    elif round==1:
        pass
    elif round==2:
        modules.append( ROOT.getFilter(cut) )
        modules.append( ROOT.muonHistos(category, 'weight_'+category+'_nominal', vec_s(), "", "", False) )
        p.branch(nodeToStart='defs', nodeToEnd=category+'_nominal', modules=modules)
    return def_modules

def branch_event_syst_weight(p, var, systs, weight, cut, category, round):
    modules = []
    def_modules = []
    syst_columns = vec_s()
    for syst in systs: syst_columns.push_back(var+syst)
    if round==0:
        def_modules.append( ROOT.getSystWeight(syst_columns, var+"All", "", var, pair_ui(0,0), "ff->Vnorm" ) )
    elif round==1:
        pass
    elif round==2:        
        modules.append( ROOT.muonHistos(category, 'weight_'+category+'_nominal', syst_columns, var+'All', "", False) )
        #p.branch(nodeToStart='defs', nodeToEnd=category+'_'+var, modules=modules)
        p.branch(nodeToStart=category+'_nominal', nodeToEnd=category+'_'+var, modules=modules)
    return def_modules

def branch_LHE_weight(p, var, systs, weight, cut, category, round):
    modules = []
    def_modules = []
    new_weight_name = var+'_'+str(systs[0])+'_'+str(systs[1])+'All'
    if round==0:
        syst_columns = vec_s()
        syst_columns.push_back(var)
        def_modules.append( ROOT.getSystWeight(syst_columns, new_weight_name, "", "", pair_ui(systs[0], systs[1]), "V->V" ) )
    elif round==1:
        pass
    elif round==2:
        syst_column_names = vec_s()
        for i in range(systs[0], systs[1]+1):
            if var=='LHEScaleWeight': 
                syst_column_names.push_back(ROOT.string('LHEScaleWeight_'+str(get_LHEScaleWeight_meaning(i))))
            elif var=='LHEPdfWeight': 
                syst_column_names.push_back(ROOT.string('LHEPdfWeight_'+str(get_LHEPdfWeight_meaning(i))))
        modules.append( ROOT.muonHistos(category, 'weight_'+category+'_nominal', syst_column_names, new_weight_name, "", False) )
        #p.branch(nodeToStart='defs', nodeToEnd=category+'_'+var, modules=modules)
        p.branch(nodeToStart=category+'_nominal', nodeToEnd=category+'_'+var, modules=modules)
    return def_modules

def branch_muon_syst_scalefactor(p, systs, weight, cut, category, round):
    modules = []
    def_modules = []

    for syst in systs:
        if syst not in weight: continue

        if round==0:
            syst_columns = { 'BCDEF' : vec_s(), 'GH' : vec_s() }
            for key,item in syst_columns.items():
                for type in ['statUp', 'statDown', 'systUp', 'systDown']:
                    syst_columns[key].push_back('Muon_'+syst+'_'+key+'_SF'+type)                
            for key,item in syst_columns.items(): 
                def_modules.append( ROOT.getSystWeight(syst_columns[key],"Muon1_"+syst+"_"+key+"_SFall", "Idx_mu1", "Muon1_"+syst+"_"+key+"_SF", pair_ui(0,0), "VVVV->Vnorm") )
                def_modules.append( ROOT.getSystWeight(syst_columns[key],"Muon2_"+syst+"_"+key+"_SFall", "Idx_mu2", "Muon2_"+syst+"_"+key+"_SF", pair_ui(0,0), "VVVV->Vnorm") )            
            def_modules.append( ROOT.mergeSystWeight(pair_s('Muon1_'+syst+'_BCDEF_SFall','Muon1_'+syst+'_GH_SFall'), 
                                                     era_ratios, 'Muon1_'+syst+'_SFall', "V,V->aV+bV") )        
            def_modules.append( ROOT.mergeSystWeight(pair_s('Muon2_'+syst+'_BCDEF_SFall','Muon2_'+syst+'_GH_SFall'), 
                                                     era_ratios, 'Muon2_'+syst+'_SFall', "V,V->aV+bV") )                        
            def_modules.append( ROOT.mergeSystWeight(pair_s('Muon1_'+syst+'_SFall','Muon2_'+syst+'_SFall'), 
                                                     pair_f(1.0,1.0), 'Muon12_'+syst+'_SFall', "V,V->V*V") ) 
        elif round==1:
            pass
        elif round==2:
            modules = []
            syst_columns = { 'ALL' : vec_s()  }
            for key,item in syst_columns.items():
                for type in ['statUp', 'statDown', 'systUp', 'systDown']:
                    syst_columns[key].push_back(syst+'_'+type)                
            new_weight_name = "Muon12_"+syst+"_SFall" if category=='DIMUON' else "Muon1_"+syst+"_SFall"
            modules.append( ROOT.muonHistos(category, 'weight_'+category+'_nominal', syst_columns['ALL'], new_weight_name, "", False) )
            #p.branch(nodeToStart='defs', nodeToEnd=category+'_'+syst, modules=modules)
            p.branch(nodeToStart=category+'_nominal', nodeToEnd=category+'_'+syst, modules=modules)
    return def_modules

''' 
Create temporary RVec columns to store muon variables X that depend on <var>
These new column names are of the form X_var_{systs}. They are needed for: 
 1) Variables that enter the cut string
 2) Variables that are plotted inside muonHistos
'''
def get_muon_syst_columns(var,systs):
    def_modules = []

    signatureF = ""
    for i in range(len(systs)) : signatureF += "f"
    signatureF += "->V"
    signatureV = ""
    for i in range(len(systs)) : signatureV += "V"
    signatureV += "->V"

    if var=='corrected':
        for col in ['Muon_corrected_pt', 'Muon_corrected_MET_nom_mt', 'Muon_corrected_MET_nom_hpt']:    
            syst_columns = vec_s()
            for syst in systs: syst_columns.push_back( col.replace(var, syst) )            
            def_modules.append( ROOT.getSystWeight( syst_columns, col.replace('Muon', 'Muon1').replace(var, var+'All'), 
                                                    "Idx_mu1", "", pair_ui(0,0), signatureV) )
            def_modules.append( ROOT.getSystWeight( syst_columns, col.replace('Muon', 'Muon2').replace(var, var+'All'), 
                                                    "Idx_mu2", "", pair_ui(0,0), signatureV) )
    elif var=='nom':
        # This is a duplication of code. FIXME
        for col in ['Muon_corrected_MET_nom_mt', 'Muon_corrected_MET_nom_hpt']:
            syst_columns = vec_s()
            for syst in systs: syst_columns.push_back( col.replace(var, syst) )
            def_modules.append( ROOT.getSystWeight( syst_columns, col.replace('Muon', 'Muon1').replace(var, var+'All'), 
                                                    "Idx_mu1", "", pair_ui(0,0), signatureV) )
            def_modules.append( ROOT.getSystWeight( syst_columns, col.replace('Muon', 'Muon2').replace(var, var+'All'), 
                                                    "Idx_mu2", "", pair_ui(0,0), signatureV) )
        for col in ['MET_nom_pt', 'MET_nom_phi']:
            syst_columns = vec_s()
            for syst in systs:
                syst_columns.push_back( col.replace(var, syst) )
            def_modules.append( ROOT.getSystWeight( syst_columns, col.replace(var, var+'All'), "", "", pair_ui(0,0), signatureF ) )

    return def_modules

'''
Branch RDF into final node of type muonHistos with name category_var. <var> is a column modifier that can affect:
 1) variables we want to plot
 2) cuts
These cases are handled:
 A) <var> changes the event cut: create cleaned cut, removed cut, and RVec of weights as {(cut_removed)*(weight)}
    i)  If the plotted column X depends on var: Book an action via THDvarsHelper with signature <V,V>. 
        [First V is a pre-computed RVec of plotted column {X_var_systs}, second V is {(cut_removed)*(weight)} ]
    ii) Else: Book an action via THDvarsHelper with signature <f,V>
 B) <var> does not change the event cut:         
    i)  If the plotted column X depends on var: Book an action via THDvarsHelper with signature <V,f>.
        [V is a pre-computed RVec of plotted column {X_var_systs}, f is the nominal event weight} ]
    ii) Else: Book an action via THDvarsHelper with signature <f,f>
'''
def branch_muon_syst_column(p, var, systs, cut, weight, category, round):
    modules = []    
    def_modules = []

    syst_columns = vec_s()
    for syst in systs: syst_columns.push_back( syst )

    # Get all the RVec needed
    if round==0:
        def_modules.extend( get_muon_syst_columns(var,systs) )
        return def_modules

    # CASE A: the event cut depends on <var>
    if var in cut:

        # 1) Remove var-dependent variables: 'cut_clean' <-- 'cut'
        cut_clean = '('
        cut_clean += copy.deepcopy(cut)
        cut_clean_split = cut_clean.split(' && ')
        garbage = []
        for i in cut_clean_split: 
            if var in i: garbage.append(i)
        for i in garbage: cut_clean = cut_clean.replace(i, '1')
        cut_clean += ')'
        # 2) Move all var-dependent variables: 'cut_removed' <-- 'cut' 
        cut_removed = '(1'
        for i in garbage: cut_removed += (' && '+i)
        cut_removed += ')'
        #print('branch_muon_syst_column(): cut: '+cut+' -> '+cut_clean)

        if round==1:
            weight_columns = vec_s()
            # 3) Create new float columns of weights of the form (cut_removed)*(weight)
            for syst in systs:
                cut_syst = cut_removed.replace(var, syst)
                weight_cut_syst = '('+cut_syst+')*('+weight+')'
                weight_cut_syst_name = 'weight_'+category+'_cut_'+var+'_'+syst
                #print('branch_muon_syst_column(): '+weight_cut_syst_name+' = '+weight_cut_syst)
                def_modules.append( ROOT.getWeight(weight_cut_syst_name, weight_cut_syst) )
                weight_columns.push_back(weight_cut_syst_name)
            signature = ""
            for i in range(len(systs)) : signature += "f"
            signature += "->V"
            # 4) Create an RVec of the form {(cut_removed)*(weight)}
            def_modules.append( ROOT.getSystWeight(weight_columns, 'weight_'+category+'_cut_'+var+'All', "", "", pair_ui(0,0), signature) )
            return def_modules

        elif round==2:
            # 5) Make the logical OR of all removed cuts and AND it with cut_clean
            cut_removed_OR = '(0 ' 
            for syst in systs: cut_removed_OR += ' || ('+cut_removed.replace(var, syst)+')'
            cut_removed_OR += ')' 
            cut_clean_OR = cut_clean+' && '+cut_removed_OR
            #print('branch_muon_syst_column(): cut_clean: '+cut_clean+' -> '+cut_clean_OR)
            # Instruct muonHistos that TH1varsHelper with a multi-cut filling is needed
            #   > ""   -> no need for "weight"
            #   > 'weight_'+category+'_cut_'+var+'All' -> use the RVec of {(cut_removed)*(weight)}
            #   > True -> multi_cuts
            modules.append( ROOT.getFilter(cut_clean_OR) )
            modules.append( ROOT.muonHistos(category, "", syst_columns, 'weight_'+category+'_cut_'+var+'All', var, True ) )
            p.branch(nodeToStart='defs', nodeToEnd=category+'_'+var, modules=modules)

    # CASE B: the event cut is does *not* depend on <var>
    else:
        if round==1:
            # Nothing to be done
            return def_modules
        elif round==2:
            modules.append( ROOT.muonHistos(category, "weight_"+category+"_nominal", syst_columns, "", var, False ) )
            #p.branch(nodeToStart='defs', nodeToEnd=category+'_'+var, modules=modules)
            p.branch(nodeToStart=category+'_nominal', nodeToEnd=category+'_'+var, modules=modules)

    return def_modules

###################################################################################

inputFile = '/scratch/sroychow/NanoAOD2016-V1MCFinal/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/tree.root'
#'/scratch/sroychow/NanoAOD2016-V1MCFinal/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext2/tree.root'
#'/scratch/sroychow/NanoAOD2016-V1MCFinal/TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1/tree.root'
#

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

# 1st PASS:  collect all GLOBAL defs (run on first category only)
# 2nd PASS:  collect all CATEGORY defs        
# 3rd PASS:  run the histograms
def_modules = []
for round in [0,1,2]:
    print "Running pass...", round
    n_cat = 0
    for category,specifics in categories.items():  
        #if category!='SIGNAL': continue
        weight,cut = specifics['weight'], specifics['cut']

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
        def_modules.extend(branch_LHE_weight(p, 'LHEPdfWeight',   [98,101], weight, cut, category,round))
        n_cat += 1 
    print " ==>", len(def_modules), " defs modules have been loaded..."

print 'Get output...'
p.getOutput()
p.saveGraph()


