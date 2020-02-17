import os
import sys
import json
import argparse
import ROOT
import pprint 
pp = pprint.PrettyPrinter(indent=2)

parser = argparse.ArgumentParser("")
parser.add_argument('-o', '--output_dir',type=str, default='TEST', help="")
parser.add_argument('-c', '--category',type=str, default='SIGNAL_Plus', help="")
parser.add_argument('-v', '--variable',type=str, default='SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge', help="")
parser.add_argument('-s', '--systematics',type=str, default='', help="")
parser.add_argument('-p', '--projection',type=str, default='x', help="")
parser.add_argument('-x', '--xtitle',type=str, default='', help="")
parser.add_argument('-y', '--ytitle',type=str, default='Events', help="")
parser.add_argument('-t', '--tag',type=str, default='eta', help="")
parser.add_argument('-b', '--batch', help="", action='store_true')
parser.add_argument('-l', '--slices',type=str, default="", help="")
args = parser.parse_args()
output_dir = args.output_dir
systematics = args.systematics
projection  = args.projection
category    = args.category
variable    = args.variable
xtitle      = args.xtitle
ytitle      = args.ytitle
tag         = args.tag
slices      = args.slices

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
    "Z"           : "Z/#gamma*#rightarrow#mu^{+}#mu^{-}",
    "ZtoMuMu"     : "Z/#gamma*#rightarrow#mu^{+}#mu^{-}",
    "ZtoTauTau"   : "Z/#gamma*#rightarrow#tau^{+}#tau^{-}",
    "TTbar"       : "t#bar{t}",
    "ST"          : "Single-t",
    "DiBoson"     : "Diboson",
    "Data"        : "Data"
    }

def setup_pad1(pad1):
    pad1.SetBottomMargin(0)
    pad1.SetLeftMargin(0.15)
    pad1.SetGridx()

def setup_pad2(pad2):
    pad2.SetLeftMargin(0.15)
    pad2.SetTopMargin(0)
    pad2.SetBottomMargin(0.25)
    pad2.SetGridx()

def setup_leg(leg):
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.SetTextSize(0.04)
    leg.SetFillColor(10)
    leg.SetNColumns(3)
    
def setup_hstack(h, ytitle):
    h.GetYaxis().SetLabelSize(0.04)
    h.GetYaxis().SetTitleSize(25)
    h.GetYaxis().SetTitleFont(43)
    h.GetYaxis().SetTitleOffset(1.55)
    h.GetYaxis().SetTitle(ytitle)

def setup_hratio(hratio, xtitle):
    hratio.SetTitle("")
    hratio.SetLineColor(ROOT.kBlack)
    hratio.SetMinimum(0.9) 
    hratio.SetMaximum(1.1)
    hratio.Sumw2()
    hratio.SetStats(0)
    hratio.SetMarkerStyle(ROOT.kFullCircle)
    hratio.SetMarkerSize(0.9)
    hratio.GetXaxis().SetTitle(xtitle)
    hratio.GetXaxis().SetTitleSize(25)
    hratio.GetXaxis().SetTitleFont(43)
    hratio.GetXaxis().SetTitleOffset(3.)
    hratio.GetXaxis().SetLabelFont(43)
    hratio.GetXaxis().SetLabelSize(18)
    hratio.GetYaxis().SetTitle("Data/Pred.")
    hratio.GetYaxis().SetNdivisions(505)
    hratio.GetYaxis().SetTitleSize(25)
    hratio.GetYaxis().SetTitleFont(43)
    hratio.GetYaxis().SetTitleOffset(1.55)
    hratio.GetYaxis().SetLabelFont(43)
    hratio.GetYaxis().SetLabelSize(18)

def density(hp, ytitle):
    variable_width = False
    bin_width = hp.GetXaxis().GetBinWidth(1)
    for i in range(2, hp.GetXaxis().GetNbins()+1):
        if hp.GetXaxis().GetBinWidth(i)!=bin_width:
            variable_width = True
    if variable_width:
        if '/bin' not in ytitle: ytitle += '/bin'
        for i in range(1, hp.GetXaxis().GetNbins()+1):
            old = hp.GetBinContent(i)
            bin_width = hp.GetXaxis().GetBinWidth(i)
            hp.SetBinContent(i, old/bin_width)
    return ytitle

def plot(category, variable, proj, xtitle, ytitle, tag, slices):

    with open(output_dir+'/hadded/dictionaryHisto_'+variable+'.json', 'r') as fp:
        js = json.load(fp)
        cat = js[category]

        c = ROOT.TCanvas("c", "canvas", 700, 700)

        pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
        setup_pad1(pad1)
        pad1.Draw()
        pad1.cd()

        leg = ROOT.TLegend(0.18,0.70,0.66,0.88, "","brNDC")
        setup_leg(leg)

        hs = ROOT.THStack("hs", "")
        hmaster = None
        hData = None
        hMC = None
        open_files = {}
        to_stack = []
        nominals = {}
        systs = {}

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
                    if hmaster==None: hmaster = h
                    if 'Plus' in category:    h.GetZaxis().SetRange(2,2)
                    elif 'Minus' in category: h.GetZaxis().SetRange(1,1)
                    else: pass
                    if slices!="":
                        sl1 = int(slices.split('_')[0])
                        sl2 = int(slices.split('_')[1])
                        if   proj=="x": h.GetYaxis().SetRange(sl1,sl2)
                        elif proj=="y": h.GetXaxis().SetRange(sl1,sl2)
                    hp = h.Project3D(proj+"e").Clone(pname+"_nominal")
                    new_ytitle = density(hp,ytitle)
                    if pname!='Data':
                        if not nominals.has_key(pname): nominals[pname] = hp.Clone(pname+"_nominal_copy")
                        to_stack.append( [pname, hp] )
                        print "MC: adding "+pname+" ("+fname+"/"+hname_fix+") -> "+"{:.3E}".format(hp.Integral())
                    else:
                        hData = hp
                        print "Data: adding "+pname+ " ("+fname+"/"+hname_fix+") -> "+"{:.3E}".format(hp.Integral())
            else:
                pass                            
        
        to_stack.sort(key=lambda h: h[1].Integral(), reverse=False)
        idx_AISO_fake = -1
        idx_SIGNAL_fake = -1
        for ih,h in enumerate(to_stack):
            if   h[0]=='AISO_Fake'   : idx_AISO_fake = ih
            elif h[0]=='SIGNAL_Fake' : idx_SIGNAL_fake = ih
        if idx_AISO_fake!=-1 and idx_SIGNAL_fake!=-1:
            to_stack[idx_AISO_fake][1].Add( to_stack[idx_SIGNAL_fake][1] )            
            #to_stack[idx_AISO_fake][1].Scale(0.6)
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

        setup_hstack(hs.GetHistogram(), new_ytitle)

        hData.SetLineColor(ROOT.kBlack)
        hData.SetMarkerStyle(ROOT.kFullCircle)
        hData.SetMarkerSize(0.9)
        leg.AddEntry(hData, nicknames['Data'], "P")
        hData.Draw("PESAME")
        leg.Draw()

        lat = ROOT.TLatex( 0.69, 0.85, "35.9 fb^{-1} (2016)")
        lat.SetNDC()
        lat.SetTextFont(43)
        lat.SetTextSize(22)
        lat.Draw()

        if slices!="":
            sl1 = int(slices.split('_')[0])
            sl2 = int(slices.split('_')[1])
            #if sl2==sl1: sl2 +=1
            txtslice = ""
            if proj=="x":
                txtslice = "p_{T}#in["+"{:0.1f}".format( hmaster.GetYaxis().GetBinLowEdge(sl1) )+ \
                    ","+"{:0.1f}".format( hmaster.GetYaxis().GetBinLowEdge(sl2) + hmaster.GetYaxis().GetBinWidth(sl2) )+"]"
            elif proj=="y":
                txtslice = "#eta#in["+"{:0.1f}".format( hmaster.GetXaxis().GetBinLowEdge(sl1) )+ \
                    ","+"{:0.1f}".format( hmaster.GetXaxis().GetBinLowEdge(sl2) + hmaster.GetXaxis().GetBinWidth(sl2) )+"]"
            lat2 = ROOT.TLatex( 0.69, 0.72, txtslice)
            lat2.SetNDC()
            lat2.SetTextFont(43)
            lat2.SetTextSize(22)
            lat2.Draw()

        c.cd()
        pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
        setup_pad2(pad2)
        pad2.Draw()
        pad2.cd()

        hratio = hData.Clone("hratio")
        hratio.Divide(hMC)
        setup_hratio(hratio, xtitle)
        hratio.Draw("ep")
        hMCStat = hMC.Clone("hMCStat")
        hMCStat.Clear()
        hMCStat.SetFillStyle(3002)
        hMCStat.SetFillColor(ROOT.kGray+1)
        for i in range(1,hMCStat.GetNbinsX()+1):
            hMCStat.SetBinContent(i, 1.0)
            hMCStat.SetBinError(i, hMC.GetBinError(i)/hMC.GetBinContent(i) if hMC.GetBinContent(i)>0. else 0.0)
        hMCStat.Draw("E3SAME")

        line = ROOT.TLine( hratio.GetXaxis().GetXmin(), 1.0, hratio.GetXaxis().GetXmax(), 1.0)
        line.SetLineWidth(1)
        line.SetLineStyle(ROOT.kSolid)
        line.Draw()
        lineUp = ROOT.TLine( hratio.GetXaxis().GetXmin(), 1.05, hratio.GetXaxis().GetXmax(), 1.05)
        lineUp.SetLineWidth(2)
        lineUp.SetLineStyle(ROOT.kDashed)
        lineUp.Draw()
        lineDown = ROOT.TLine( hratio.GetXaxis().GetXmin(), 0.95, hratio.GetXaxis().GetXmax(), 0.95)
        lineDown.SetLineWidth(2)
        lineDown.SetLineStyle(ROOT.kDashed)
        lineDown.Draw()

        for key,val in cat.items():
            if key in ["nominal", "fakerate"]: continue
            for kvar,var in val.items():
                inputs = var["inputs"]
                for i in inputs: 
                    pname = i["pname"]
                    fname = i["fname"]
                    hname = i["hname"]
                    if not open_files.has_key(fname):
                        open_files[fname] = ROOT.TFile.Open(output_dir+'/hadded/'+fname)
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
                    if not systs.has_key(key+"_"+kvar):
                        systs[key+"_"+kvar] = h.Project3D(proj+"e").Clone(pname+"_"+key+"_"+kvar)
                        systs[key+"_"+kvar].Add(nominals[pname], -1.0)
                    else:
                        systs[key+"_"+kvar].Add( h.Project3D(proj+"e") )
                        systs[key+"_"+kvar].Add(nominals[pname], -1.0)    

        for k,v in systs.items(): 
            for kp,vp in nominals.items(): v.Add(vp, 1.0)                
            print k, v.Integral()/hMC.Integral() 
        for k,v in systs.items():
            accept = False
            for s in systematics.split(','): 
                if s in k: 
                    accept = True
                    break
            if not accept: continue
            v.Divide(hMC)
            v.SetLineColor(ROOT.kRed)
            v.SetLineWidth(2)
            v.Draw("HISTSAME")

        c.Update()
        c.Draw()

        if not args.batch: raw_input()
        else:
            os.system('mkdir -p '+output_dir+'/plots')
            c.SaveAs(output_dir+'/plots/'+category+'_'+variable+'_'+tag+'.png')
            c.IsA().Destructor( c )

    #for fk,v in open_files.items(): v.Close()
    fp.close()
    return


if __name__ == "__main__":
    plot(category, variable, projection, xtitle, ytitle, tag, slices)
