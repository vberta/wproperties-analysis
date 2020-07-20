import sys
import ROOT
import os
import copy
import argparse
from contextlib import contextmanager


# @contextmanager
# def cd(newdir):
#     prevdir = os.getcwd()
#     os.chdir(os.path.expanduser(newdir))
#     try: 
#         yield

parser = argparse.ArgumentParser("")
parser.add_argument('-bkgInput', '--bkgInput',type=str, default='./data/', help="input dir name for bkgAna")
parser.add_argument('-bkgOutput', '--bkgOutput',type=str, default='./bkg/', help="output dir name for bkgAna")

args = parser.parse_args()
bkgInput = args.bkgInput
bkgOutput = args.bkgOutput


#bkg input preparation 
# if not os.path.isdir('output'): os.system('mkdir output')
# os.system('python runAnalysisOnMC.py 1 0')
# os.system('python runAnalysisOnWJetsMC.py 1 0')
# os.system('python runAnalysisOnData.py 1 0')

# # bkg analysis
# if not os.path.isdir('../bkgAnalysis/'+bkgInput): os.system('mkdir ../bkgAnalysis/'+bkgInput)
# os.system('cp -r output ../bkgAnalysis/+'bkgInput+'/raw)
# os.chdir('../bkgAnalysis')
# os.system('python bkg_prepareHistos.py --inputDir '+bkgInput+'/raw --outputDir '+bkgInput)
# os.system('python bkg_config.py --mainAna 1 --CFAna 1 --inputDir '+bkgInput+'/hadded/ --outputDir '+bkgOutput+' --syst 1 --compAna 1)

#prefit plots
# os.chdir('../analysisOnData')
os.system('python runAnalysisOnMC.py 0 0')
os.system('python runAnalysisOnWJetsMC.py 0 0')
os.system('python runAnalysisOnData.py 0 0')

#plotter
# os.chdir('python')
# os,.system('python prefit_plotter.py --hadd 1 --output ../plotter_output --input ../output/')

