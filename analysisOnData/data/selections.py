selections = {
  "QCDPlus":  "Vtype==1 && HLT_SingleMu24 && Mu1_pt>25. && MT>0. && MET_filters==1 && nVetoElectrons==0 && 1 && Mu1_charge>0", 
  "QCDMinus": "Vtype==1 && HLT_SingleMu24 && Mu1_pt>25. && MT>0. && MET_filters==1 && nVetoElectrons==0 && 1 && Mu1_charge<0", 
  "SignalPlus": "Vtype==0 && HLT_SingleMu24 && Mu1_pt>25. && MT>0. && MET_filters==1 && nVetoElectrons==0 && 1 && Mu1_charge>0", 
  "SignalMinus": "Vtype==0 && HLT_SingleMu24 && Mu1_pt>25. && MT>0. && MET_filters==1 && nVetoElectrons==0 && 1 && Mu1_charge<0"
}

selectionVars = { 
  "correctedUp" : 1, "correctedDown" : 1, "jerUp" : 2, "jerDown" : 2, 
  "jesTotalUp" : 2, "jesTotalDown" : 2, "unclustEnUp" : 2,"unclustEnDown" : 2
}
