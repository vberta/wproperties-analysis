import os
import ROOT
import copy
import sys

class plotter:
    
    def __init__(self, outdir, indir = '', norm = 1):

        self.indir = indir # indir containig the various outputs
         # list of files in each indirs
        self.canvas = []
        self.outdir = outdir
        self.norm = norm
        self.hmap = {}
        self.fileList = {
        "WJets"       : 'WJets_plots.root',
        "DYJets"      : 'DYJets_plots.root',
        "WtoTau"      : 'WJets_plots.root',
        "TW"          : 'TW_plots.root',
        "TTbar"       : 'TTJets_plots.root',
        "ST"          : 'SingleTop_plots.root',
        "DiBoson"     : 'Diboson_plots.root',
        "SIGNAL_Fake" : 'Data_plots.root',
        "Data"        : 'Data_plots.root'
            }

        self.dirList = {
        "WJets"       : 'prefit_SignalWToMu/Nominal',
        "DYJets"      : 'prefit_Signal/Nominal',
        "WtoTau"      : 'prefit_SignalWToTau/Nominal',
        "TW"          : 'prefit_Signal/Nominal',
        "TTbar"       : 'prefit_Signal/Nominal',
        "ST"          : 'prefit_Signal/Nominal',
        "DiBoson"     : 'prefit_Signal/Nominal',
        "SIGNAL_Fake" : 'prefit_fakes/Nominal',
        "Data"        : 'prefit_Signal/Nominal'
            }

        self.colors = {
        "WtoMuP"      : ROOT.kBlue-1,
        "WtoMuN"      : ROOT.kBlue-1,
        "WtoTau"      : ROOT.kRed,
        "DYJets"      : ROOT.kAzure+2,
        "TW"          : ROOT.kGreen+3,
        "TTbar"       : ROOT.kGreen+3,
        "ST"          : ROOT.kGreen+3,
        "DiBoson"     : ROOT.kViolet+2,
        "SIGNAL_Fake" : ROOT.kGray+2,
        "Data"        : 1
            }

        self.legendtag = {
        "WtoMuP"      : "W^{+}#rightarrow #mu^{+}#nu_{#mu}",
        "WtoMuN"      : "W^{-}#rightarrow #mu^{-}#nu_{#bar{#mu}}",
        "WtoTau"      : "W^{#pm}#rightarrow #tau^{#pm}#nu_{#tau}",
        "SIGNAL_Fake" : "Fakes",
        "DYJets"      : "DYJets",
        "TW"          : "Top",
        "TTbar"       : "t#bar{t}",
        "ST"          : "Single-t",
        "DiBoson"     : "di-boson",
        "Data"        : "Data"
            }

        self.axisnames = {
            "Mu1_pt_plus"   :  ["p_{T} #mu^{+}", "Events"],
            "Mu1_pt_minus"  :  ["p_{T} #mu^{-}", "Events"],
            "Mu1_eta_plus"  :  ["#eta #mu^{+}", "Events"],
            "Mu1_eta_minus" :  ["#eta #mu^{-}", "Events"],
                "MT_plus"            :  ["M_{T}", "Events"],      
                "MT_minus"            :  ["M_{T}", "Events"],      
        }

        ROOT.gROOT.SetBatch()

        if not os.path.exists(self.outdir):
            os.system("mkdir -p " + self.outdir)

    def density(self,hp):
        variable_width = False
        bin_width = hp.GetXaxis().GetBinWidth(1)
        for i in range(2, hp.GetNbinsX()+1):
            if hp.GetXaxis().GetBinWidth(i)!=bin_width:
                variable_width = True
                break
        for i in range(1, hp.GetNbinsX()+1):
            old = hp.GetBinContent(i)
            bin_width = hp.GetXaxis().GetBinWidth(i)
            hp.SetBinContent(i, old/bin_width)
        return hp

    def getHistos(self):

        self.histos = []
        os.chdir(self.indir)
        for proc, fin in self.fileList.iteritems():
            print proc
            subdir = self.dirList[proc]
            htagplus = proc
            htagminus = htagplus
            hlist = []
            fIn = ROOT.TFile.Open(self.fileList[proc])
            fDir = fIn.Get(subdir)
            for key in fDir.GetListOfKeys():
                h2d=ROOT.TH2D
                h2d=fDir.Get(key.GetName())
                hminus = h2d.ProjectionX(key.GetName() + "_minus", 1,1)
                hminus.Sumw2()
                axiskey = hminus.GetName()
                hminus=self.density(hminus)
                hlist.append((copy.deepcopy(hminus),htagminus))

                hplus = h2d.ProjectionX(key.GetName() + "_plus", 2,2)
                hplus.Sumw2()
                axiskey = hplus.GetName()
                hplus=self.density(hplus)
                hlist.append((copy.deepcopy(hplus),htagplus))
            self.histos.append(hlist)

        os.chdir('..')

        self.histos = zip(*self.histos) # now in the right order
        print self.hmap

    def plotStack(self):

        self.getHistos()
        fname = "{dir}/stackplots.root".format(dir=self.outdir)
        outF =  ROOT.TFile(fname, "RECREATE")
        for group in self.histos: 

            hs = ROOT.THStack((group[0])[0].GetName(),"")

            c = ROOT.TCanvas(hs.GetName(), '')

            legend = ROOT.TLegend(0.52, 0.75, 0.88, 0.92)
            legend.SetNColumns(3);
            legend.SetFillColor(0)
            legend.SetBorderSize(0)
            legend.SetTextSize(0.03)

            hdata = ROOT.TH1D()
            hsignal = ROOT.TH1D()
            for i,tup in enumerate(group):
                print i, '\t', tup[1]
                if 'Data' in tup[1]: 
                    hdata = tup[0]
                    hdata.SetMarkerStyle(20)
                    hdata.SetMarkerColor(self.colors["Data"])
                    continue
                ltag = tup[1]
                if tup[1] == "WJets":
                    hsignal = tup[0]
                    continue
                tup[0].Scale(self.norm)
                tup[0].SetFillStyle(1001)
                tup[0].SetLineWidth(0)
                tup[0].SetFillColor(self.colors[ltag])
                hs.Add(tup[0])
                if tup[1] == 'ST' or tup[1] == 'TTbar' : continue
                legend.AddEntry(tup[0], self.legendtag[ltag], "f")
            
            #Add signal at the end
            if "plus" in hsignal.GetName() : ltag = "WtoMuP"
            if "minus" in hsignal.GetName(): ltag = "WtoMuN"
            hsignal.Scale(self.norm)
            hsignal.SetFillStyle(1001)
            hsignal.SetLineWidth(0)
            hsignal.SetFillColor(self.colors[ltag])
            hs.Add(hsignal)
            legend.AddEntry(hsignal, self.legendtag[ltag], "f")
                
            legend.AddEntry(hdata, self.legendtag["Data"], "PE1")

            c.SetTicks(0, 1)
            c.cd()

            hs.Draw("HIST")
            hs.GetXaxis().SetTitle(self.axisnames[hdata.GetName()][0])
            hs.GetYaxis().SetTitle(self.axisnames[hdata.GetName()][1])
            hs.GetYaxis().SetTitleOffset(1.2)
            maxdata = hdata.GetMaximum()
            maxstack = hs.GetMaximum()
            hs.SetMaximum(1.5*max(maxdata,maxstack))
            #hdata.Draw("PE1same")
            rp = ROOT.TRatioPlot(hs, hdata)
            rp.Draw()
            rp.GetLowerRefYaxis().SetRangeUser(0.9,1.1)
            rp.GetLowYaxis().SetNdivisions(505)
            rp.GetLowerRefYaxis().SetTitle("MC / DATA")

            legend.Draw()
            c.Update()
            c.SaveAs("{dir}/{c}.pdf".format(dir=self.outdir,c=c.GetName()))
            c.SaveAs("{dir}/{c}.png".format(dir=self.outdir,c=c.GetName()))

            outF.cd()
            c.Write()
        outF.Save()
        outF.Close()

p=plotter(sys.argv[1], indir = sys.argv[1])
p.plotStack()
