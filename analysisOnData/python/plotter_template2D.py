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
                            "Data"        : ('Data_plots.root', 0)
                          }

        self.extSyst = copy.deepcopy(bkg_utils.bkg_systematics)
        self.extSyst['Nominal'] = ['']
        
        self.histoDict ={} 
    
    def getHistoforSample(self, sample, infile, selection, systType, chargeBin) :
        self.histoDict[sample][selection] = {}
        syst = self.extSyst
        if 'Data' in sample:
            syst = {}
            syst['Nominal'] = ['']
        for sKind, sList in syst.iteritems():
            if 'Fake' in sample and sKind == 'WHSFVars': continue
            if systType != 2 and 'LHE' in sKind : continue
            self.histoDict[sample][selection][sKind]  = []
            gap = '' if sKind == 'Nominal' else '_'
            basepath = selection + '/' + sKind + '/templates' +  gap
            for sname in sList:
                hname =  basepath + sname
                print "Reading:", hname
                th3=infile.Get(hname)
                if not hname:
                    print hname, ' not found in file'
                    continue
                #plus charge bin 2, minus bin 1
                th3.GetZaxis().SetRange(chargeBin,chargeBin)
                th2=th3.Project3D("yx")
                th2.SetDirectory(0)
                th2.SetName(th3.GetName())
                self.histoDict[sample][ selection][sKind].append(th2)

    def writeHistos(self, sample, chargeTag):
        outname = self.outdir  + '/' + sample + '_templates2D' + chargeTag + '.root'
        fout = ROOT.TFile(outname, 'RECREATE')
        if sample not in  self.histoDict.keys() : 
            print "No histo dict for sample:", sample, " What have you done??!!!!"
            return 1
        for dirTag, regionDict in self.histoDict[sample].iteritems():
            fout.mkdir(dirTag)
            #fout.cd(dirTag)
            for region, hlist in regionDict.iteritems():
                fout.mkdir(dirTag +'/' +region)
                fout.cd( dirTag +'/' +region)
                for h in hlist:
                    h.Write()
                fout.cd()
        fout.Save()
        fout.Write()   
        fout.Close()

    def getHistos(self, chargeBin) :
        for sample,fname in self.sampleDict.iteritems():
            print  "Procesing sample:", sample
            infile = ROOT.TFile(self.indir + '/' + fname[0])
            systType = fname[1]
            if not infile:
                print infile,' does not exist'
                continue
            self.histoDict[sample] = {}
            selection = "templates_Signal" 
            if 'Fake' in sample:
                selection = "templates_fakes"

            self.getHistoforSample(sample,infile, selection, systType, chargeBin)
            if sample == 'WToMu'  : 
                self.getHistoforSample(sample,infile, 'templatesLowAcc_Signal', systType, chargeBin)
            chargeTag='minus' if chargeBin == 1 else 'plus'
            self.writeHistos(sample, chargeTag)

parser = argparse.ArgumentParser("")
parser.add_argument('-o','--output', type=str, default='./',help="name of the output directory")
parser.add_argument('-i','--input', type=str, default='./',help="name of the input direcory root file")

args = parser.parse_args()
OUTPUT = args.output
INPUT = args.input

p=plotter(outDir=OUTPUT, inDir = INPUT)
p.getHistos(1)
p.getHistos(2)
