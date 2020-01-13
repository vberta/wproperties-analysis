import copy

modules_nominal = { 
    'muon_nominal' : [] 
    }

modules_all = {
    'muon_nominal' : [],
    'event_syst_puWeight' : ['Up', 'Down'],
    'muon_syst_scalefactor_ID' : [],
    'muon_syst_scalefactor_ISO' : [],
    'muon_syst_scalefactor_Trigger' : [],
    'muon_syst_column_corrected' : ['correctedUp','correctedDown'],
    'muon_syst_column_nom' : ['jerUp','jerDown','jesTotalUp','jesTotalDown','unclustEnUp','unclustEnDown'],
    }

submodules_LHE = {
    'event_syst_LHEScaleWeight' : [0,8],
    'event_syst_LHEPdfWeight'   : [98,101]    
    }

modules_LHE = {
    'muon_nominal' : [],    
    }
modules_LHE.update(submodules_LHE)

modules_wLHE = copy.deepcopy(modules_all)
modules_wLHE.update( submodules_LHE )


categories_all = { 
    'SIGNAL': {
        'weight' : 'puWeight*lumiweight*SelMuon1_ID_SF*SelMuon1_ISO_SF*SelMuon1_Trigger_SF',
        'cut' : 'Vtype==0 ' + \
        '&& HLT_SingleMu24 '+ \
        '&& MET_filters==1 ' + \
        '&& nVetoElectrons==0 ' + \
        '&& SelMuon1_corrected_pt>25.0 ' + \
        '&& SelMuon1_corrected_MET_nom_mt>40.0 ',
        'modules' : modules_all,
    },    
    'QCD': {
        'weight' : 'puWeight*lumiweight*SelMuon1_ID_SF*SelMuon1_ISO_SF*SelMuon1_Trigger_SF',
        'cut' : 'Vtype==1 ' + \
        '&& HLT_SingleMu24 '+ \
        '&& MET_filters==1 ' + \
        '&& nVetoElectrons==0 ' + \
        '&& SelMuon1_corrected_pt>25.0 ' + \
        '&& SelMuon1_corrected_MET_nom_mt<40.0 ',
        'modules' : modules_all,
    },
    'DIMUON': {
        'weight' : 'puWeight*lumiweight*SelMuon1_ID_SF*SelMuon1_ISO_SF*SelMuon1_Trigger_SF*SelMuon2_ID_SF*SelMuon2_ISO_SF*SelMuon2_Trigger_SF',
        'cut' : 'Vtype==2 ' + \
        '&& HLT_SingleMu24 '+ \
        '&& MET_filters==1 ' + \
        '&& nVetoElectrons==0 ' + \
        '&& SelMuon1_corrected_pt>25.0 ' + \
        '&& SelMuon2_corrected_pt>25.0 ',
        'modules' : modules_all,
        },
    }

def get_categories(dataType,categories_str):
    categories_split = categories_str.split(',')
    categories_split_clean = []
    categories_split_syst  = []
    for c in categories_split:
        if ':' in c:
            pos = c.find(':')
            c_clean,c_syst = c[:pos], c[pos+1:]
            categories_split_clean.append(c_clean)
            categories_split_syst.append(c_syst)
        else:
            categories_split_clean.append(c)
            categories_split_syst.append('')
    ret = copy.deepcopy(categories_all)
    for c in ['SIGNAL', 'QCD', 'DIMUON']:        
        run_c,pos_c = False, -1
        for icc,cc in enumerate(categories_split_clean):
            if cc==c:
                run_c = True
                pos_c = icc
        if not run_c: 
            del ret[c]
        else:
            if dataType=='DATA':
                ret[c]['weight'] = 'Float_t(1.0)'
                ret[c]['modules'] =  modules_nominal
            else:
                if categories_split_syst[pos_c] == 'nominal':
                    ret[c]['modules'] = modules_nominal
                elif categories_split_syst[pos_c] == 'all':
                    ret[c]['modules'] = modules_all
                elif categories_split_syst[pos_c] == 'LHE':
                    ret[c]['modules'] = modules_LHE
                elif categories_split_syst[pos_c] == 'wLHE':
                    ret[c]['modules'] = modules_wLHE                
                
    return ret
                
