import copy

class bc:
    H    = '\033[95m'
    B    = '\033[94m'
    G    = '\033[92m'
    E    = '\033[0m'

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
    'event_syst_LHEScaleWeight' : [0,8,1,7,3,5],
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

submodules_fakerate = {
    'event_syst_fakerate' : {
        'input' : './data/bkg_parameters_file.root',
        'systs' : ['nominal']
        }
    }

modules_fakerate = copy.deepcopy(modules_nominal)
modules_fakerate.update(submodules_fakerate)

modules_wLHE = copy.deepcopy(modules_all)
modules_wLHE.update( submodules_LHE )

modules_wMass = copy.deepcopy(modules_all)
modules_wMass.update( submodules_mass )

modules_wLHEMass = copy.deepcopy(modules_wLHE)
modules_wLHEMass.update( submodules_mass )

modules_any = copy.deepcopy(modules_wLHEMass)
modules_any.update(modules_fakerate)

categories_all = { 
    'SIGNAL': {
        'weight' : 'puWeight*lumiweight*SelMuon1_ID_SF*SelMuon1_ISO_SF*SelMuon1_Trigger_SF',
        'category_weight_base' : 'SIGNAL',
        'cut' : 'Vtype==0 ' + \
            '&& HLT_SingleMu24 '+ \
            '&& MET_filters==1 ' + \
            '&& nVetoElectrons==0 ' + \
            '&& SelMuon1_corrected_pt>26.0 ' + \
            '&& SelMuon1_corrected_pt<65.0 ' + \
            '&& SelMuon1_corrected_MET_nom_mt>=40.0 ',
        'cut_base' : '',
        'category_cut_base' : 'defs',
        'modules' : modules_nominal
        },
    'SIGNALNORM': {
        'weight' : 'puWeight*lumiweight*SelMuon1_ID_SF*SelMuon1_ISO_SF*SelMuon1_Trigger_SF',
        'category_weight_base' : 'SIGNAL',
        'cut' : 'Vtype==0 ' + \
            '&& HLT_SingleMu24 '+ \
            '&& MET_filters==1 ' + \
            '&& nVetoElectrons==0 ' + \
            '&& SelMuon1_corrected_pt>26.0 ' + \
            '&& SelMuon1_corrected_pt<65.0 ' + \
            '&& SelMuon1_corrected_MET_nom_mt>=90.0 ',
        'cut_base' : '',
        'category_cut_base' : 'defs',
        'modules' : modules_nominal
        },
    'QCD': {
        'weight' : 'puWeight*lumiweight*SelMuon1_ID_SF*SelMuon1_ISO_SF*SelMuon1_Trigger_SF',
        'category_weight_base' : 'SIGNAL',
        'cut' : 'Vtype==0 ' + \
            '&& HLT_SingleMu24 '+ \
            '&& MET_filters==1 ' + \
            '&& nVetoElectrons==0 ' + \
            '&& SelMuon1_corrected_pt>26.0 ' + \
            '&& SelMuon1_corrected_pt<65.0 ' + \
            '&& SelMuon1_corrected_MET_nom_mt<30.0 ',
        'cut_base' : '',
        'category_cut_base' : 'defs',
        'modules' : modules_nominal,
    },
    'SIGNALNOISOSF': {
        'weight' : 'puWeight*lumiweight*SelMuon1_ID_SF*SelMuon1_Trigger_SF',
        'category_weight_base' : 'SIGNALNOISOSF',
        'cut' : 'Vtype==0 ' + \
            '&& HLT_SingleMu24 '+ \
            '&& MET_filters==1 ' + \
            '&& nVetoElectrons==0 ' + \
            '&& SelMuon1_corrected_pt>26.0 ' + \
            '&& SelMuon1_corrected_pt<65.0 ' + \
            '&& SelMuon1_corrected_MET_nom_mt>=40.0 ',
        'cut_base' : '',
        'category_cut_base' : 'defs',
        'modules' : modules_nominal
    },
    'AISO': {
        'weight' : 'puWeight*lumiweight*SelMuon1_ID_SF*SelMuon1_Trigger_SF*SelMuon1_ISO_SF',
        'category_weight_base' : 'AISO',
        'cut' : 'Vtype==1 ' + \
            '&& HLT_SingleMu24 '+ \
            '&& MET_filters==1 ' + \
            '&& nVetoElectrons==0 ' + \
            '&& SelMuon1_corrected_pt>26.0 ' + \
            '&& SelMuon1_corrected_pt<65.0 ' + \
            '&& SelMuon1_corrected_MET_nom_mt>=40.0 ',
        'cut_base' : '',
        'category_cut_base' : 'defs',
        'modules' : modules_nominal,
        },
    'AISONORM': {
        'weight' : 'puWeight*lumiweight*SelMuon1_ID_SF*SelMuon1_Trigger_SF*SelMuon1_ISO_SF',
        'category_weight_base' : 'AISO',
        'cut' : 'Vtype==1 ' + \
            '&& HLT_SingleMu24 '+ \
            '&& MET_filters==1 ' + \
            '&& nVetoElectrons==0 ' + \
            '&& SelMuon1_corrected_pt>26.0 ' + \
            '&& SelMuon1_corrected_pt<65.0 ' + \
            '&& SelMuon1_corrected_MET_nom_mt>=90.0 ',
        'cut_base' : '',
        'category_cut_base' : 'defs',
        'modules' : modules_nominal,
        },
    'SIDEBAND': {
        'weight' : 'puWeight*lumiweight*SelMuon1_ID_SF*SelMuon1_Trigger_SF*SelMuon1_ISO_SF',
        'category_weight_base' : 'AISO',
        'cut' : 'Vtype==1 ' + \
            '&& HLT_SingleMu24 '+ \
            '&& MET_filters==1 ' + \
            '&& nVetoElectrons==0 ' + \
            '&& SelMuon1_corrected_pt>26.0 ' + \
            '&& SelMuon1_corrected_pt<65.0 ' + \
            '&& SelMuon1_corrected_MET_nom_mt<30.0 ',
        'cut_base' : '',
        'category_cut_base' : 'defs',
        'modules' : modules_nominal,
        },
    'DIMUON': {
        'weight' : 'puWeight*lumiweight*SelMuon1_ID_SF*SelMuon1_ISO_SF*SelMuon1_Trigger_SF*SelMuon2_ID_SF*SelMuon2_ISO_SF',
        'category_weight_base' : 'DIMUON',
        'cut' : 'Vtype==2 ' + \
            '&& HLT_SingleMu24 '+ \
            '&& MET_filters==1 ' + \
            '&& nVetoElectrons==0 ' + \
            '&& SelMuon1_corrected_pt>26.0 ' + \
            '&& SelMuon2_corrected_pt>26.0 ' + \
            '&& SelMuon1_mediumId && SelMuon2_mediumId ' + \
            '&& SelMuon1_pfRelIso04_all<0.15 && SelMuon2_pfRelIso04_all<0.15 ' + \
            '&& TMath::Abs(SelRecoZ_corrected_mass-90.0)<15.0', 
        'cut_base' : '',
        'category_cut_base' : 'defs',
        'modules' : modules_all,
        },
    'GENINCLUSIVE': {
        'weight' : 'lumiweight',
        'category_weight_base' : 'GENINCLUSIVE',
        'cut' : '1',
        'cut_base' : '',
        'category_cut_base' : 'defs',
        'modules' : modules_nominal
        },
    }

def get_categories(dataType,categories_str, common, apply_SmoothAntiISOSF, apply_SmoothISOSF, use_externalSF):
    categories_split = categories_str.split(',')
    categories_split_name  = []
    categories_split_syst  = []
    categories_split_slice = []
    categories_split_reweight = []
    categories_split_Z_reweight = []
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

        # qt/y reweighting ?
        if "+" in c: 
            count = c.count('+')
            c = c.replace("+", "")
            categories_split_Z_reweight.append(count)
        else:
            categories_split_Z_reweight.append(0)

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

    # global customization of SF
    if apply_SmoothAntiISOSF:
        for k,v in ret.items():
            if k not in ['SIDEBAND', 'AISO', 'AISONORM']: continue
            old = copy.deepcopy(v['weight'])
            v['weight'] = old.replace('ISO_SF', 'ISO_SmoothAntiSF')
            print k+': \n', bc.H, old, bc.E, ' --> \n', bc.B, v['weight'], bc.E
    if apply_SmoothISOSF and use_externalSF==0:
        for k,v in ret.items():
            if k not in ['SIGNAL', 'SIGNALNORM', 'QCD', 'DIMUON']: continue
            old = copy.deepcopy(v['weight'])
            v['weight'] = old.replace('ISO_SF', 'ISO_SmoothSF')
            print k+': \n', bc.H, old, bc.E, ' --> \n', bc.B, v['weight'], bc.E
    if use_externalSF:
        for k,v in ret.items():
            old = copy.deepcopy(v['weight'])
            v['weight'] = old.replace('ISO_SF','ISO_WHelicitySF').replace('ID_SF','ID_WHelicitySF').replace('Trigger_SF', 'Trigger_WHelicitySF')
            print k+': \n', bc.H, old, bc.E, ' --> \n', bc.B, v['weight'], bc.E
                    
    # these are all the base categories
    for c in ['SIGNAL_WtoMuP', 'SIGNAL_WtoMuN', 'SIGNAL_WtoTau',
              'SIGNAL_ZtoMuMu','SIGNAL_ZtoTauTau',
              'SIGNAL',
              'SIGNALNORM',
              'SIGNALNOISOSF',
              'DIMUON_ZtoMuMu','DIMUON_ZtoTauTau',
              'DIMUON',
              'AISO',
              'AISONORM',
              'QCD',
              'SIDEBAND',
              'GENINCLUSIVE_WtoMuP', 'GENINCLUSIVE_WtoMuN',
              'GENINCLUSIVE',
              ]:

        # check whether c is in the json file
        run_c,pos_c = False, -1
        for icc,cc in enumerate(categories_split_name):
            if cc==c: (run_c,pos_c) = (True,icc)
        if not run_c:
            if ret.has_key(c): del ret[c]
            continue        

        charge = ""
        if ("Wto" in c) or ("Zto" in c):
            charge = c.split('_')[1]
            dec = "Wto" if "Wto" in c else "Zto"
            ret[c] = copy.deepcopy(ret[c.split('_')[0]])
            ret[c]["category_cut_base"] = c.split('_')[0] 
            ret[c]["cut"] = str(common[dec][c.split('_')[1].lstrip(dec)])
            ret[c]["cut_base"] = str(ret[c.split('_')[0]]['cut'])
            if not ret_base.has_key(c.split('_')[0]):
                ret_base[c.split('_')[0]] = copy.deepcopy(ret[c.split('_')[0]])

        cat_syst = categories_split_syst[pos_c]
        if dataType=='DATA':
            ret[c]['weight'] = 'Float_t(1.0)'
            if cat_syst == 'nominal':
                ret[c]['modules'] =  modules_nominal
            elif cat_syst == 'fakerate':
                ret[c]['modules'] =  modules_fakerate
        else:
            if cat_syst == 'nominal':
                ret[c]['modules'] = modules_nominal
            elif cat_syst == 'all':
                ret[c]['modules'] = modules_all
            elif cat_syst == 'LHE':
                ret[c]['modules'] = modules_LHE
            elif cat_syst == 'wLHE':
                ret[c]['modules'] = modules_wLHE                
            elif cat_syst == 'wLHEMass':
                ret[c]['modules'] = modules_wLHEMass
            elif cat_syst == 'wMass':
                ret[c]['modules'] = modules_wMass                

        cat_Z_reweight = categories_split_Z_reweight[pos_c]
        if cat_Z_reweight>0:            
            if charge=="": charge += "V"
            ret[c]['category_weight_base'] += (charge+'REWEIGHT')
            ret[c]['weight'] += '*reweight_'+charge+'_qt'
            if cat_Z_reweight>1: ret[c]['weight'] += '*reweight_'+charge+'_y'

        # phase-space slicing is enabled
        if categories_split_slice[pos_c]:
            if not ret_base.has_key(c): ret_base[c] = copy.deepcopy(ret[c])
            lepton_def = common["genLepton"]
            ps = common["phase_space_"+lepton_def]

            cat_OF = copy.deepcopy(ret[c])
            cat_OF['category_cut_base'] = str(c)
            cat_OF['cut'] = '0'
            cat_OF['cut_base'] = ret[c]['cut_base']+' && '+ret[c]['cut']

            for ps_key,ps_val in ps.items():
                y_bin = ps_key.lstrip("y[").rstrip("]").split(',')
                (y_low,y_high) = (y_bin[0],y_bin[1])
                qT_bins = ps_val["qT"]
                for iqT in range(len(qT_bins)-1):
                    qT_low  = "{:0.1f}".format(qT_bins[iqT])
                    qT_high = "{:0.1f}".format(qT_bins[iqT+1]) if qT_bins[iqT+1]>=0. else "Inf"
                    ps_cut = str("("+ \
                        "GenV_"+lepton_def+"_absy>="+y_low + \
                        (" && GenV_"+lepton_def+"_absy<"+y_high if y_high!="Inf" else "") + \
                        " && GenV_"+lepton_def+"_qt>="+qT_low + \
                        (" && GenV_"+lepton_def+"_qt<"+qT_high if qT_high!="Inf" else "") + \
                        ")")
                    if ("Inf" in qT_high) or ("Inf" in y_high):
                        cat_OF['cut'] += ' || ('+ps_cut+')'
                        continue
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
                        for a in common["harmonics"]["coefficients"]:
                            new_cat = copy.deepcopy(ret[str(c+'_'+cat_name)])
                            # dummy for the moment...
                            new_cat["weight"] = str(new_cat["weight"]+"*weight_coeff_"+charge+"_"+a)
                            # NOT the nominal weight for top category
                            c_weight_base = c.split('_')[0]
                            new_cat["category_weight_base"] = str(c_weight_base+"_"+a)
                            # inherits cut from top category
                            new_cat['cut'] = ""
                            new_cat['cut_base'] = str(ret[str(c+'_'+cat_name)]['cut_base']+' && '+ret[str(c+'_'+cat_name)]['cut'])
                            new_cat["category_cut_base"] = str(c+'_'+cat_name)
                            ret[str(c+'_'+cat_name+'_coeff'+a)] = new_cat
                        # remove the MC?
                        del ret[str(c+'_'+cat_name)]
            ret[str(c+'_OF')] = cat_OF                        
            del ret[c]

    return ret, ret_base
                

def get_LHEScaleWeight_meaning(self,wid=0):
    if wid==0:
        return 'muR0p5_muF0p5'
    elif wid==1:
        return 'muR0p5_muF1p0'
    elif wid==2:
        return 'muR0p5_muF2p0'
    elif wid==3:
        return 'muR1p0_muF0p5'
    elif wid==4:
        return 'muR1p0_muF1p0'
    elif wid==5:
        return 'muR1p0_muF2p0'
    elif wid==6:
        return 'muR2p0_muF0p5'
    elif wid==7:
        return 'muR2p0_muF1p0'
    elif wid==8:
        return 'muR2p0_muF2p0'
    else:
        return 'muRX_muFX'

def LHEPdfWeight_meaning(wid=0):
    if wid<100:
        return 'NNPDF_'+str(wid)+'replica'
    elif wid==100:
        return 'NNPDF_alphaSDown'
    elif wid==101:
        return 'NNPDF_alphaSUp'
    else:
        return 'NNPDF_XXXreplica'                

def get_histo_coeff(ps):
    import ROOT
    from array import array
    x,y = [],[]
    read_once = False
    for ps_key,ps_val in ps.items():
        y_bin = ps_key.lstrip("y[").rstrip("]").split(',')
        (y_low,y_high) = (y_bin[0],y_bin[1])
        x.append(float(y_low))
        qT_bins = ps_val["qT"]
        if read_once: continue
        for iqT in range(len(qT_bins)-1):
            qT_low  = "{:0.1f}".format(qT_bins[iqT])
            qT_high = "{:0.1f}".format(qT_bins[iqT+1]) if qT_bins[iqT+1]>=0. else "Inf"    
            y.append(float(qT_low))
        read_once = True
    x = sorted(x, key=float)
    y = sorted(y, key=float)
    print '|y| bins:', x
    print 'qt bins: ', y
    xx = array('f', x)
    yy = array('f', y)
    h = ROOT.TH2F('histo','', len(xx)-1, xx, len(yy)-1, yy)
    return h
