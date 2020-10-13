selections = {
  "Signal": "Vtype==0 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT>=40.0 && MET_filters==1 && nVetoElectrons==0 && 1", 
  }

selections_bkg = {
  "Signal":         "Vtype==0 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT>=40.0 && MET_filters==1 && nVetoElectrons==0 && 1",
  "Signal_aiso":    "Vtype==1 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT>=40.0 && MET_filters==1 && nVetoElectrons==0 && 1",
  "Sideband":       "Vtype==0 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=30.0 && MET_filters==1 && nVetoElectrons==0 && 1",
  "Sideband_aiso":  "Vtype==1 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=30.0 && MET_filters==1 && nVetoElectrons==0 && 1",
  "Sideband15":       "Vtype==0 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=15.0 && MET_filters==1 && nVetoElectrons==0 && 1",
  "Sideband_aiso15":  "Vtype==1 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=15.0 && MET_filters==1 && nVetoElectrons==0 && 1", 
  "Sideband30":       "Vtype==0 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=30.0 && MET_filters==1 && nVetoElectrons==0 && 1 && MT>=15.0",
  "Sideband_aiso30":  "Vtype==1 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=30.0 && MET_filters==1 && nVetoElectrons==0 && 1 && MT>=15.0",
  "Sideband40":       "Vtype==0 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=40.0 && MET_filters==1 && nVetoElectrons==0 && 1 && MT>=30.0",
  "Sideband_aiso40":  "Vtype==1 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=40.0 && MET_filters==1 && nVetoElectrons==0 && 1 && MT>=30.0"
}

selections_fakes = {
  "fakes": "HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT>=40.0 && MET_filters==1 && nVetoElectrons==0 && 1", 
  "fakes_SideBand": "HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<30.0 && MET_filters==1 && nVetoElectrons==0 && 1", 
  }

selectionVars = { 
    "ptScale" : { "_correctedUp" : 1, "_correctedDown" : 1, 
                  "_zptsystUp" : 1, "_zptsystDown" : 1,
                  "_EwksystUp" : 1, "_EwksystDown" : 1,
                  "_deltaMsystUp" : 1, "_deltaMsystDown" : 1,
                  "_Ewk2systUp" : 1, "_Ewk2systDown" : 1
              }, 
  # "jme" : { "_jerUp" : 2, "_jerDown" : 2 , "_jesTotalUp" : 2, "_jesTotalDown" : 2, "_unclustEnUp" : 2,"_unclustEnDown" : 2}
  "jme" : {"_jesTotalUp" : 2, "_jesTotalDown" : 2, "_unclustEnUp" : 2,"_unclustEnDown" : 2}
}
for idx in range(0, 99):
   upName = "_stateig" + str(idx) + "Up"
   selectionVars["ptScale"].update({upName : 1})
   #downName = "_stateig" + str(idx) + "Down"
   #selectionVars["ptScale"].update({downName : 1})

##Selections as in WHelicity analysis
selections_whelicity = {
  "Signal": "Vtype==0 && HLT_SingleMu24 && Mu1_pt>26.0 && Mu1_pt<56.0 && MT>=40.0 && MET_filters==1 && nVetoElectrons==0 && 1",
}

selections_bkg_whelicity = {
  "Signal":         "Vtype==0 && HLT_SingleMu24 && Mu1_pt>26.0 && Mu1_pt<56.0 && MT>=40.0 && MET_filters==1 && nVetoElectrons==0 && 1",
  "Signal_aiso":    "Vtype==1 && HLT_SingleMu24 && Mu1_pt>26.0 && Mu1_pt<56.0 && MT>=40.0 && MET_filters==1 && nVetoElectrons==0 && 1",
  "Sideband":       "Vtype==0 && HLT_SingleMu24 && Mu1_pt>26.0 && Mu1_pt<56.0 && MT<=30.0 && MET_filters==1 && nVetoElectrons==0 && 1",
  "Sideband_aiso":  "Vtype==1 && HLT_SingleMu24 && Mu1_pt>26.0 && Mu1_pt<56.0 && MT<=30.0 && MET_filters==1 && nVetoElectrons==0 && 1",
  "Sideband15":       "Vtype==0 && HLT_SingleMu24 && Mu1_pt>26.0 && Mu1_pt<56.0 && MT<=15.0 && MET_filters==1 && nVetoElectrons==0 && 1",
  "Sideband_aiso15":  "Vtype==1 && HLT_SingleMu24 && Mu1_pt>26.0 && Mu1_pt<56.0 && MT<=15.0 && MET_filters==1 && nVetoElectrons==0 && 1",
  "Sideband30":       "Vtype==0 && HLT_SingleMu24 && Mu1_pt>26.0 && Mu1_pt<56.0 && MT<=30.0 && MET_filters==1 && nVetoElectrons==0 && 1 && MT>=15.0",
  "Sideband_aiso30":  "Vtype==1 && HLT_SingleMu24 && Mu1_pt>26.0 && Mu1_pt<56.0 && MT<=30.0 && MET_filters==1 && nVetoElectrons==0 && 1 && MT>=15.0",
  "Sideband40":       "Vtype==0 && HLT_SingleMu24 && Mu1_pt>26.0 && Mu1_pt<56.0 && MT<=40.0 && MET_filters==1 && nVetoElectrons==0 && 1 && MT>=30.0",
  "Sideband_aiso40":  "Vtype==1 && HLT_SingleMu24 && Mu1_pt>26.0 && Mu1_pt<56.0 && MT<=40.0 && MET_filters==1 && nVetoElectrons==0 && 1 && MT>=30.0"
}


selections_fakes_whelicity = {
  "fakes": "HLT_SingleMu24 && Mu1_pt>26.0 && Mu1_pt<56.0 && MT>=40.0 && MET_filters==1 && nVetoElectrons==0 && 1",
}
