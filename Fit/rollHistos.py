import ROOT
from array import array
import math
from termcolor import colored

ROOT.gROOT.SetBatch()

yArr = [0, 0.4, 0.8, 1.2 ,1.6, 2.0, 2.5, 3.0, 6.0]
ptArr = [0., 4., 8., 12., 16., 20., 24., 32., 40., 60., 100., 200.]

fFit = ROOT.TFile.Open("testfit.root")
res = fFit.fitresults

#factors = ['L', 'I', 'T', 'A', 'P', 'UL']
factors = ['a0', 'a1','a2','a3', 'a4', 'unpolarizedxsec']

histos = []

for c in factors:

    h = ROOT.TH2D('h{c}'.format(c=c), 'h{c}'.format(c=c), len(yArr)-1, array('f',yArr), len(ptArr)-1, array('f',ptArr))
    h1 = ROOT.TH2D('hGen{c}'.format(c=c), 'hGen{c}'.format(c=c), len(yArr)-1, array('f',yArr), len(ptArr)-1, array('f',ptArr))
    out = []
    gen = []
    err = []
    for ev in res:
        for i in range(1, h.GetNbinsX()+1):
            for j in range(1, h.GetNbinsY()+1):
                try:
                    h.SetBinContent(i,j,eval('ev.y_{i}_pt_{j}_{c}'.format(c=c, j=j, i=i)))
                    h.SetBinError(i,j,eval('ev.y_{i}_pt_{j}_{c}_err'.format(c=c, j=j, i=i)))
                    h1.SetBinContent(i,j,eval('ev.y_{i}_pt_{j}_{c}_gen'.format(c=c, j=j, i=i)))
                    #out.append(eval('ev.{c}_pt{j}_y{i}_mu'.format(c=c, j=j, i=i)))
                    #err.append(eval('ev.{c}_pt{j}_y{i}_mu_err'.format(c=c, j=j, i=i)))
                    #gen.append(eval('ev.{c}_pt{j}_y{i}_mu_gen'.format(c=c, j=j, i=i)))
                except AttributeError: 
                    print colored('bin of pt {} and y {}'.format(j,i), 'red')
                    h.SetBinContent(i,j,-99.)
                    h.SetBinError(i,j,0.)
                    h1.SetBinContent(i,j,0.)

    #for i in range (0, h.GetNbinsX()): #y
        #for j in range (0, h.GetNbinsY()): #pt

            #h.SetBinContent(i+1,j+1, out[i + j*h.GetNbinsX()])
            #h.SetBinError(i+1,j+1, err[i + j*h.GetNbinsX()])

            #h1.SetBinContent(i+1,j+1, gen[i + j*h.GetNbinsX()])

    histos.append(h)
    histos.append(h1)

fO = ROOT.TFile("out.root", "recreate")
fO.cd()
for h in histos:
    h.Write()
        
