selections = {
  "SignalPlus": "Vtype==0 && HLT_SingleMu24 && Mu1_pt>26.0 && Mu1_pt<55.0 && MT>=40.0 && MET_filters==1 && nVetoElectrons==0 && 1 && Mu1_charge>0", 
  "SignalMinus": "Vtype==0 && HLT_SingleMu24 && Mu1_pt>26.0 && Mu1_pt<55.0 && MT>=40.0 && MET_filters==1 && nVetoElectrons==0 && 1 && Mu1_charge<0", 
}

selectionVars = { 
  "ptScale" : { "correctedUp" : 1, "correctedDown" : 1}, 
  "jme" : { "jerUp" : 2, "jerDown" : 2 , "jesTotalUp" : 2, "jesTotalDown" : 2, "unclustEnUp" : 2,"unclustEnDown" : 2}
}
