import os
import sys
import json
import argparse
import ROOT
import pprint 
pp = pprint.PrettyPrinter(indent=2)

sys.path.append('python/')

from configRDF import *
from utils import *

print "Loading shared library..."
ROOT.gSystem.Load('bin/libAnalysisOnData.so')

parser = argparse.ArgumentParser("")
parser.add_argument('-o', '--output',  type=str, default='test', help="")
parser.add_argument('-y', '--dataYear',type=str, default='2016', help="")
parser.add_argument('-r', '--restrict',type=str, default="",   help="")
args = parser.parse_args()
output = args.output
dataYear = args.dataYear
restrictDataset = [ x for x in args.restrict.split(',') if args.restrict != ""]

samplef = open('./python/samples_'+dataYear+'.json')
sampledata = json.load(samplef)
samplef.close()

for k,v in sampledata.items():
   if k=='common': continue
   if len(restrictDataset)>0 and k not in restrictDataset: 
       continue
   dataType = v['dataType']
   isMC   = (dataType=='MC')
   xsec   = v['xsec']
   ncores = v['ncores']
   categories = v['categories']
   lumi = sampledata["common"]["luminosity"]
   era_ratios = sampledata["common"]["era_ratios"]

   print "key:       ", k
   print "dataType:  ", dataType
   print "xsec:      ", xsec
   print "ncores:    ", ncores
   print "categories:", categories

   inputFiles = ROOT.std.vector(ROOT.std.string)()
   for subdirs,files in v['dirs'].items():
      for f in files:
         #lf = '/scratch/sroychow/NanoAOD'+dataYear+'-V1MCFinal/'+str(subdirs)+'/'+str(f)+'.root'
         lf = '/scratchssd/bianchini/NanoAOD'+dataYear+'-V1MCFinal/'+str(subdirs)+'/'+str(f)+'.root'
         inputFiles.push_back(lf)
   print "Running on", len(inputFiles), "input files..."

   print "Running with {} cores".format(ncores)
   ROOT.ROOT.EnableImplicitMT(ncores)

   config = ConfigRDF(inputFiles, output, k+'.root')
   config.set_sample_specifics(isMC, lumi, xsec, dataYear, era_ratios)
   
   ret,ret_base = get_categories(dataType, categories, sampledata["common"])
   print "Categories:"
   pp.pprint(ret)
   print "Base categories:"
   pp.pprint(ret_base)   
   print "Running..."
   config.run( ret, ret_base )
