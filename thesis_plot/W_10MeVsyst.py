import os
import ROOT
import copy
import sys
import argparse
import math

sys.path.append('../../bkgAnalysis')
# import bkg_utils
ROOT.gROOT.SetBatch()
ROOT.TH1.AddDirectory(False)
ROOT.TH2.AddDirectory(False)
ROOT.gStyle.SetOptStat(0)
# ROOT.gStyle.SetTitleH(0.1,"t")
# ROOT.gStyle.SetTitleW(1,"t")

class plotter:
    
    def __init__(self, outFile, inFile,ms,qts,qtr):
        
        self.ms = ms
        self.qts = qts
        self.qtr = qtr
        self.inFile = inFile # indir containig the various output
        self.outFile = outFile+'_m'+self.ms+'_qt'+self.qts+'_cut'+self.qtr

        
        self.dir ='WToMu/prefit_Signal/'

        self.signDict = {
            'minus' : [1, ROOT.kRed+1, "W^{-}#rightarrow #mu^{-}#bar{#nu}_{#mu}"],
            'plus' :  [2, ROOT.kRed+2, "W^{+}#rightarrow #mu^{+}#nu_{#mu}"]
        }
        
        self.histoDict ={} 
        
        self.extSyst = {
            "LHEPdfWeight" : ["_LHEPdfWeightHess{}".format(i+1) for i in range(60)],
            "alphaS"       : ["_alphaSUp", "_alphaSDown"],
            "mass"         : ["_massUp","_massDown"],
            "Qt"          : ["_QtUp","_QtDown"], 
            "Nominal"    : ['']
}
        
        self.groupedSystColors = {
            "LHEPdfWeight" : [ROOT.kRed+1, 'PDF+#alpha_{s}'],
            "Nominal" : [1, 'Stat. Unc. 4 fb^{-1}'],
            "alphaS" : [ROOT.kOrange-3, '#alpha_{s}'],
            "Qt" : [ROOT.kGreen-3, "q_{T}^{W} #pm "+self.qts+"% [0,"+self.qtr+" GeV]"],
            "mass" : [ROOT.kBlue-4, 'm_{W} #pm '+self.ms+' MeV', 35],
            "PDF" : [ROOT.kRed+1, 'PDF+#alpha_{s}']
        }
        
        # self.doNotPlotGroup = ["alphaS" ] #already included in other groups (summed)

    def varBinWidth_modifier(self,histo):
        for i in range(1, histo.GetNbinsX()+1):
            old = histo.GetBinContent(i)
            bin_width = histo.GetXaxis().GetBinWidth(i)
            histo.SetBinContent(i, old/bin_width)
        
    # def CloneEmpty(self, histo,name) :
    #     hout = histo.Clone(name)
    #     for i in range(0, histo.GetNbinsX()+2) :
    #         hout.SetBinContent(i,0)
    #         hout.SetBinError(i,0)
    #     return hout 
            
    def getHistos(self):
        inFile = ROOT.TFile.Open(self.inFile)
        for sKind, sList in self.extSyst.items():
             for sName in sList :
                 h2 = inFile.Get(self.dir+sKind+"/Mu1_pt"+sName)
                 
                 for s,sInfo in self.signDict.items() :
                    self.histoDict[s+sName] = h2.ProjectionX(h2.GetName() + s,sInfo[0],sInfo[0])
                    self.varBinWidth_modifier(self.histoDict[s+sName])


    def plotStack(self,skipSyst=[]):

        self.getHistos()
        outFile =  ROOT.TFile(self.outFile+'.root', "RECREATE")
        
        #do the ratios
        for s,sInfo in self.signDict.items() :
            for sKind, sList in self.extSyst.items():
                # if sKind =='Nominal' : continue
                for sName in sList :
                    self.histoDict['ratio'+s+sName] = self.histoDict[s].Clone('ratio'+s+sName)
                    self.histoDict['ratio'+s+sName].Divide(self.histoDict[s+sName])
                
        
        #make the band for PDF+alpha (wrt nominal)
        for s,sInfo in self.signDict.items() : 
            self.histoDict['ratio'+s+'_pdfUp'] = self.histoDict[s].Clone('ratio'+s+'pdfUp')
            self.histoDict['ratio'+s+'_pdfDown'] = self.histoDict[s].Clone('ratio'+s+'pdfDown')
            for i in range(1,self.histoDict[s].GetNbinsX()+1) :
                deltaPDF = 0 
                for sName in self.extSyst['LHEPdfWeight'] :
                    deltaPDF+= (self.histoDict['ratio'+s+sName].GetBinContent(i)-1)**2
                
                deltaAlphaUp = (self.histoDict['ratio'+s+'_alphaSUp'].GetBinContent(i)-1)**2
                deltaAlphaDown = (self.histoDict['ratio'+s+'_alphaSDown'].GetBinContent(i)-1)**2

                deltapdfUp = math.sqrt(deltaPDF+deltaAlphaUp)
                deltaPDFdown = math.sqrt(deltaPDF+deltaAlphaDown)
                
                self.histoDict['ratio'+s+'_pdfUp'].SetBinContent(i,1+deltapdfUp)
                self.histoDict['ratio'+s+'_pdfDown'].SetBinContent(i,1-deltaPDFdown)
        
            #redbuild the absolute pdfUp/Down 
            self.histoDict[s+'_pdfUp'] = self.histoDict[s].Clone(s+'pdfUp')
            self.histoDict[s+'_pdfDown'] = self.histoDict[s].Clone(s+'pdfDown')
            # self.histoDict[s+'_pdfUp'].Multiply(self.histoDict['ratio'+s+'_pdfUp'])
            # self.histoDict[s+'_pdfDown'].Multiply(self.histoDict['ratio'+s+'_pdfDown'])
            for i in range(1,self.histoDict[s].GetNbinsX()+1) :
                deltaPDF = 0 
                for sName in self.extSyst['LHEPdfWeight'] :
                    deltaPDF+= (self.histoDict[s+sName].GetBinContent(i)-self.histoDict[s].GetBinContent(i))**2
                
                deltaAlphaUp = (self.histoDict[s+'_alphaSUp'].GetBinContent(i)-self.histoDict[s].GetBinContent(i))**2
                deltaAlphaDown = (self.histoDict[s+'_alphaSDown'].GetBinContent(i)-self.histoDict[s].GetBinContent(i))**2

                deltapdfUp = math.sqrt(deltaPDF+deltaAlphaUp)
                deltaPDFdown = math.sqrt(deltaPDF+deltaAlphaDown)
                
                self.histoDict[s+'_pdfUp'].SetBinContent(i,self.histoDict[s].GetBinContent(i)+deltapdfUp)
                self.histoDict[s+'_pdfDown'].SetBinContent(i,self.histoDict[s].GetBinContent(i)-deltaPDFdown)
                  
        self.extSyst['PDF'] = ['_pdfUp','_pdfDown']
                
        #color and aestethics
        for s,sInfo in self.signDict.items() : 
            for sKind, sList in self.extSyst.items():  
                for sName in sList :
                    self.histoDict[s+sName].SetLineColor(self.groupedSystColors[sKind][0])
                    self.histoDict[s+sName].SetLineWidth(2)
                    self.histoDict[s+sName].SetFillStyle(0)
                    self.histoDict['ratio'+s+sName].SetLineColor(self.groupedSystColors[sKind][0])
                    self.histoDict['ratio'+s+sName].SetLineWidth(2)
        
            self.histoDict['ratio'+s].SetFillColor(1)
            self.histoDict['ratio'+s].SetFillStyle(3002)
            self.histoDict['ratio'+s].GetXaxis().SetTitle('p_{T}^{#mu} [GeV]')
            self.histoDict['ratio'+s].GetYaxis().SetTitle('Var/Nom')
            self.histoDict['ratio'+s].SetTitle('')
            self.histoDict['ratio'+s].GetYaxis().SetTitleOffset(0.50)#0.25
            self.histoDict['ratio'+s].GetYaxis().SetNdivisions(506)
            self.histoDict['ratio'+s].SetTitleSize(0.10,'y')#0.15
            self.histoDict['ratio'+s].SetLabelSize(0.08,'y')#0.12
            self.histoDict['ratio'+s].GetXaxis().SetTitleOffset(0.8)
            self.histoDict['ratio'+s].SetTitleSize(0.11,'x')#0.18
            self.histoDict['ratio'+s].SetLabelSize(0.08,'x')#0.16
            self.histoDict['ratio'+s].GetYaxis().SetRangeUser(0.975,1.025)
            
            self.histoDict[s].GetXaxis().SetTitle('p_{T}^{#mu} [GeV]')
            self.histoDict[s].GetYaxis().SetTitle('dN/dp_{T} [GeV^{-1}]')
            # self.histoDict[s].SetTitle('Muon trasverse momentum,'+sInfo[2])
            self.histoDict[s].SetTitle('')
            # self.histoDict[s].SetMaximum(1.3*self.histoDict[s].GetMaximum()) 
            self.histoDict[s].GetYaxis().SetTitleOffset(1.3)
            self.histoDict[s].GetXaxis().SetTitleOffset(3)
            self.histoDict[s].GetXaxis().SetLabelOffset(3)
            self.histoDict[s].GetYaxis().SetTitleOffset(0.55)#0.25
            self.histoDict[s].SetTitleSize(0.09,'y')#0.15
            self.histoDict[s].SetLabelSize(0.06,'y')#0.12

            
            
        #legend
        legDict = {}
        for s,sInfo in self.signDict.items() : 
            legDict[s] = ROOT.TLegend(0.59, 0.45, 0.988, 0.97)
            # legDict[s].SetFillStyle(0)
            # legDict[s].SetBorderSize(0)
            legDict[s].AddEntry(self.histoDict[s],self.groupedSystColors['Nominal'][1]+", #mu="+str(round(self.histoDict[s].GetMean(),3))+' GeV')
            legDict[s].SetMargin(0.1)
            legDict[s].SetHeader(" "+sInfo[2])
            for sKind, sList in self.extSyst.items():  
                if sKind =='alphaS' : continue
                if sKind =='LHEPdfWeight' : continue
                if sKind =='Nominal' : continue
                
                dmu = round(abs(1000*(self.histoDict[s+sList[0]].GetMean()-self.histoDict[s].GetMean())),0)#in MeV
                legDict[s].AddEntry(self.histoDict[s+sList[0]],self.groupedSystColors[sKind][1]+", #Delta#mu="+str(dmu)+' MeV')
        
        
        #canvas
        for s,sInfo in self.signDict.items() :
            can = ROOT.TCanvas('pT_'+s,'pT_'+s,1600,1400)
            can.cd()
            pad_histo = ROOT.TPad("pad_histo_"+s, "pad_histo_"+s,0,0.5,1,1)#0.2
            pad_ratio = ROOT.TPad("pad_ratio_"+s, "pad_ratio_"+s,0,0,1,0.5)
            pad_histo.SetBottomMargin(0.02)
            pad_histo.Draw()
            pad_ratio.SetTopMargin(0)
            pad_ratio.SetBottomMargin(0.2)
            pad_ratio.Draw()
            
            pad_histo.cd()
            pad_histo.SetGridx()
            pad_histo.SetGridy()
            self.histoDict[s].Draw()
            
            for sKind, sList in self.extSyst.items():
                if sKind =='Nominal' : continue
                if sKind =='alphaS' : continue
                if sKind =='LHEPdfWeight' : continue
                for sName in sList : 
                    self.histoDict[s+sName].Draw("same")
            
            legDict[s].Draw("SAME")
            
            pad_ratio.cd()
            pad_ratio.SetGridx()
            pad_ratio.SetGridy()
            
            self.histoDict['ratio'+s].Draw('E3')
            for sKind, sList in self.extSyst.items():
                if sKind =='Nominal' : continue
                if sKind =='alphaS' : continue
                if sKind =='LHEPdfWeight' : continue
                for sName in sList : 
                    self.histoDict['ratio'+s+sName].Draw("hist same")
            
            can.SaveAs("{name}_{sign}.pdf".format(name=self.outFile,sign=s))
            can.SaveAs("{name}_{sign}.png".format(name=self.outFile,sign=s))
            
            outFile.cd()
            can.Write()
        
        
        

    
parser = argparse.ArgumentParser("")
parser.add_argument('-o','--output', type=str, default='TEST',help="name of the output file")
parser.add_argument('-i','--input', type=str, default='TEST',help="name of the input file")
parser.add_argument('-m','--mShift', type=str, default='10',help="mass shift (meV)")
parser.add_argument('-q','--qtShift', type=str, default='4',help="qt shift (per cent)")
parser.add_argument('-r','--qtrange', type=str, default='5',help="qt shift range (GeV)")

args = parser.parse_args()
OUTPUT = args.output
INPUT = args.input
MSHIFT = args.mShift
QTSHIFT = args.qtShift
QTRANGE = args.qtrange

p=plotter(outFile=OUTPUT, inFile = INPUT, ms=MSHIFT, qts = QTSHIFT, qtr=QTRANGE)
p.plotStack()

