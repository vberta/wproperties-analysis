import ROOT
from array import array
import math
from termcolor import colored
import copy

ROOT.gROOT.SetBatch()

yArr = [0, 0.4, 0.8, 1.2 ,1.6, 2.0, 2.4]
ptArr = [0., 4., 8., 12., 16., 20., 24., 28., 32.]

fFit = ROOT.TFile.Open("fit_testbkg.root")
res = fFit.fitresults

fmap = ROOT.TFile.Open("/scratch/emanca/wproperties-analysis/analysisOnGen/genInput.root")
imap = ROOT.TH2D
imap = fmap.Get("accMaps/mapTot")
cov = ROOT.TH2D
cov = fFit.Get('covariance_matrix_channelhelpois')

hgen = {}
hgen['a0'] = []
hgen['a1'] = []
hgen['a2'] = []
hgen['a3'] = []
hgen['a4'] = []
hgen['unpolarizedxsec'] = []

for i in range(60):
    hgen['a0'].append(fmap.Get("angularCoefficients_LHEPdfWeight/harmonicsA0_LHEPdfWeightHess{}".format(i+1)))
    hgen['a1'].append(fmap.Get("angularCoefficients_LHEPdfWeight/harmonicsA1_LHEPdfWeightHess{}".format(i+1)))
    hgen['a2'].append(fmap.Get("angularCoefficients_LHEPdfWeight/harmonicsA2_LHEPdfWeightHess{}".format(i+1)))
    hgen['a3'].append(fmap.Get("angularCoefficients_LHEPdfWeight/harmonicsA3_LHEPdfWeightHess{}".format(i+1)))
    hgen['a4'].append(fmap.Get("angularCoefficients_LHEPdfWeight/harmonicsA4_LHEPdfWeightHess{}".format(i+1)))
    hgen['unpolarizedxsec'].append(fmap.Get("angularCoefficients_LHEPdfWeight/harmonicsAUL_LHEPdfWeightHess{}".format(i+1)))


#factors = ['L', 'I', 'T', 'A', 'P', 'UL']
factors = {}
factors["a0"]= 2.
factors["a1"]=2.*math.sqrt(2)
factors["a2"]=4.
factors["a3"]=4.*math.sqrt(2)
factors["a4"]=2.
factors["unpolarizedxsec"]=1.

histos = {}
histos['a0'] = []
histos['a1'] = []
histos['a2'] = []
histos['a3'] = []
histos['a4'] = []
histos['unpolarizedxsec'] = []

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
                    
                    pdferr = 0.
                    h1.SetBinContent(i,j,eval('ev.y_{i}_pt_{j}_{c}_gen'.format(c=c, j=j, i=i)))
                    for pdf in hgen[c]:
                        pdferr+= (coeff - pdf.GetBinContent(i,j))**2
                    h1.SetBinError(i,j,math.sqrt(pdferr))
                    
                except AttributeError: 
                    pass
                    
        for j in range(1, h.GetNbinsY()+1): #loop over pt bins
            try:
                coeff = eval('ev.pt_{j}_helmeta_{c}'.format(c=c, j=j))
                coeff_err = eval('ev.pt_{j}_helmeta_{c}_err'.format(c=c, j=j))
                
                hpt.SetBinContent(j,coeff)
                hpt.SetBinError(j,coeff_err)


            except AttributeError: 
                pass
        for i in range(1, h.GetNbinsY()+1): #loop over rapidity bins
            try:
                coeff = eval('ev.y_{i}_helmeta_{c}'.format(c=c, i=i))
                coeff_err = eval('ev.y_{i}_helmeta_{c}_err'.format(c=c, i=i))
                
                hy.SetBinContent(i,coeff)
                hy.SetBinError(i,coeff_err)

            except AttributeError: 
                pass

    histos[c].append(h)
    histos[c].append(h1)
    histos[c].append(hpt)
    histos[c].append(hy)

#projections
canv = {}
canv['a0'] = []
canv['a1'] = []
canv['a2'] = []
canv['a3'] = []
canv['a4'] = []
canv['unpolarizedxsec'] = []

for c in factors:
    h = ROOT.TH2D('h{c}'.format(c=c), 'h{c}'.format(c=c), len(yArr)-1, array('f',yArr), len(ptArr)-1, array('f',ptArr))
    for i in range(1, h.GetNbinsX()+1): #loop over rapidity bins
        c1 = ROOT.TCanvas("projPt{}_{}".format(i,c),"")
        pr = histos[c][0].ProjectionY("projPt{}_{}".format(i,c),i,i)
        pg = histos[c][1].ProjectionY("projgPt{}_{}".format(i,c),i,i)
        c1.cd()
        pr.Draw()
        pg.SetFillColor(ROOT.kGreen)
        pg.SetFillStyle(3001)
        pg.Draw("E2 same")
        canv[c].append(copy.deepcopy(c1))
    for j in range(1, h.GetNbinsY()+1): #loop over pt bins
        c1 = ROOT.TCanvas("projY{}_{}".format(j,c),"")
        pr = histos[c][0].ProjectionX("projY{}_{}".format(j,c),j,j)
        pg = histos[c][1].ProjectionX("projgY{}_{}".format(j,c),j,j)
        c1.cd()
        pr.Draw()
        pg.SetFillColor(ROOT.kMagenta)
        pg.SetFillStyle(3001)
        pg.Draw("E2 same")
        canv[c].append(copy.deepcopy(c1))

fO = ROOT.TFile("outSyst2Coeff.root", "recreate")
fO.cd()

for c,hlist in histos.iteritems():
    for h in hlist:
        h.Write()

for c,hlist in canv.iteritems():
    for h in hlist:
        h.Write()
    
    
        
