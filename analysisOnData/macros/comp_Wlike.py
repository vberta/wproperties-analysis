import ROOT

fileZ = ROOT.TFile.Open("../DEBUG_DIMUON_WLIKE/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext2.root")
fileZ.cd()
h1Z= ROOT.gDirectory.Get("DIMUON_ZtoMuMu_nominal/DIMUON_ZtoMuMu__SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_corrected_MET_nom_Wlike_mt__").Project3D('ze').Clone("h1Z")
h2Z = ROOT.gDirectory.Get("DIMUON_ZtoMuMu_nominal/DIMUON_ZtoMuMu__SelMuon2_eta_SelMuon2_corrected_pt_SelMuon2_corrected_MET_nom_Wlike_mt__").Project3D('ze').Clone("h2Z")

h1Z.Add(h2Z)
h1Z.Scale(13.0)
h1Z.Draw("HISTE")

fileW = ROOT.TFile.Open("../TEST_WHELICITYSF_V3/hadded/WJets.root")
fileW.cd()
hPW = ROOT.gDirectory.Get("SIGNAL_WtoMuP_nominal/SIGNAL_WtoMuP__SelMuon1_corrected_MET_nom_mt_SelMuon1_corrected_MET_nom_hpt_SelMuon1_charge__").Project3D('xe').Clone("hPW")
hNW = ROOT.gDirectory.Get("SIGNAL_WtoMuN_nominal/SIGNAL_WtoMuN__SelMuon1_corrected_MET_nom_mt_SelMuon1_corrected_MET_nom_hpt_SelMuon1_charge__").Project3D('xe').Clone("hNW")

hW_QCD = ROOT.gDirectory.Get("QCD_nominal/QCD__SelMuon1_corrected_MET_nom_mt_SelMuon1_corrected_MET_nom_hpt_SelMuon1_charge__").Project3D('xe').Clone("hWQCD")

hPW.Add(hNW)
hPW.Add(hW_QCD)
hPW.SetLineColor(ROOT.kRed)
hPW.Draw("HISTESAME")

raw_input()

