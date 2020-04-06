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
parser.add_argument('-p', '--plot',      help="", action='store_true')
parser.add_argument('-o', '--output_dir',type=str, default='TEST', help="")
parser.add_argument('-y', '--dataYear',  type=str, default='2016', help="")
parser.add_argument('-i', '--input',     type=str, default="",     help="")
parser.add_argument('-c', '--config',    type=str, default="data/samples_2016.json",     help="")
parser.add_argument('-w', '--whoami',    type=str, default="sroychow",     help="")
parser.add_argument('-v', '--verbose',   help="", action='store_true')
args = parser.parse_args()
output_dir = args.output_dir
dataYear = args.dataYear
config = args.config
whoami = args.whoami
verbose = args.verbose
restrictDataset = [ x for x in args.input.split(',') if args.input != ""]

samplef = open('./'+config)
sampledata = json.load(samplef)
samplef.close()

if args.rdf:
   print "Loading shared library..."
   ROOT.gSystem.Load('bin/libAnalysisOnData.so')

def run_one_sample(inputFiles,output_dir, sampledata, sample, verbose=verbose, print_graph=False):
   v          = sampledata[sample]
   dataType   = v['dataType']
   dirs       = v['dirs']
   xsec       = v['xsec']
   ncores     = v['ncores']
   categories = v['categories']
   lumi       = sampledata["common"]["luminosity"]
   era_ratios = sampledata["common"]["era_ratios"]
   lepton_def = sampledata["common"]["genLepton"]
   isMC       = (dataType=='MC')
   procId = ''
   if   'WJets'  in sample: procId = 'W'
   elif 'DYJets' in sample: procId = 'Z'   

   if sampledata["common"].has_key("phase_space_"+lepton_def):
      ps = sampledata["common"]["phase_space_"+lepton_def]
   else:
      ps = {}
   if sampledata["common"].has_key("harmonics"):
      harmonics  = sampledata["common"]["harmonics"]
   else:
      harmonics = {}
   if sampledata["common"].has_key("Z_reweighter"):
      Z_reweighter = sampledata["common"]["Z_reweighter"]
   else:
      Z_reweighter = {}
   if sampledata["common"].has_key("external_SF"):
      external_SF = sampledata["common"]["external_SF"]
   else:
      external_SF = {}

   use_externalSF        = external_SF['use_externalSF']
   apply_SmoothAntiISOSF = external_SF['apply_SmoothAntiISOSF']
   apply_SmoothISOSF     = external_SF['apply_SmoothISOSF']

   print "sample:                ", sample
   print "num of dirs:           ", len(dirs)
   print "dataType:              ", dataType
   print "xsec:                  ", xsec
   print "ncores:                ", ncores
   print "categories:            ", categories
   print "procId:                ", (procId if procId!="" else "UNKOWN")
   print "use_externalSF:        ", "True" if use_externalSF else "False"
   print "apply_SmoothAntiISOSF: ", "True" if apply_SmoothAntiISOSF else "False"
   print "apply_SmoothISOSF:     ", "True" if apply_SmoothISOSF else "False"
   
   config = ConfigRDF(inputFiles, output_dir, sample+'.root', verbose, print_graph, apply_SmoothAntiISOSF, use_externalSF)
   config.set_sample_specifics(isMC, lumi, xsec, dataYear, era_ratios, lepton_def, ps, harmonics, Z_reweighter, procId, external_SF)   
   ret,ret_base = get_categories(dataType, categories, sampledata["common"], apply_SmoothAntiISOSF, apply_SmoothISOSF, use_externalSF)

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
      if len(restrictDataset)>0 and "*" not in restrictDataset[0] and (k not in restrictDataset): continue
      if len(restrictDataset)>0 and "*" in restrictDataset[0] and restrictDataset[0].replace('*','') not in k: continue 

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
      if len(restrictDataset)>0 and "*" not in restrictDataset[0] and (k not in restrictDataset): continue
      if len(restrictDataset)>0 and "*" in restrictDataset[0] and restrictDataset[0].replace('*','') not in k: continue 

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

def make_dictionary_histo(sampledata, vname, verbose=verbose):
   out = {}
   out['variable'] = vname
   output = sampledata["common"]["output"]
   
   # categories
   for krc,r in output.items():
      out[krc] = {}
      # strip charge (-> Plus/Minus)
      kr = krc.split('_')[0]
      # process
      for kp,p in r.items():         
         multifiles = p.split(';')
         for sp in multifiles:
            fname = sp.split('/')[0]
            f     = ROOT.TFile(output_dir+'/hadded/'+fname)
            specs = sp.split('/')[1].split(':')
            dname = specs[0].replace('*',kr)
            cats  = specs[1].split(',')
            tot_nominal = -1.
            for cat in cats:
               if not out[krc].has_key(cat):
                  out[krc][cat] = {}
               systs = []
               for sk,sv in modules_any.items():
                  if cat==(sk.split('_')[-1]):
                     systs = sv
                     if cat=='fakerate': 
                        systs = sv['systs']
                     elif cat=='mass':
                        systs = sv['masses']
               if len(systs)==0: systs.append('')
               if cat=='LHEScaleWeight':
                  systs_clone = copy.deepcopy(systs)
                  systs = []
                  for syst in systs_clone:
                     systs.append(LHEScaleWeight_meaning(syst))
               elif cat=='LHEPdfWeight':
                  first,last = systs[0],systs[1]
                  systs = []
                  for i in range(first,last+1):
                     systs.append(LHEPdfWeight_meaning(i))
               # systs
               for syst in systs:               
                  tag = syst
                  if cat in ['ISO','Trigger']: tag = cat+tag
                  elif cat=='puWeight':        tag = cat+syst
                  elif cat=='fakerate':        tag = cat+'_'+tag
                  elif 'LHE' in cat:           tag = cat+'_'+tag                  
                  hname = dname+'_'+cat+'/'+dname+'__'+vname+'__'+tag
                  f.cd()
                  h3 = ROOT.gDirectory.Get(hname)
                  if h3==None:
                     if verbose: print 'NOT FOUND: '+fname+'/'+hname
                     continue
                  if not out[krc][cat].has_key(syst):
                     print "Adding ", krc+':'+cat+':'+syst+' --> '+vname
                     out[krc][cat][syst] = {'inputs' : [ { 'pname': kp, 'fname' : fname, 'hname' : hname.replace(vname,'*') } ] }
                     pass
                  else:
                     out[krc][cat][syst]['inputs'].append( { 'pname': kp, 'fname' : fname, 'hname' : hname.replace(vname,'*') } )
                     pass
            f.Close()

   from json import encoder
   encoder.FLOAT_REPR = lambda o: format(o, '.3f')
   with open(output_dir+'/hadded/dictionaryHisto_'+vname+'.json', 'w') as fp:
      json.dump(out, fp)
   
   return



if __name__ == '__main__':
   if args.rdf:
      run_multithread_all(sampledata, restrictDataset, output_dir)
      run_multicore_all(sampledata, restrictDataset, output_dir)
   elif args.merge:
      merge(sampledata)
   elif args.dictionary:
      for v in ['SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge', 
                'SelMuon2_eta_SelMuon2_corrected_pt_SelMuon2_charge', 
                'SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_corrected_MET_nom_Wlike_mt', 
                'SelMuon2_eta_SelMuon2_corrected_pt_SelMuon2_corrected_MET_nom_Wlike_mt', 
                #'SelRecoZ_corrected_qt_SelRecoZ_corrected_y_SelRecoZ_corrected_mass',
                #'SelMuon1_corrected_MET_nom_mt_SelMuon1_corrected_MET_nom_hpt_SelMuon1_charge',
                #'SelMuon1_pfRelIso04_all_SelMuon1_dxy_SelMuon1_charge', 
                #'SelMuon2_pfRelIso04_all_SelMuon2_dxy_SelMuon2_charge' 
                ]:
         make_dictionary_histo(sampledata, v)
   elif args.plot:
      os.system('./plot.sh '+output_dir)
