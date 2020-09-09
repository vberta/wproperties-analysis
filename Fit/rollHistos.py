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

inFile = ROOT.TFile.Open("/scratch/emanca/wproperties-analysis/analysisOnGen/genInput.root")

coeffDict = {
    'A0' : 1.,
    'A1' : 5.,
    'A2' : 20.,
    'A3' : 4.,
    'A4' : 4.,
    'unpolarizedxsec' : 1.
}

histos = {}
for coeff in coeffDict:
    histos[coeff] = []

systDict = {
    "_LHEScaleWeight" : ["_LHEScaleWeight_muR0p5_muF0p5", "_LHEScaleWeight_muR0p5_muF1p0","_LHEScaleWeight_muR1p0_muF0p5","_LHEScaleWeight_muR1p0_muF2p0","_LHEScaleWeight_muR2p0_muF1p0", "_LHEScaleWeight_muR2p0_muF2p0"],
    "_LHEPdfWeight" : ["_LHEPdfWeightHess" + str(i)  for i in range(1, 61)],
}

hGen = {}
hGen['mapTot'] =  inFile.Get('angularCoefficients/mapTot')
for coeff,div in coeffDict.iteritems() :
    hGen[coeff] =  inFile.Get('angularCoefficients/harmonics'+coeff)
for sKind, sList in systDict.iteritems():
    for sName in sList :
        hGen[sName+'mapTot'] =  inFile.Get('angularCoefficients'+sKind+'/mapTot'+sName)
        for coeff,div in coeffDict.iteritems() :
            if "unpolarizedxsec" in coeff: continue
            hGen[sName+coeff] =  inFile.Get('angularCoefficients'+sKind+'/harmonics'+coeff+sName)

hels = ['L', 'I', 'T', 'A', 'P', 'UL']

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

#plot angular coefficients with bands 
for c in coeffDict:
    h = ROOT.TH2D('h{c}'.format(c=c), 'h{c}'.format(c=c), len(yArr)-1, array('f',yArr), len(ptArr)-1, array('f',ptArr))
    for ev in res: #dummy because there's one event only
        for i in range(1, h.GetNbinsX()+1): #loop over rapidity bins
            for j in range(1, h.GetNbinsY()+1): #loop over pt bins
                try:
                    coeff = eval('ev.y_{i}_pt_{j}_{c}'.format(c=c, j=j, i=i))
                    coeff_err = eval('ev.y_{i}_pt_{j}_{c}_err'.format(c=c, j=j, i=i))
                    if 'unpol' in c:
                        coeff = coeff/(3./16./math.pi)
                        coeff_err = coeff_err/(3./16./math.pi)
                    h.SetBinContent(i,j,coeff)
                    h.SetBinError(i,j,coeff_err)
                    
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
    
    central = ROOT.TH2D()
    if not "unpol" in c:
        central = hGen[c]
    else:
        central = hGen['mapTot']

    for i in range(1, h.GetNbinsX()+1): #loop over rapidity bins
        for j in range(1, h.GetNbinsY()+1): #loop over pt bins
            err = 0.
            cval = central.GetBinContent(i,j)
            if 'unpol' in c:
                cval=cval/35.9
                #print cval,h.GetBinContent(i,j), i, j
            
            for sKind, sList in systDict.iteritems():
                for sName in sList:
                    content = 1.
                    if 'unpol' in c:
                        #print content, coeff, "before"
                        content=hGen[sName+'mapTot'].GetBinContent(i,j)/35.9
                        print cval, content
                    else:
                        content = hGen[sName+c].GetBinContent(i,j)
                    err+= (cval - content)**2
                    
            central.SetBinError(i,j,math.sqrt(err))
    
    histos[c].append(h)
    if 'unpol' in c:
        central.Scale(1./35.9)
    histos[c].append(central)

#projections
canv = {}
for coeff in coeffDict:
    canv[coeff] = []

for c in coeffDict:
    h = ROOT.TH2D('h{c}'.format(c=c), 'h{c}'.format(c=c), len(yArr)-1, array('f',yArr), len(ptArr)-1, array('f',ptArr))
    for i in range(1, h.GetNbinsX()+1): #loop over rapidity bins
        c1 = ROOT.TCanvas("projPt{}_{}".format(i,c),"")
        pr = histos[c][0].ProjectionY("projPt{}_{}".format(i,c),i,i)
        pg = histos[c][1].ProjectionY("projgPt{}_{}".format(i,c),i,i)

        c1.cd()
        pr.GetXaxis().SetTitle('W rapidity')
        pr.GetYaxis().SetTitle('W p_{T}')
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
        pr.GetXaxis().SetTitle('W rapidity')
        pr.GetYaxis().SetTitle('W p_{T}')
        pr.Draw()
        pg.SetFillColor(ROOT.kMagenta)
        pg.SetFillStyle(3001)
        pg.Draw("E2 same")
        canv[c].append(copy.deepcopy(c1))

fO = ROOT.TFile("outSyst2Coeff.root", "recreate")
fO.cd()

for c,hlist in histos.iteritems():
    for h in hlist:
        h.GetXaxis().SetTitle('W rapidity')
        h.GetYaxis().SetTitle('W p_T')
        h.Write()

for c,hlist in canv.iteritems():
    for h in hlist:
        h.Write()
    
    
        
