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

# selections_bkg = {
#   "Signal":         "Vtype==0 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT>=40.0 && MET_filters==1 && nVetoElectrons==0 && 1",
#   "Signal_aiso":    "Vtype==1 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT>=40.0 && MET_filters==1 && nVetoElectrons==0 && 1",
#   "Sideband":       "Vtype==0 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=30.0 && MET_filters==1 && nVetoElectrons==0 && 1",
#   "Sideband_aiso":  "Vtype==1 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=30.0 && MET_filters==1 && nVetoElectrons==0 && 1",
#   "Sideband10":       "Vtype==0 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=10.0 && MET_filters==1 && nVetoElectrons==0 && 1",
#   "Sideband_aiso10":  "Vtype==1 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=10.0 && MET_filters==1 && nVetoElectrons==0 && 1", 
#   "Sideband20":       "Vtype==0 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=20.0 && MET_filters==1 && nVetoElectrons==0 && 1 && MT>=10.0",
#   "Sideband_aiso20":  "Vtype==1 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=20.0 && MET_filters==1 && nVetoElectrons==0 && 1 && MT>=10.0", 
#   "Sideband30":       "Vtype==0 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=30.0 && MET_filters==1 && nVetoElectrons==0 && 1 && MT>=20.0",
#   "Sideband_aiso30":  "Vtype==1 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=30.0 && MET_filters==1 && nVetoElectrons==0 && 1 && MT>=20.0",
#   "Sideband40":       "Vtype==0 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=40.0 && MET_filters==1 && nVetoElectrons==0 && 1 && MT>=30.0",
#   "Sideband_aiso40":  "Vtype==1 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=40.0 && MET_filters==1 && nVetoElectrons==0 && 1 && MT>=30.0",
#   "Sideband50":       "Vtype==0 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=50.0 && MET_filters==1 && nVetoElectrons==0 && 1 && MT>=40.0",
#   "Sideband_aiso50":  "Vtype==1 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=50.0 && MET_filters==1 && nVetoElectrons==0 && 1 && MT>=40.0",
#   "Sideband60":       "Vtype==0 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=60.0 && MET_filters==1 && nVetoElectrons==0 && 1 && MT>=50.0",
#   "Sideband_aiso60":  "Vtype==1 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=60.0 && MET_filters==1 && nVetoElectrons==0 && 1 && MT>=50.0",
#   "Sideband70":       "Vtype==0 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=70.0 && MET_filters==1 && nVetoElectrons==0 && 1 && MT>=60.0",
#   "Sideband_aiso70":  "Vtype==1 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=70.0 && MET_filters==1 && nVetoElectrons==0 && 1 && MT>=60.0",
#   "Sideband80":       "Vtype==0 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=80.0 && MET_filters==1 && nVetoElectrons==0 && 1 && MT>=70.0",
#   "Sideband_aiso80":  "Vtype==1 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=80.0 && MET_filters==1 && nVetoElectrons==0 && 1 && MT>=70.0",
#   "Sideband90":       "Vtype==0 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=90.0 && MET_filters==1 && nVetoElectrons==0 && 1 && MT>=80.0",
#   "Sideband_aiso90":  "Vtype==1 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=90.0 && MET_filters==1 && nVetoElectrons==0 && 1 && MT>=80.0",
#   "Sideband100":      "Vtype==0 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=100.0 && MET_filters==1 && nVetoElectrons==0 && 1 && MT>=90.0",
#   "Sideband_aiso100": "Vtype==1 && HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT<=100.0 && MET_filters==1 && nVetoElectrons==0 && 1 && MT>=90.0"
# }

selections_fakes = {
  "fakes": "HLT_SingleMu24 && Mu1_pt>25.0 && Mu1_pt<55.0 && MT>=40.0 && MET_filters==1 && nVetoElectrons==0 && 1", 
  }

selectionVars = { 
  "ptScale" : { "_correctedUp" : 1, "_correctedDown" : 1}, 
  # "jme" : { "_jerUp" : 2, "_jerDown" : 2 , "_jesTotalUp" : 2, "_jesTotalDown" : 2, "_unclustEnUp" : 2,"_unclustEnDown" : 2}
  "jme" : {"_jesTotalUp" : 2, "_jesTotalDown" : 2, "_unclustEnUp" : 2,"_unclustEnDown" : 2}
}

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
