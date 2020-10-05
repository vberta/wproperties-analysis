import ROOT
from array import array
import math
from termcolor import colored
import copy
import argparse

ROOT.gROOT.SetBatch()
ROOT.TH1.AddDirectory(False)
ROOT.TH2.AddDirectory(False)


class plotter :
    
    def __init__(self):
            
        self.yArr = [0, 0.4, 0.8, 1.2 ,1.6, 2.0, 2.4]
        self.qtArr = [0., 4., 8., 12., 16., 20., 24., 28., 32.]
        
        self.systDict = {
            "_LHEScaleWeight" : ["_LHEScaleWeight_muR0p5_muF0p5", "_LHEScaleWeight_muR0p5_muF1p0","_LHEScaleWeight_muR1p0_muF0p5","_LHEScaleWeight_muR1p0_muF2p0","_LHEScaleWeight_muR2p0_muF1p0", "_LHEScaleWeight_muR2p0_muF2p0"],
            "_LHEPdfWeight" : ["_LHEPdfWeightHess" + str(i)  for i in range(1, 61)],
        }
        
        self.hels = ['L', 'I', 'T', 'A', 'P', 'UL']
        self.coeffDict = {
            'A0' : 1.,
            'A1' : 5.,
            'A2' : 20.,
            'A3' : 4.,
            'A4' : 4.,
            'unpolarizedxsec' : 1
        }
        
        self.histos = {}
        self.canvas = {}
        self.leg = {}
        
        self.groupedSystColors = {
            # "WHSFVars"  : [ROOT.kGreen+1, 'Scale Factors'],
            "LHEScaleWeightVars" : [ROOT.kViolet-2, 'MC Scale'],
            # "ptScaleVars" : [ROOT.kBlue-4, 'pT Scale'],
            # "jmeVars" : [ROOT.kAzure+10, 'MET'],
            "LHEPdfWeightVars" : [ROOT.kRed+1, 'PDF'],
            "Nominal" : [1, 'Fit Unc.']
        }
        
        
        #unrolled binning: qt large, y fine
        self.unrolledQtY= list(self.yArr)
        intervalYBin = []
        for y in self.yArr[:-1] :
            intervalYBin.append(self.yArr[self.yArr.index(y)+1]-self.yArr[self.yArr.index(y)])
        for q in range(len(self.qtArr)-2) :
            for y in intervalYBin :
                self.unrolledQtY.append(self.unrolledQtY[-1]+y)
        
        #unrolled binning: y large, qt fine        
        self.unrolledYQt= list(self.qtArr)
        intervalQtBin = []
        for q in self.qtArr[:-1] :
            intervalQtBin.append(self.qtArr[self.qtArr.index(q)+1]-self.qtArr[self.qtArr.index(q)])
        for y in range(len(self.yArr)-2) :
            for q in intervalQtBin :
                self.unrolledYQt.append(self.unrolledYQt[-1]+q)
        
        
        
    def getHistos(self,inFile, resFit, uncorrelate,suff) :
        
        #MC (Pre Fit) angular coefficients and variations
        self.histos[suff+'MC'+'mapTot'] =  inFile.Get('angularCoefficients/mapTot')
        for coeff,div in self.coeffDict.iteritems() :
            self.histos[suff+'MC'+coeff] =  inFile.Get('angularCoefficients/harmonics'+coeff+'_nom_nom')

        for sKind, sList in self.systDict.iteritems():

            sListMod = copy.deepcopy(sList)
            if sKind=='_LHEScaleWeight' and UNCORR :
                sListMod.append("_nom") #add nominal variation
            
            for sName in sListMod :
                self.histos[suff+'MC'+sName+'mapTot'] =  inFile.Get('angularCoefficients'+sKind+'/mapTot'+sName)
                for sNameDen in sListMod :
                    if sNameDen!=sName and not (sKind=='_LHEScaleWeight' and UNCORR) : #PDF or correlated Scale
                        continue 
                    if sName=='_nom' and sNameDen=='_nom' : 
                        continue
                    for coeff,div in self.coeffDict.iteritems() :
                        if "unpolarizedxsec" in coeff: continue
                        if UNCORR :
                            if sKind=='_LHEScaleWeight':
                                self.histos[suff+'MC'+sName+sNameDen+coeff] =  inFile.Get('angularCoefficients'+sKind+'/harmonics'+coeff+sName+sNameDen)
                            else :
                                self.histos[suff+'MC'+sName+coeff] =  inFile.Get('angularCoefficients'+sKind+'/harmonics'+coeff+sName+sNameDen)
                        else :
                            self.histos[suff+'MC'+sName+coeff] =  inFile.Get('angularCoefficients'+sKind+'/harmonics'+coeff+sName) 
        
         
        #fit - helicity xsecs histos 
        for hel in self.hels:
            self.histos[suff+'FitHel'+hel] = ROOT.TH2D(suff+'FitHel{c}'.format(c=hel), suff+'FitHel{c}'.format(c=hel), len(self.yArr)-1, array('f',self.yArr), len(self.qtArr)-1, array('f',self.qtArr))
            self.histos[suff+'FitHel'+hel+'norm'] = ROOT.TH2D(suff+'FitHel{c}norm'.format(c=hel), suff+'FitHel{c}norm'.format(c=hel), len(self.yArr)-1, array('f',self.yArr), len(self.qtArr)-1, array('f',self.qtArr))
            self.histos[suff+'FitHel'+hel].GetXaxis().SetTitle('W rapidity')
            self.histos[suff+'FitHel'+hel].GetYaxis().SetTitle('W q_{T}')
            self.histos[suff+'FitHel'+hel+'norm'].GetXaxis().SetTitle('W rapidity')
            self.histos[suff+'FitHel'+hel+'norm'].GetYaxis().SetTitle('W q_{T}')
            for ev in resFit: #dummy because there's one event only
                for i in range(1, self.histos[suff+'FitHel'+hel].GetNbinsX()+1): #loop over rapidity bins
                    for j in range(1, self.histos[suff+'FitHel'+hel].GetNbinsY()+1): #loop over pt bins
                        try:
                            coeff = eval('ev.helXsecs{}_y_{}_qt_{}_pmaskedexp'.format(hel, i, j))
                            coeff_err = eval('ev.helXsecs{}_y_{}_qt_{}_pmaskedexp_err'.format(hel, i, j))
                            self.histos[suff+'FitHel'+hel].SetBinContent(i,j,coeff)
                            self.histos[suff+'FitHel'+hel].SetBinError(i,j,coeff_err)

                            coeffnorm = eval('ev.helXsecs{}_y_{}_qt_{}_pmaskedexpnorm'.format(hel, i, j))
                            coeffnorm_err = eval('ev.helXsecs{}_y_{}_qt_{}_pmaskedexpnorm_err'.format(hel, i, j))
                            self.histos[suff+'FitHel'+hel+'norm'].SetBinContent(i,j,coeffnorm)
                            self.histos[suff+'FitHel'+hel+'norm'].SetBinError(i,j,coeffnorm_err)
                            
                        except AttributeError:
                            pass

        #fit - angular coefficients with band
        for c in self.coeffDict:
            self.histos[suff+'FitAC'+c] = ROOT.TH2D(suff+'FitAC{c}'.format(c=c), suff+'FitAC{c}'.format(c=c), len(self.yArr)-1, array('f',self.yArr), len(self.qtArr)-1, array('f',self.qtArr))
            self.histos[suff+'FitACqt'+c] = ROOT.TH1D(suff+'FitACqt{c}'.format(c=c), suff+'FitACqt{c}'.format(c=c), len(self.qtArr)-1, array('f',self.qtArr))
            self.histos[suff+'FitACy'+c] = ROOT.TH1D(suff+'FitACy{c}'.format(c=c), suff+'FitACy{c}'.format(c=c), len(self.yArr)-1, array('f',self.yArr))
            for ev in resFit: #dummy because there's one event only
                for i in range(1, self.histos[suff+'FitAC'+c].GetNbinsX()+1): #loop over rapidity bins
                    for j in range(1, self.histos[suff+'FitAC'+c].GetNbinsY()+1): #loop over pt bins
                        try:
                            coeff = eval('ev.y_{i}_qt_{j}_{c}'.format(c=c, j=j, i=i))
                            coeff_err = eval('ev.y_{i}_qt_{j}_{c}_err'.format(c=c, j=j, i=i))
                            if 'unpol' in c:
                                coeff = coeff/(3./16./math.pi)
                                coeff_err = coeff_err/(3./16./math.pi)
                            self.histos[suff+'FitAC'+c].SetBinContent(i,j,coeff)
                            self.histos[suff+'FitAC'+c].SetBinError(i,j,coeff_err)
                            
                        except AttributeError: 
                            pass
                for j in range(1, self.histos[suff+'FitAC'+c].GetNbinsY()+1): #loop over pt bins
                    try:
                        coeff = eval('ev.pt_{j}_helmeta_{c}'.format(c=c, j=j))
                        coeff_err = eval('ev.pt_{j}_helmeta_{c}_err'.format(c=c, j=j))
                        
                        self.histos[suff+'FitACqt'+c].SetBinContent(j,coeff)
                        self.histos[suff+'FitACqt'+c].SetBinError(j,coeff_err)


                    except AttributeError: 
                        pass
                for i in range(1, self.histos[suff+'FitAC'+c].GetNbinsY()+1): #loop over rapidity bins
                    try:
                        coeff = eval('ev.y_{i}_helmeta_{c}'.format(c=c, i=i))
                        coeff_err = eval('ev.y_{i}_helmeta_{c}_err'.format(c=c, i=i))
                        
                        self.histos[suff+'FitACy'+c].SetBinContent(i,coeff)
                        self.histos[suff+'FitACy'+c].SetBinError(i,coeff_err)

                    except AttributeError: 
                        pass
            
              
    def AngCoeffPlots(self,inputFile, fitFile, uncorrelate,suff) :
        
        fileFit = ROOT.TFile.Open(fitFile)
        resFit = fileFit.fitresults
        inFile = ROOT.TFile.Open(inputFile)
        self.getHistos(inFile=inFile, resFit=resFit, uncorrelate=uncorrelate,suff=suff)
        print "WARNING: syst.band done with the fit central value (ok if asimov only)"
        
        # ------------- build the bands for the angular coefficient ---------------------------# 
        for c in self.coeffDict:
            self.histos[suff+'FitBand'+c] = self.histos[suff+'FitAC'+c].Clone('FitBand'+c) #from fit (good in case of asimov)
            self.histos[suff+'FitBandPDF'+c] = self.histos[suff+'FitAC'+c].Clone('FitBandPDF'+c) #from fit (good in case of asimov) NB: NB: not used in the plots now
            self.histos[suff+'FitBandScale'+c] = self.histos[suff+'FitAC'+c].Clone('FitBandScale'+c) #from fit (good in case of asimov) NB: not used in the plots now

            
            #UNCOMMENT THIS BLOCK IF NOT ASIMOV FIT (and don't plot for reco) NOT FULLY IMPLMENTED!!!
            # if not "unpol" in c: 
                # self.histos[suff+'FitBand'+c] = self.histos[suff+'MC'+c].Clone('FitBand'+c)
            # else:
                # self.histos[suff+'FitBand'+c] = self.histos[suff+'MC'+'mapTot'].Clone('FitBand'+c)
                #self.histos[suff+'FitBand'+c].Scale(1./35.9)

            for i in range(1, self.histos[suff+'FitAC'+c].GetNbinsX()+1): #loop over rapidity bins
                for j in range(1, self.histos[suff+'FitAC'+c].GetNbinsY()+1): #loop over pt bins
                    errPDF = 0.
                    MCVal = self.histos[suff+'FitAC'+c].GetBinContent(i,j) #form Fit (the same in case of asimov fit)
                    # if 'unpol' in c:
                    #     MCVal=MCVal/35.9
                    
                    for sName in self.systDict['_LHEPdfWeight']:
                        if 'unpol' in c:
                            systVal=self.histos[suff+'MC'+sName+'mapTot'].GetBinContent(i,j)/35.9
                        else:
                            systVal = self.histos[suff+'MC'+sName+c].GetBinContent(i,j)
                        errPDF+= (MCVal - systVal)**2  
                    self.histos[suff+'FitBandPDF'+c].SetBinError(i,j,math.sqrt(errPDF)) 
                            
                    sListMod = copy.deepcopy(self.systDict['_LHEScaleWeight'])
                    if UNCORR :
                        sListMod.append("_nom") #add nominal variation
                    errScale = 0.
                    for sName in sListMod:
                        for sNameDen in sListMod :
                            if sNameDen!=sName and not UNCORR : continue
                            if sNameDen!=sName and 'unpol' in c : continue
                            if sName=='_nom' and sNameDen=='_nom' : continue
                            if 'unpol' in c:
                                systVal=self.histos[suff+'MC'+sName+'mapTot'].GetBinContent(i,j)/35.9
                            else:
                                if UNCORR :
                                    systVal = self.histos[suff+'MC'+sName+sNameDen+c].GetBinContent(i,j)
                                else : 
                                    systVal = self.histos[suff+'MC'+sName+c].GetBinContent(i,j)
                            err_temp= (MCVal - systVal)**2
                            if err_temp>errScale : 
                                errScale = err_temp
                    self.histos[suff+'FitBandScale'+c].SetBinError(i,j,math.sqrt(errScale)) 

                    err=errPDF+errScale
                    self.histos[suff+'FitBand'+c].SetBinError(i,j,math.sqrt(err)) 
        
        #--------------- build the relative uncertainity breakdown plots -----------------------#
        for c in self.coeffDict:
            self.histos[suff+'FitErr'+c] = self.histos[suff+'FitAC'+c].Clone('FitErr'+c) #from fit (good in case of asimov)
            self.histos[suff+'FitErrPDF'+c] = self.histos[suff+'FitBandPDF'+c].Clone('FitErrPDF'+c) #from fit (good in case of asimov)
            self.histos[suff+'FitErrScale'+c] = self.histos[suff+'FitBandScale'+c].Clone('FitErrScale'+c) #from fit (good in case of asimov)
            for i in range(1, self.histos[suff+'FitAC'+c].GetNbinsX()+1): 
                for j in range(1, self.histos[suff+'FitAC'+c].GetNbinsY()+1):
                    valCentral = self.histos[suff+'FitAC'+c].GetBinContent(i,j)
                    self.histos[suff+'FitErr'+c].SetBinContent(i,j, self.histos[suff+'FitErr'+c].GetBinError(i,j)/abs(valCentral))
                    self.histos[suff+'FitErrPDF'+c].SetBinContent(i,j,self.histos[suff+'FitErrPDF'+c].GetBinError(i,j)/abs(valCentral))
                    self.histos[suff+'FitErrScale'+c].SetBinContent(i,j,self.histos[suff+'FitErrScale'+c].GetBinError(i,j)/abs(valCentral))
                    self.histos[suff+'FitErr'+c].SetBinError(i,j,0)
                    self.histos[suff+'FitErrPDF'+c].SetBinError(i,j,0)
                    self.histos[suff+'FitErrScale'+c].SetBinError(i,j,0)   
                    # print suff, c, i, j, "central=",valCentral, "main=", self.histos[suff+'FitErr'+c].GetBinContent(i,j), "pdf=",self.histos[suff+'FitErrPDF'+c].GetBinContent(i,j),"scale=",self.histos[suff+'FitErrScale'+c].GetBinContent(i,j)
                    
            
        #--------------- Ai 1D canvas -------------------#
        for c in self.coeffDict:
            for i in range(1, self.histos[suff+'FitAC'+c].GetNbinsX()+1): #loop over rapidity bins
                self.canvas[suff+'FitAC'+'qt'+str(i)+c] = ROOT.TCanvas(suff+"_c_projQt{}_{}".format(i,c),suff+"_c_projQt{}_{}".format(i,c))
                self.canvas[suff+'FitAC'+'qt'+str(i)+c].SetGridx()
                self.canvas[suff+'FitAC'+'qt'+str(i)+c].SetGridy()
                self.histos[suff+'FitAC'+'qt'+str(i)+c] = self.histos[suff+'FitAC'+c].ProjectionY("projQt{}_{}".format(i,c),i,i)
                self.histos[suff+'FitBand'+'qt'+str(i)+c] = self.histos[suff+'FitBand'+c].ProjectionY("projQt{}_{}_err".format(i,c),i,i)
                self.histos[suff+'FitAC'+'qt'+str(i)+c].SetTitle(c+" vs W transverse momentum, "+str(self.yArr[i-1])+"<Y_{W}<"+str(self.yArr[i]))
                self.canvas[suff+'FitAC'+'qt'+str(i)+c].cd()
                self.histos[suff+'FitAC'+'qt'+str(i)+c].GetXaxis().SetTitle('q_{T}^{W} [GeV]')
                self.histos[suff+'FitAC'+'qt'+str(i)+c].GetYaxis().SetTitle(c)
                self.histos[suff+'FitAC'+'qt'+str(i)+c].SetLineWidth(2)
                self.histos[suff+'FitAC'+'qt'+str(i)+c].SetStats(0)
                self.histos[suff+'FitAC'+'qt'+str(i)+c].Draw()
                self.histos[suff+'FitAC'+'qt'+str(i)+c].GetYaxis().SetRangeUser(-4,4)
                self.histos[suff+'FitBand'+'qt'+str(i)+c].SetFillColor(ROOT.kOrange-3)
                self.histos[suff+'FitBand'+'qt'+str(i)+c].SetFillStyle(0)
                self.histos[suff+'FitBand'+'qt'+str(i)+c].SetLineColor(ROOT.kOrange-3)
                self.histos[suff+'FitBand'+'qt'+str(i)+c].SetLineWidth(2)
                self.histos[suff+'FitBand'+'qt'+str(i)+c].DrawCopy("E2 same")
                self.histos[suff+'FitBand'+'qt'+str(i)+c].SetFillStyle(3001)
                self.histos[suff+'FitBand'+'qt'+str(i)+c].Draw("E2 same")
                self.histos[suff+'FitAC'+'qt'+str(i)+c].DrawCopy("same") #to have foreground
            for j in range(1, self.histos[suff+'FitAC'+c].GetNbinsY()+1): #loop over pt bins
                self.canvas[suff+'FitAC'+'y'+str(j)+c] = ROOT.TCanvas(suff+"_c_projY{}_{}".format(j,c),suff+"_c_projY{}_{}".format(j,c))
                self.canvas[suff+'FitAC'+'y'+str(j)+c].SetGridx()
                self.canvas[suff+'FitAC'+'y'+str(j)+c].SetGridy()
                self.histos[suff+'FitAC'+'y'+str(j)+c] = self.histos[suff+'FitAC'+c].ProjectionX("projY{}_{}".format(j,c),j,j)
                self.histos[suff+'FitBand'+'y'+str(j)+c] = self.histos[suff+'FitBand'+c].ProjectionX("projY{}_{}_err".format(j,c),j,j)
                self.histos[suff+'FitAC'+'y'+str(j)+c].SetTitle(c+" vs W rapidity, "+str(self.qtArr[j-1])+"<q_{T}^{W}<"+str(self.qtArr[j]))
                self.canvas[suff+'FitAC'+'y'+str(j)+c].cd()
                self.histos[suff+'FitAC'+'y'+str(j)+c].GetXaxis().SetTitle('Y_{W}')
                self.histos[suff+'FitAC'+'y'+str(j)+c].GetYaxis().SetTitle(c)
                self.histos[suff+'FitAC'+'y'+str(j)+c].SetLineWidth(2)
                self.histos[suff+'FitAC'+'y'+str(j)+c].SetStats(0)
                self.histos[suff+'FitAC'+'y'+str(j)+c].Draw()
                self.histos[suff+'FitAC'+'y'+str(j)+c].GetYaxis().SetRangeUser(-4,4)
                self.histos[suff+'FitBand'+'y'+str(j)+c].SetFillColor(ROOT.kMagenta-7)
                self.histos[suff+'FitBand'+'y'+str(j)+c].SetFillStyle(0)
                self.histos[suff+'FitBand'+'y'+str(j)+c].SetLineColor(ROOT.kMagenta-7)
                self.histos[suff+'FitBand'+'y'+str(j)+c].SetLineWidth(2)
                self.histos[suff+'FitBand'+'y'+str(j)+c].DrawCopy("E2 same")
                self.histos[suff+'FitBand'+'y'+str(j)+c].SetFillStyle(3001)
                self.histos[suff+'FitBand'+'y'+str(j)+c].Draw("E2 same")
                self.histos[suff+'FitAC'+'y'+str(j)+c].DrawCopy("same") #to have foreground        
        
          

            
            #-------------- unrolled: qt large, y small ----------------- #
            self.histos[suff+'FitAC'+'UNRqty'+c] = ROOT.TH1F(suff+'_coeff_UNRqty'+c,suff+'_coeff_UNRqty'+c,len(self.unrolledQtY)-1, array('f',self.unrolledQtY))
            self.histos[suff+'FitBand'+'UNRqty'+c] = ROOT.TH1F(suff+'_coeff_UNRqty_syst'+c,suff+'_coeff_UNRqty_syst'+c,len(self.unrolledQtY)-1, array('f',self.unrolledQtY))
            for q in self.qtArr[:-1] :
                for y in self.yArr[:-1] :
                    indexUNRqty = self.qtArr.index(float(q))*(len(self.yArr)-1)+self.yArr.index(float(y))
                    self.histos[suff+'FitAC'+'UNRqty'+c].SetBinContent(indexUNRqty+1,self.histos[suff+'FitAC'+c].GetBinContent(self.yArr.index(y)+1,self.qtArr.index(q)+1))
                    self.histos[suff+'FitAC'+'UNRqty'+c].SetBinError(indexUNRqty+1,self.histos[suff+'FitAC'+c].GetBinError(self.yArr.index(y)+1,self.qtArr.index(q)+1))
                    self.histos[suff+'FitBand'+'UNRqty'+c].SetBinContent(indexUNRqty+1,self.histos[suff+'FitBand'+c].GetBinContent(self.yArr.index(y)+1,self.qtArr.index(q)+1))
                    self.histos[suff+'FitBand'+'UNRqty'+c].SetBinError(indexUNRqty+1,self.histos[suff+'FitBand'+c].GetBinError(self.yArr.index(y)+1,self.qtArr.index(q)+1))
                    # if self.yArr.index(y)==len(self.yArr)-2 :
                        # self.histos[suff+'FitAC'+'UNRqty'+c].GetXaxis().SetBinLabel(indexUNRqty+1,"q_{T}="+str(q)+", Y="+str(y))
                    if self.yArr.index(y)==0 :
                        self.histos[suff+'FitAC'+'UNRqty'+c].GetXaxis().SetBinLabel(indexUNRqty+1,"q_{T}^{W}#in[%.0f,%.0f]" % (q, self.qtArr[self.qtArr.index(q)+1]))
                        self.histos[suff+'FitAC'+'UNRqty'+c].GetXaxis().ChangeLabel(indexUNRqty+1,340,0.03)
                    # else :
                    #     self.histos[suff+'FitAC'+'UNRqty'+c].GetXaxis().SetBinLabel(indexUNRqty+1,str(y))        
            self.histos[suff+'FitAC'+'UNRqty'+c].SetTitle(suff+' '+c+", unrolled q_{T}(Y) ")
            # self.histos[suff+'FitAC'+'UNRqty'+c].GetXaxis().SetTitle('q_{T}^{W} large, Y_{W} small')
            self.histos[suff+'FitAC'+'UNRqty'+c].GetXaxis().SetTitle('fine binning: Y_{W} 0#rightarrow 2.4')
            self.histos[suff+'FitAC'+'UNRqty'+c].GetXaxis().SetTitleOffset(1.45)
            self.histos[suff+'FitAC'+'UNRqty'+c].GetYaxis().SetTitle(c)
            self.histos[suff+'FitAC'+'UNRqty'+c].GetYaxis().SetRangeUser(-4,4)
            self.histos[suff+'FitAC'+'UNRqty'+c].SetLineWidth(2)
            self.histos[suff+'FitAC'+'UNRqty'+c].SetStats(0)
            self.histos[suff+'FitBand'+'UNRqty'+c].SetFillColor(ROOT.kOrange-3)
            self.histos[suff+'FitBand'+'UNRqty'+c].SetFillStyle(0)
            self.histos[suff+'FitBand'+'UNRqty'+c].SetLineColor(ROOT.kOrange-3)
            self.histos[suff+'FitBand'+'UNRqty'+c].SetLineWidth(2)
            
            self.canvas[suff+'FitAC'+'UNRqty'+c] = ROOT.TCanvas(suff+'_c_UNRqty'+c,suff+'_c_UNRqty'+c,800,600)
            self.canvas[suff+'FitAC'+'UNRqty'+c].cd()
            self.canvas[suff+'FitAC'+'UNRqty'+c].SetGridx()
            self.canvas[suff+'FitAC'+'UNRqty'+c].SetGridy()
            self.histos[suff+'FitAC'+'UNRqty'+c].Draw()
            self.histos[suff+'FitBand'+'UNRqty'+c].DrawCopy('E2 same')
            self.histos[suff+'FitBand'+'UNRqty'+c].SetFillStyle(3001)
            self.histos[suff+'FitBand'+'UNRqty'+c].Draw("E2 same")
            self.histos[suff+'FitAC'+'UNRqty'+c].DrawCopy("same") #to have foreground                    



            #------------- unrolled: y large, qt small -----------------                    
            self.histos[suff+'FitAC'+'UNRyqt'+c] = ROOT.TH1F(suff+'_coeff_UNRyqt'+c,suff+'_coeff_UNRyqt'+c,len(self.unrolledYQt)-1, array('f',self.unrolledYQt))
            self.histos[suff+'FitBand'+'UNRyqt'+c] = ROOT.TH1F(suff+'_coeff_UNRyqt_syst'+c,suff+'_coeff_UNRyqt_syst'+c,len(self.unrolledYQt)-1, array('f',self.unrolledYQt))
            for y in self.yArr[:-1] :
                for q in self.qtArr[:-1] :
                    indexUNRyqt = self.yArr.index(float(y))*(len(self.qtArr)-1)+self.qtArr.index(float(q))
                    self.histos[suff+'FitAC'+'UNRyqt'+c].SetBinContent(indexUNRyqt+1,self.histos[suff+'FitAC'+c].GetBinContent(self.yArr.index(y)+1,self.qtArr.index(q)+1))
                    self.histos[suff+'FitAC'+'UNRyqt'+c].SetBinError(indexUNRyqt+1,self.histos[suff+'FitAC'+c].GetBinError(self.yArr.index(y)+1,self.qtArr.index(q)+1))
                    self.histos[suff+'FitBand'+'UNRyqt'+c].SetBinContent(indexUNRyqt+1,self.histos[suff+'FitBand'+c].GetBinContent(self.yArr.index(y)+1,self.qtArr.index(q)+1))
                    self.histos[suff+'FitBand'+'UNRyqt'+c].SetBinError(indexUNRyqt+1,self.histos[suff+'FitBand'+c].GetBinError(self.yArr.index(y)+1,self.qtArr.index(q)+1))
                    if self.qtArr.index(q)==0 :
                        # self.histos[suff+'FitAC'+'UNRyqt'+c].GetXaxis().SetBinLabel(indexUNRyqt+1,"Y_{W}=%.1f" % y)
                        self.histos[suff+'FitAC'+'UNRyqt'+c].GetXaxis().SetBinLabel(indexUNRyqt+1,"Y_{W}#in[%.1f,%.1f]" % (y, self.yArr[self.yArr.index(y)+1]))
                        # self.histos[suff+'FitAC'+'UNRyqt'+c].GetXaxis().ChangeLabel(indexUNRyqt+1,340,0.03)
            self.histos[suff+'FitAC'+'UNRyqt'+c].SetTitle(suff+' '+c+", unrolled Y(q_{T}) ")
            # self.histos[suff+'FitAC'+'UNRyqt'+c].GetXaxis().SetTitle('Y_{W} large, q_{T}^{W}small')
            self.histos[suff+'FitAC'+'UNRyqt'+c].GetXaxis().SetTitle('fine binning: q_{T}^{W} 0#rightarrow 32 GeV')
            self.histos[suff+'FitAC'+'UNRyqt'+c].GetXaxis().SetTitleOffset(1.45)
            self.histos[suff+'FitAC'+'UNRyqt'+c].GetYaxis().SetTitle(c)
            self.histos[suff+'FitAC'+'UNRyqt'+c].GetYaxis().SetRangeUser(-4,4)
            self.histos[suff+'FitAC'+'UNRyqt'+c].SetLineWidth(2)
            self.histos[suff+'FitAC'+'UNRyqt'+c].SetStats(0)
            self.histos[suff+'FitBand'+'UNRyqt'+c].SetFillColor(ROOT.kMagenta-7)
            self.histos[suff+'FitBand'+'UNRyqt'+c].SetFillStyle(0)
            self.histos[suff+'FitBand'+'UNRyqt'+c].SetLineColor(ROOT.kMagenta-7)
            self.histos[suff+'FitBand'+'UNRyqt'+c].SetLineWidth(2)
            
            self.canvas[suff+'FitAC'+'UNRyqt'+c] = ROOT.TCanvas(suff+'_c_UNRyqt'+c,suff+'_c_UNRyqt'+c,800,600)
            self.canvas[suff+'FitAC'+'UNRyqt'+c].cd()
            self.canvas[suff+'FitAC'+'UNRyqt'+c].SetGridx()
            self.canvas[suff+'FitAC'+'UNRyqt'+c].SetGridy()
            self.histos[suff+'FitAC'+'UNRyqt'+c].Draw()
            self.histos[suff+'FitBand'+'UNRyqt'+c].DrawCopy('E2 same')
            self.histos[suff+'FitBand'+'UNRyqt'+c].SetFillStyle(3001)
            self.histos[suff+'FitBand'+'UNRyqt'+c].Draw("E2 same")
            self.histos[suff+'FitAC'+'UNRyqt'+c].DrawCopy("same") #to have foreground
            
            
        
        
             #--------------- Ai 1D relative syst. band canvas -------------------#
            for i in range(1, self.histos[suff+'FitErr'+c].GetNbinsX()+1): #loop over rapidity bins
                self.canvas[suff+'FitErr'+'qt'+str(i)+c] = ROOT.TCanvas(suff+"_c_projQt{}_{}_Err".format(i,c),suff+"_c_ErrprojQt{}_{}_Err".format(i,c))
                self.canvas[suff+'FitErr'+'qt'+str(i)+c].SetGridx()
                self.canvas[suff+'FitErr'+'qt'+str(i)+c].SetGridy()
                self.leg[suff+'FitErr'+'qt'+str(i)+c] = ROOT.TLegend(0.6,0.75,0.9,0.9)
                self.histos[suff+'FitErr'+'qt'+str(i)+c] = self.histos[suff+'FitErr'+c].ProjectionY("projQt{}_{}_Err".format(i,c),i,i)
                self.histos[suff+'FitErrPDF'+'qt'+str(i)+c] = self.histos[suff+'FitErrPDF'+c].ProjectionY("projQt{}_{}_ErrPDF".format(i,c),i,i)
                self.histos[suff+'FitErrScale'+'qt'+str(i)+c] = self.histos[suff+'FitErrScale'+c].ProjectionY("projQt{}_{}_ErrScale".format(i,c),i,i)
                self.histos[suff+'FitErr'+'qt'+str(i)+c].SetTitle(suff+' '+c+" relative uncertainity vs W transverse momentum, "+str(self.yArr[i-1])+"<Y_{W}<"+str(self.yArr[i]))
                self.canvas[suff+'FitErr'+'qt'+str(i)+c].cd()
                self.histos[suff+'FitErr'+'qt'+str(i)+c].GetXaxis().SetTitle('q_{T}^{W} [GeV]')
                self.histos[suff+'FitErr'+'qt'+str(i)+c].GetYaxis().SetTitle('#Delta'+c+'/'+c)
                self.histos[suff+'FitErr'+'qt'+str(i)+c].GetYaxis().SetRangeUser(0.001,1300)
                self.canvas[suff+'FitErr'+'qt'+str(i)+c].SetLogy()
                self.histos[suff+'FitErr'+'qt'+str(i)+c].SetLineWidth(3)
                self.histos[suff+'FitErr'+'qt'+str(i)+c].SetStats(0)
                self.histos[suff+'FitErr'+'qt'+str(i)+c].Draw('hist')
                self.histos[suff+'FitErr'+'qt'+str(i)+c].SetLineColor(self.groupedSystColors['Nominal'][0])
                self.histos[suff+'FitErrPDF'+'qt'+str(i)+c].SetLineColor(self.groupedSystColors['LHEPdfWeightVars'][0])
                self.histos[suff+'FitErrScale'+'qt'+str(i)+c].SetLineColor(self.groupedSystColors['LHEScaleWeightVars'][0])
                self.histos[suff+'FitErrPDF'+'qt'+str(i)+c].SetLineWidth(3)
                self.histos[suff+'FitErrScale'+'qt'+str(i)+c].SetLineWidth(3)
                self.histos[suff+'FitErrPDF'+'qt'+str(i)+c].Draw("hist same")
                self.histos[suff+'FitErrScale'+'qt'+str(i)+c].Draw("hist same")
                self.leg[suff+'FitErr'+'qt'+str(i)+c].AddEntry(self.histos[suff+'FitErr'+'qt'+str(i)+c],self.groupedSystColors['Nominal'][1])
                self.leg[suff+'FitErr'+'qt'+str(i)+c].AddEntry(self.histos[suff+'FitErrPDF'+'qt'+str(i)+c],self.groupedSystColors['LHEPdfWeightVars'][1])
                self.leg[suff+'FitErr'+'qt'+str(i)+c].AddEntry(self.histos[suff+'FitErrScale'+'qt'+str(i)+c],self.groupedSystColors['LHEScaleWeightVars'][1])
                self.leg[suff+'FitErr'+'qt'+str(i)+c].Draw("Same")
            for j in range(1, self.histos[suff+'FitErr'+c].GetNbinsY()+1): #loop over pt bins
                self.canvas[suff+'FitErr'+'y'+str(j)+c] = ROOT.TCanvas(suff+"_c_projY{}_{}_Err".format(j,c),suff+"_c_projY{}_{}_Err".format(j,c))
                self.canvas[suff+'FitErr'+'y'+str(j)+c].SetGridx()
                self.canvas[suff+'FitErr'+'y'+str(j)+c].SetGridy()
                self.leg[suff+'FitErr'+'y'+str(j)+c] = ROOT.TLegend(0.6,0.75,0.9,0.9)
                self.histos[suff+'FitErr'+'y'+str(j)+c] = self.histos[suff+'FitErr'+c].ProjectionX("projY{}_{}".format(j,c),j,j)
                self.histos[suff+'FitErrPDF'+'y'+str(j)+c] = self.histos[suff+'FitErrPDF'+c].ProjectionY("projY{}_{}_ErrPDF".format(j,c),j,j)
                self.histos[suff+'FitErrScale'+'y'+str(j)+c] = self.histos[suff+'FitErrScale'+c].ProjectionY("projY{}_{}_ErrScale".format(j,c),j,j)
                self.histos[suff+'FitErr'+'y'+str(j)+c].SetTitle(suff+' '+c+"relative uncertainity vs W rapidity, "+str(self.qtArr[j-1])+"<q_{T}^{W}<"+str(self.qtArr[j]))
                self.canvas[suff+'FitErr'+'y'+str(j)+c].cd()
                self.histos[suff+'FitErr'+'y'+str(j)+c].GetXaxis().SetTitle('Y_{W}')
                self.histos[suff+'FitErr'+'y'+str(j)+c].GetYaxis().SetTitle('#Delta'+c+'/'+c)
                self.histos[suff+'FitErr''y'+str(j)+c].GetYaxis().SetRangeUser(0.001,1300)
                self.canvas[suff+'FitErr''y'+str(j)+c].SetLogy()
                self.histos[suff+'FitErr'+'y'+str(j)+c].SetLineWidth(3)
                self.histos[suff+'FitErr'+'y'+str(j)+c].SetStats(0)
                self.histos[suff+'FitErr'+'y'+str(j)+c].Draw('hist')
                self.histos[suff+'FitErr'+'y'+str(j)+c].SetLineColor(self.groupedSystColors['Nominal'][0])
                self.histos[suff+'FitErrPDF'+'y'+str(j)+c].SetLineColor(self.groupedSystColors['LHEPdfWeightVars'][0])
                self.histos[suff+'FitErrScale'+'y'+str(j)+c].SetLineColor(self.groupedSystColors['LHEScaleWeightVars'][0])
                self.histos[suff+'FitErrPDF'+'y'+str(j)+c].SetLineWidth(3)
                self.histos[suff+'FitErrScale'+'y'+str(j)+c].SetLineWidth(3)
                self.histos[suff+'FitErrPDF'+'y'+str(j)+c].Draw("hist same")
                self.histos[suff+'FitErrScale'+'y'+str(j)+c].Draw("hist same")
                self.leg[suff+'FitErr'+'y'+str(j)+c].AddEntry(self.histos[suff+'FitErr'+'y'+str(j)+c],self.groupedSystColors['Nominal'][1])
                self.leg[suff+'FitErr'+'y'+str(j)+c].AddEntry(self.histos[suff+'FitErrPDF'+'y'+str(j)+c],self.groupedSystColors['LHEPdfWeightVars'][1])
                self.leg[suff+'FitErr'+'y'+str(j)+c].AddEntry(self.histos[suff+'FitErrScale'+'y'+str(j)+c],self.groupedSystColors['LHEScaleWeightVars'][1])
                self.leg[suff+'FitErr'+'y'+str(j)+c].Draw("Same")
                
                
            #-------------- unrolled: qt large, y small - relative syst. band canvas ----------------- #
            self.histos[suff+'FitErr'+'UNRqty'+c] = ROOT.TH1F(suff+'_coeff_Err_UNRqty'+c,suff+'_coeff_Err_UNRqty'+c,len(self.unrolledQtY)-1, array('f',self.unrolledQtY))
            self.histos[suff+'FitErrPDF'+'UNRqty'+c] = ROOT.TH1F(suff+'_coeff_ErrPDF_UNRqty'+c,suff+'_coeff_ErrPDF_UNRqty'+c,len(self.unrolledQtY)-1, array('f',self.unrolledQtY))
            self.histos[suff+'FitErrScale'+'UNRqty'+c] = ROOT.TH1F(suff+'_coeff_ErrScale_UNRqty'+c,suff+'_coeff_ErrScale_UNRqty'+c,len(self.unrolledQtY)-1, array('f',self.unrolledQtY))
            for q in self.qtArr[:-1] :
                for y in self.yArr[:-1] :
                    indexUNRqty = self.qtArr.index(float(q))*(len(self.yArr)-1)+self.yArr.index(float(y))
                    self.histos[suff+'FitErr'+'UNRqty'+c].SetBinContent(indexUNRqty+1,self.histos[suff+'FitErr'+c].GetBinContent(self.yArr.index(y)+1,self.qtArr.index(q)+1))
                    self.histos[suff+'FitErrPDF'+'UNRqty'+c].SetBinContent(indexUNRqty+1,self.histos[suff+'FitErrPDF'+c].GetBinContent(self.yArr.index(y)+1,self.qtArr.index(q)+1))
                    self.histos[suff+'FitErrScale'+'UNRqty'+c].SetBinContent(indexUNRqty+1,self.histos[suff+'FitErrScale'+c].GetBinContent(self.yArr.index(y)+1,self.qtArr.index(q)+1))
                    if self.yArr.index(y)==0 :
                        self.histos[suff+'FitErr'+'UNRqty'+c].GetXaxis().SetBinLabel(indexUNRqty+1,"q_{T}^{W}#in[%.0f,%.0f]" % (q, self.qtArr[self.qtArr.index(q)+1]))
                        self.histos[suff+'FitErr'+'UNRqty'+c].GetXaxis().ChangeLabel(indexUNRqty+1,340,0.03)    
            self.histos[suff+'FitErr'+'UNRqty'+c].SetTitle(suff+' '+c+", unrolled q_{T}(Y) ")
            self.histos[suff+'FitErr'+'UNRqty'+c].GetXaxis().SetTitle('fine binning: Y_{W} 0#rightarrow 2.4')
            self.histos[suff+'FitErr'+'UNRqty'+c].GetXaxis().SetTitleOffset(1.45)
            self.histos[suff+'FitErr'+'UNRqty'+c].GetYaxis().SetTitle('#Delta'+c+'/'+c)
            self.histos[suff+'FitErr'+'UNRqty'+c].SetLineWidth(3)
            self.histos[suff+'FitErrPDF'+'UNRqty'+c].SetLineWidth(3)
            self.histos[suff+'FitErrScale'+'UNRqty'+c].SetLineWidth(3)
            self.histos[suff+'FitErr'+'UNRqty'+c].SetStats(0)
            self.histos[suff+'FitErr'+'UNRqty'+c].SetLineColor(self.groupedSystColors['Nominal'][0])
            self.histos[suff+'FitErrPDF'+'UNRqty'+c].SetLineColor(self.groupedSystColors['LHEPdfWeightVars'][0])
            self.histos[suff+'FitErrScale'+'UNRqty'+c].SetLineColor(self.groupedSystColors['LHEScaleWeightVars'][0])

            self.canvas[suff+'FitErr'+'UNRqty'+c] = ROOT.TCanvas(suff+'_c_Err_UNRqty'+c,suff+'_c_Err_UNRqty'+c,800,600)
            self.leg[suff+'FitErr'+'UNRqty'+c] = ROOT.TLegend(0.6,0.75,0.9,0.9)
            self.canvas[suff+'FitErr'+'UNRqty'+c].cd()
            self.canvas[suff+'FitErr'+'UNRqty'+c].SetGridx()
            self.canvas[suff+'FitErr'+'UNRqty'+c].SetGridy()
            self.histos[suff+'FitErr'+'UNRqty'+c].GetYaxis().SetRangeUser(0.001,1300)
            self.canvas[suff+'FitErr'+'UNRqty'+c].SetLogy()
            self.histos[suff+'FitErr'+'UNRqty'+c].Draw()
            self.histos[suff+'FitErrPDF'+'UNRqty'+c].Draw("same")
            self.histos[suff+'FitErrScale'+'UNRqty'+c].Draw("same")
            self.leg[suff+'FitErr'+'UNRqty'+c].AddEntry(self.histos[suff+'FitErr'+'UNRqty'+c],self.groupedSystColors['Nominal'][1])
            self.leg[suff+'FitErr'+'UNRqty'+c].AddEntry(self.histos[suff+'FitErrPDF'+'UNRqty'+c],self.groupedSystColors['LHEPdfWeightVars'][1])
            self.leg[suff+'FitErr'+'UNRqty'+c].AddEntry(self.histos[suff+'FitErrScale'+'UNRqty'+c],self.groupedSystColors['LHEScaleWeightVars'][1])
            self.leg[suff+'FitErr'+'UNRqty'+c].Draw("Same")



            #------------- unrolled: y large, qt small - relative syst. band canvas -----------------                    
            self.histos[suff+'FitErr'+'UNRyqt'+c] = ROOT.TH1F(suff+'_coeff_Err_UNRyqt'+c,suff+'_coeff_Err_UNRyqt'+c,len(self.unrolledYQt)-1, array('f',self.unrolledYQt))
            self.histos[suff+'FitErrPDF'+'UNRyqt'+c] = ROOT.TH1F(suff+'_coeff_ErrPDF_UNRyqt'+c,suff+'_coeff_ErrPDF_UNRyqt'+c,len(self.unrolledYQt)-1, array('f',self.unrolledYQt))
            self.histos[suff+'FitErrScale'+'UNRyqt'+c] = ROOT.TH1F(suff+'_coeff_ErrScale_UNRyqt'+c,suff+'_coeff_ErrScale_UNRyqt'+c,len(self.unrolledYQt)-1, array('f',self.unrolledYQt))
            for y in self.yArr[:-1] :
                for q in self.qtArr[:-1] :
                    indexUNRyqt = self.yArr.index(float(y))*(len(self.qtArr)-1)+self.qtArr.index(float(q))
                    self.histos[suff+'FitErr'+'UNRyqt'+c].SetBinContent(indexUNRyqt+1,self.histos[suff+'FitErr'+c].GetBinContent(self.yArr.index(y)+1,self.qtArr.index(q)+1))
                    self.histos[suff+'FitErrPDF'+'UNRyqt'+c].SetBinContent(indexUNRyqt+1,self.histos[suff+'FitErrPDF'+c].GetBinContent(self.yArr.index(y)+1,self.qtArr.index(q)+1))
                    self.histos[suff+'FitErrScale'+'UNRyqt'+c].SetBinContent(indexUNRyqt+1,self.histos[suff+'FitErrScale'+c].GetBinContent(self.yArr.index(y)+1,self.qtArr.index(q)+1))
                    if self.qtArr.index(q)==0 :
                        self.histos[suff+'FitErr'+'UNRyqt'+c].GetXaxis().SetBinLabel(indexUNRyqt+1,"Y_{W}#in[%.1f,%.1f]" % (y, self.yArr[self.yArr.index(y)+1]))
            self.histos[suff+'FitErr'+'UNRyqt'+c].SetTitle(suff+' '+c+", unrolled Y(q_{T}) ")
            self.histos[suff+'FitErr'+'UNRyqt'+c].GetXaxis().SetTitle('fine binning: q_{T}^{W} 0#rightarrow 32 GeV')
            self.histos[suff+'FitErr'+'UNRyqt'+c].GetXaxis().SetTitleOffset(1.45)
            self.histos[suff+'FitErr'+'UNRyqt'+c].GetYaxis().SetTitle('#Delta'+c+'/'+c)
            self.histos[suff+'FitErr'+'UNRyqt'+c].SetLineWidth(3)
            self.histos[suff+'FitErrPDF'+'UNRyqt'+c].SetLineWidth(3)
            self.histos[suff+'FitErrScale'+'UNRyqt'+c].SetLineWidth(3)
            self.histos[suff+'FitErr'+'UNRyqt'+c].SetStats(0)
            self.histos[suff+'FitErr'+'UNRyqt'+c].SetLineColor(self.groupedSystColors['Nominal'][0])
            self.histos[suff+'FitErrPDF'+'UNRyqt'+c].SetLineColor(self.groupedSystColors['LHEPdfWeightVars'][0])
            self.histos[suff+'FitErrScale'+'UNRyqt'+c].SetLineColor(self.groupedSystColors['LHEScaleWeightVars'][0])
            
            self.canvas[suff+'FitErr'+'UNRyqt'+c] = ROOT.TCanvas(suff+'_c_Err_UNRyqt'+c,suff+'_c_Err_UNRyqt'+c,800,600)
            self.leg[suff+'FitErr'+'UNRyqt'+c] = ROOT.TLegend(0.6,0.75,0.9,0.9)
            self.canvas[suff+'FitErr'+'UNRyqt'+c].cd()
            self.canvas[suff+'FitErr'+'UNRyqt'+c].SetGridx()
            self.canvas[suff+'FitErr'+'UNRyqt'+c].SetGridy()
            self.histos[suff+'FitErr'+'UNRyqt'+c].GetYaxis().SetRangeUser(0.001,1300)
            self.canvas[suff+'FitErr'+'UNRyqt'+c].SetLogy()
            self.histos[suff+'FitErr'+'UNRyqt'+c].Draw()
            self.histos[suff+'FitErrPDF'+'UNRyqt'+c].Draw("same")
            self.histos[suff+'FitErrScale'+'UNRyqt'+c].Draw("same")
            self.leg[suff+'FitErr'+'UNRyqt'+c].AddEntry(self.histos[suff+'FitErr'+'UNRyqt'+c],self.groupedSystColors['Nominal'][1])
            self.leg[suff+'FitErr'+'UNRyqt'+c].AddEntry(self.histos[suff+'FitErrPDF'+'UNRyqt'+c],self.groupedSystColors['LHEPdfWeightVars'][1])
            self.leg[suff+'FitErr'+'UNRyqt'+c].AddEntry(self.histos[suff+'FitErrScale'+'UNRyqt'+c],self.groupedSystColors['LHEScaleWeightVars'][1])
            self.leg[suff+'FitErr'+'UNRyqt'+c].Draw("Same")
    
    
    def GenRecoComparison(self,suffGen, suffReco) :
        
        for c in self.coeffDict:
            
            # ------------------ Ai plots -------------------------------
            
            for i in range(1, self.histos[suffGen+'FitAC'+c].GetNbinsX()+1):
                self.canvas['comp'+'FitAC'+'qt'+str(i)+c] = self.canvas[suffGen+'FitAC'+'qt'+str(i)+c].Clone(self.canvas[suffGen+'FitAC'+'qt'+str(i)+c].GetName().replace(suffGen,'comp'))
                self.canvas['comp'+'FitAC'+'qt'+str(i)+c].SetTitle(self.canvas[suffGen+'FitAC'+'qt'+str(i)+c].GetTitle().replace(suffGen,'comp'))
                self.canvas['comp'+'FitAC'+'qt'+str(i)+c].cd()
                self.histos[suffReco+'FitAC'+'qt'+str(i)+c+'4comp'] = self.histos[suffReco+'FitAC'+'qt'+str(i)+c].Clone(suffReco+'FitAC'+'qt'+str(i)+c+'4comp')
                self.histos[suffReco+'FitAC'+'qt'+str(i)+c+'4comp'].SetLineColor(ROOT.kGreen-4)
                self.histos[suffReco+'FitAC'+'qt'+str(i)+c+'4comp'].Draw("same")
                self.histos[suffGen+'FitAC'+'qt'+str(i)+c].DrawCopy("same") #to have foreground
                
                self.leg['comp'+'FitAC'+'qt'+str(i)+c] = ROOT.TLegend(0.6,0.75,0.9,0.9)
                self.leg['comp'+'FitAC'+'qt'+str(i)+c].AddEntry(self.histos[suffReco+'FitAC'+'qt'+str(i)+c+'4comp'],'Reco Asimov')
                self.leg['comp'+'FitAC'+'qt'+str(i)+c].AddEntry(self.histos[suffGen+'FitAC'+'qt'+str(i)+c],'Gen Asimov')
                self.leg['comp'+'FitAC'+'qt'+str(i)+c].AddEntry(self.histos[suffGen+'FitBand'+'qt'+str(i)+c],'Gen Syst')
                self.leg['comp'+'FitAC'+'qt'+str(i)+c].Draw("same")
                
            for j in range(1, self.histos[suffGen+'FitErr'+c].GetNbinsY()+1):
                self.canvas['comp'+'FitAC'+'y'+str(j)+c] = self.canvas[suffGen+'FitAC'+'y'+str(j)+c].Clone(self.canvas[suffGen+'FitAC'+'y'+str(j)+c].GetName().replace(suffGen,'comp'))
                self.canvas['comp'+'FitAC'+'y'+str(j)+c].SetTitle(self.canvas[suffGen+'FitAC'+'y'+str(j)+c].GetTitle().replace(suffGen,'comp'))
                self.canvas['comp'+'FitAC'+'y'+str(j)+c].cd()
                self.histos[suffReco+'FitAC'+'y'+str(j)+c+'4comp'] = self.histos[suffReco+'FitAC'+'y'+str(j)+c].Clone(suffReco+'FitAC'+'y'+str(j)+c+'4comp')
                self.histos[suffReco+'FitAC'+'y'+str(j)+c+'4comp'].SetLineColor(ROOT.kGreen-4)
                self.histos[suffReco+'FitAC'+'y'+str(j)+c+'4comp'].Draw("same")
                self.histos[suffGen+'FitAC'+'y'+str(j)+c].DrawCopy("same") #to have foreground
                
                self.leg['comp'+'FitAC'+'y'+str(j)+c] = ROOT.TLegend(0.6,0.75,0.9,0.9)
                self.leg['comp'+'FitAC'+'y'+str(j)+c].AddEntry(self.histos[suffReco+'FitAC'+'y'+str(j)+c+'4comp'],'Reco Asimov')
                self.leg['comp'+'FitAC'+'y'+str(j)+c].AddEntry(self.histos[suffGen+'FitAC'+'y'+str(j)+c],'Gen Asimov')
                self.leg['comp'+'FitAC'+'y'+str(j)+c].AddEntry(self.histos[suffGen+'FitBand'+'y'+str(j)+c],'Gen Syst')
                self.leg['comp'+'FitAC'+'y'+str(j)+c].Draw("same")
            
            self.canvas['comp'+'FitAC'+'UNRqty'+c] = self.canvas[suffGen+'FitAC'+'UNRqty'+c].Clone(self.canvas[suffGen+'FitAC'+'UNRqty'+c].GetName().replace(suffGen,'comp'))
            self.canvas['comp'+'FitAC'+'UNRqty'+c].SetTitle(self.canvas[suffGen+'FitAC'+'UNRqty'+c].GetTitle().replace(suffGen,'comp'))
            self.canvas['comp'+'FitAC'+'UNRqty'+c].cd()
            self.histos[suffReco+'FitAC'+'UNRqty'+c+'4comp'] = self.histos[suffReco+'FitAC'+'UNRqty'+c].Clone(suffReco+'FitAC'+'y'+str(j)+c+'4comp')
            self.histos[suffReco+'FitAC'+'UNRqty'+c+'4comp'].SetLineColor(ROOT.kGreen-4)
            self.histos[suffReco+'FitAC'+'UNRqty'+c+'4comp'].Draw("same")
            self.histos[suffGen+'FitAC'+'UNRqty'+c].DrawCopy("same") #to have foreground
            self.leg['comp'+'FitAC'+'UNRqty'+c] = ROOT.TLegend(0.6,0.75,0.9,0.9)
            self.leg['comp'+'FitAC'+'UNRqty'+c].AddEntry(self.histos[suffReco+'FitAC'+'UNRqty'+c+'4comp'],'Reco Asimov')
            self.leg['comp'+'FitAC'+'UNRqty'+c].AddEntry(self.histos[suffGen+'FitAC'+'UNRqty'+c],'Gen Asimov')
            self.leg['comp'+'FitAC'+'UNRqty'+c].AddEntry(self.histos[suffGen+'FitBand'+'y'+str(j)+c],'Gen Syst')
            self.leg['comp'+'FitAC'+'UNRqty'+c].Draw("same")
            
            self.canvas['comp'+'FitAC'+'UNRyqt'+c] = self.canvas[suffGen+'FitAC'+'UNRyqt'+c].Clone(self.canvas[suffGen+'FitAC'+'UNRyqt'+c].GetName().replace(suffGen,'comp'))
            self.canvas['comp'+'FitAC'+'UNRyqt'+c].SetTitle(self.canvas[suffGen+'FitAC'+'UNRyqt'+c].GetTitle().replace(suffGen,'comp'))
            self.canvas['comp'+'FitAC'+'UNRyqt'+c].cd()
            self.histos[suffReco+'FitAC'+'UNRyqt'+c+'4comp'] = self.histos[suffReco+'FitAC'+'UNRyqt'+c].Clone(suffReco+'FitAC'+'y'+str(j)+c+'4comp')
            self.histos[suffReco+'FitAC'+'UNRyqt'+c+'4comp'].SetLineColor(ROOT.kGreen-4)
            self.histos[suffReco+'FitAC'+'UNRyqt'+c+'4comp'].Draw("same")
            self.histos[suffGen+'FitAC'+'UNRyqt'+c].DrawCopy("same") #to have foreground    
            self.leg['comp'+'FitAC'+'UNRyqt'+c] = ROOT.TLegend(0.6,0.75,0.9,0.9)
            self.leg['comp'+'FitAC'+'UNRyqt'+c].AddEntry(self.histos[suffReco+'FitAC'+'UNRyqt'+c+'4comp'],'Reco Asimov')
            self.leg['comp'+'FitAC'+'UNRyqt'+c].AddEntry(self.histos[suffGen+'FitAC'+'UNRyqt'+c],'Gen Asimov')
            self.leg['comp'+'FitAC'+'UNRyqt'+c].AddEntry(self.histos[suffGen+'FitBand'+'y'+str(j)+c],'Gen Syst')
            self.leg['comp'+'FitAC'+'UNRyqt'+c].Draw("same")
            
            
            #-------------------- Ai errors plots -------------------------------
            
            for i in range(1, self.histos[suffGen+'FitErr'+c].GetNbinsX()+1):
                self.canvas['comp'+'FitErr'+'qt'+str(i)+c] = self.canvas[suffGen+'FitErr'+'qt'+str(i)+c].Clone(self.canvas[suffGen+'FitErr'+'qt'+str(i)+c].GetName().replace(suffGen,'comp'))
                self.canvas['comp'+'FitErr'+'qt'+str(i)+c].SetTitle(self.canvas[suffGen+'FitErr'+'qt'+str(i)+c].GetTitle().replace(suffGen,'comp'))
                self.canvas['comp'+'FitErr'+'qt'+str(i)+c].cd()
                self.histos[suffReco+'FitErr'+'qt'+str(i)+c+'4comp'] = self.histos[suffReco+'FitErr'+'qt'+str(i)+c].Clone(suffReco+'FitErr'+'qt'+str(i)+c+'4comp')
                self.histos[suffReco+'FitErr'+'qt'+str(i)+c+'4comp'].SetLineColor(ROOT.kGreen-4)
                self.histos[suffReco+'FitErr'+'qt'+str(i)+c+'4comp'].Draw("same")
                self.histos[suffGen+'FitErr'+'qt'+str(i)+c].DrawCopy("same") #to have foreground
                
                self.leg['comp'+'FitErr'+'qt'+str(i)+c] = self.leg[suffGen+'FitErr'+'qt'+str(i)+c].Clone()
                self.leg['comp'+'FitErr'+'qt'+str(i)+c].AddEntry(self.histos[suffReco+'FitErr'+'qt'+str(i)+c+'4comp'],'Reco Fit Err.')
                self.leg['comp'+'FitErr'+'qt'+str(i)+c].Draw("same")
                
            for j in range(1, self.histos[suffGen+'FitErr'+c].GetNbinsY()+1):
                self.canvas['comp'+'FitErr'+'y'+str(j)+c] = self.canvas[suffGen+'FitErr'+'y'+str(j)+c].Clone(self.canvas[suffGen+'FitErr'+'y'+str(j)+c].GetName().replace(suffGen,'comp'))
                self.canvas['comp'+'FitErr'+'y'+str(j)+c].SetTitle(self.canvas[suffGen+'FitErr'+'y'+str(j)+c].GetTitle().replace(suffGen,'comp'))
                self.canvas['comp'+'FitErr'+'y'+str(j)+c].cd()
                self.histos[suffReco+'FitErr'+'y'+str(j)+c+'4comp'] = self.histos[suffReco+'FitErr'+'y'+str(j)+c].Clone(suffReco+'FitErr'+'y'+str(j)+c+'4comp')
                self.histos[suffReco+'FitErr'+'y'+str(j)+c+'4comp'].SetLineColor(ROOT.kGreen-4)
                self.histos[suffReco+'FitErr'+'y'+str(j)+c+'4comp'].Draw("same")
                self.histos[suffGen+'FitErr'+'y'+str(j)+c].DrawCopy("same") #to have foreground
                
                self.leg['comp'+'FitErr'+'y'+str(j)+c] = self.leg[suffGen+'FitErr'+'y'+str(j)+c].Clone()
                self.leg['comp'+'FitErr'+'y'+str(j)+c].AddEntry(self.histos[suffReco+'FitErr'+'y'+str(j)+c+'4comp'],'Reco Fit Err.')
                self.leg['comp'+'FitErr'+'y'+str(j)+c].Draw("same")
            
            self.canvas['comp'+'FitErr'+'UNRqty'+c] = self.canvas[suffGen+'FitErr'+'UNRqty'+c].Clone(self.canvas[suffGen+'FitErr'+'UNRqty'+c].GetName().replace(suffGen,'comp'))
            self.canvas['comp'+'FitErr'+'UNRqty'+c].SetTitle(self.canvas[suffGen+'FitErr'+'UNRqty'+c].GetTitle().replace(suffGen,'comp'))
            self.canvas['comp'+'FitErr'+'UNRqty'+c].cd()
            self.histos[suffReco+'FitErr'+'UNRqty'+c+'4comp'] = self.histos[suffReco+'FitErr'+'UNRqty'+c].Clone(suffReco+'FitErr'+'y'+str(j)+c+'4comp')
            self.histos[suffReco+'FitErr'+'UNRqty'+c+'4comp'].SetLineColor(ROOT.kGreen-4)
            self.histos[suffReco+'FitErr'+'UNRqty'+c+'4comp'].Draw("same")
            self.histos[suffGen+'FitErr'+'UNRqty'+c].DrawCopy("same") #to have foreground
            self.leg['comp'+'FitErr'+'UNRqty'+c] = self.leg[suffGen+'FitErr'+'UNRqty'+c].Clone()
            self.leg['comp'+'FitErr'+'UNRqty'+c].AddEntry(self.histos[suffReco+'FitErr'+'UNRqty'+c+'4comp'],'Reco Fit Err.')
            self.leg['comp'+'FitErr'+'UNRqty'+c].Draw("same")
            
            self.canvas['comp'+'FitErr'+'UNRyqt'+c] = self.canvas[suffGen+'FitErr'+'UNRyqt'+c].Clone(self.canvas[suffGen+'FitErr'+'UNRyqt'+c].GetName().replace(suffGen,'comp'))
            self.canvas['comp'+'FitErr'+'UNRyqt'+c].SetTitle(self.canvas[suffGen+'FitErr'+'UNRyqt'+c].GetTitle().replace(suffGen,'comp'))
            self.canvas['comp'+'FitErr'+'UNRyqt'+c].cd()
            self.histos[suffReco+'FitErr'+'UNRyqt'+c+'4comp'] = self.histos[suffReco+'FitErr'+'UNRyqt'+c].Clone(suffReco+'FitErr'+'y'+str(j)+c+'4comp')
            self.histos[suffReco+'FitErr'+'UNRyqt'+c+'4comp'].SetLineColor(ROOT.kGreen-4)
            self.histos[suffReco+'FitErr'+'UNRyqt'+c+'4comp'].Draw("same")
            self.histos[suffGen+'FitErr'+'UNRyqt'+c].DrawCopy("same") #to have foreground    
            self.leg['comp'+'FitErr'+'UNRyqt'+c] = self.leg[suffGen+'FitErr'+'UNRyqt'+c].Clone()
            self.leg['comp'+'FitErr'+'UNRyqt'+c].AddEntry(self.histos[suffReco+'FitErr'+'UNRyqt'+c+'4comp'],'Reco Fit Err.')
            self.leg['comp'+'FitErr'+'UNRyqt'+c].Draw("same")
            
                
        

    def makeRootOutput(self,outFile,save, suffList, comparison) :

        outFile = ROOT.TFile(outFile+".root", "recreate")
        outFile.cd()
        dirFinalDict = {}

        for suff in suffList : 
            dirFinalDict['coeff2D'+suff] = outFile.mkdir('coeff2D_'+suff)
            dirFinalDict['coeff2D'+suff].cd()
            for hel in self.hels:
                self.histos[suff+'FitHel'+hel].Write()
                self.histos[suff+'FitHel'+hel+'norm'].Write()
            for c in self.coeffDict:
                self.histos[suff+'FitAC'+c].Write()
                self.histos[suff+'FitACqt'+c].Write()
                self.histos[suff+'FitACy'+c].Write()
                self.histos[suff+'FitBand'+c].Write()
                    
            dirFinalDict['coeff'+suff] = outFile.mkdir('coeff_'+suff)
            dirFinalDict['coeff'+suff].cd()
            for c in self.coeffDict:
                for i in range(1, self.histos[suff+'FitAC'+c].GetNbinsX()+1):
                    self.canvas[suff+'FitAC'+'qt'+str(i)+c].Write()
                    self.canvas[suff+'FitErr'+'qt'+str(i)+c].Write()
                for j in range(1, self.histos[suff+'FitAC'+c].GetNbinsY()+1):
                    self.canvas[suff+'FitAC'+'y'+str(j)+c].Write()
                    self.canvas[suff+'FitErr'+'y'+str(j)+c].Write()
        
            dirFinalDict['coeff_unrolled'+suff] = outFile.mkdir('coeff_unrolled_'+suff)
            dirFinalDict['coeff_unrolled'+suff].cd()
            for c in self.coeffDict:
                self.canvas[suff+'FitAC'+'UNRqty'+c].Write()
                self.canvas[suff+'FitErr'+'UNRqty'+c].Write()
                self.canvas[suff+'FitAC'+'UNRyqt'+c].Write()
                self.canvas[suff+'FitErr'+'UNRyqt'+c].Write()
            
        if comparison :
            
            dirFinalDict['comparison_coeff'] = outFile.mkdir('comparison_coeff')
            dirFinalDict['comparison_coeff'].cd()
            for c in self.coeffDict:
                for i in range(1, self.histos[suff+'FitAC'+c].GetNbinsX()+1):
                    self.canvas['comp'+'FitAC'+'qt'+str(i)+c].Write()
                    self.canvas['comp'+'FitErr'+'qt'+str(i)+c].Write()
                for j in range(1, self.histos[suff+'FitAC'+c].GetNbinsY()+1):
                     self.canvas['comp'+'FitAC'+'y'+str(j)+c].Write()
                     self.canvas['comp'+'FitErr'+'y'+str(j)+c].Write()
                     
            dirFinalDict['comparison_coeff_unrolled'] = outFile.mkdir('comparison_coeff_unrolled')
            dirFinalDict['comparison_coeff_unrolled'].cd()
            for c in self.coeffDict:
                self.canvas['comp'+'FitAC'+'UNRqty'+c].Write()                
                self.canvas['comp'+'FitErr'+'UNRqty'+c].Write()
                self.canvas['comp'+'FitAC'+'UNRyqt'+c].Write()
                self.canvas['comp'+'FitErr'+'UNRyqt'+c].Write()

                
            # dirFinalDict['coeffALL'+suff] = outFile.mkdir('coeffALL_'+suff)
            # dirFinalDict['coeffALL'+suff].cd()
            # for c in self.coeffDict:
            #     for i in range(1, self.histos[suff+'FitAC'+c].GetNbinsX()+1):
            #         self.histos[suff+'FitAC'+'qt'+str(i)+c].Write()
            #         self.histos[suff+'FitBand'+'qt'+str(i)+c].Write()
            #     for j in range(1, self.histos[suff+'FitAC'+c].GetNbinsY()+1):
            #         self.histos[suff+'FitAC'+'y'+str(j)+c].Write()
            #         self.histos[suff+'FitBand'+'qt'+str(i)+c].Write()
            #     self.histos[suff+'FitAC'+'UNRqty'+c].Write()
            #     self.histos[suff+'FitBand'+'UNRqty'+c].Write()
            #     self.histos[suff+'FitAC'+'UNRyqt'+c].Write()
            #     self.histos[suff+'FitBand'+'UNRyqt'+c].Write()
    
        
parser = argparse.ArgumentParser("")

parser.add_argument('-o','--output', type=str, default='fitResult',help="name of the output file")
parser.add_argument('-f','--fitFile', type=str, default='fit_Wplus.root',help="name of the fit result root file. If comparison active the name must be: NAME.root, NAME_reco.root")
parser.add_argument('-i','--input', type=str, default='../analysisOnGen/genInputUncorr.root',help="name of the input root file")
parser.add_argument('-u','--uncorrelate', type=int, default=True,help="if true uncorrelate num and den of Angular Coeff in MC scale variation")
parser.add_argument('-c','--comparison', type=int, default=True,help="comparison between reco and gen fit")
parser.add_argument('-s','--save', type=int, default=False,help="save .png and .pdf canvas")

args = parser.parse_args()
OUTPUT = args.output
FITFILE = args.fitFile
INPUT = args.input
UNCORR = args.uncorrelate
COMP = args.comparison
SAVE= args.save

p=plotter()
p.AngCoeffPlots(inputFile=INPUT, fitFile=FITFILE, uncorrelate=UNCORR,suff='gen')
if COMP :
    recoFit = FITFILE.replace('.root', '_reco.root')
    p.AngCoeffPlots(inputFile=INPUT, fitFile=recoFit, uncorrelate=UNCORR, suff='reco')
    p.GenRecoComparison(suffGen='gen', suffReco='reco')
p.makeRootOutput(outFile=OUTPUT, save=SAVE,suffList=['gen','reco'],comparison=COMP)