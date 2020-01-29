import os
import sys
import json
import argparse
import ROOT
import pprint 
pp = pprint.PrettyPrinter(indent=2)

parser = argparse.ArgumentParser("")
parser.add_argument('-o', '--output_dir',type=str, default='TEST', help="")
parser.add_argument('-b', '--batch', help="", action='store_true')
args = parser.parse_args()
output_dir = args.output_dir

if args.batch:
    from sys import argv
    argv.append( '-b-' )
    ROOT.gROOT.SetBatch(True)
    argv.remove( '-b-' )

colors = {
    "WtoMuP"      : ROOT.kBlue-7,
    "WtoMuN"      : ROOT.kRed-7,
    "W"           : ROOT.kRed-7,
    "ZtoMuMu"     : ROOT.kCyan-3,
    "ZtoTauTau"   : ROOT.kOrange+5,
    "WtoTau"      : ROOT.kOrange+1,
    "AISO_Fake"   : ROOT.kGray,
    "SIGNAL_Fake" : ROOT.kGray,
    "Z"           : ROOT.kCyan-3,
    "TTbar"       : ROOT.kYellow-3,
    "ST"          : ROOT.kYellow-7,
    "DiBoson"     : ROOT.kMagenta-5,
    "Data"        : 1
    }

nicknames = {
    "WtoMuP"      : "W^{+}#rightarrow#mu^{+}#nu_{#mu}",
    "WtoMuN"      : "W^{-}#rightarrow#mu^{-}#nu_{#bar{#mu}}",
    "WtoTau"      : "W^{#pm}#rightarrow#tau#nu",
    "W"           : "W^{#pm}",
    "AISO_Fake"   : "Fakes",
    "SIGNAL_Fake" : "Fakes",
    "Z"           : "Z/#gamma^{*}#rightarrow#mu^{+}#mu^{-}",
    "ZtoMuMu"     : "Z/#gamma^{*}#rightarrow#mu^{+}#mu^{-}",
    "ZtoTauTau"   : "Z/#gamma^{*}#rightarrow#tau^{+}#tau^{-}",
    "TTbar"       : "t#bar{t}",
    "ST"          : "Single-t",
    "DiBoson"     : "Diboson",
    "Data"        : "Data"
    }

def plot(category, variable, proj, xtitle, ytitle, tag):

    with open(output_dir+'/hadded/dictionary2_'+variable+'.json', 'r') as fp:
        js = json.load(fp)
        cat = js[category]

        c = ROOT.TCanvas("c", "canvas", 700, 700)
        c.SetLeftMargin(0.15)

        pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
        pad1.SetBottomMargin(0)
        pad1.SetGridx()
        pad1.Draw()
        pad1.cd()

        leg = ROOT.TLegend(0.12,0.65,0.35,0.88, "","brNDC")
        leg.SetFillStyle(0)
        leg.SetBorderSize(0)
        leg.SetTextSize(0.03)
        leg.SetFillColor(10)

        hs = ROOT.THStack("hs", "")
        hData = None
        hMC = None
        open_files = {}
        to_stack = []

        h_base = None
        for key,val in cat.items():
            if key in ["nominal", "fakerate"]:
                var = "" if key=="nominal" else "nominal"
                inputs = val[var]["inputs"]
                for i in inputs: 
                    pname = i["pname"]
                    fname = i["fname"]
                    hname = i["hname"]
                    if not open_files.has_key(fname):
                        open_files[fname] = ROOT.TFile.Open(output_dir+'/hadded/'+fname)
                        #print "Opening file "+fname
                    open_files[fname].cd()
                    hname_fix = hname.replace('*', js["variable"])
                    h = ROOT.gDirectory.Get(hname_fix)
                    if h==None:                     
                        print "File NOT found"
                        continue
                    if 'Plus' in category:
                        h.GetZaxis().SetRange(2,2)
                    elif 'Minus' in category:
                        h.GetZaxis().SetRange(1,1)
                    else:
                        pass
                    hp = h.Project3D(proj+"e").Clone(pname+"_nominal")
                    if pname!='Data':
                        to_stack.append( [pname, hp] )
                        print "MC: adding "+pname+" ("+fname+"/"+hname_fix+") -> "+"{:.3E}".format(hp.Integral())
                    else:
                        hData = hp
                        print "Data: adding "+fname+"/"+hname_fix


        to_stack.sort(key=lambda h: h[1].Integral(), reverse=False)
        idx_AISO_fake = -1
        idx_SIGNAL_fake = -1
        for ih,h in enumerate(to_stack):
            if   h[0]=='AISO_Fake'   : idx_AISO_fake = ih
            elif h[0]=='SIGNAL_Fake' : idx_SIGNAL_fake = ih
        if idx_AISO_fake!=-1 and idx_SIGNAL_fake!=-1:
            to_stack[idx_AISO_fake][1].Add( to_stack[idx_SIGNAL_fake][1] )            
            to_stack[idx_AISO_fake][1].Scale(0.5)
            to_stack.pop(idx_SIGNAL_fake)
        for h in to_stack: 
            h[1].SetFillColor(colors[h[0]])
            h[1].SetFillStyle(1001)            
            hs.Add(h[1])
            if hMC==None: hMC = h[1].Clone("MC")
            else: hMC.Add(h[1])

        to_stack.sort(key=lambda h: h[1].Integral(), reverse=True)
        for h in to_stack:  leg.AddEntry(h[1], nicknames[h[0]], "F")
        hs.SetMaximum( max(hData.GetMaximum(), hs.GetMaximum())*1.30 )
        hs.Draw("HIST")
        hData.SetLineColor(ROOT.kBlack)
        hData.SetMarkerStyle(ROOT.kFullCircle)
        hData.SetMarkerSize(0.8)
        leg.AddEntry(hData, nicknames['Data'], "P")
        hData.Draw("PESAME")
        leg.Draw()

        h = hs.GetHistogram()
        h.GetYaxis().SetLabelSize(18)
        h.GetYaxis().SetTitleSize(20)
        h.GetYaxis().SetTitleFont(43)
        h.GetYaxis().SetTitleOffset(1.15)
        h.GetYaxis().SetTitle(ytitle)

        #axis = ROOT.TGaxis( -5, 20, -5, 220, 20,220,510,"")
        #axis.SetLabelFont(43)
        #axis.SetLabelSize(18)
        #axis.SetTitle(ytitle)
        #axis.SetTitleOffset(0.8)
        #axis.Draw()

        c.cd()
        pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
        pad2.SetTopMargin(0)
        pad2.SetBottomMargin(0.2)
        pad2.SetGridx()
        pad2.Draw()
        pad2.cd()

        hratio = hData.Clone("hratio")
        hratio.SetTitle("")
        hratio.SetLineColor(ROOT.kBlack)
        hratio.SetMinimum(0.8) 
        hratio.SetMaximum(1.2)
        hratio.Sumw2()
        hratio.SetStats(0)
        hratio.Divide(hMC)
        hratio.SetMarkerStyle(21)
        hratio.Draw("ep")

 
        hratio.GetYaxis().SetTitle("Data/MC")
        hratio.GetXaxis().SetTitle(xtitle)
        hratio.GetYaxis().SetNdivisions(505)
        hratio.GetYaxis().SetTitleSize(20)
        hratio.GetYaxis().SetTitleFont(43)
        hratio.GetYaxis().SetTitleOffset(1.35)
        hratio.GetYaxis().SetLabelFont(43)
        hratio.GetYaxis().SetLabelSize(18)
        hratio.GetXaxis().SetTitleSize(20)
        hratio.GetXaxis().SetTitleFont(43)
        hratio.GetXaxis().SetTitleOffset(3.)
        hratio.GetXaxis().SetLabelFont(43)
        hratio.GetXaxis().SetLabelSize(18)

        c.Update()
        c.Draw()
        if not args.batch: raw_input()
        c.SaveAs(output_dir+'/plots/'+category+'_'+variable+'_'+tag+'.png')
        c.IsA().Destructor( c )
    
    for fk,v in open_files.items(): v.Close()
    fp.close()
    return


if __name__ == "__main__":
    #plot('DIMUON',  'SelRecoZ_corrected_qt_SelRecoZ_corrected_y_SelRecoZ_corrected_mass', 'y', 'mass',  'Events', 'mass')
    plot('SIGNAL_Plus',  'SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge', 'x', '#eta',  'Events', 'eta')
    #plot('SIGNAL_Plus',  'SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge', 'y', 'p_{T}', 'Events', 'pt')
    #plot('SIGNAL_Minus', 'SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge', 'x', '#eta',  'Events', 'eta')
    #plot('SIGNAL_Minus', 'SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge', 'y', 'p_{T}', 'Events', 'pt')
