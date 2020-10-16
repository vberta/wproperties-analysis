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
        "type":"shape"
    },
    "WHSFStat"  : {
        "vars": ["WHSFSyst0Eta{}".format(i) for i in range(1, 49)]+["WHSFSyst1Eta{}".format(i) for i in range(1, 49)]+["WHSFSyst2Eta{}".format(i) for i in range(1, 49)],
        "procs": ["Signal", "LowAcc"],
        "type":"shape"},
    "WHSFSyst":{
        "vars": ["WHSFSystFlat"],
        "procs": ["Signal","LowAcc"],
        "type": "shape"},
    #"ptScale" : {
    #    "vars":["corrected"], 
    #    "procs": ["Signal", "DY","Diboson","Top","Tau","LowAcc","Fakes"],
    #    "type": "shape"
    #},
    #"jme" : {
    #    "vars":["jesTotal", "unclustEn"],
    #    "procs": ["Signal", "DY","Diboson","Top","Tau","LowAcc","Fakes"],
    #    "type": "shape"
    #},
    #"PrefireWeight":{
    #    "vars":["PrefireWeight"],
    #    "procs": ["Signal", "DY","Diboson","Top","Tau","LowAcc","Fakes"],
    #    "type": "shape"
    #}
    #"LHEPdfWeight" : {
    #    "vars":["LHEPdfWeightHess{}".format(i+1) for i in range(60)],
    #    "procs": ["Signal", "LowAcc"],
    #    "type": "shape"
    #},
    #"alphaS" :{
    #    "vars": ["alphaS"],
    #    "procs": ["Signal", "DY","Tau","LowAcc"],
    #    "type": "shape"
    #}
}
