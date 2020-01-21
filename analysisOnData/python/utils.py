import copy

modules_nominal = { 
    'muon_nominal' : [] 
    }

modules_all = {
    'muon_nominal'                  : [],
    'event_syst_puWeight'           : ['Up', 'Down'],
    'muon_syst_scalefactor_ID'      : ['statUp', 'statDown', 'systUp', 'systDown'],
    'muon_syst_scalefactor_ISO'     : ['statUp', 'statDown', 'systUp', 'systDown'],
    'muon_syst_scalefactor_Trigger' : ['statUp', 'statDown', 'systUp', 'systDown'],
    'muon_syst_column_corrected'    : ['correctedUp','correctedDown'],
    'muon_syst_column_nom'          : ['jerUp','jerDown','jesTotalUp','jesTotalDown','unclustEnUp','unclustEnDown'],
    }

submodules_LHE = {
    'event_syst_LHEScaleWeight' : [0,8],
    'event_syst_LHEPdfWeight'   : [98,101]    
    }
modules_LHE = {
    'muon_nominal' : [],    
    }
modules_LHE.update(submodules_LHE)

submodules_mass = {
    'event_syst_mass_reweight' : {
        'masses'     : [80.319,80.519],
        'M'          : 80.419,
        'G'          : 2.047,
        'leptonType' : 'preFSR',
        'scheme'     : 'Fixed',
        },
    }

modules_wLHE = copy.deepcopy(modules_all)
modules_wLHE.update( submodules_LHE )

modules_wMass = copy.deepcopy(modules_all)
modules_wMass.update( submodules_mass )

modules_wLHEMass = copy.deepcopy(modules_wLHE)
modules_wLHEMass.update( submodules_mass )

modules_any = copy.deepcopy(modules_wLHEMass)

categories_all = { 
    'SIGNAL': {
        'weight' : 'puWeight*lumiweight*SelMuon1_ID_SF*SelMuon1_ISO_SF*SelMuon1_Trigger_SF',
        'category_weight_base' : 'SIGNAL',
        'cut' : 'Vtype==0 ' + \
            '&& HLT_SingleMu24 '+ \
            '&& MET_filters==1 ' + \
            '&& nVetoElectrons==0 ' + \
            '&& SelMuon1_corrected_pt>26.0 ' + \
            '&& SelMuon1_corrected_pt<55.0 ' + \
            '&& SelMuon1_corrected_MET_nom_mt>40.0 ',
        'cut_base' : '',
        'category_cut_base' : 'defs',
        'modules' : modules_nominal
    },    
    'QCD': {
        'weight' : 'puWeight*lumiweight*SelMuon1_ID_SF*SelMuon1_ISO_SF*SelMuon1_Trigger_SF',
        'category_weight_base' : 'QCD',
        'cut' : 'Vtype==1 ' + \
        '&& HLT_SingleMu24 '+ \
        '&& MET_filters==1 ' + \
        '&& nVetoElectrons==0 ' + \
        '&& SelMuon1_corrected_pt>26.0 ' + \
        '&& SelMuon1_corrected_pt<55.0 ' + \
        '&& SelMuon1_corrected_MET_nom_mt<40.0 ',
        'cut_base' : '',
        'category_cut_base' : 'defs',
        'modules' : modules_nominal,
    },
    'DIMUON': {
        'weight' : 'puWeight*lumiweight*SelMuon1_ID_SF*SelMuon1_ISO_SF*SelMuon1_Trigger_SF*SelMuon2_ID_SF*SelMuon2_ISO_SF*SelMuon2_Trigger_SF',
        'category_weight_base' : 'DIMUON',
        'cut' : 'Vtype==2 ' + \
        '&& HLT_SingleMu24 '+ \
        '&& MET_filters==1 ' + \
        '&& nVetoElectrons==0 ' + \
        '&& SelMuon1_corrected_pt>26.0 ' + \
        '&& SelMuon2_corrected_pt>26.0 ',
        'cut_base' : '',
        'category_cut_base' : 'defs',
        'modules' : modules_all,
        },
    }

def get_categories(dataType,categories_str, common):
    categories_split = categories_str.split(',')
    categories_split_name  = []
    categories_split_syst  = []
    categories_split_slice = []
    categories_split_reweight = []
    for c in categories_split:

        # phase-space splitting ?
        if "*" in c: 
            c = c.replace("*", "")
            categories_split_slice.append(True)
        else:
            categories_split_slice.append(False)

        # harmonics reweighting ?
        if "^" in c: 
            c = c.replace("^", "")
            categories_split_reweight.append(True)
        else:
            categories_split_reweight.append(False)

        # modules to be run. Default: all
        if ':' in c:
            pos = c.find(':')
            c_name,c_syst = c[:pos], c[pos+1:]
            categories_split_name.append(c_name)
            categories_split_syst.append(c_syst)
        else:
            categories_split_name.append(c)
            categories_split_syst.append('')

    # start from a fresh copy
    ret = copy.deepcopy(categories_all)
    ret_base = {}

    # these are all the base categories
    for c in ['SIGNAL_WtoMuP', 'SIGNAL_WtoMuN','SIGNAL_WtoTau',
              'SIGNAL_ZtoMuMu','SIGNAL_ZtoTauTau',
              'SIGNAL',
              'DIMUON_ZtoMuMu','DIMUON_ZtoTauTau',
              'DIMUON',
              'QCD'
              ]:

        # check whether c is in the json file
        run_c,pos_c = False, -1
        for icc,cc in enumerate(categories_split_name):
            if cc==c: (run_c,pos_c) = (True,icc)
        if not run_c:
            if ret.has_key(c): del ret[c]
            continue        

        if ("Wto" in c) or ("Zto" in c):
            dec = "Wto" if "Wto" in c else "Zto"
            ret[c] = copy.deepcopy(ret[c.split('_')[0]])
            ret[c]["category_cut_base"] = c.split('_')[0] 
            ret[c]["cut"] = str(common[dec][c.split('_')[1].lstrip(dec)])
            ret[c]["cut_base"] = str(ret[c.split('_')[0]]['cut'])
            if not ret_base.has_key(c.split('_')[0]):
                ret_base[c.split('_')[0]] = copy.deepcopy(ret[c.split('_')[0]])

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
            elif categories_split_syst[pos_c] == 'wLHEMass':
                ret[c]['modules'] = modules_wLHEMass
            elif categories_split_syst[pos_c] == 'wMass':
                ret[c]['modules'] = modules_wMass                
                

        # phase-space slicing is enabled
        if categories_split_slice[pos_c]:
            if not ret_base.has_key(c):
                ret_base[c] = copy.deepcopy(ret[c])
            lepton_def = common["genLepton"]
            ps = common["phase_space_"+lepton_def]
            for ps_key,ps_val in ps.items():
                y_bin = ps_key.lstrip("y[").rstrip("]").split(',')
                (y_low,y_high) = (y_bin[0],y_bin[1])
                qT_bins = ps_val["qT"]
                for iqT in range(len(qT_bins)-1):
                    qT_low  = "{:0.1f}".format(qT_bins[iqT])
                    qT_high = "{:0.1f}".format(qT_bins[iqT+1]) if qT_bins[iqT+1]>=0. else "Inf"
                    ps_cut = str("("+ \
                        "TMath::Abs(GenV_"+lepton_def+"_y)>="+y_low + \
                        (" && TMath::Abs(GenV_"+lepton_def+"_y)<"+y_high if y_high!="Inf" else "") + \
                        " && GenV_"+lepton_def+"_qt>="+qT_low + \
                        (" && GenV_"+lepton_def+"_qt<"+qT_high if qT_high!="Inf" else "") + \
                        ")")
                    cat_name = str("y"+y_low.replace('.','p')+"to"+y_high.replace('.','p') + \
                        "_qt"+qT_low.replace('.','p')+"to"+qT_high.replace('.','p'))
                    new_cat = copy.deepcopy(ret[c])
                    new_cat['category_cut_base'] = str(c)
                    new_cat['cut'] = str(ps_cut)
                    new_cat['cut_base'] = ret[c]['cut_base']+' && '+ret[c]['cut']
                    ret[str(c+'_'+cat_name)] = new_cat                       
                    if categories_split_reweight[pos_c]:
                        if not ret_base.has_key(c+'_'+cat_name):
                            ret_base[c+'_'+cat_name] = copy.deepcopy(new_cat)
                        for a in common["harmonics"]:
                            new_cat = copy.deepcopy(ret[str(c+'_'+cat_name)])
                            # dummy for the moment...
                            new_cat["weight"] = str(new_cat["weight"]+"*Float_t(1.0+"+str(a[-1])+")")
                            # NOT the nominal weight for top category
                            c_weight_base = c.split('_')[0]
                            new_cat["category_weight_base"] = str(c_weight_base+"_"+a)
                            # inherits cut from top category
                            new_cat['cut'] = ""
                            new_cat['cut_base'] = str(ret[str(c+'_'+cat_name)]['cut_base']+' && '+ret[str(c+'_'+cat_name)]['cut'])
                            new_cat["category_cut_base"] = str(c+'_'+cat_name)
                            ret[str(c+'_'+cat_name+'_'+a)] = new_cat
                        # remove the MC?
                        del ret[str(c+'_'+cat_name)]
            del ret[c]

    return ret, ret_base
                
