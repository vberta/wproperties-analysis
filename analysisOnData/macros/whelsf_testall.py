import ROOT

proj = 'yx'
region = 'SIGNAL'
syst = 'reco'

c = ROOT.TCanvas("c", "canvas", 1600, 800)
ROOT.gStyle.SetOptStat(0)
c.Divide(4,3)

fileWeight = ROOT.TFile.Open("DEBUG_WHELSYSTS2/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.root")
hNoWeight = fileWeight.Get(region+"_nominal/"+region+"__SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge__").Project3D(proj).Clone("hnom")
#fileWeight.cd()

trigger_systs = [syst+"_data_eigen0Up", syst+"_data_eigen0Down", 
                 syst+"_mc_eigen0Up",   syst+"_mc_eigen0Down", 
                 syst+"_data_eigen1Up", syst+"_data_eigen1Down", 
                 syst+"_mc_eigen1Up",   syst+"_mc_eigen1Down", 
                 syst+"_data_eigen2Up", syst+"_data_eigen2Down",
                 syst+"_mc_eigen2Up",   syst+"_mc_eigen2Down"
                 ]

hists = []
for it,t in enumerate(trigger_systs):
    hWeight = fileWeight.Get(region+"_"+("Trigger" if syst=='trigger' else "ISO")+"/"+region+"__SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge__"+("Trigger" if syst=='trigger' else "ISO")+t).Project3D(proj).Clone("hsyst_"+t)
    hists.append( hWeight )
    c.cd(it+1)
    hWeight.SetTitle(t)
    hWeight.SetTitleSize(24)
    hWeight.Divide(hNoWeight)
    print t+" => ratio w/wo: " , hWeight.Integral()    
    hWeight.Draw("COLZ")
    zmin = 0.995
    zmax = 1.005
    if 'eigen0' in t: 
        zmin = 0.990
        zmax = 1.010
    elif 'eigen1' in t: 
        zmin = 0.990
        zmax = 1.010
    hWeight.SetMinimum(zmin)
    hWeight.SetMaximum(zmax)
c.Update()
c.Draw()
raw_input()
c.SaveAs('test_WHelicitySF_'+syst+'.png')
fileWeight.Close()

