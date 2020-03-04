import ROOT

proj = 'yx'
region = 'SIGNAL'

fileNoWeight = ROOT.TFile.Open("../DEBUG_SYSTSF/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext2.root")
fileNoWeight.cd()
hNoWeightXYZ = ROOT.gDirectory.Get(region+"_nominal/"+region+"__SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge__")
hNoWeight = hNoWeightXYZ.Project3D(proj).Clone("hold")

fileWeight = ROOT.TFile.Open("../DEBUG_SYSTSF/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext2.root")
fileWeight.cd()
hWeightXYZ = ROOT.gDirectory.Get(region+"_ISO/"+region+"__SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge__ISOreco_mc_syst0Down")
hWeight = hWeightXYZ.Project3D(proj).Clone("hnew")

print proj
print "w/o weight:", hNoWeight.Integral()
print "w/  weight:", hWeight.Integral()
print "Ratio w/wo: " , hWeight.Integral()/hNoWeight.Integral()

hWeight.Divide(hNoWeight)
hWeight.Draw("COLZ")

raw_input()
fileNoWeight.Close()
fileWeight.Close()

