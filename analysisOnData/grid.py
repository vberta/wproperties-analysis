import os
import sys
import json
import argparse
import ROOT
import pprint 
import math
import numpy as np
from array import array
import scipy
from scipy import special
pp = pprint.PrettyPrinter(indent=2)

parser = argparse.ArgumentParser("")
parser.add_argument('-o', '--output_dir',type=str, default='TEST', help="")
args = parser.parse_args()
output_dir = args.output_dir

ROOT.Math.MinimizerOptions.SetDefaultMinimizer("Minuit2")

class fit_func:
    def __init__(self, idx_x, idx_y):
        self.idx_x = idx_x
        self.idx_y = idx_y
    def __call__(self, x, parameters):
        y,qt = x[0],x[1]
        val = 0.0
        for iix,ix in enumerate(self.idx_x):
            for iiy,iy in enumerate(self.idx_y):
                val += parameters[iix*(len(self.idx_y))+iiy]*scipy.special.eval_chebyt(ix, qt)*scipy.special.eval_chebyt(iy, y) 
        return val

def fit_coeff(fname="WJets.root", charge="WtoMuP", coeff="A0", qt_max = 24., y_max = 2.0):

    fin = ROOT.TFile.Open(output_dir+'/hadded/'+fname)
    hA  = ROOT.gDirectory.Get("GENINCLUSIVE_"+charge+"_nominal/GENINCLUSIVE_"+charge+"_"+coeff)
    hMC = ROOT.gDirectory.Get("GENINCLUSIVE_"+charge+"_nominal/GENINCLUSIVE_"+charge+"_MC")
    hA.Divide(hMC)

    qt_max_bin = hMC.GetYaxis().FindBin( qt_max )
    qt_max_cut = hMC.GetYaxis().GetBinCenter(qt_max_bin)        
    y_max_bin  = hMC.GetXaxis().FindBin( y_max )
    y_max_cut  = hMC.GetXaxis().GetBinCenter(y_max_bin)        
    
    x,y = [], []
    for i in range(1, y_max_bin+2): x.append( hMC.GetXaxis().GetBinLowEdge(i) )
    for i in range(1, qt_max_bin+2): y.append( hMC.GetYaxis().GetBinLowEdge(i) )
    xx = array('f', x)
    yy = array('f', y)
    
    hA_cut = ROOT.TH2F("hA_cut", "", len(xx)-1, xx, len(yy)-1, yy)
    
    for i in range(1, hA_cut.GetXaxis().GetNbins()+1):
        for j in range(1, hA_cut.GetYaxis().GetNbins()+1):
            hA_cut.SetBinContent(i,j, hA.GetBinContent(i,j) )
            hA_cut.SetBinError(i,j, hA.GetBinError(i,j) )
    
    #hA_cut.Draw("colz")

    idx_x = [1,2,4]
    idx_y = [0,2,4]
    func = fit_func(idx_x,idx_y)
    nparams = len(idx_x)*len(idx_y)

    fit = ROOT.TF2("fit"+coeff, func, 0.0, y_max_cut, 0.0, qt_max_cut, nparams)

    res = hA_cut.Fit(fit, "RSV")
    res.Print()
    
    hPulls2D = hA_cut.Clone("hPulls2D")
    hPulls2D.Reset()
    for iy in range(1, hPulls2D.GetXaxis().GetNbins()+1):
        for iq in range(1, hPulls2D.GetYaxis().GetNbins()+1):
            hPulls2D.SetBinContent( iy, iq, (fit.Eval( hPulls2D.GetXaxis().GetBinCenter(iy), hPulls2D.GetYaxis().GetBinCenter(iq) ) - hA_cut.GetBinContent(iy,iq))/hA_cut.GetBinError(iy,iq) )
    hPulls2D.SetMinimum(-3)
    hPulls2D.SetMaximum(+3)

    hPulls1D = ROOT.TH1F("hPulls1D", "", 100,-5,5)
    for iy in range(1, hPulls2D.GetXaxis().GetNbins()+1):
        for iq in range(1, hPulls2D.GetYaxis().GetNbins()+1):
            hPulls1D.Fill( hPulls2D.GetBinContent( iy, iq) )

    c = ROOT.TCanvas("c", "canvas", 1200, 600)
    c.Divide(2,1)

    c.cd(1)
    hPulls2D.SetStats(0)
    hPulls2D.Draw("colz")
    c.cd(2)
    hPulls1D.Fit("gaus", "", "", -3,3)
    gaus = hPulls1D.GetFunction("gaus")
    hPulls1D.Draw("HIST")
    gaus.Draw("same")

    c.Update()
    c.cd()
    c.Draw()
    raw_input()
    return

if __name__ == "__main__":
    fit_coeff()
