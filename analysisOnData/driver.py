import os
import sys
import ROOT
import json
import argparse
from math import *
from runAnalysisOnData import *
sys.path.append('../data/')
from systematics import *
from selections import *

parser = argparse.ArgumentParser("")

parser.add_argument('-y', '--dataYear',type=int, default=2016, help="")
parser.add_argument('-n', '--ncores',type=int, default=24, help="")
parser.add_argument('-restrict', '--restrict',type=str, default="", help="")

args = parser.parse_args()
dataYear = args.dataYear

restrictDataset = [ x for x in args.restrict.split(',') if args.restrict != ""]

samplef = open('../data/samples_' + str(dataYear) + '.json')
sampledata = json.load(samplef)
samplef.close()
print len(restrictDataset)

wtvariations= systematics['WeightVariations'] if 'WeightVariations' in systematics.keys() else {}

for (k, v) in sampledata.items():
   if len(restrictDataset) and k not in restrictDataset:    continue
   print "Key: " + k
   print "DataType:" + v['datatype']
   print "XSec=",  v['xsec']
   print "Multiprocessing=", v['multiprocessing']
   print "Source files:"
   print "Systematics category(O=None, 1=Full, 2=Full + LHE):", v['systematics'] 

   inputFiles=ROOT.std.vector(ROOT.std.string)()
   for subdirs, files  in v['dir'].items():
      for f in files:
         lf='/scratch/sroychow/NanoAOD2016-V1MCFinal/' + str(subdirs) + '/' + str(f)
         inputFiles.push_back(lf)
         #print lf
   print inputFiles

   _cutMap = {} 
   for region in ['Signal', 'Sideband']:
      cutString = selections[region][v['datatype']]['cut']
      _cutMap['%sPlus' % region] = cutString + ' && Muon_charge[Idx_mu1]>0'
      _cutMap['%sMinus' % region] = cutString + ' && Muon_charge[Idx_mu1]<0'
   
   print _cutMap


   if not v['multiprocessing']:
      runRDFForaSample(24, sampleKey=k, inputFiles=inputFiles, xSec=v['xsec'], dataType=v['datatype'], cutMap = _cutMap, systCategory = v['systematics'], weightVarDict=wtvariations)
   else:
      runRDFForaSample(0, sampleKey=k, inputFiles=inputFiles, xSec=v['xsec'], systCategory = v['systematics'], dataType=v['datatype'], cutMap=_cutMap)
