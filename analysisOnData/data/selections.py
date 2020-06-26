# corrected = Rochester
muon = '_corrected'

# nom = MET w/ jet smearing
met = '_nom'
histoweights = {
    'MC': {
        'totalWeight_Muon1' : 'Generator_weight*' +\
                            'puWeight*' + 
                            'Muon_Trigger_BCDEF_SF[Idx_mu1]*' + \
                            'Muon_ID_BCDEF_SF[Idx_mu1]*' + \
                            'Muon_ISO_BCDEF_SF[Idx_mu1]',
        'totalWeight_Dimuon' : 'Generator_weight*' +\
                             'puWeight*' +\
                             'Muon_Trigger_BCDEF_SF[Idx_mu1]*Muon_ISO_BCDEF_SF[Idx_mu1]*Muon_ID_BCDEF_SF[Idx_mu1]*' +\
                             'Muon_ISO_BCDEF_SF[Idx_mu2]*Muon_ID_BCDEF_SF[Idx_mu2]'
        },
    'DATA' : {
        'totalWeight_Data' : '1'
    }
}
selections = {
    'Signal' : {
        'MC' : {
            'cut': \
                'Vtype==0 && ' + \
                'HLT_SingleMu24 && '+ \
                ('Muon%s_pt[Idx_mu1]>25. && ' % muon) + \
                ('Muon%s_MET%s_mt[Idx_mu1]>0. && ' % (muon, met) ) + \
                'MET_filters==1 && ' + \
                'nVetoElectrons==0 && ' + \
                '1',            
            'weight' : 'totalWeight_Muon1'
            },
        'DATA' : {
            'cut': \
                'Vtype==0 && ' + \
                'HLT_SingleMu24 && ' + \
                ('Muon%s_pt[Idx_mu1]>25. && ' % muon) + \
                ('Muon%s_MET%s_mt[Idx_mu1]>0. && ' % (muon, met)) +\
                'MET_filters==1 && ' + \
                'nVetoElectrons==0 && ' + \
                '1',
            'weight' : 'totalWeight_Data',
            },
        },

    'Sideband' : {
        'MC' : {
            'cut': \
                'Vtype==1 && ' +\
                'HLT_SingleMu24 && ' +\
                ('Muon%s_pt[Idx_mu1]>25. && ' % muon) + \
                ('Muon%s_MET%s_mt[Idx_mu1]>0. && ' % (muon, met)) + \
                'MET_filters==1 && ' +\
                'nVetoElectrons==0 && ' +\
                '1',
            'weight' : 'totalWeight_Muon1',
            },
        'DATA' : {
            'cut': \
                'Vtype==1 && ' +\
                'HLT_SingleMu24 && '+ \
                ('Muon%s_pt[Idx_mu1]>25. && ' % muon) + \
                ('Muon%s_MET%s_mt[Idx_mu1]>0. && ' % (muon, met)) + \
                'MET_filters==1 && ' +\
                'nVetoElectrons==0 && ' + \
                '1',
            'weight' : 'totalWeight_Data',
            },
        },

    'Dimuon' : {
        'MC' : {
            'cut': \
                'Vtype==2 && '+ \
                'HLT_SingleMu24 && '+ \
                ('Muon%s_pt[Idx_mu1]>25. && Muon%s_pt[Idx_mu2]>20. && ' % (muon, muon) ) + \
                'MET_filters==1 && '+ \
                'nVetoElectrons==0 && '+ \
                '1',
            'weight' : 'totalWeight_Dimuon'
            },
        'DATA' : {
            'cut': \
                'Vtype==2 && '+ \
                'HLT_SingleMu24 && '+ \
                ('Muon%s_pt[Idx_mu1]>25. && Muon%s_pt[Idx_mu2]>20. && ' % (muon, muon))+ \
                'MET_filters==1 && '+ \
                'nVetoElectrons==0 && '+ \
                '1',
            'weight' : 'totalWeight_Data',
            },
        },
    }


