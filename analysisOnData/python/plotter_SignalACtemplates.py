import ROOT
import copy
import sys
import argparse
from collections import OrderedDict
sys.path.append('../../bkgAnalysis')
import bkg_utils
import math

ROOT.gROOT.SetBatch()
ROOT.TH1.AddDirectory(False)
ROOT.TH2.AddDirectory(False)


class plotter:
    
    def __init__(self, outDir, ACfile, inDir = ''):
        self.indir = inDir # indir containig the various outputs
        self.outdir = outDir
        self.sampleFile = 'WToMu_plots.root'
        self.extSyst = copy.deepcopy(bkg_utils.bkg_systematics)
        self.extSyst['Nominal'] =  ['', 'massUp', 'massDown']
        self.histoDict ={} 
        self.clist = ["L", "I", "T", "A", "P", "7", "8", "9", "UL"]
        self.varName = 'helXsecs'
        self.inFile = ROOT.TFile.Open(self.indir+'/'+self.sampleFile)
        if not self.inFile :
            print self.inFile, ' does not exist'
            sys.exit(1)
        self.ACfile = ROOT.TFile.Open(ACfile)
        self.imap = self.ACfile.Get("accMaps/mapTot")
        
        self.helXsecs = OrderedDict()
        self.helXsecs["L"] = "A0"
        self.helXsecs["I"] = "A1" 
        self.helXsecs["T"] = "A2" 
        self.helXsecs["A"] = "A3" 
        self.helXsecs["P"] = "A4" 
        self.helXsecs["7"] = "A5" 
        self.helXsecs["8"] = "A6" 
        self.helXsecs["9"] = "A7" 
        self.helXsecs["UL"] = "AUL"
        
        self.factors = {}
        self.factors["A0"]= 2.
        self.factors["A1"]=2.*math.sqrt(2)
        self.factors["A2"]=4.
        self.factors["A3"]=4.*math.sqrt(2)
        self.factors["A4"]=2.
        self.factors["A5"]=2.
        self.factors["A6"]=2.*math.sqrt(2)
        self.factors["A7"]=4.*math.sqrt(2)

    def makeTH5slices(self, thn5, systname, chargeBin):
        hname=thn5.GetName()
        coeff = hname.replace('helXsecs',"")
        try:
            syst = "_" + coeff.split('_')[1]
            coeff = coeff.split('_')[0]
        except IndexError:
            syst = ""
        #minus charge
        thn5.GetAxis(4).SetRange(chargeBin, chargeBin)
        for iY in range(1, 7):
            for iQt in range(1, 9):
                #w_y = 0. + iY*0.4
                #w_qt = 0 + iQt*4
                slicename = 'helXsecs'+ coeff + '_y_{}'.format(iY)+'_qt_{}'.format(iQt) + syst
                thn5.GetAxis(2).SetRange(iY, iY)
                thn5.GetAxis(3).SetRange(iQt, iQt)
                th2slice=thn5.Projection(1, 0)
                th2slice.SetName(slicename)
                #normalise templates to its helicity xsec
                nsum = (3./16./math.pi)*self.imap.GetBinContent(iY,iQt)
                if not 'UL' in hname:
                    hAC = self.ACfile.Get("angularCoefficients/harmonics{}".format(self.helXsecs[coeff]))
                    nsum = nsum*hAC.GetBinContent(iY,iQt)/self.factors[self.helXsecs[coeff]]
                th2slice.Scale(nsum)
                th2slice.SetDirectory(0)
                self.histoDict[systname].append(th2slice)

    def getHistos(self, chargeBin) :
        basepath="templatesAC_Signal/"
        #self.chargeBin = 2  if charge == 1 else 1
        for sKind, sList in self.extSyst.iteritems():
            self.histoDict[sKind]  = []
            #print sKind, sList
            for sname in sList:#variations of each sKind
                for htype in self.clist:
                    fpath = basepath + sKind + '/helXsecs' + htype + '_'  + sname
                    if sKind == 'Nominal' and sname == '': 
                        fpath = basepath + sKind + '/helXsecs' + htype + sname
                    print "Histo read:", fpath
                    thn5 = self.inFile.Get(fpath)
                    self.makeTH5slices(thn5, sKind, chargeBin)
        self.writeHistos(chargeBin)

    def writeHistos(self, chargeBin):
        foutName = 'WPlus' if chargeBin == 2 else 'WMinus'
        foutName += '_2D_ACTemplates.root'
        fout = ROOT.TFile.Open(self.outdir + '/' + foutName, "RECREATE")
        fout.cd()
        for sKind, hlist in self.histoDict.iteritems():
            fout.mkdir(sKind)
            fout.cd(sKind)
            for h in hlist:
                h.Write()
            fout.cd()
        fout.Save()
        fout.Close()

parser = argparse.ArgumentParser("")
parser.add_argument('-o','--output', type=str, default='./',help="name of the output directory")
parser.add_argument('-i','--input', type=str, default='./',help="name of the input directory root file")
parser.add_argument('-AC','--AC', type=str, default='./',help="name of the input AC file root file")
args = parser.parse_args()
OUTPUT = args.output
INPUT = args.input
ACfile = args.AC
p=plotter(outDir=OUTPUT, inDir = INPUT, ACfile=ACfile)
p.getHistos(1)
p.getHistos(2)
