import os
import copy
import math
import argparse
import sys
import ROOT

import bkg_utils
import bkg_fakerateAnalyzer

ROOT.gROOT.Reset()
ROOT.gROOT.SetBatch(True)


parser = argparse.ArgumentParser("")
parser.add_argument('-systAna', '--syst',type=int, default=False, help="enable systemtatics analysis")
parser.add_argument('-mainAna', '--mainAna',type=int, default=False, help="main bkg analysis")
parser.add_argument('-correlatedFitAna', '--CFAna',type=int, default=False, help="second run of main ana, with correlated Fit")
parser.add_argument('-comparisonAna', '--compAna',type=int, default=False, help="comparison plots of systematic analysis")
parser.add_argument('-strategySyst', '--straSyst',type=int, default=False, help="strategy systemtatics analysis")
parser.add_argument('-inputDir', '--inputDir',type=str, default='./data/', help="input dir name")
parser.add_argument('-outputDir', '--outputDir',type=str, default='./bkg_V2/', help="output dir name")

args = parser.parse_args()
mainAna = args.mainAna
comparisonAna = args.compAna
correlatedFitAna = args.CFAna
strategySyst = args.straSyst
systAna = args.syst
inputDir = args.inputDir
outputDir = args.outputDir

#internal parameters:
STATANA = True
CORRFITFINAL= True #correlated fit in the final plots
TEMPLATE = True
NOM = ['Nominal','']
EXTRAP = False #extrapolation syst


def fakerate_analysis(systKind, systName,correlatedFit,statAna, template, ptBinning=bkg_utils.ptBinning, etaBinning=bkg_utils.etaBinning, outdir=outputDir, indir=inputDir, extrapSuff='') :
    outdirBkg = outdir+'/bkg_'+systName+extrapSuff        
    if not os.path.isdir(outdirBkg): os.system('mkdir '+outdirBkg)
    
    fake = bkg_fakerateAnalyzer.bkg_analyzer(systKind=systKind,systName=systName,correlatedFit=correlatedFit,statAna=statAna, ptBinning=ptBinning, etaBinning=etaBinning, outdir=outdirBkg, inputDir=indir)
    fake.main_analysis(correlatedFit=correlatedFit,template=template,output4Plots=template,produce_ext_output=True,extrapSuff=extrapSuff)
    if template :
        fake.bkg_plots()


print "----> Background analyzer:"
if not os.path.isdir(outputDir): os.system('mkdir '+outputDir)

if mainAna :
    print "--> Not correlated analysis path:"
    fakerate_analysis(systKind=NOM[0], systName=NOM[1], correlatedFit=False, statAna=False, template = TEMPLATE)
    if systAna :
        for sKind, sList in bkg_utils.bkg_systematics.iteritems():
            for sName in sList :
                print "-> systematic:", sKind,sName
                fakerate_analysis(systKind=sKind, systName=sName, correlatedFit=False, statAna=False, template = TEMPLATE)
    if EXTRAP:
        for lcut, lbin in bkg_utils.looseCutDict.iteritems() :    
            fakerate_analysis(systKind=NOM[0], systName=NOM[1], correlatedFit=False, statAna=False, template = TEMPLATE, extrapSuff=lcut)
        fakeExtrap = bkg_fakerateAnalyzer.bkg_analyzer(systKind=NOM[0],systName=NOM[1],correlatedFit=CORRFITFINAL,statAna=False, ptBinning=bkg_utils.ptBinning, etaBinning=bkg_utils.etaBinning, outdir=outputDir+'/bkg_', inputDir=inputDir)
        if not os.path.isdir(outputDir+'/extrapolation_plots'): os.system('mkdir '+outputDir+'/extrapolation_plots')
        fakeExtrap.extrapolationSyst(extrapDict=bkg_utils.looseCutDict,linearFit=True)
        fakeExtrap.extrapolationSyst(extrapDict=bkg_utils.looseCutDict,linearFit=False)
    
if correlatedFitAna :
    print "--> Correlated analysis path:"
    fakerate_analysis(systKind=NOM[0], systName=NOM[1], correlatedFit=True, statAna=False, template = TEMPLATE)
    if STATANA :
        print "-> statistical uncertainity analysis:"
        fakerate_analysis(systKind=NOM[0], systName=NOM[1], correlatedFit=True, statAna=STATANA, template = TEMPLATE)
    if systAna :
        for sKind, sList in bkg_utils.bkg_systematics.iteritems():
            for sName in sList : 
                print "-> systematatic:", sKind,sName
                fakerate_analysis(systKind=sKind, systName=sName, correlatedFit=True, statAna=False, template = TEMPLATE)

if comparisonAna :
    print "--> Syst comparison plots..."
    fakeFinal = bkg_fakerateAnalyzer.bkg_analyzer(systKind=NOM[0],systName=NOM[1],correlatedFit=CORRFITFINAL,statAna=False, ptBinning=bkg_utils.ptBinning, etaBinning=bkg_utils.etaBinning, outdir=outputDir+'/bkg_'+NOM[1], inputDir=inputDir)
    fakeFinal.syst_comparison(systDict=bkg_utils.bkg_systematics, SymBands=True, outDir=outputDir, noratio=False, statAna=STATANA)


# if strategySyst :
#     print "--> Strategy syst plots..."
#     fakeFinal.strategy_syst(preOutDir=outputDir)