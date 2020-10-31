systematicsDict = {
    "Nominal": {
    },
    #"CMSlumi": {
    #    "vars":[],
    #    "procs": ["Signal", "DY","Diboson","Top","Tau","LowAcc"],
    #    "type": "logN"
    #},
    #"DYxsec":{
    #    "vars":[],
    #    "procs": ["DY"],
    #    "type": "logN"
    #},
    #"Topxsec":{
    #    "vars":[],
    #    "procs": ["Top"],
    #    "type": "logN"
    #},
    #"Dibosonxsec":{
    #    "vars":[],
    #    "procs": ["Diboson"],
    #    "type": "logN"
    #},
    "mass" : {
        "vars":["mass"],
        "procs": ["Signal", "LowAcc"],
        "type": "shapeNoConstraint"
    },
    #"WHSFStat"  : {
    #    "vars": ["WHSFSyst0Eta{}".format(i) for i in range(1, 49)]+["WHSFSyst1Eta{}".format(i) for i in range(1, 49)]+["WHSFSyst2Eta{}".format(i) for i in range(1, 49)],
    #    "procs": ["Signal", "LowAcc"],
    #    "type":"shape"},
    #"WHSFSyst":{
    #    "vars": ["WHSFSystFlat"],
    #    "procs": ["Signal","LowAcc"],
    #    "type": "shape"},
    #"ptScale" : {
    #    "vars": ["Eta{}zptsyst".format(j) for j in range(1, 5)] + ["Eta{}Ewksyst".format(j) for j in range(1, 5)] + ["Eta{}deltaMsyst".format(j) for j in range(1, 5)]+["Eta{}stateig{}".format(j, i) for i in range(0, 99) for j in range(1, 5)],
    #    "procs": ["Signal"],
    #    "type": "shape"
    #},
    #"jme" : {
    #    "vars":["jesTotal", "unclustEn"],
    #    "procs": ["Signal", "LowAcc"],
    #    "type": "shape"
    #},
    #"PrefireWeight":{
    #    "vars":["PrefireWeight"],
    #    "procs": ["Signal", "LowAcc"],
    #    "type": "shape"
    #},
    #"LHEPdfWeight" : {
    #    "vars":["LHEPdfWeightHess{}".format(i+1) for i in range(60)],
    #    "procs": ["Signal", "LowAcc"],
    #    "type": "shape"
    #},
    #"alphaS" :{
    #    "vars": ["alphaS"],
    #    "procs": ["Signal", "LowAcc"],
    #    "type": "shape"
    #}
}
