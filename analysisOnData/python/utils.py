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
        'category_base' : 'SIGNAL'
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
        'category_base' : 'QCD'
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
        'category_base' : 'DIMUON'
        },
    }

def get_categories(dataType,categories_str, general):
    categories_split = categories_str.split(',')
    categories_split_name  = []
    categories_split_syst  = []
    categories_split_slice = []
    categories_split_reweight = []
    for c in categories_split:
        # phase-space splitting
        if "*" in c: 
            c = c.replace("*", "")
            categories_split_slice.append(True)
        else:
            categories_split_slice.append(False)
        # harmonics reweighting
        if "^" in c: 
            c = c.replace("^", "")
            categories_split_reweight.append(True)
        else:
            categories_split_reweight.append(False)
        # modules to be run
        if ':' in c:
            pos = c.find(':')
            c_name,c_syst = c[:pos], c[pos+1:]
            categories_split_name.append(c_name)
            categories_split_syst.append(c_syst)
        else:
            categories_split_name.append(c)
            categories_split_syst.append('')

    # start from a sreash copy
    ret = copy.deepcopy(categories_all)

    for c in ['SIGNAL_WtoMuP','SIGNAL_WtoMuN','SIGNAL_WtoTau','SIGNAL','QCD','DIMUON']:

        if "Wto" in c:
            ret[c] = copy.deepcopy(ret[c.split('_')[0]])
            ret[c]["cut"] += "&& "+ general["Wto"][c.split('_')[1].lstrip('Wto')]

        run_c,pos_c = False, -1
        for icc,cc in enumerate(categories_split_name):
            if cc==c: (run_c,pos_c) = (True,icc)
        if not run_c:
            if ret.has_key(c): del ret[c]
            continue

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

        lep = general["genLepton"]
        ps = general["phase_space_"+lep]
        if categories_split_slice[pos_c]:
            for ps_key,ps_val in ps.items():
                y_bin = ps_key.lstrip("y[").rstrip("]").split(',')
                (y_low,y_high) = (y_bin[0],y_bin[1])
                qT_bins = ps_val["qT"]
                for iqT in range(len(qT_bins)-1):
                    qT_low  = "{:0.1f}".format(qT_bins[iqT])
                    qT_high = "{:0.1f}".format(qT_bins[iqT+1]) if qT_bins[iqT+1]>=0. else "Inf"
                    ps_cut = str("("+ \
                        "TMath::Abs(GenV_"+lep+"_y)>="+y_low + \
                        (" && TMath::Abs(GenV_"+lep+"_y)<"+y_high if y_high!="Inf" else "") + \
                        " && GenV_"+lep+"_qt>="+qT_low + \
                        (" && GenV_"+lep+"_qt<"+qT_high if qT_high!="Inf" else "") + \
                        ")")
                    cat_name = str("y"+y_low.replace('.','p')+"_"+y_high.replace('.','p') + \
                        "_qT"+qT_low.replace('.','p')+"_"+qT_high.replace('.','p'))
                    new_cat = copy.deepcopy(ret[c])
                    new_cat['cut'] = str(new_cat['cut'])+str(" && "+ps_cut)
                    ret[str(c+'_'+cat_name)] = new_cat                       
                    if categories_split_reweight[pos_c]:
                        for a in general["harmonics"]:
                            new_cat = copy.deepcopy(ret[str(c+'_'+cat_name)])
                            # dummy for the moment...
                            new_cat["weight"] = str(new_cat["weight"]+"*Float_t(1.0)")
                            c_base = c
                            if "Wto" in c: 
                                c_base = c.split('_')[0]
                            new_cat["category_base"] = str(c_base+"_"+a)
                            ret[str(c+'_'+cat_name+'_'+a)] = new_cat
                        # remove the MC?
                        #del ret[str(c+'_'+cat_name)]
            del ret[c]

    return ret
                
