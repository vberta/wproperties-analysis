import sys
import ROOT
import os
import copy
import argparse
# from contextlib import contextmanager

################################################################################################################################################
#
#  usage: python runTheMatrix --outputDir OUTPUT --bkgOutput BKGOUT --ncores 64 --bkgFile MYBKG --bkgPrep 1 --bkgAna 1 --prefit 1 --plotter 1
#
#  each parameters is described below in the argparse
#
#  NB: if --bkgFile myBKG --> special string to use the file that runTheMatrix produce at step2. 
#
#################################################################################################################################################

# @contextmanager
# def cd(newdir):
#     prevdir = os.getcwd()
#     os.chdir(os.path.expanduser(newdir))
#     try: 
#         yield

parser = argparse.ArgumentParser("")
parser.add_argument('-outputDir', '--outputDir',type=str, default='output/', help="output dir name of step1 and step3 (inside analysisOnData/)")
parser.add_argument('-bkgOutput', '--bkgOutput',type=str, default='bkg/', help="output dir name for bkgAna (inside bkgAnalysis/)")
parser.add_argument('-bkgFile', '--bkgFile',type=str, default='/scratch/bertacch/wmass/wproperties-analysis/bkgAnalysis/TEST_runTheMatrix/bkg_parameters_CFstatAna.root', help="bkg parameters file path/name.root, or the special 'MYBKG' for the one produced in the same loop")
parser.add_argument('-ncores', '--ncores',type=int, default=64, help="number of cores used")
parser.add_argument('-step1', '--bkgPrep',type=int, default=False, help="run the bkg input preparation")
parser.add_argument('-step2', '--bkgAna',type=int, default=False, help="run the bkg analysis")
parser.add_argument('-step3', '--prefit',type=int, default=False, help="run the prefit hitograms building")
parser.add_argument('-step4', '--plotter',type=int, default=False, help="run the prfit plotter, the result are saved in outputDir/plot/")


args = parser.parse_args()
outputDir = args.outputDir
bkgOutput = args.bkgOutput
bkgFile = args.bkgFile
ncores = str(args.ncores)
step1 = args.bkgPrep
step2 = args.bkgAna
step3 = args.prefit
step4 = args.plotter

if bkgFile == 'MYBKG' :
    bkgFile = '../bkgAnalysis/'+bkgOutput+'/bkg_parameters_CFstatAna.root'
    
    if not step2 :
        raw_input('You are using self-produced bkg file but you are not running step2, are you sure? [press Enter to continue]')

if step1 :
    print "step1: bkg input preparation... "
    os.chdir('./analysisOnData')
    if not os.path.isdir(outputDir): os.system('mkdir '+ outputDir)
    os.system('python runAnalysisOnMC.py --pretend 0 --ncores '+ncores+' --outputDir '+outputDir)
    os.system('python runAnalysisOnWJetsMC.py --pretend 0 --ncores '+ncores+' --outputDir '+outputDir)
    os.system('python runAnalysisOnData.py    --runBKG 1 --pretend 0 --ncores '+ncores+' --outputDir '+outputDir)
    os.chdir('../')

if step2 :
    print "step2: bkg analysis..."
    if not os.path.isdir('bkgAnalysis/'+bkgOutput): os.system('mkdir bkgAnalysis/'+bkgOutput)
    if not os.path.isdir('bkgAnalysis/'+bkgOutput+'/bkgInput/'): os.system('mkdir bkgAnalysis/'+bkgOutput+'/bkgInput/')
    os.chdir('bkgAnalysis')
    os.system('python bkg_prepareHistos.py --inputDir ../analysisOnData/'+outputDir+' --outputDir '+bkgOutput+'/bkgInput/')
    os.system('python bkg_config.py --mainAna 1 --CFAna 1 --inputDir '+bkgOutput+'/bkgInput/hadded/ --outputDir '+bkgOutput+' --syst 1 --compAna 1')
    os.chdir('../')

if step3 :
    print "step3: prefit plots..."
    os.chdir('analysisOnData')
    if not os.path.isdir(outputDir): os.system('mkdir '+ outputDir)
    #os.system('python runAnalysisOnMC.py      --runBKG 0 --pretend 0 --ncores '+ncores+' --outputDir '+outputDir)
    #os.system('python runAnalysisOnWJetsMC.py --runBKG 0 --pretend 0 --ncores '+ncores+' --outputDir '+outputDir)
    os.system('python runAnalysisOnData.py --runBKG 0 --pretend 0 --ncores '+ncores+' --outputDir '+outputDir+' --bkgFile '+bkgFile)
    os.chdir('../')

if step4 :
    print "step4: plotter..."
    os.chdir('analysisOnData/python')
    if not os.path.isdir('../'+outputDir): os.system('mkdir ../'+outputDir)
    os.system('python plotter_prefit.py --hadd 1 --output ../'+outputDir+'/plot/ --input ../'+outputDir+' --systComp 1')
    
    sys.path.append('../../bkgAnalysis')
    import bkg_utils
    for sKind,sList in bkg_utils.bkg_systematics.iteritems() : 
        skipList = ""
        for sKindInt,sListInt in bkg_utils.bkg_systematics.iteritems() :
            if sKindInt==sKind : continue
            else : skipList+= ' '+str(sKindInt)
        print "Skipped systematics:", skipList 
        os.system('python plotter_prefit.py --hadd 1 --output ../'+outputDir+'/plot_only_'+str(sKind)+' --input ../'+outputDir+' --systComp 1 --skipSyst '+skipList)
