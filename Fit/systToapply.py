##syst type and it's variations
systematicsDict = {
    "Nominal" : [""],
    "mass" : ["mass"],
}
###Mapping of nuisance to which sample they are applicable
systToSampleDict = {
    "mass" : ["LowAcc"],
}
###mapping of nuisance and their type - 
systTypeDict = {
    "mass" : "shape",
}

'''
#ideal
systematicsDict = {
    "Nominal" : [""],
    "mass" : ["mass"],
    "WHSFVars"  : ["WHSFSyst0", "WHSFSyst1","WHSFSyst2","WHSFSystFlat"],
    "ptScaleVars" : [ "corrected"], 
    "jmeVars" : ["jesTotal", "unclustEn"],
    "LHEPdfWeightVars" : ["LHEPdfWeightHess{}".format(i+1) for i in range(60)]
    #"LHEScaleWeightVars" : ["LHEScaleWeight_muR0p5_muF0p5", "LHEScaleWeight_muR0p5_muF1p0","LHEScaleWeight_muR1p0_muF0p5","LHEScaleWeight_muR1p0_muF2OAp0","LHEScaleWeight_muR2p0_muF1p0", "LHEScaleWeight_muR2p0_muF2p0"],
}


systToSampleDict = {
    "mass" : ["Signal", "LowAcc"],
    "WHSFVars"  : ["Signal", "DY","Diboson","Top","Tau","LowAcc"],                                                                        
    "ptScaleVars" : ["Signal", "DY","Diboson","Top","Fake","Tau","LowAcc"],
    "jmeVars" : ["Signal", "DY","Diboson","Top","Fake","Tau","LowAcc"],
    "LHEPdfWeightVars" : ["Signal", "DY", "LowAcc", "Tau" ]                                                                  
    #"LHEScaleWeightVars" : [] 
}

systType = {
    "mass" : "shape"
    "WHSFVars"  : "shape"
    "ptScaleVars" : "shape"
    "jmeVars" : "shape"
    "LHEPdfWeightVars" : "shape" 
    #"LHEScaleWeightVars" : [] 
}

'''
