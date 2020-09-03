import ROOT
import copy
import sys
import argparse

sys.path.append('../../bkgAnalysis')
import bkg_utils

ROOT.gROOT.SetBatch()
ROOT.TH1.AddDirectory(False)
ROOT.TH2.AddDirectory(False)


class plotter:
    
    def __init__(self, outDir, inDir = ''):
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

    def makeTH5slices(self, thn5, systname, chargeBin):
        hname=thn5.GetName()
        #minus charge
        thn5.GetAxis(4).SetRange(chargeBin, chargeBin)
        for iY in range(1, 7):
            for iQt in range(1, 9):
                #w_y = 0. + iY*0.4
                #w_qt = 0 + iQt*4
                slicename = hname + '_y_{}'.format(iY)+'_qt_{}'.format(iQt)
                thn5.GetAxis(2).SetRange(iY, iY)
                thn5.GetAxis(3).SetRange(iQt, iQt)
                th2slice=thn5.Projection(1, 0)
                th2slice.SetName(slicename)
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
parser.add_argument('-i','--input', type=str, default='./',help="name of the input direcory root file")

args = parser.parse_args()
OUTPUT = args.output
INPUT = args.input
p=plotter(outDir=OUTPUT, inDir = INPUT)
p.getHistos(1)
p.getHistos(2)
