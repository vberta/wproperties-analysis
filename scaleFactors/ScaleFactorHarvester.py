import math
import ROOT
import sys
import argparse
ROOT.gROOT.SetBatch(True)

#########################  DOCUMENTATION BEFORE THE MAIN FUNCTION #######################

def SFHarvester_nom(fileDict) :
    outDict = {}
    outDict['Trigger'+'Plus'] = fileDict['Trigger'+'Plus'].Get('scaleFactor')
    outDict['Trigger'+'Minus'] = fileDict['Trigger'+'Minus'].Get('scaleFactor')
    outDict['Reco'] = fileDict['Reco'].Get('scaleFactor_etaInterpolated')
    for ind, h in outDict.iteritems() :
        if 'Reco' in ind :
            h.Rebin2D(3,5)
            rebFactor=15
        else :
            h.RebinY(5)
            rebFactor=5
        for xx in range(1,h.GetXaxis().GetNbins()+1) :
            for yy in range(1,h.GetYaxis().GetNbins()+1) :
                h.SetBinContent(xx,yy,h.GetBinContent(xx,yy)/rebFactor)
    return outDict


def SFHarvester_triggerSyst(fileDict, SFhisto, RATIO=True) :
    outDict = {}
    signList = ['Plus', 'Minus']
    parList = ['0','1','2']
    systDict = {}
    
    for s in signList :
        for par in parList :
            systDict['Trigger'+s+'Syst'+par+'Ratio']= fileDict['Trigger'+s+'syst'].Get('p'+par)
            outDict['Trigger'+s+'Syst'+par+'Up'] = SFhisto['Trigger'+s].Clone('Trigger'+s+'Syst'+par+'Up')
            outDict['Trigger'+s+'Syst'+par+'Down'] = SFhisto['Trigger'+s].Clone('Trigger'+s+'Syst'+par+'Down')
            nEtaBins = outDict['Trigger'+s+'Syst'+par+'Up'].GetXaxis().GetNbins()
            nPtBins = outDict['Trigger'+s+'Syst'+par+'Up'].GetYaxis().GetNbins()
            for eta in range(1,nEtaBins+1) :
                for pt in range(1,nPtBins+1) :
                    valUp = outDict['Trigger'+s+'Syst'+par+'Up'].GetBinContent(eta,pt)*(1+systDict['Trigger'+s+'Syst'+par+'Ratio'].GetBinContent(eta,pt))
                    valDown = outDict['Trigger'+s+'Syst'+par+'Down'].GetBinContent(eta,pt)*(1-systDict['Trigger'+s+'Syst'+par+'Ratio'].GetBinContent(eta,pt))
                    outDict['Trigger'+s+'Syst'+par+'Up'].SetBinContent(eta,pt,valUp)
                    outDict['Trigger'+s+'Syst'+par+'Down'].SetBinContent(eta,pt,valDown)
    if RATIO :
       outDict.update(systDict)
                
    return outDict

           
def SFHarvester_recoSyst(fileDict, SFhisto, RATIO=True) :
    outDict = {}
    era_ratios = [0.548,0.452]
    print "WARNING: era ratios hardcoded [BCDEF, GH]=", era_ratios
    parList = ['Syst','Stat']
    systDict = {}
    
    for par in parList :
        hBCDEF=fileDict['Reco'+'syst'+'BCDEF'].Get('NUM_TightRelIso_DEN_MediumID_eta_pt_'+par.lower())
        hGH=fileDict['Reco'+'syst'+'GH'].Get('NUM_TightRelIso_DEN_MediumID_eta_pt_'+par.lower())
        outDict['Reco'+par+'Up'] = SFhisto['Reco'].Clone('Reco'+par+'Up')
        outDict['Reco'+par+'Down'] = SFhisto['Reco'].Clone('Reco'+par+'Down')
        nEtaBins = outDict['Reco'+par+'Up'].GetXaxis().GetNbins()
        nPtBins = outDict['Reco'+par+'Up'].GetYaxis().GetNbins()
        
        if RATIO :
           systDict['Reco'+par+'Ratio'] =  SFhisto['Reco'].Clone('Reco'+par+'Ratio') #dummy clone to build the binning
           systDict['Reco'+par+'Ratio'].GetZaxis().SetRangeUser(-0.01,0.01)
           
        for eta in range(1,nEtaBins+1) :
            for pt in range(1,nPtBins+1) :
                etaBin = hBCDEF.GetXaxis().FindBin(outDict['Reco'+par+'Up'].GetXaxis().GetBinCenter(eta))
                ptBin = hBCDEF.GetYaxis().FindBin(outDict['Reco'+par+'Up'].GetYaxis().GetBinCenter(pt))
                val = hBCDEF.GetBinError(etaBin,ptBin)*era_ratios[0]+hGH.GetBinError(etaBin,ptBin)*era_ratios[1]
                valUp = outDict['Reco'+par+'Up'].GetBinContent(eta,pt)+val
                valDown = outDict['Reco'+par+'Down'].GetBinContent(eta,pt)-val
                outDict['Reco'+par+'Up'].SetBinContent(eta,pt,valUp)
                outDict['Reco'+par+'Down'].SetBinContent(eta,pt,valDown)
                if RATIO :
                    systDict['Reco'+par+'Ratio'].SetBinContent(eta,pt,val/SFhisto['Reco'].GetBinContent(eta,pt))
                    systDict['Reco'+par+'Ratio'].SetBinError(eta,pt,0)              
    if RATIO :
       outDict.update(systDict)
                
    return outDict        
    

#####################################################################################################################
#
#   AUTHOR: V. Bertacchi (06/2020)
#
#   USAGE: python SaleFactorHarvester.py (--output_name) (--saveRatio) (--syst)
#   
#   INPUT:
#   expected to run in the directory where is placed data/SF_*.root
#   the .root input name are hardcoded in the main function
#
#   OUTPUT STRUCTURE: 
#   main dir: eta vs pt SF and their Up/Down variation
#   "ratios" dir: eta vs pt (variedSF-nominalSF)/nominalSF
#   
#   OUTPUT NAMING CONVENTION: Kind+(Sign)+Syst+("ratio")
#   Kind = "Trigger", "Reco"
#   Sign (Trigger) = "Plus", "Minus"
#   Sign (Reco) = ""
#   Syst = SystName+"Up", SystName+"Down"
#   SystName (Trigger) = "Syst0","Syst1","Syst2" (they are the variation of the parameter of: [0]*erf((x-[1])/[2]) )
#   SystName (Reco) = "Syst", "Stat"
#
#   #Which SF are used?
#   The central values are from WHeliciy (SMP18-012)
#   the variation of trigger are from WHelicity statistical variation of erf
#   the variation of the Reco=ID+ISO are from the ISO SF of the POG 
#   (because in SMP18-012 they overestimated it and they did not use for FR and PR eval., where ISO alone is needed)
#
#
#####################################################################################################################
    

parser = argparse.ArgumentParser("")
parser.add_argument('-o','--output_name', type=str, default='ScaleFactors',help="name of the output root file")
parser.add_argument('-saveRatio', '--saveRatio',type=int, default=True, help="1=Save also sf variation ratios")
parser.add_argument('-syst', '--syst',type=int, default=True, help="1=run the syst. variation")

args = parser.parse_args()
RATIO = args.saveRatio  # ratio = (variedSF-nominalSF)/nominalSF
OUTPUT = args.output_name
SYST = args.syst

#input files
fileDict = {}
fileDict['Trigger'+'Plus'] = ROOT.TFile.Open('data/SF_WHelicity_Trigger_Plus.root')
fileDict['Trigger'+'Minus'] = ROOT.TFile.Open('data/SF_WHelicity_Trigger_Minus.root')
fileDict['Reco'] = ROOT.TFile.Open('data/SF_WHelicity_Reco.root')
if SYST: 
    fileDict['Trigger'+'Plus'+'syst'] = ROOT.TFile.Open('data/SF_WHelicity_Trigger_Plus_syst.root')
    fileDict['Trigger'+'Minus'+'syst'] = ROOT.TFile.Open('data/SF_WHelicity_Trigger_Minus_syst.root')
    fileDict['Reco'+'syst'+'BCDEF'] = ROOT.TFile.Open('data/SF_POG_iso_BCDEF.root')
    fileDict['Reco'+'syst'+'GH'] = ROOT.TFile.Open('data/SF_POG_iso_GH.root')

#nominal SF
SFhisto = SFHarvester_nom(fileDict)

if SYST : #variation
    SFhisto.update(SFHarvester_triggerSyst(fileDict, SFhisto,RATIO))
    SFhisto.update(SFHarvester_recoSyst(fileDict, SFhisto,RATIO))

#output saving
output = ROOT.TFile(OUTPUT+".root", "recreate")
output.cd()
for ind, histo in SFhisto.iteritems() :
    histo.SetName(ind)
    if 'Ratio' in ind : continue
    histo.Write()
    
if RATIO :
    direc = output.mkdir('ratios')
    direc.cd()
    for ind, histo in SFhisto.iteritems() :
        if not 'Ratio' in ind : continue
        histo.Write()