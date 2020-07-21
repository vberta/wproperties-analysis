import sys
import ROOT
import os
import copy
import argparse
from contextlib import contextmanager

#########################################################################################################################
#
#  usage: python runTheMatrix --bkgInput BKGIN --bkgOutput BKGOUT --bkgPrep 1 --bkgAna 1 --prefit 1 --plotter 1
#
#  each parameters is described below in the argparse
#
#  NB: the name of the BKGOUT/bkg_parameters_CFstatAna.root should be written by yourself inside runAnalysisOnData.py
#
#########################################################################################################################

# @contextmanager
# def cd(newdir):
#     prevdir = os.getcwd()
#     os.chdir(os.path.expanduser(newdir))
#     try: 
#         yield

parser = argparse.ArgumentParser("")
parser.add_argument('-bkgInput', '--bkgInput',type=str, default='./data/', help="input dir name for bkgAna")
parser.add_argument('-bkgOutput', '--bkgOutput',type=str, default='./bkg/', help="output dir name for bkgAna")
parser.add_argument('-step1', '--bkgPrep',type=int, default=False, help="run the bkg input preparation")
parser.add_argument('-step2', '--bkgAna',type=int, default=False, help="run the bkg analysis")
parser.add_argument('-step3', '--prefit',type=int, default=False, help="run the prefit hitograms building")
parser.add_argument('-step4', '--plotter',type=int, default=False, help="run the prfit plotter")


args = parser.parse_args()
bkgInput = args.bkgInput
bkgOutput = args.bkgOutput
step1 = args.bkgPrep
step2 = args.bkgAna
step3 = args.prefit
step4 = args.plotter

if step1 :
    #bkg input preparation 
    os.chdir('/analysisOnData')
    if not os.path.isdir('output'): os.system('mkdir output')
    os.system('python runAnalysisOnMC.py 1 0')
    os.system('python runAnalysisOnWJetsMC.py 1 0')
    os.system('python runAnalysisOnData.py 1 0')

if step2 :
    # bkg analysis
    if not os.path.isdir('../bkgAnalysis/'+bkgInput): os.system('mkdir ../bkgAnalysis/'+bkgInput)
    os.system('cp -r output ../bkgAnalysis/+'bkgInput+'/raw)
    os.chdir('../bkgAnalysis')
    os.system('python bkg_prepareHistos.py --inputDir '+bkgInput+'/raw --outputDir '+bkgInput)
    os.system('python bkg_config.py --mainAna 1 --CFAna 1 --inputDir '+bkgInput+'/hadded/ --outputDir '+bkgOutput+' --syst 1 --compAna 1)

if step3 :
    #prefit plots
    os.chdir('../analysisOnData')
    os.system('python runAnalysisOnMC.py 0 0')
    os.system('python runAnalysisOnWJetsMC.py 0 0')
    os.system('python runAnalysisOnData.py 0 0')

if step4 :
    #plotter
    os.chdir('python')
    os,.system('python prefit_plotter.py --hadd 1 --output ../plotter_output --input ../output/')

