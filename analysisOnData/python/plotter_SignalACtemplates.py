from time import time
import ROOT
import copy
import sys
import argparse
from collections import OrderedDict
sys.path.append('../data')
from systematics import systematics
import math
import copy

ROOT.gROOT.SetBatch()
ROOT.TH1.AddDirectory(False)
ROOT.TH2.AddDirectory(False)

class plotter:
    
    def __init__(self, outDir, ACfile, inDir = ''):
        self.indir = inDir # indir containig the various outputs
        self.outdir = outDir
        self.sampleFile = 'WToMu_AC_plots.root'

        self.extSyst = copy.deepcopy(systematics)
        self.extSyst['Nominal'] =  (['', '_massUp', '_massDown'],"Nom")
        self.histoDict ={} 
        self.clist = ["L", "I", "T", "A", "P", "7", "8", "9", "UL"]
        self.varName = 'helXsecs'
        self.inFile = ROOT.TFile.Open(self.indir+'/'+self.sampleFile)
        if not self.inFile :
            print self.inFile, ' does not exist'
            sys.exit(1)
        self.ACfile = ROOT.TFile.Open(ACfile)
        self.imap = self.ACfile.Get("angularCoefficients/mapTot")
        self.clos = copy.deepcopy(ROOT.TH2D("clos", "clos", self.imap.GetXaxis().GetNbins(),self.imap.GetXaxis().GetXbins().GetArray(),self.imap.GetYaxis().GetNbins(),self.imap.GetYaxis().GetXbins().GetArray()))
        self.yields = {}
        
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
    def unroll2D(self, th2):

        nbins = th2.GetNbinsX()*th2.GetNbinsY()
        #th2.Sumw2() #don't think it's necessary
        new = th2.GetName()
        old = new + '_roll'
        th2.SetName(old)
        unrolledth2 = ROOT.TH1F(new, '', nbins, 1., nbins+1)
        for ibin in range(1, th2.GetNbinsX()+1):
            for jbin in range(1, th2.GetNbinsY()+1):
                bin1D = th2.GetBin(ibin, jbin)
                unrolledth2.SetBinContent(bin1D, th2.GetBinContent(ibin, jbin))
                unrolledth2.SetBinError(bin1D, th2.GetBinError(ibin, jbin))
        return unrolledth2
    def makeTH3slices(self, th3, systname, chargeBin):
        
        hname=th3.GetName()
        iQt = int(hname.split('_')[1])
        coeff = hname.split('_')[3]
        
        try:
            syst = "_" + hname.split('_')[4]
        except IndexError:
            syst = ""
        
        for iY in range(1, th3.GetNbinsZ()+1):
            
            slicename = 'helXsecs'+ coeff + '_y_{}'.format(iY)+'_qt_{}'.format(iQt) + syst
            th3.GetZaxis().SetRange(iY, iY)
            
            th2slice=th3.Project3D("y_{iY}_yxe".format(iY=iY))
            th2slice.SetName(slicename)
            #normalise templates to its helicity xsec
            nsum = (3./16./math.pi)*self.imap.GetBinContent(iY,iQt)
            if not 'UL' in hname:
                hAC = self.ACfile.Get("angularCoefficients/harmonics{}".format(self.helXsecs[coeff]))
                nsum = nsum*hAC.GetBinContent(iY,iQt)/self.factors[self.helXsecs[coeff]]
            th2slice.Scale(nsum)
            th2slice.SetDirectory(0)
            self.histoDict[systname].append(th2slice)

            if syst=="":
                #print th2slice.GetName(), th2slice.Integral(0,th2slice.GetNbinsX()+2,0,th2slice.GetNbinsY()+2)
                self.yields[(iY,iQt)]+=th2slice.Integral(0,th2slice.GetNbinsX()+2,0,th2slice.GetNbinsY()+2)
    def closureMap(self):
        for iY in range(1, 7):
            for iQt in range(1, 9):
                self.clos.SetBinContent(iY,iQt, self.yields[(iY,iQt)])

        self.clos.Divide(self.imap)
        for iY in range(1, 7):
            for iQt in range(1, 9):
                print self.clos.GetBinContent(iY,iQt)
        fout = ROOT.TFile("accMap.root","recreate")
        fout.cd()
        self.clos.Write()
        fout.Close()
    def getHistos(self, chargeBin) :
        
        for iY in range(1, 7):
            for iQt in range(1, 9):
               self.yields[(iY,iQt)]=0.
        
        basepath="templatesAC_Signal/"
        #self.chargeBin = 2  if charge == 1 else 1
        for sKind, sList in self.extSyst.iteritems():
            self.histoDict[sKind]  = []
            #print sKind, sList
            for sname in sList[0]:#variations of each sKind
                for htype in self.clist:
                    for iQt in range(1,9):
                        fpath = basepath + sKind + '/qt_{}_helXsecs_'.format(iQt) + htype + sname
                        if sKind == 'Nominal' and sname == '': 
                            fpath = basepath + sKind + '/qt_{}_helXsecs_'.format(iQt) + htype + sname
                        print "Histo read:", fpath
                        th3 = self.inFile.Get(fpath)
                        if not th3: continue
                        self.makeTH3slices(th3, sKind, chargeBin)
        #self.uncorrelateEff()
        #self.symmetrisePDF()
        self.closureMap()
        self.writeHistos(chargeBin)   
    def uncorrelateEff(self):
        aux = {}
        aux['WHSF'] = []
        for h in self.histoDict['Nominal']:
            if 'mass' in h.GetName():
                continue
            for i in range(3):
                for hvar in self.histoDict['WHSF']:
                    for updown in ['Up', 'Down']:
                        #print h.GetName() + 'WHSFSyst{}{}'.format(i, updown), "match"
                        if hvar.GetName() == h.GetName() + '_WHSFSyst{}{}'.format(i, updown):
                            for j in range(1, hvar.GetNbinsX()+1):  # loop over eta bins
                                #create one histogram per eta bin
                                haux = h.Clone()
                                haux.SetName(
                                    h.GetName() + '_WHSFSyst{}Eta{}{}'.format(i, j, updown))
                                #print haux.GetName()
                                for k in range(1, hvar.GetNbinsY()+1):  # loop over pt bins
                                    bin1D = hvar.GetBin(j, k)
                                    varcont = hvar.GetBinContent(bin1D)
                                    haux.SetBinContent(bin1D, varcont)
                                aux['WHSF'].append(haux)
        for hvar in self.histoDict['WHSF']:
            if 'Flat' in hvar.GetName():  # leave syst uncertainty as it is
                aux['WHSF'].append(hvar)
        self.histoDict.update(aux)
    def symmetrisePDF(self):

        aux = {}
        aux['LHEPdfWeight']=[]
        for h in self.histoDict['Nominal']:
            if 'mass' in h.GetName(): continue
            for i in range(60):
                for hvar in self.histoDict['LHEPdfWeight']:
                    if hvar.GetName() == h.GetName()+ '_LHEPdfWeightHess{}'.format(i+1):
                        th2var = hvar
                        break
                print h.GetName(), "pdf {}".format(i+1)
                th2c = h.Clone()
                th2varD = th2var.Clone()
                th2var.Divide(th2c)
                th2c.Divide(th2varD)
                nbinsX = h.GetXaxis().GetNbins()
                nbinsY = h.GetYaxis().GetNbins()
                th2Up = ROOT.TH2D("up","up",nbinsX,h.GetXaxis().GetBinLowEdge(1),h.GetXaxis().GetBinUpEdge(nbinsX),nbinsY,h.GetYaxis().GetBinLowEdge(1),h.GetYaxis().GetBinUpEdge(nbinsY))
                th2Up.Sumw2()
                th2Down =ROOT.TH2D("down","down",nbinsX,h.GetXaxis().GetBinLowEdge(1),h.GetXaxis().GetBinUpEdge(nbinsX),nbinsY,h.GetYaxis().GetBinLowEdge(1),h.GetYaxis().GetBinUpEdge(nbinsY))
                th2Down.Sumw2()
                for j in range(1,h.GetNbinsX()+1):
                    for k in range(1,h.GetNbinsY()+1):
                    
                        th2Up.SetBinContent(j,k,h.GetBinContent(j,k)*th2var.GetBinContent(j,k))
                        th2Down.SetBinContent(j,k,h.GetBinContent(j,k)*th2c.GetBinContent(j,k))
                
                th2Up.SetName(h.GetName()+ '_LHEPdfWeightHess{}Up'.format(i+1))
                th2Down.SetName(h.GetName()+ '_LHEPdfWeightHess{}Down'.format(i+1))
                aux['LHEPdfWeight'].append(th2Up)
                aux['LHEPdfWeight'].append(th2Down)

        self.histoDict.update(aux)
    def writeHistos(self, chargeBin):
        print 'writing histograms'
        foutName = 'Wplus_reco' if chargeBin == 2 else 'Wminus_reco'
        foutName += '.root'
        fout = ROOT.TFile.Open(self.outdir + '/' + foutName, "RECREATE")
        fout.cd()
        start = time()
        for sKind, hlist in self.histoDict.iteritems():
            #fout.mkdir(sKind)
            #fout.cd(sKind)
            fout.cd()
            for h in hlist:
                #th1=self.unroll2D(h)
                h.Write()
        fout.cd()
        fout.Save()
        fout.Close()
        end = time()
        print "time: {}".format(end - start)

parser = argparse.ArgumentParser("")
parser.add_argument('-o','--output', type=str, default='./',help="name of the output directory")
parser.add_argument('-i','--input', type=str, default='./',help="name of the input directory root file")
parser.add_argument('-AC','--AC', type=str, default='./',help="name of the input AC file root file")
args = parser.parse_args()
OUTPUT = args.output
INPUT = args.input
ACfile = args.AC
p=plotter(outDir=OUTPUT, inDir = INPUT, ACfile=ACfile)
#p.getHistos(1)
p.getHistos(2)
