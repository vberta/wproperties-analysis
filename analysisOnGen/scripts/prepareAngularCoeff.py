import os
import ROOT
import copy
import sys
import argparse
import math

sys.path.append('../../bkgAnalysis')

ROOT.gROOT.SetBatch()
ROOT.TH1.AddDirectory(False)
ROOT.TH2.AddDirectory(False)
ROOT.gStyle.SetOptStat(0)


parser = argparse.ArgumentParser("")
parser.add_argument('-o','--output', type=str, default='genInput',help="name of the output file")
parser.add_argument('-i','--input', type=str, default='/scratchssd/emanca/wproperties-analysis/analysisOnGen/GenInfo/genInfo.root',help="name of the input root file")

args = parser.parse_args()
OUTPUT = args.output
INPUT = args.input

coeffDict = {
    'A0' : 1.,
    'A1' : 5.,
    'A2' : 20.,
    'A3' : 4.,
    'A4' : 4.,
    'A5' : 5.,
    'A6' : 5.,
    'A7' : 4.,
    'AUL' : 1.,
}

systDict = {
    "_LHEScaleWeight" : ["_LHEScaleWeight_muR0p5_muF0p5", "_LHEScaleWeight_muR0p5_muF1p0","_LHEScaleWeight_muR1p0_muF0p5","_LHEScaleWeight_muR1p0_muF2p0","_LHEScaleWeight_muR2p0_muF1p0", "_LHEScaleWeight_muR2p0_muF2p0"],
    "_LHEPdfWeight" : ["_LHEPdfWeightHess" + str(i)  for i in range(1, 61)],
    "" : [""]
}


#GET HISTOS
hDict = {}
inFile = ROOT.TFile.Open(INPUT)
for sKind, sList in systDict.iteritems():
    for sName in sList :
        hDict[sName+'mapTot'] =  inFile.Get('angularCoefficients'+sKind+'/mapTot'+sName)
        for coeff,div in coeffDict.iteritems() :
            hDict[sName+coeff] =  inFile.Get('angularCoefficients'+sKind+'/harmonics'+coeff+sName)
# get maps
mapTot = inFile.Get('basicSelection/mapTot')
mapAccEta = inFile.Get('basicSelection/mapAccEta')
mapAcc = inFile.Get('basicSelection/mapAcc')
sumw = inFile.Get('basicSelection/sumw')

#BUILD OUTPUT
outFile =  ROOT.TFile(OUTPUT+'.root', "RECREATE")
outFile.cd()
for sKind, sList in systDict.iteritems():
    outFile.mkdir('angularCoefficients'+sKind)
    outFile.cd('angularCoefficients'+sKind) 
    for sName in sList :
         for coeff,div in coeffDict.iteritems() :
            hist = hDict[sName+coeff].Clone()
            if coeff!='AUL' : 
                hist.Divide(hDict[sName+'mapTot'])
                hist.Scale(div)
            if coeff=='A0' :
                for xx in range(1,hist.GetNbinsX()+1) :
                    for yy in range(1,hist.GetNbinsY()+1) :
                        content = hist.GetBinContent(xx,yy)
                        hist.SetBinContent(xx,yy,20./3*(content+1./10.))
            hist.Write()
outFile.mkdir('accMaps')
outFile.cd('accMaps')
mapTot.Write()
mapAccEta.Write()
mapAcc.Write()
sumw.Write()

outFile.Close()






