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
hgen['A0'] = {}
hgen['A1'] = {}
hgen['A2'] = {}
hgen['A3'] = {}
hgen['A4'] = {}
hgen['unpolarizedxsec'] = {}

systDict = {
    "_LHEScaleWeight" : ["_LHEScaleWeight_muR0p5_muF0p5", "_LHEScaleWeight_muR0p5_muF1p0","_LHEScaleWeight_muR1p0_muF0p5","_LHEScaleWeight_muR1p0_muF2p0","_LHEScaleWeight_muR2p0_muF1p0", "_LHEScaleWeight_muR2p0_muF2p0"],
    "_LHEPdfWeight" : ["_LHEPdfWeightHess" + str(i)  for i in range(1, 61)]
}
for coeff in hgen:
    for syst,var in systDict.iteritems():
        hgen[coeff][syst]=[]
        for v in var:
            if not 'unpol' in coeff:
                hgen[coeff][syst].append(fmap.Get("angularCoefficients_{}/harmonics{}_{}".format(syst,coeff,v)))
            else:
                hgen[coeff][syst].append(fmap.Get("angularCoefficients_{}/mapTot_{}".format(syst,v)))

hels = ['L', 'I', 'T', 'A', 'P', 'UL']
factors = {}
factors["A0"]= 2.
factors["A1"]=2.*math.sqrt(2)
factors["A2"]=4.
factors["A3"]=4.*math.sqrt(2)
factors["A4"]=2.
factors["unpolarizedxsec"]=1.

histos = {}
histos['A0'] = []
histos['A1'] = []
histos['A2'] = []
histos['A3'] = []
histos['A4'] = []
histos['unpolarizedxsec'] = []

#plot the helicity xsecs
for hel in hels:
    h = ROOT.TH2D('h{c}'.format(c=hel), 'h{c}'.format(c=hel), len(yArr)-1, array('f',yArr), len(ptArr)-1, array('f',ptArr))
    hnorm = ROOT.TH2D('hnorm{c}'.format(c=hel), 'hnorm{c}'.format(c=hel), len(yArr)-1, array('f',yArr), len(ptArr)-1, array('f',ptArr))
    histos[hel]=[]
    for ev in res: #dummy because there's one event only
        for i in range(1, h.GetNbinsX()+1): #loop over rapidity bins
            for j in range(1, h.GetNbinsY()+1): #loop over pt bins
                try:
                    coeff = eval('ev.helXsecs_{}_y_{}_pt_{}_pmaskedexp'.format(hel, i, j))
                    coeff_err = eval('ev.helXsecs_{}_y_{}_pt_{}_pmaskedexp_err'.format(hel, i, j))
                    h.SetBinContent(i,j,coeff)
                    h.SetBinError(i,j,coeff_err)

                    coeffnorm = eval('ev.helXsecs_{}_y_{}_pt_{}_pmaskedexpnorm'.format(hel, i, j))
                    coeffnorm_err = eval('ev.helXsecs_{}_y_{}_pt_{}_pmaskedexpnorm_err'.format(hel, i, j))
                    hnorm.SetBinContent(i,j,coeffnorm)
                    hnorm.SetBinError(i,j,coeffnorm_err)

                except AttributeError:
                    pass

    histos[hel].append(h)
    histos[hel].append(hnorm)

for c in factors:

    h = ROOT.TH2D('h{c}'.format(c=c), 'h{c}'.format(c=c), len(yArr)-1, array('f',yArr), len(ptArr)-1, array('f',ptArr))
    h1 = ROOT.TH2D('hGen{c}'.format(c=c), 'hGen{c}'.format(c=c), len(yArr)-1, array('f',yArr), len(ptArr)-1, array('f',ptArr))
    hpt = ROOT.TH1D('hpt{c}'.format(c=c), 'hpt{c}'.format(c=c),len(ptArr)-1, array('f',ptArr))
    hy = ROOT.TH1D('hy{c}'.format(c=c), 'hy{c}'.format(c=c),len(yArr)-1, array('f',yArr))
    for ev in res: #dummy because there's one event only
        for i in range(1, h.GetNbinsX()+1): #loop over rapidity bins
            for j in range(1, h.GetNbinsY()+1): #loop over pt bins
                try:
                    coeff = eval('ev.y_{i}_pt_{j}_{c}'.format(c=c, j=j, i=i))
                    coeff_err = eval('ev.y_{i}_pt_{j}_{c}_err'.format(c=c, j=j, i=i))
                    h.SetBinContent(i,j,coeff)
                    h.SetBinError(i,j,coeff_err)
                    
                    pdferr = 0.
                    h1.SetBinContent(i,j,coeff)
                    for pdf in hgen[c]:
                        content = pdf.GetBinContent(i,j)
                        if 'unpol' in c:
                            print content, coeff, "before"
                            content=content/10./35.9
                            print content, coeff, "after"
                        pdferr+= (h1.GetBinContent(i,j) - content)**2
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
    
    
        
