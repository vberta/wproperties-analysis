import ROOT
from array import array
import math
from termcolor import colored
import copy
import argparse

ROOT.gROOT.SetBatch()

parser = argparse.ArgumentParser("")

parser.add_argument('-o','--output', type=str, default='fitResult',help="name of the output file")
parser.add_argument('-f','--fitFile', type=str, default='fit_Wplus.root',help="name of the fit result root file")
parser.add_argument('-i','--input', type=str, default='../analysisOnGen/genInputUncorr.root',help="name of the input root file")
parser.add_argument('-u','--uncorrelate', type=int, default=True,help="if true uncorrelate num and den of Angular Coeff in MC scale variation")

args = parser.parse_args()
OUTPUT = args.output
FITFILE = args.fitFile
INPUT = args.input
UNCORR = args.uncorrelate


yArr = [0, 0.4, 0.8, 1.2 ,1.6, 2.0, 2.4]
ptArr = [0., 4., 8., 12., 16., 20., 24., 28., 32.]

fFit = ROOT.TFile.Open(FITFILE)
res = fFit.fitresults

inFile = ROOT.TFile.Open(INPUT)

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
    hGen[coeff] =  inFile.Get('angularCoefficients/harmonics'+coeff+'_nom_nom')

for sKind, sList in systDict.iteritems():

    sListMod = copy.deepcopy(sList)
    if sKind=='_LHEScaleWeight' and UNCORR :
        sListMod.append("_nom") #add nominal variation
    
    for sName in sListMod :
        hGen[sName+'mapTot'] =  inFile.Get('angularCoefficients'+sKind+'/mapTot'+sName)
        for sNameDen in sListMod :
            if sNameDen!=sName and not (sKind=='_LHEScaleWeight' and UNCORR) : #PDF or correlated Scale
                continue 
            if sName=='_nom' and sNameDen=='_nom' : 
                continue
            for coeff,div in coeffDict.iteritems() :
                if "unpolarizedxsec" in coeff: continue
                if UNCORR :
                    if sKind=='_LHEScaleWeight':
                        hGen[sName+sNameDen+coeff] =  inFile.Get('angularCoefficients'+sKind+'/harmonics'+coeff+sName+sNameDen)
                    else :
                        hGen[sName+coeff] =  inFile.Get('angularCoefficients'+sKind+'/harmonics'+coeff+sName+sNameDen)
                else :
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
                    coeff = eval('ev.helXsecs{}_y_{}_qt_{}_pmaskedexp'.format(hel, i, j))
                    coeff_err = eval('ev.helXsecs{}_y_{}_qt_{}_pmaskedexp_err'.format(hel, i, j))
                    h.SetBinContent(i,j,coeff)
                    h.SetBinError(i,j,coeff_err)

                    coeffnorm = eval('ev.helXsecs{}_y_{}_qt_{}_pmaskedexpnorm'.format(hel, i, j))
                    coeffnorm_err = eval('ev.helXsecs{}_y_{}_qt_{}_pmaskedexpnorm_err'.format(hel, i, j))
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
                    coeff = eval('ev.y_{i}_qt_{j}_{c}'.format(c=c, j=j, i=i))
                    coeff_err = eval('ev.y_{i}_qt_{j}_{c}_err'.format(c=c, j=j, i=i))
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
            
            for sName in systDict['_LHEPdfWeight']:
                # content = 1.
                if 'unpol' in c:
                    #print content, coeff, "before"
                    content=hGen[sName+'mapTot'].GetBinContent(i,j)/35.9
                    # print cval, content
                else:
                    content = hGen[sName+c].GetBinContent(i,j)
                err+= (cval - content)**2
                       
            sListMod = copy.deepcopy(systDict['_LHEScaleWeight'])
            if UNCORR :
                sListMod.append("_nom") #add nominal variation
            errScale = 0.
            for sName in sListMod:
                for sNameDen in sListMod :
                    if sNameDen!=sName and not UNCORR : continue
                    if sNameDen!=sName and 'unpol' in c : continue
                    if sName=='_nom' and sNameDen=='_nom' : continue
                    if 'unpol' in c:
                        content=hGen[sName+'mapTot'].GetBinContent(i,j)/35.9
                    else:
                        if UNCORR :
                            content = hGen[sName+sNameDen+c].GetBinContent(i,j)
                        else : 
                            content = hGen[sName+c].GetBinContent(i,j)
                    err_temp= (cval - content)**2
                    if err_temp>errScale : 
                        errScale = err_temp
            err+=errScale
        
            central.SetBinError(i,j,math.sqrt(err))
  
    histos[c].append(h)
    if 'unpol' in c:
        central.Scale(1./35.9)
    histos[c].append(central)

#--------------- projections canvas -------------------#
canv = {}
for coeff in coeffDict:
    canv[coeff] = []

for c in coeffDict:
    h = ROOT.TH2D('htemp{c}'.format(c=c), 'htemp{c}'.format(c=c), len(yArr)-1, array('f',yArr), len(ptArr)-1, array('f',ptArr))
    for i in range(1, h.GetNbinsX()+1): #loop over rapidity bins
        c1 = ROOT.TCanvas("projPt{}_{}".format(i,c),"projPt{}_{}".format(i,c))
        c1.SetGridx()
        c1.SetGridy()
        pr = histos[c][0].ProjectionY("projPt{}_{}".format(i,c),i,i)
        pg = histos[c][1].ProjectionY("projgPt{}_{}".format(i,c),i,i)
        pr.SetTitle(c+" vs W transverse momentum, "+str(yArr[i-1])+"<Y_{W}<"+str(yArr[i]))
        c1.cd()
        pr.GetXaxis().SetTitle('q_{T}^{W} [GeV]')
        pr.GetYaxis().SetTitle(c)
        pr.SetLineWidth(2)
        pr.SetStats(0)
        pr.Draw()
        pg.SetFillColor(ROOT.kGreen-7)
        pg.SetFillStyle(3001)
        pg.SetLineColor(ROOT.kGreen-7)
        pg.SetLineWidth(2)
        pg.DrawCopy("E2 same")
        pg.SetFillStyle(0)
        pg.Draw("E2 same")
        pr.DrawCopy("same") #to have foreground
        canv[c].append(copy.deepcopy(c1))
    for j in range(1, h.GetNbinsY()+1): #loop over pt bins
        c1 = ROOT.TCanvas("projY{}_{}".format(j,c),"projY{}_{}".format(j,c))
        c1.SetGridx()
        c1.SetGridy()
        pr = histos[c][0].ProjectionX("projY{}_{}".format(j,c),j,j)
        pg = histos[c][1].ProjectionX("projgY{}_{}".format(j,c),j,j)
        pr.SetTitle(c+" vs W rapidity, "+str(ptArr[j-1])+"<q_{T}^{W}<"+str(ptArr[j]))
        c1.cd()
        pr.GetXaxis().SetTitle('Y_{W}')
        pr.GetYaxis().SetTitle(c)
        pr.SetLineWidth(2)
        pr.SetStats(0)
        pr.Draw()
        pg.SetFillColor(ROOT.kMagenta-7)
        pg.SetFillStyle(3001)
        pg.SetLineColor(ROOT.kMagenta-7)
        pg.SetLineWidth(2)
        pg.DrawCopy("E2 same")
        pg.SetFillStyle(0)
        pg.Draw("E2 same")
        pr.DrawCopy("same") #to have foreground
        canv[c].append(copy.deepcopy(c1))
    
    
    
    
    #-------------- unrolled: qt large, y small -----------------
    unrolledQtY= list(yArr)
    intervalYBin = []
    for y in yArr[:-1] :
        intervalYBin.append(yArr[yArr.index(y)+1]-yArr[yArr.index(y)])
    for q in range(len(ptArr)-2) :
        for y in intervalYBin :
            unrolledQtY.append(unrolledQtY[-1]+y)
    
    coeff_UNRqty = ROOT.TH1F('coeff_UNRqty'+c,'coeff_UNRQtY'+c,len(unrolledQtY)-1, array('f',unrolledQtY))
    coeff_UNRqty_syst = ROOT.TH1F('coeff_UNRqty_syst'+c,'coeff_UNRQtY_syst'+c,len(unrolledQtY)-1, array('f',unrolledQtY))
    for q in ptArr[:-1] :
        for y in yArr[:-1] :
            indexUNRqty = ptArr.index(float(q))*(len(yArr)-1)+yArr.index(float(y))
            coeff_UNRqty.SetBinContent(indexUNRqty+1,histos[c][0].GetBinContent(yArr.index(y)+1,ptArr.index(q)+1))
            coeff_UNRqty.SetBinError(indexUNRqty+1,histos[c][0].GetBinError(yArr.index(y)+1,ptArr.index(q)+1))
            coeff_UNRqty_syst.SetBinContent(indexUNRqty+1,histos[c][1].GetBinContent(yArr.index(y)+1,ptArr.index(q)+1))
            coeff_UNRqty_syst.SetBinError(indexUNRqty+1,histos[c][1].GetBinError(yArr.index(y)+1,ptArr.index(q)+1))
            # if yArr.index(y)==len(yArr)-2 :
                # coeff_UNRqty.GetXaxis().SetBinLabel(indexUNRqty+1,"q_{T}="+str(q)+", Y="+str(y))
            if yArr.index(y)==0 :
                coeff_UNRqty.GetXaxis().SetBinLabel(indexUNRqty+1,"q_{T}^{W}#in[%.0f,%.0f]" % (q, ptArr[ptArr.index(q)+1]))
                coeff_UNRqty.GetXaxis().ChangeLabel(indexUNRqty+1,340,0.03)
            # else :
            #     coeff_UNRqty.GetXaxis().SetBinLabel(indexUNRqty+1,str(y))
            
    coeff_UNRqty.SetTitle(c+", unrolled q_{T}(Y) ")
    # coeff_UNRqty.GetXaxis().SetTitle('q_{T}^{W} large, Y_{W} small')
    coeff_UNRqty.GetXaxis().SetTitle('fine binning: Y_{W} 0#rightarrow 2.4')
    coeff_UNRqty.GetXaxis().SetTitleOffset(1.45)
    coeff_UNRqty.GetYaxis().SetTitle(c)
    coeff_UNRqty.SetLineWidth(2)
    coeff_UNRqty.SetStats(0)
    coeff_UNRqty_syst.SetFillColor(ROOT.kGreen-7)
    coeff_UNRqty_syst.SetFillStyle(3001)
    coeff_UNRqty_syst.SetLineColor(ROOT.kGreen-7)
    coeff_UNRqty_syst.SetLineWidth(2)
    
    c_UNRqty = ROOT.TCanvas('c_UNRqty'+c,'c_UNRqty'+c,800,600)
    c_UNRqty.cd()
    c_UNRqty.SetGridx()
    c_UNRqty.SetGridy()
    coeff_UNRqty.Draw()
    coeff_UNRqty_syst.DrawCopy('E2 same')
    coeff_UNRqty_syst.SetFillStyle(0)
    coeff_UNRqty_syst.Draw("E2 same")
    coeff_UNRqty.DrawCopy("same") #to have foreground
    canv[c].append(copy.deepcopy(c_UNRqty))
            

    #------------- unrolled: y large, qt small -----------------
    unrolledYQt= list(ptArr)
    intervalQtBin = []
    for q in ptArr[:-1] :
        intervalQtBin.append(ptArr[ptArr.index(q)+1]-ptArr[ptArr.index(q)])
    for y in range(len(yArr)-2) :
        for q in intervalQtBin :
            unrolledYQt.append(unrolledYQt[-1]+q)
            
    coeff_UNRyqt = ROOT.TH1F('coeff_UNRyqt'+c,'coeff_UNRyqt'+c,len(unrolledYQt)-1, array('f',unrolledYQt))
    coeff_UNRyqt_syst = ROOT.TH1F('coeff_UNRyqt_syst'+c,'coeff_UNRyqt_syst'+c,len(unrolledYQt)-1, array('f',unrolledYQt))
    for y in yArr[:-1] :
        for q in ptArr[:-1] :
            indexUNRyqt = yArr.index(float(y))*(len(ptArr)-1)+ptArr.index(float(q))
            coeff_UNRyqt.SetBinContent(indexUNRyqt+1,histos[c][0].GetBinContent(yArr.index(y)+1,ptArr.index(q)+1))
            coeff_UNRyqt.SetBinError(indexUNRyqt+1,histos[c][0].GetBinError(yArr.index(y)+1,ptArr.index(q)+1))
            coeff_UNRyqt_syst.SetBinContent(indexUNRyqt+1,histos[c][1].GetBinContent(yArr.index(y)+1,ptArr.index(q)+1))
            coeff_UNRyqt_syst.SetBinError(indexUNRyqt+1,histos[c][1].GetBinError(yArr.index(y)+1,ptArr.index(q)+1))
            if ptArr.index(q)==0 :
                # coeff_UNRyqt.GetXaxis().SetBinLabel(indexUNRyqt+1,"Y_{W}=%.1f" % y)
                coeff_UNRyqt.GetXaxis().SetBinLabel(indexUNRyqt+1,"Y_{W}#in[%.1f,%.1f]" % (y, yArr[yArr.index(y)+1]))
                # coeff_UNRyqt.GetXaxis().ChangeLabel(indexUNRyqt+1,340,0.03)
    coeff_UNRyqt.SetTitle(c+", unrolled Y(q_{T}) ")
    # coeff_UNRyqt.GetXaxis().SetTitle('Y_{W} large, q_{T}^{W}small')
    coeff_UNRyqt.GetXaxis().SetTitle('fine binning: q_{T}^{W} 0#rightarrow 32 GeV')
    coeff_UNRyqt.GetXaxis().SetTitleOffset(1.45)
    coeff_UNRyqt.GetYaxis().SetTitle(c)
    coeff_UNRyqt.SetLineWidth(2)
    coeff_UNRyqt.SetStats(0)
    coeff_UNRyqt_syst.SetFillColor(ROOT.kMagenta-7)
    coeff_UNRyqt_syst.SetFillStyle(3001)
    coeff_UNRyqt_syst.SetLineColor(ROOT.kMagenta-7)
    coeff_UNRyqt_syst.SetLineWidth(2)
    
    c_UNRyqt = ROOT.TCanvas('c_UNRyqt'+c,'c_UNRyqt'+c,800,600)
    c_UNRyqt.cd()
    c_UNRyqt.SetGridx()
    c_UNRyqt.SetGridy()
    coeff_UNRyqt.Draw()
    coeff_UNRyqt_syst.DrawCopy('E2 same')
    coeff_UNRyqt_syst.SetFillStyle(0)
    coeff_UNRyqt_syst.Draw("E2 same")
    coeff_UNRyqt.DrawCopy("same") #to have foreground
    canv[c].append(copy.deepcopy(c_UNRyqt))
    




# ------------------------- save histos ----------------------------- #
outFile = ROOT.TFile(OUTPUT+".root", "recreate")
outFile.cd()
dirFinalDict = {}

dirFinalDict['coeff2D'] = outFile.mkdir('coeff2D')
dirFinalDict['coeff2D'].cd()
for c,hlist in histos.iteritems():
    for h in hlist:
        h.GetXaxis().SetTitle('W rapidity')
        h.GetYaxis().SetTitle('W q_{T}')
        h.Write()
        
dirFinalDict['coeff'] = outFile.mkdir('coeff')
dirFinalDict['coeff'].cd()

for c,hlist in canv.iteritems():
    for h in hlist:
        if 'UNR' in h.GetName() : continue
        h.Write()

dirFinalDict['coeff_unrolled'] = outFile.mkdir('coeff_unrolled')
dirFinalDict['coeff_unrolled'].cd()

for c,hlist in canv.iteritems():
    for h in hlist:
        if not 'UNR' in h.GetName() : continue
        h.Write()
    
    
        
