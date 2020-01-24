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
parser.add_argument('-r', '--rdf',       help="", action='store_true')
parser.add_argument('-m', '--merge',     help="", action='store_true')
parser.add_argument('-d', '--dictionary',help="", action='store_true')
parser.add_argument('-o', '--output_dir',type=str, default='TEST', help="")
parser.add_argument('-y', '--dataYear',  type=str, default='2016', help="")
parser.add_argument('-i', '--input',     type=str, default="",     help="")
args = parser.parse_args()
output_dir = args.output_dir
dataYear = args.dataYear
restrictDataset = [ x for x in args.input.split(',') if args.input != ""]

#whoami = 'sroychow'
whoami = 'bianchini'

samplef = open('./python/samples_'+dataYear+'.json')
sampledata = json.load(samplef)
samplef.close()

if args.rdf:
   print "Loading shared library..."
   ROOT.gSystem.Load('bin/libAnalysisOnData.so')

def run_one_sample(inputFiles,output_dir, sampledata, sample, verbose=True):
   v          = sampledata[sample]
   dataType   = v['dataType']
   dirs       = v['dirs']
   xsec       = v['xsec']
   ncores     = v['ncores']
   categories = v['categories']
   lumi       = sampledata["common"]["luminosity"]
   era_ratios = sampledata["common"]["era_ratios"]
   lepton_def = sampledata["common"]["genLepton"]
   ps         = sampledata["common"]["phase_space_"+lepton_def]    
   isMC       = (dataType=='MC')
   print "sample:      ", sample
   print "num of dirs: ", len(dirs)
   print "dataType:    ", dataType
   print "xsec:        ", xsec
   print "ncores:      ", ncores
   print "categories:  ", categories
   config = ConfigRDF(inputFiles, output_dir, sample+'.root', verbose)
   config.set_sample_specifics(isMC, lumi, xsec, dataYear, era_ratios, lepton_def, ps)   
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
            lf = '/scratchssd/'+whoami+'/NanoAOD'+dataYear+'-V1MCFinal/'+str(subdir)+'/'+str(f)+'.root'
            if subdir==k: inputFiles.push_back(lf)
      for subdir,files in v['dirs'].items():
         for f in files:
            lf = '/scratchssd/'+whoami+'/NanoAOD'+dataYear+'-V1MCFinal/'+str(subdir)+'/'+str(f)+'.root'
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
            lf = '/scratchssd/'+whoami+'/NanoAOD'+dataYear+'-V1MCFinal/'+str(subdir)+'/'+str(f)+'.root'
            if subdir==k: inputFiles.push_back(lf)
      for subdir,files in v['dirs'].items():
         for f in files:
            lf = '/scratchssd/'+whoami+'/NanoAOD'+dataYear+'-V1MCFinal/'+str(subdir)+'/'+str(f)+'.root'
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

def make_dictionary(sampledata, vname, verbose=True):
   out = {}
   out['variable'] = vname
   output = sampledata["common"]["output"]
   for krc,r in output.items():
      out[krc] = {}
      if verbose: print krc
      charge = krc.split('_')[1] if '_' in krc else ''
      kr = krc.split('_')[0]
      total_data = 0.0
      total_mc   = 0.0
      for kp,p in r.items():
         out[krc][kp] = {}
         if verbose: print '\t'+kp
         fname = p.split('/')[0]
         f     = ROOT.TFile(output_dir+'/hadded/'+fname)
         dname = ((p.split('/')[1].split(':')[0]).replace('*',kr))
         cats  = p.split('/')[1].split(':')[1].split(',')
         tot_nominal = -1.
         for cat in cats:
            out[krc][kp][cat] = {}
            systs = []
            for sk,sv in modules_any.items():
               if cat==(sk.split('_')[-1]):
                  systs = sv
                  if cat=='fakerate': 
                     systs = sv['systs']
                  elif cat=='mass':
                     systs = sv['masses']
            if len(systs)==0: systs.append('')
            if verbose: print '\t\t'+cat
            if cat=='LHEScaleWeight':
               first,last = systs[0],systs[1]
               systs = []
               for i in range(first,last+1):
                  systs.append(LHEScaleWeight_meaning(i))
            elif cat=='LHEPdfWeight':
               first,last = systs[0],systs[1]
               systs = []
               for i in range(first,last+1):
                  systs.append(LHEPdfWeight_meaning(i))
            for syst in systs:               
               tag = syst
               if cat in ['ISO','ID','Trigger']:
                  tag = cat+'_'+tag
               elif cat=='puWeight':
                  tag = cat+syst
               elif cat=='fakerate':
                  tag = cat+'_'+tag
               elif 'LHE' in cat:
                  tag = cat+'_'+tag                  
               hname = dname+'_'+cat+'/'+dname+'__'+vname+'__'+tag
               f.cd()
               h3 = ROOT.gDirectory.Get(hname)
               if h3==None:
                  continue
               if charge=='Plus': 
                  h3.GetZaxis().SetRange(2,2)
               elif charge=='Minus':
                  h3.GetZaxis().SetRange(1,1)
               else:
                  pass
               tot = h3.Project3D("yxe").Integral() 
               out[krc][kp][cat][syst] = { 'hname' : (fname+'/'+hname).replace(vname,'*'), 'integral' : tot, 'delta' : 0.0}
               if cat=='nominal': 
                  tot_nominal = tot
                  if kp=='Data': total_data += tot
                  else: total_mc += tot
                  if verbose: print '\t\t\t'+syst+' --> '+'{:.3E}'.format(tot_nominal)
               elif cat=='fakerate' and syst=='nominal':
                  total_mc += tot
                  if verbose: print '\t\t\t'+syst+' --> '+'{:.3E}'.format(tot) 
               else:
                  if verbose: print '\t\t\t'+syst+' --> '+'{:.3f}'.format((tot-tot_nominal)/tot_nominal*1e+02)+'%'                     
                  out[krc][kp][cat][syst]['delta'] = (tot-tot_nominal)/tot_nominal*1e+02

         f.Close()
      if verbose: print 'Data: '+'{:.3E}'.format(total_data)
      if verbose: print 'MC:   '+'{:.3E}'.format(total_mc)
      from json import encoder
      encoder.FLOAT_REPR = lambda o: format(o, '.3f')
      with open(output_dir+'/hadded/dictionary_'+vname+'.json', 'w') as fp:
         json.dump(out, fp)
   return

if __name__ == '__main__':
   if args.rdf:
      run_multithread_all(sampledata, restrictDataset, output_dir)
      run_multicore_all(sampledata, restrictDataset, output_dir)
   elif args.merge:
      merge(sampledata)
   elif args.dictionary:
      make_dictionary(sampledata, 'SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge')
      #make_dictionary(sampledata, 'SelRecoZ_corrected_qt_SelRecoZ_corrected_y_SelRecoZ_corrected_mass')
