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

selectionVars = { 
  "ptScale" : { "correctedUp" : 1, "correctedDown" : 1}, 
  "jme" : { "jerUp" : 2, "jerDown" : 2 , "jesTotalUp" : 2, "jesTotalDown" : 2, "unclustEnUp" : 2,"unclustEnDown" : 2}
}
