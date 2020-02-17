import ROOT

charge = 'WtoMuP'


fileNoWeight = ROOT.TFile.Open("../GENINCLUSIVE_NOWREWEIGHT/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_GENINCLUSIVE_0.root")
fileNoWeight.cd()
hNoWeight = ROOT.gDirectory.Get("GENINCLUSIVE_"+charge+"_nominal/GENINCLUSIVE_"+charge+"_MC").ProjectionY("_py1",1,1)
#fileNoWeight.Close()

for i in range(1,hNoWeight.GetNbinsX()+1): hNoWeight.SetBinContent(i, hNoWeight.GetBinContent(i)/hNoWeight.GetBinWidth(i) )

#hNoWeight.Draw("HISTE")

fileWeight = ROOT.TFile.Open("../GENINCLUSIVE_WREWEIGHT/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_GENINCLUSIVE_0.root")
fileWeight.cd()
hWeight = ROOT.gDirectory.Get("GENINCLUSIVE_"+charge+"_nominal/GENINCLUSIVE_"+charge+"_MC").ProjectionY("_py2",1,1)
#fileWeight.Close()

for i in range(1,hWeight.GetNbinsX()+1): hWeight.SetBinContent(i, hWeight.GetBinContent(i)/hWeight.GetBinWidth(i) )

hWeight.SetLineColor(ROOT.kRed)
#hWeight.Draw("HISTESAME")

print charge
print "w/o weight:", hNoWeight.Integral()
print "w/  weight:", hWeight.Integral()
print "Ratio: " , (hWeight.Integral()/hNoWeight.Integral())

hWeight.Divide(hNoWeight)
hWeight.Draw("HISTE")

raw_input()
fileNoWeight.Close()
fileWeight.Close()

