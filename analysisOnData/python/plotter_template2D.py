import os
import ROOT
import copy
import sys
import argparse
import math

sys.path.append('../../bkgAnalysis')
import bkg_utils
ROOT.gROOT.SetBatch()
ROOT.TH1.AddDirectory(False)
ROOT.TH2.AddDirectory(False)
ROOT.gStyle.SetOptStat(0)

class plotter:
    
    def __init__(self, outDir, inDir = ''):

        self.indir = inDir # indir containig the various outputs
        self.outdir = outDir
        
        self.sampleDict = { "WToMu"      :  ('WToMu_plots.root', 2 ),
                            "DYJets"      : ('DYJets_plots.root', 2 ),
                            "WtoTau"      : ('WToTau_plots.root', 2 ),
                            "TW"          : ('TW_plots.root', 1),
                            "TTbar"       : ('TTJets_plots.root',1),
                            "ST"          : ('SingleTop_plots.root',1),
                            "DiBoson"     : ('Diboson_plots.root', 1),
                            "SIGNAL_Fake" : ('FakeFromData_plots.root', 0), 
                            "Data"        : ('Data_plots.root', 0),
                            "LowAcc": ('WToMu_plots.root', 2 )
                          }

        self.selections =["Signal"] 
        self.selectionFake = ['fakes']       
        self.extSyst = copy.deepcopy(bkg_utils.bkg_systematics)
        self.extSyst['Nominal'] = ['']
        self.histoDict ={} 
    
    def getHistoforSample(self, sample, infile, chargeBin) :
        if not 'FakeFromData' in sample:
            for sKind in self.extSyst:
                self.histoDict[sample][sKind] = []
                gap = '' if sKind == 'Nominal' else '_'
                basepath = 'templates_Signal/' + sKind
                if 'LowAcc' in sample: basepath = 'templatesLowAcc_Signal/' + sKind
                if infile.GetDirectory(basepath):
                    if 'LowAcc' in sample: print basepath
                    for key in infile.Get(basepath).GetListOfKeys():
                        if 'LowAcc' in sample: print key.GetName()
                        th3=infile.Get(basepath+'/'+key.GetName())
                        #plus charge bin 2, minus bin 1
                        th3.GetZaxis().SetRange(chargeBin,chargeBin)
                        th2=th3.Project3D("yx")
                        th2.SetDirectory(0)
                        th2.SetName(th3.GetName())
                        self.histoDict[sample][sKind].append(th2)
                        
        else:
            for sKind in self.extSyst:
                self.histoDict[sample][sKind] = []
                gap = '' if sKind == 'Nominal' else '_'
                basepath = 'templates_fakes/' + sKind
                if infile.GetDirectory(basepath):
                    print basepath
                    for key in infile.Get(basepath).GetListOfKeys():
                        print key.GetName()
                        th3=infile.Get(basepath+'/'+key.GetName())
                        #plus charge bin 2, minus bin 1
                        th3.GetZaxis().SetRange(chargeBin,chargeBin)
                        th2=th3.Project3D("yx")
                        th2.SetDirectory(0)
                        th2.SetName(th3.GetName())
                        self.histoDict[sample][sKind].append(th2)
                        
    def getHistos(self, chargeBin) :
        for sample,fname in self.sampleDict.iteritems():
            print  "Processing sample:", sample
            infile = ROOT.TFile(self.indir + '/' + fname[0])
            systType = fname[1]
            if not infile:
                print infile,' does not exist'
                continue
            self.histoDict[sample] = {}
            self.getHistoforSample(sample,infile, chargeBin)
            chargeTag='minus' if chargeBin == 1 else 'plus'
            outname = self.outdir  + '/' + sample + '_templates2D' + chargeTag + '.root'
            fout = ROOT.TFile(outname, 'RECREATE')
            if sample not in  self.histoDict : 
                print "No histo dict for sample:", sample, " What have you done??!!!!"
                continue
            for syst, hlist in self.histoDict[sample].iteritems():
                fout.mkdir(syst)
                fout.cd(syst)
                for h in hlist:
                    h.Write()
                fout.cd()
            fout.Save()
            fout.Write()

parser = argparse.ArgumentParser("")
parser.add_argument('-o','--output', type=str, default='./',help="name of the output directory")
parser.add_argument('-i','--input', type=str, default='./',help="name of the input direcory root file")

args = parser.parse_args()
OUTPUT = args.output
INPUT = args.input

p=plotter(outDir=OUTPUT, inDir = INPUT)
p.getHistos(1)
p.getHistos(2)
