import os
import ROOT
import copy
import sys
import argparse
import math


ROOT.gROOT.SetBatch()
ROOT.TH1.AddDirectory(False)
ROOT.TH2.AddDirectory(False)
ROOT.gStyle.SetOptStat(0)


parser = argparse.ArgumentParser("")

parser.add_argument('-o','--output', type=str, default='genInput',help="name of the output file")
parser.add_argument('-i','--input', type=str, default='./GenInfo/genInfo.root',help="name of the input root file")
parser.add_argument('-u','--uncorrelate', type=int, default=True,help="if true uncorrelate num and den of Angular Coeff in MC scale variation")


args = parser.parse_args()
OUTPUT = args.output
INPUT = args.input
UNCORR = args.uncorrelate

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
        #hDict[sName+'Y'] =  inFile.Get('angularCoefficients'+sKind+'/Y'+sName)
        #hDict[sName+'Pt'] =  inFile.Get('angularCoefficients'+sKind+'/Pt'+sName)
        for coeff,div in coeffDict.iteritems() :
            hDict[sName+coeff] =  inFile.Get('angularCoefficients'+sKind+'/harmonics'+coeff+sName)
            #hDict[sName+coeff+'Y'] =  inFile.Get('angularCoefficients'+sKind+'/harmonicsY'+coeff+sName)
            #hDict[sName+coeff+'Pt'] =  inFile.Get('angularCoefficients'+sKind+'/harmonicsPt'+coeff+sNamep)
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
    
    sListMod = copy.deepcopy(sList)
    if sKind=='_LHEScaleWeight' and UNCORR :
        sListMod.append("") #add nominal variation
        
    for sName in sListMod :
            hDict[sName+'mapTot'].Write()
            for sNameDen in sListMod :
                if sNameDen!=sName and not (sKind=='_LHEScaleWeight' and UNCORR) : #PDF or correlated Scale
                    continue 
                for coeff,div in coeffDict.iteritems() :
                    hist = hDict[sName+coeff].Clone()
                    #histY = hDict[sName+coeff+'Y'].Clone()
                    #histPt = hDict[sName+coeff+'Pt'].Clone()
                    if coeff!='AUL' : 
                        hist.Divide(hDict[sNameDen+'mapTot'])
                        #histY.Divide(hDict[sName+'Y'])
                        #histPt.Divide(hDict[sName+'Pt'])
                        hist.Scale(div)
                        #histY.Scale(div)
                        #histPt.Scale(div)
                    if coeff=='A0' :
                        for xx in range(1,hist.GetNbinsX()+1) :
                            for yy in range(1,hist.GetNbinsY()+1) :
                                content = hist.GetBinContent(xx,yy)
                                hist.SetBinContent(xx,yy,20./3*(content+1./10.))
                        """
                        for xx in range(1,histY.GetNbinsX()+1):
                            content = histY.GetBinContent(xx)
                            histY.SetBinContent(xx,20./3*(content+1./10.))
                        for xx in range(1,histPt.GetNbinsX()+1):
                            content = histPt.GetBinContent(xx)
                            histPt.SetBinContent(xx,20./3*(content+1./10.))
                        """
                    suff = ''
                    suffDen = ''
                    if sName == "" : suff = '_nom'
                    if sNameDen == '' : suffDen = '_nom'
                    hist.SetName(hist.GetName()+suff+sNameDen+suffDen)
                    hist.SetTitle(hist.GetTitle()+suff+sNameDen+suffDen)
                    hist.Write()
                    #histY.Write()
                    #histPt.Write()
        
outFile.mkdir('accMaps')
outFile.cd('accMaps')
mapTot.Write()
mapAccEta.Write()
mapAcc.Write()
sumw.Write()
#hDict[sName+'Y'].Write()
#hDict[sName+'Pt'].Write()

outFile.Close()

