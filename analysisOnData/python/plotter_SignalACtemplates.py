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
        self.symmetrisePDF()
        self.writeHistos(chargeBin)
    
    def symmetrisePDF(self):
        #helXsecs9_y_3_qt_1_LHEPdfWeightHess60
        #helXsecs9_y_3_qt_1
        aux = {}
        aux['LHEPdfWeightVars']=[]
        for h in self.histoDict['Nominal']:
            if 'mass' in h.GetName(): continue
            for i in range(60):
                for hvar in self.histoDict['LHEPdfWeightVars']:
                    if hvar.GetName() == h.GetName()+ '_LHEPdfWeightHess{}'.format(i+1):
                        th2var = hvar
                        break
                print h.GetName()
                th2c = h.Clone()
                th2varD = th2var.Clone()
                th2var.Divide(th2c)
                th2c.Divide(th2varD)
                nbinsX = h.GetXaxis().GetNbins()
                nbinsY = h.GetYaxis().GetNbins()
                th2Up = ROOT.TH2D("up","up",nbinsX,h.GetXaxis().GetBinLowEdge(1),h.GetXaxis().GetBinUpEdge(nbinsX),nbinsY,h.GetYaxis().GetBinLowEdge(1),h.GetYaxis().GetBinUpEdge(nbinsY))
                th2Down =ROOT.TH2D("down","down",nbinsX,h.GetXaxis().GetBinLowEdge(1),h.GetXaxis().GetBinUpEdge(nbinsX),nbinsY,h.GetYaxis().GetBinLowEdge(1),h.GetYaxis().GetBinUpEdge(nbinsY))

                for j in range(1,h.GetNbinsX()+1):
                    for k in range(1,h.GetNbinsY()+1):
                    
                        th2Up.SetBinContent(j,k,h.GetBinContent(j,k)*th2var.GetBinContent(j,k))
                        th2Down.SetBinContent(j,k,h.GetBinContent(j,k)*th2c.GetBinContent(j,k))

                th2Up.SetName(h.GetName()+ '_LHEPdfWeightHess{}Up'.format(i+1))
                th2Down.SetName(h.GetName()+ '_LHEPdfWeightHess{}Down'.format(i+1))
                aux['LHEPdfWeightVars'].append(th2Up)
                aux['LHEPdfWeightVars'].append(th2Down)

        self.histoDict.update(aux)
        print aux

    def writeHistos(self, chargeBin):
        foutName = 'WPlus' if chargeBin == 2 else 'WMinus'
        foutName += '_2D_ACTemplates.root'
        fout = ROOT.TFile.Open(self.outdir + '/' + foutName, "RECREATE")
        fout.cd()
        for sKind, hlist in self.histoDict.iteritems():
            fout.mkdir(sKind)
            fout.cd(sKind)
            for h in hlist:
                print h.GetName()
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
