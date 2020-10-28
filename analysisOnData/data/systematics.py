systematics = {
    #"puWeight"  : (["puWeightUp", "puWeightDown"],"puWeightVars"),
    "PrefireWeight"  : (["_PrefireWeightUp", "_PrefireWeightDown"],"PrefireWeightVars"),
    "WHSF"  : (["_WHSFSyst0Up", "_WHSFSyst1Up","_WHSFSyst2Up","_WHSFSystFlatUp","_WHSFSyst0Down", "_WHSFSyst1Down","_WHSFSyst2Down","_WHSFSystFlatDown"],"WHSFVars"),
    #"LHEScaleWeight" : (["_LHEScaleWeight_muR0p5_muF0p5", "_LHEScaleWeight_muR0p5_muF1p0","_LHEScaleWeight_muR1p0_muF0p5","_LHEScaleWeight_muR1p0_muF2p0","_LHEScaleWeight_muR2p0_muF1p0","_LHEScaleWeight_muR2p0_muF2p0"], "LHEScaleWeightred"),
    "LHEPdfWeight" : (["_LHEPdfWeightHess{}".format(i+1) for i in range(60)], "LHEPdfWeightHess"),
    "alphaS"       : (["_alphaSUp", "_alphaSDown"], "alphaSVars"),
}
