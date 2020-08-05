import ROOT

In = ROOT.TFile.Open("../TEST/test.root")
f = In.Get("AngCoeff")

h = f.Get("harmonics_AUL")

h2 = ROOT.TH2F("h2","", h.GetNbinsX(),1, h.GetNbinsX(), h.GetNbinsY(),1, h.GetNbinsY())

for i in range(1, h.GetNbinsX()+1):
    for j in range(1, h.GetNbinsY()+1):
        
        bin1D = h.GetBin(i,j)
        h2.SetBinContent(bin1D, h.GetBinContent(bin1D))
        h2.GetXaxis().SetBinLabel(i, "y {:.1f} to {:.1f}".format(h.GetXaxis().GetBinLowEdge(i), h.GetXaxis().GetBinUpEdge(i)))
        h2.GetYaxis().SetBinLabel(j, "pt {:.0f} to {:.0f}".format(h.GetYaxis().GetBinLowEdge(j), h.GetYaxis().GetBinUpEdge(j)))

fOut = ROOT.TFile("out.root", "recreate")
fOut.cd()

h.Write()
h2.Write()
