import ROOT

proj = 'x'
region = 'AISO'

fileNoWeight = ROOT.TFile.Open("NEWFAKE_WHELICITYSF_prev/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.root")
fileNoWeight.cd()
hNoWeight = ROOT.gDirectory.Get(region+"_nominal/"+region+"__SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge__").Project3D(proj).Clone("hold")
for i in range(1,hNoWeight.GetNbinsX()+1): hNoWeight.SetBinContent(i, hNoWeight.GetBinContent(i)/hNoWeight.GetBinWidth(i) )

#hNoWeight.Draw("HISTE")

fileWeight = ROOT.TFile.Open("NEWFAKE_WHELICITYSF_debug/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.root")
fileWeight.cd()
hWeight = ROOT.gDirectory.Get(region+"_nominal/"+region+"__SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge__").Project3D(proj).Clone("hnew")
#fileWeight.Close()

for i in range(1,hWeight.GetNbinsX()+1): hWeight.SetBinContent(i, hWeight.GetBinContent(i)/hWeight.GetBinWidth(i) )

hWeight.SetLineColor(ROOT.kRed)
#hWeight.Draw("HISTESAME")

print proj
print "w/o weight:", hNoWeight.Integral()
print "w/  weight:", hWeight.Integral()
print "Ratio w/wo: " , hWeight.Integral()/hNoWeight.Integral()

hWeight.Divide(hNoWeight)
hWeight.Draw("HISTE")

raw_input()
fileNoWeight.Close()
fileWeight.Close()

