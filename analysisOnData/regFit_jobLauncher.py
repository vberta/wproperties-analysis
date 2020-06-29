import os
import sys
import json
import argparse
import ROOT
import pprint 
import math
import numpy as np
from array import array
import scipy
import copy
from scipy import special
from scipy import stats

#scale
LHElist = ["muR0p5_muF0p5", "muR0p5_muF1p0", "muR1p0_muF0p5","muR1p0_muF2p0","muR2p0_muF1p0","muR2p0_muF2p0"]
for syst in LHElist :
    print "lounching", syst, "..."
    os.system('nohup python regularizationFit.py --validation_only 0 -o TEST_syst --map01 0 --syst_kind LHEScaleWeight --syst_name '+syst+' > log_LHEScaleWeights_'+syst+'.log 2>&1 &')
    
    # rebuild
    # os.system('nohup python regularizationFit.py --validation_only 1 -o TEST_syst_scale --map01 0 --syst_kind LHEScaleWeight --syst_name '+syst+' --input_name regularizationFit_range11__LHEScaleWeight_'+syst+' > log_LHEScaleWeights_'+syst+'.log 2>&1 &')
    

#PDF
PDFList = ['alphaSDown','alphaSUp']
# for i in range(1,30) : #needed to avoid to use 101 CPU
# for i in range(30,60) :
# for i in range(60,100) :
PDFList = []
for i in range(1,100) :
    PDFList.append(str(i)+'replica')
for syst in PDFList :
    print "lounching", syst, "..."
    os.system('nohup python regularizationFit.py --validation_only 0 -o TEST_syst_PDF --map01 0 --syst_kind LHEPdfWeight --syst_name '+syst+' > log_LHEPdfWeight_'+syst+'.log 2>&1 &')