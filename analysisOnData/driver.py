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
parser.add_argument('-o', '--output_dir',  type=str, default='test', help="")
parser.add_argument('-y', '--dataYear',type=str, default='2016', help="")
parser.add_argument('-r', '--restrict',type=str, default="",   help="")
args = parser.parse_args()
output_dir = args.output_dir
dataYear = args.dataYear
restrictDataset = [ x for x in args.restrict.split(',') if args.restrict != ""]

samplef = open('./python/samples_'+dataYear+'.json')
sampledata = json.load(samplef)
samplef.close()

def run_one_sample(inputFiles,output_dir, sampledata, k, verbose=False):
   v          = sampledata[k]
   dataType   = v['dataType']
   xsec       = v['xsec']
   ncores     = v['ncores']
   categories = v['categories']
   lumi       = sampledata["common"]["luminosity"]
   era_ratios = sampledata["common"]["era_ratios"]
   isMC       = (dataType=='MC')
   print "key:       ", k
   print "dataType:  ", dataType
   print "xsec:      ", xsec
   print "ncores:    ", ncores
   print "categories:", categories

   config = ConfigRDF(inputFiles, output_dir, k+'.root')
   config.set_sample_specifics(isMC, lumi, xsec, dataYear, era_ratios)   
   ret,ret_base = get_categories(dataType, categories, sampledata["common"])
   if verbose:
      print "Categories:"
      pp.pprint(ret)
      print "Base categories:"
      pp.pprint(ret_base)   
   print "Running..."
   config.run( ret, ret_base )
   return

from multiprocessing import Process

print "Running multithread..."
procs = []
for k,v in sampledata.items():

   if k=='common': continue
   if len(restrictDataset)>0 and (k not in restrictDataset): continue

   if v['ncores']>0: continue

   inputFiles = ROOT.std.vector(ROOT.std.string)()
   for subdirs,files in v['dirs'].items():
      for f in files:
         lf = '/scratchssd/sroychow/NanoAOD'+dataYear+'-V1MCFinal/'+str(subdirs)+'/'+str(f)+'.root'
         if f==k: inputFiles.push_back(lf)
   for subdirs,files in v['dirs'].items():
      for f in files:
         lf = '/scratchssd/sroychow/NanoAOD'+dataYear+'-V1MCFinal/'+str(subdirs)+'/'+str(f)+'.root'
         if f!=k: inputFiles.push_back(lf)

   print "Running on", len(inputFiles), "input files..."

   p = Process(target=run_one_sample, args=(inputFiles, output_dir, sampledata, k))
   p.start()
   procs.append(p)

for p in procs: p.join()

print "Running multicore..."
for k,v in sampledata.items():

   if k=='common': continue
   if len(restrictDataset)>0 and (k not in restrictDataset): continue

   if v['ncores']<=0: continue

   inputFiles = ROOT.std.vector(ROOT.std.string)()
   for subdirs,files in v['dirs'].items():
      for f in files:
         lf = '/scratchssd/sroychow/NanoAOD'+dataYear+'-V1MCFinal/'+str(subdirs)+'/'+str(f)+'.root'
         if f==k: inputFiles.push_back(lf)
   for subdirs,files in v['dirs'].items():
      for f in files:
         lf = '/scratchssd/sroychow/NanoAOD'+dataYear+'-V1MCFinal/'+str(subdirs)+'/'+str(f)+'.root'
         if f!=k: inputFiles.push_back(lf)
   print "Running on", len(inputFiles), "input files..."

   print "Running with {} cores".format(v['ncores'])
   ROOT.ROOT.EnableImplicitMT(v['ncores'])

   run_one_sample(inputFiles, output_dir, sampledata, k)

