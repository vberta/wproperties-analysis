import ROOT
from array import array
import math
from termcolor import colored

ROOT.gROOT.SetBatch()

yArr = [0, 0.4, 0.8, 1.2 ,1.6, 2.0, 2.5, 3.0, 6.0]
ptArr = [0., 4., 8., 12., 16., 20., 24., 32., 40., 60., 100., 200.]

fFit = ROOT.TFile.Open("fit_testbkg.root")
res = fFit.fitresults

fmap = ROOT.TFile.Open("/scratchssd/emanca/wproperties-analysis/signalAnalysis/ACvalues.root")
imap = ROOT.TH2D
imap = fmap.Get("mapTot")

#factors = ['L', 'I', 'T', 'A', 'P', 'UL']
factors = {}
factors["a0"]= 2.
factors["a1"]=2.*math.sqrt(2)
factors["a2"]=4.
factors["a3"]=4.*math.sqrt(2)
factors["a4"]=2.
factors["unpolarizedxsec"]=1.

histos = []

for c in factors:


    h = ROOT.TH2D('h{c}'.format(c=c), 'h{c}'.format(c=c), len(yArr)-1, array('f',yArr), len(ptArr)-1, array('f',ptArr))
    h1 = ROOT.TH2D('hGen{c}'.format(c=c), 'hGen{c}'.format(c=c), len(yArr)-1, array('f',yArr), len(ptArr)-1, array('f',ptArr))
    hpt = ROOT.TH1D('hpt{c}'.format(c=c), 'hpt{c}'.format(c=c),len(ptArr)-1, array('f',ptArr))
    hy = ROOT.TH1D('hy{c}'.format(c=c), 'hy{c}'.format(c=c),len(yArr)-1, array('f',yArr))
    for ev in res: #dummy because there's one event only
        for i in range(1, h.GetNbinsX()+1): #loop over rapidity bins
            content = 0.
            norm = 0.
            err = 0.
            for j in range(1, h.GetNbinsY()+1): #loop over pt bins
                try:
                    coeff = eval('ev.y_{i}_pt_{j}_{c}'.format(c=c, j=j, i=i))
                    coeff_err = eval('ev.y_{i}_pt_{j}_{c}_err'.format(c=c, j=j, i=i))
                    h.SetBinContent(i,j,coeff)
                    h.SetBinError(i,j,coeff_err)
                    
                    h1.SetBinContent(i,j,eval('ev.y_{i}_pt_{j}_{c}_gen'.format(c=c, j=j, i=i)))
                    #out.append(eval('ev.{c}_pt{j}_y{i}_mu'.format(c=c, j=j, i=i)))
                    #err.append(eval('ev.{c}_pt{j}_y{i}_mu_err'.format(c=c, j=j, i=i)))
                    #gen.append(eval('ev.{c}_pt{j}_y{i}_mu_gen'.format(c=c, j=j, i=i)))
                    content = content + coeff*imap.GetBinContent(i,j)
                    norm = norm + imap.GetBinContent(i,j)
                    err = err + coeff_err*imap.GetBinContent(i,j)
                    hy.SetBinContent(i,content/norm)
                    hy.SetBinError(i,err/norm)
                except AttributeError: 
                    #print colored('bin of pt {} and y {}'.format(j,i), 'red')
                    h.SetBinContent(i,j,-9999.)
                    h.SetBinError(i,j,0.)
                    #h1.SetBinContent(i,j,0.)
                    
        for j in range(1, h.GetNbinsY()+1): #loop over pt bins
            content = 0.
            norm = 0.
            err = 0.
            for i in range(1, h.GetNbinsY()+1): #loop over rapidity bins
                try:
                    coeff = eval('ev.y_{i}_pt_{j}_{c}'.format(c=c, j=j, i=i))
                    coeff_err = eval('ev.y_{i}_pt_{j}_{c}_err'.format(c=c, j=j, i=i))
                    
                    content = content + coeff*imap.GetBinContent(i,j)
                    norm = norm + imap.GetBinContent(i,j)
                    err = err + coeff_err*imap.GetBinContent(i,j)
                    hpt.SetBinContent(j,content/norm)
                    hpt.SetBinError(j,err/norm)
                    #h1.SetBinContent(i,j,eval('ev.y_{i}_pt_{j}_{c}_gen'.format(c=c, j=j, i=i)))
                    #out.append(eval('ev.{c}_pt{j}_y{i}_mu'.format(c=c, j=j, i=i)))
                    #err.append(eval('ev.{c}_pt{j}_y{i}_mu_err'.format(c=c, j=j, i=i)))
                    #gen.append(eval('ev.{c}_pt{j}_y{i}_mu_gen'.format(c=c, j=j, i=i)))
                except AttributeError: 
                    #print colored('bin of pt {} and y {}'.format(j,i), 'red')
                    h.SetBinContent(i,j,-9999.)
                    h.SetBinError(i,j,0.)
    #for i in range (0, h.GetNbinsX()): #y
        #for j in range (0, h.GetNbinsY()): #pt

            #h.SetBinContent(i+1,j+1, out[i + j*h.GetNbinsX()])
            #h.SetBinError(i+1,j+1, err[i + j*h.GetNbinsX()])

            #h1.SetBinContent(i+1,j+1, gen[i + j*h.GetNbinsX()])

    histos.append(h)
    histos.append(h1)
    histos.append(hpt)
    histos.append(hy)


fO = ROOT.TFile("outSyst.root", "recreate")
fO.cd()
for h in histos:
    h.Write()
        
