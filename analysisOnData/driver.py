import os
import sys
import json
import argparse
import ROOT

sys.path.append('python/')

from configRDF import *
from utils import *

print "Loading shared library..."
ROOT.gSystem.Load('bin/libAnalysisOnData.so')

parser = argparse.ArgumentParser("")
parser.add_argument('-o', '--output',  type=str, default='test', help="")
parser.add_argument('-y', '--dataYear',type=str, default='2016', help="")
parser.add_argument('-l', '--lumi',    type=float, default=1.0,  help="")
parser.add_argument('-r', '--restrict',type=str, default="",   help="")
args = parser.parse_args()
output = args.output
dataYear = args.dataYear
lumi = args.lumi
restrictDataset = [ x for x in args.restrict.split(',') if args.restrict != ""]

samplef = open('./python/samples_'+dataYear+'.json')
sampledata = json.load(samplef)
samplef.close()

for k,v in sampledata.items():
   if len(restrictDataset)>0 and k not in restrictDataset: 
       continue
   dataType = v['dataType']
   isMC   = (dataType=='MC')
   xsec   = v['xsec']
   ncores = v['ncores']
   categories = v['categories']

   print "key:       ", k
   print "dataType:  ", dataType
   print "xsec:      ", xsec
   print "ncores:    ", ncores
   print "categories:", categories

   inputFiles = ROOT.std.vector(ROOT.std.string)()
   for subdirs,files in v['dirs'].items():
      for f in files:
         #lf = '/scratch/sroychow/NanoAOD'+dataYear+'-V1MCFinal/'+str(subdirs)+'/'+str(f)+'.root'
         lf = '/scratchssd/bianchini/'+str(f)+'.root'
         inputFiles.push_back(lf)
   print "Running on", len(inputFiles), "input files..."

   print "Running with {} cores".format(ncores)
   ROOT.ROOT.EnableImplicitMT(ncores)

   config = ConfigRDF(inputFiles, output, k+'.root')
   config.set_sample_specifics(isMC, lumi, xsec, dataYear, v['era_ratios'])
   
   ret = get_categories(dataType, categories)
   print ret
   config.run( ret )
