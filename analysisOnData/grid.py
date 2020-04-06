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
import copy
from scipy import special
pp = pprint.PrettyPrinter(indent=2)

parser = argparse.ArgumentParser("")
parser.add_argument('-o', '--output_dir',type=str, default='TEST', help="")
args = parser.parse_args()
output_dir = args.output_dir

ROOT.Math.MinimizerOptions.SetDefaultMinimizer("Minuit2")

class fit_func:

    def __init__(self, idx_x, idx_y, constraints='qt->0,y-even'):
        self.idx_x = idx_x
        self.M = int(len(idx_x)-1)
        self.idx_y = idx_y
        self.N = int(len(idx_y)-1)
        self.nparams =  len(idx_x)*len(idx_y)
        self.limqt = 'qt->0' in constraints
        self.limy = 'y->0' in constraints
        self.yeven = 'y-even' in constraints

    def __call__(self, x, parameters):
        y,qt = x[0],x[1]
        val = 0.0
        p = [0.]*self.nparams                

        for iix,ix in enumerate(self.idx_x):
            for iiy,iy in enumerate(self.idx_y):
                idx = iix*(len(self.idx_y))+iiy
                p[idx] = parameters[idx]

        if self.limqt:
            p1 = copy.deepcopy(p)
            for iix,ix in enumerate(self.idx_x):
                if iix!=self.M: continue
                for iiy,iy in enumerate(self.idx_y):
                    idx = iix*(len(self.idx_y))+iiy
                    constr = 0.0
                    for k in range(0, self.M): 
                        constr += np.power(-1., self.M+k+1)*p[ k*(len(self.idx_y))+iiy]
                    p1[idx] = constr
            p = p1

        if self.limy:
            p1 = copy.deepcopy(p)
            for iiy,iy in enumerate(self.idx_y):
                if iiy!=self.N: continue
                for iix,ix in enumerate(self.idx_x):
                    idx = iix*(len(self.idx_y))+iiy
                    constr = 0.0
                    for k in range(0, self.N): 
                        constr += np.power(-1., self.N+k+1)*p[ ix*(len(self.idx_y))+k]
                    p1[idx] = constr
            p = p1

        #print qt,y
        for iix,ix in enumerate(self.idx_x):
            for iiy,iy in enumerate(self.idx_y):
                idx = iix*(len(self.idx_y))+iiy
                val += p[idx]*scipy.special.eval_chebyt(ix, qt)*scipy.special.eval_chebyt(iy, y) 
        return val

def fit_coeff(fname="WJets.root", charge="WtoMuP", coeff="A4", qt_max = 24., y_max = 2.5):

    fin   = ROOT.TFile.Open(output_dir+'/hadded/'+fname)
    hA    = ROOT.gDirectory.Get("GENINCLUSIVE_"+charge+"_nominal/GENINCLUSIVE_"+charge+"_"+coeff)
    hAErr = ROOT.gDirectory.Get("GENINCLUSIVE_"+charge+"_nominal/GENINCLUSIVE_"+charge+"_"+coeff+"Err")
    hMC   = ROOT.gDirectory.Get("GENINCLUSIVE_"+charge+"_nominal/GENINCLUSIVE_"+charge+"_MC")

    y_max_bin  = hMC.GetXaxis().FindBin( y_max )
    y_min_bin  = hMC.GetXaxis().FindBin( 0.0 )
    y_max_cut  = hMC.GetXaxis().GetBinLowEdge(y_max_bin+1)        
    y_min_cut  = 0.0   #hMC.GetXaxis().GetBinCenter(y_min_bin)        

    qt_max_bin = hMC.GetYaxis().FindBin( qt_max )
    qt_min_bin = hMC.GetYaxis().FindBin( 0.0 )
    qt_max_cut = hMC.GetYaxis().GetBinLowEdge(qt_max_bin+1)        
    qt_min_cut = 0.0    #hMC.GetYaxis().GetBinCenter(qt_min_bin)        
    
    print qt_max_bin,qt_min_bin,qt_max_cut,qt_min_cut
    print y_max_bin,y_min_bin,y_max_cut,y_min_cut

    x,y = [], []
    for i in range(y_min_bin, y_max_bin+1):   x.append( 2*(hMC.GetXaxis().GetBinCenter(i)- y_min_cut)/(y_max_cut-  y_min_cut) - 1.)
    for i in range(qt_min_bin, qt_max_bin+1): y.append( 2*(hMC.GetYaxis().GetBinCenter(i)-qt_min_cut)/(qt_max_cut-qt_min_cut) - 1.)
    xx = array('f', x)
    yy = array('f', y)
    print xx
    print yy
    #raw_input()
    
    hA_cut = ROOT.TH2F("hA_cut", "", len(xx)-1, xx, len(yy)-1, yy)
    for i in range(1, hA_cut.GetXaxis().GetNbins()+1):
        for j in range(1, hA_cut.GetYaxis().GetNbins()+1):
            mc_eff = hMC.GetBinContent(i,j)**2/hMC.GetBinError(i,j)**2
            A = hA.GetBinContent(i,j)/hMC.GetBinContent(i,j)
            A2 = hAErr.GetBinContent(i,j)/hMC.GetBinContent(i,j)
            A_err = math.sqrt(A2 - A**2)/math.sqrt(mc_eff)
            #print A, '+/-', A_err
            hA_cut.SetBinContent(i,j, A )
            hA_cut.SetBinError(i,j, A_err )
    
    #hA_cut.Draw("colz")

    idx_x = [0,1,2,3]
    idx_y = [0,1,2]

    constraint = 'y->0'
    #constraint = ''
    func = fit_func(idx_x,idx_y, constraint)
    nparams = len(idx_x)*len(idx_y)

    fit = ROOT.TF2("fit"+coeff, func, -1.0, 1.0, -1.0, 1.0, nparams)    
    
    for iix,ix in enumerate(idx_x):
        for iiy,iy in enumerate(idx_y):
            idx = iix*(len(idx_y))+iiy
            fit.SetParName(idx, "T"+str(iix)+"_"+"T"+str(iiy))
            fit.SetParError(idx, 0.002)

    if 'qt->0' in constraint:
        for iix,ix in enumerate(idx_x):
            if iix!=int(len(idx_x)-1): continue
            for iiy,iy in enumerate(idx_y):
                idx = iix*(len(idx_y))+iiy
                fit.SetParName(idx, "T"+str(iix)+"_"+"T"+str(iiy))
                fit.SetParError(idx, 0.002)
                print "qt->0: Fix parameter", idx
                fit.FixParameter(idx, 0.0)

    if 'y->0' in constraint:
        for iiy,iy in enumerate(idx_y):
            if iiy!=int(len(idx_y)-1): continue
            for iix,ix in enumerate(idx_x):
                idx = iix*(len(idx_y))+iiy
                fit.SetParName(idx, "T"+str(iix)+"_"+"T"+str(iiy))
                fit.SetParError(idx, 0.002)
                print "y->0: Fix parameter", idx
                fit.FixParameter(idx, 0.0)

    res = hA_cut.Fit(fit, "RSV")
    res.Print()

    fit.SetNpx(5000)
    for y in [-1.0, 0.0, +1.0]:
        print 'f(qt=0, y=', y, ')=', fit.Eval(y, -1.0 )
    for qt in [-1.0, 0.0, +1.0]:
        print 'f(qt=', qt, ', y=0)=', fit.Eval(-1.0, qt )
    
    hPulls2D = hA_cut.Clone("hPulls2D")
    hPulls2D.Reset()
    for iy in range(1, hPulls2D.GetXaxis().GetNbins()+1):
        for iq in range(1, hPulls2D.GetYaxis().GetNbins()+1):
            hPulls2D.SetBinContent( iy, iq, (fit.Eval( hPulls2D.GetXaxis().GetBinCenter(iy), hPulls2D.GetYaxis().GetBinCenter(iq) ) - hA_cut.GetBinContent(iy,iq))/hA_cut.GetBinError(iy,iq) )
    hPulls2D.SetMinimum(-4)
    hPulls2D.SetMaximum(+4)

    hPulls1D = ROOT.TH1F("hPulls1D", "", 100,-4,4)
    for iy in range(1, hPulls2D.GetXaxis().GetNbins()+1):
        for iq in range(1, hPulls2D.GetYaxis().GetNbins()+1):
            hPulls1D.Fill( hPulls2D.GetBinContent( iy, iq) )

    c = ROOT.TCanvas("c", "canvas", 1200, 600)
    c.Divide(2,1)

    c.cd(1)
    hPulls2D.SetStats(0)
    hPulls2D.Draw("colz")
    c.cd(2)
    #hPulls1D.Fit("gaus", "", "", -3,3)
    #gaus = hPulls1D.GetFunction("gaus")
    hPulls1D.Draw("HIST")
    #gaus.Draw("same")

    c.Update()
    c.cd()
    c.Draw()
    raw_input()
    return

if __name__ == "__main__":
    fit_coeff()
