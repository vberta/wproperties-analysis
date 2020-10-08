systematicsDict = {
    "Nominal": {
        
    },
    "CMSlumi": {
        vars:[],
        procs: ["Signal", "DY","Diboson","Top","Tau","LowAcc"],
        type: "logN"
    },
    "DYxsec":{
        vars:[],
        procs: ["DY"],
        type: "logN"
    },
    "Topxsec":{
        vars:[],
        procs: ["Top"],
        type: "logN"
    },
    "Dibosonxsec":{
        vars:[],
        procs: ["Diboson"],
        type: "logN"
    },
    "mass" : {
        vars:["mass"],
        procs: ["Signal", "LowAcc"],
        type:"shape"},
    "WHSFVars"  : {
        vars:["WHSFSyst0", "WHSFSyst1","WHSFSyst2","WHSFSystFlat"],
        procs: ["Signal", "DY","Diboson","Top","Tau","LowAcc","Fakes"],
        type:"shape"},
    "ptScaleVars" : {
        vars:["corrected"], 
        procs: ["Signal", "DY","Diboson","Top","Tau","LowAcc","Fakes"],
        type: "shape"
    },
    "jmeVars" : {
        vars:["jesTotal", "unclustEn"],
        procs: ["Signal", "DY","Diboson","Top","Tau","LowAcc","Fakes"],
        type: "shape"
    },
    "PrefireWeight":{
        vars:["PrefireWeight"],
        procs: ["Signal", "DY","Diboson","Top","Tau","LowAcc","Fakes"],
        type: "shape"
    }
    "LHEPdfWeightVars" : {
        vars:["LHEPdfWeightHess{}".format(i+1) for i in range(60)],
        procs: ["Signal", "DY","Tau","LowAcc"],
        type: "shape"
    },
    "alphaS" :{
        vars: ["alphaS"],
        procs: ["Signal", "DY","Tau","LowAcc"],
        type: "shape"
    }
}
