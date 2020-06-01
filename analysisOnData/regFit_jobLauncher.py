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

LHElist = ["muR0p5_muF0p5", "muR0p5_muF1p0", "muR1p0_muF0p5","muR1p0_muF2p0","muR2p0_muF1p0","muR2p0_muF2p0"]
for syst in LHElist :
    print "lounching", syst, "..."
    os.system('nohup python regularizationFit.py --validation_only 0 -o TEST_syst --map01 0 --syst_kind LHEScaleWeight --syst_name '+syst+' > log_LHEScaleWeights_'+syst+'.log 2>&1 &')