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

parser = argparse.ArgumentParser("")
parser.add_argument('-p', '--plot',  help="", action='store_true')
parser.add_argument('-m', '--merge',  help="", action='store_true')
parser.add_argument('-v', '--validate',  help="", action='store_true')
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

if args.plot:
   print "Loading shared library..."
   ROOT.gSystem.Load('bin/libAnalysisOnData.so')

def run_one_sample(inputFiles,output_dir, sampledata, sample, verbose=False):
   v          = sampledata[sample]
   dataType   = v['dataType']
   dirs       = v['dirs']
   xsec       = v['xsec']
   ncores     = v['ncores']
   categories = v['categories']
   lumi       = sampledata["common"]["luminosity"]
   era_ratios = sampledata["common"]["era_ratios"]
   isMC       = (dataType=='MC')
   print "sample:      ", sample
   print "num of dirs: ", len(dirs)
   print "dataType:    ", dataType
   print "xsec:        ", xsec
   print "ncores:      ", ncores
   print "categories:  ", categories
   config = ConfigRDF(inputFiles, output_dir, sample+'.root', verbose)
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


def run_multithread_all(sampledata, restrictDataset, output_dir):

   # First pass: run all multithreaded samples
   from multiprocessing import Process

   print "Running multithread..."
   procs = []
   for k,v in sampledata.items():

      if k=='common': continue
      if len(restrictDataset)>0 and (k not in restrictDataset): continue

      if v['ncores']>0: continue

      # inputFiles[0] must be the same as in the key: processing one file at the time
      inputFiles = ROOT.std.vector(ROOT.std.string)()
      for subdir,files in v['dirs'].items():
         for f in files:
            lf = '/scratchssd/sroychow/NanoAOD'+dataYear+'-V1MCFinal/'+str(subdir)+'/'+str(f)+'.root'
            if subdir==k: inputFiles.push_back(lf)
      for subdir,files in v['dirs'].items():
         for f in files:
            lf = '/scratchssd/sroychow/NanoAOD'+dataYear+'-V1MCFinal/'+str(subdir)+'/'+str(f)+'.root'
            if subdir!=k: inputFiles.push_back(lf)

      print "Running on", len(inputFiles), "input files..."

      p = Process(target=run_one_sample, args=(inputFiles, output_dir, sampledata, k))
      p.start()
      procs.append(p)

   for p in procs: 
      p.join()
   return

def run_multicore_all(sampledata, restrictDataset, output_dir):

   # Second pass: run all multicore samples
   print "Running multicore..."
   for k,v in sampledata.items():

      if k=='common': continue
      if len(restrictDataset)>0 and (k not in restrictDataset): continue

      if v['ncores']<=0: continue

      # inputFiles[0] must be the same as in the key: processing one file at the time
      inputFiles = ROOT.std.vector(ROOT.std.string)()
      for subdir,files in v['dirs'].items():
         for f in files:
            lf = '/scratchssd/sroychow/NanoAOD'+dataYear+'-V1MCFinal/'+str(subdir)+'/'+str(f)+'.root'
            if subdir==k: inputFiles.push_back(lf)
      for subdir,files in v['dirs'].items():
         for f in files:
            lf = '/scratchssd/sroychow/NanoAOD'+dataYear+'-V1MCFinal/'+str(subdir)+'/'+str(f)+'.root'
            if subdir!=k: inputFiles.push_back(lf)
      print "Running on", len(inputFiles), "input files..."

      print "Running with {} cores".format(v['ncores'])
      ROOT.ROOT.EnableImplicitMT(v['ncores'])
   
      run_one_sample(inputFiles, output_dir, sampledata, k)

def merge(sampledata):   
   os.system('mkdir -p '+output_dir+'/hadded')
   merged = sampledata["common"]["merged"]
   for k,v in merged.items():
      cmd = 'hadd -j -f '+output_dir+'/hadded/'+k+'.root'
      for s in v:
         cmd += (' '+output_dir+'/'+s+'.root ')
      print cmd
      os.system(cmd)   

def validate(sampledata, vname):
   output = sampledata["common"]["output"]
   for krc,r in output.items():
      print krc
      charge = krc.split('_')[1]
      kr = krc.split('_')[0]
      for kp,p in r.items():
         print '\t'+kp
         fname = p.split('/')[0]
         f     = ROOT.TFile(output_dir+'/hadded/'+fname)
         dname = ((p.split('/')[1].split(':')[0]).replace('*',kr))
         cats  = p.split('/')[1].split(':')[1].split(',')
         for cat in cats:
            systs = []
            for sk,sv in modules_any.items():
               if cat==(sk.split('_')[-1]):
                  systs = sv
            if len(systs)==0: systs.append('')
            print '\t\t'+cat, len(systs)
            for syst in systs:
               tag = syst
               if cat in ['ISO','ID','Trigger']:
                  tag = cat+'_'+tag
               elif cat=='puWeight':
                  tag = cat+syst
               hname = dname+'_'+cat+'/'+dname+'__'+vname+'__'+tag
               f.cd()
               h3 = ROOT.gDirectory.Get(hname)
               if h3==None:
                  continue
               if charge=='Plus': 
                  h3.GetZaxis().SetRange(2,2)
               else:
                  h3.GetZaxis().SetRange(1,1)            
               tot = h3.Project3D("yxe").Integral()
               print '\t\t\t'+syst+' --> '+'{:3.3f}'.format(tot)

         f.Close()

if __name__ == '__main__':
   if args.plot:
      run_multithread_all(sampledata, restrictDataset, output_dir)
      run_multicore_all(sampledata, restrictDataset, output_dir)
   elif args.merge:
      merge(sampledata)
   elif args.validate:
      validate(sampledata, 'SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge')
      
