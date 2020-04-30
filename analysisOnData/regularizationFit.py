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
from scipy import stats
# from ROOT import *
from ROOT import gStyle
ROOT.gROOT.SetBatch(True)
ROOT.TH1.AddDirectory(False)
ROOT.TH2.AddDirectory(False)


pp = pprint.PrettyPrinter(indent=2)

parser = argparse.ArgumentParser("")
parser.add_argument('-o', '--output_dir',type=str, default='TEST', help="")
parser.add_argument('-validation_only', '--validation_only',type=int, default=False, help="False: skip fit and do validation only")
parser.add_argument('-input_name', '--input_name',type=str, default='regularizationFit', help="Name of the input file for validation_only")


args = parser.parse_args()
output_dir = args.output_dir
VALONLY = args.validation_only
IN_NAME = args.input_name


# ROOT.Math.MinimizerOptions.SetDefaultMinimizer("Minuit2")

class fit_func01:

    def __init__(self, id_y,id_qt, constraints='qt->0'):
        self.id_qt = id_qt
        self.len_qt = int(len(id_qt)-1)
        self.id_y = id_y
        self.len_y = int(len(id_y)-1)
        self.nparams =  len(id_qt)*len(id_y)
        self.limqt = 'qt->0' in constraints
        self.limy = 'y->0' in constraints
        
        # even-odd dependent members
        if self.len_y%2==0 : 
            self.yeven = True
        else : 
            self.yeven = False
        
        if self.len_qt%2==0 : 
            self.qteven = True
        else : 
            self.qteven = False
            

    def __call__(self, x, parameters):
        y,qt = x[0],x[1]
        val = 0.0
        p = [0.]*self.nparams                
        
        for iqt,vqt in enumerate(self.id_qt):
            for iy,vy in enumerate(self.id_y):
                itot = iqt*(len(self.id_y))+iy
                p[itot] = parameters[itot]

        if self.limqt:
            p1 = copy.deepcopy(p)
            for iqt,vqt in enumerate(self.id_qt):
                if self.qteven :
                    if iqt!=self.len_qt: continue
                    lastId=self.len_qt
                else : #N odd
                    if iqt!=(self.len_qt-1): continue
                    lastId=self.len_qt-1
                for iy,vy in enumerate(self.id_y):
                    itot = iqt*(len(self.id_y))+iy
                    constr = 0.0
                    for k in range(0, lastId): 
                        # constr += np.power(-1., self.len_qt+k+1)*p[ k*(len(self.id_y))+iy]
                        if k%2!=0 : continue
                        constr += np.power(-1.,0.5*(k-lastId)-1) *p[ k*(len(self.id_y))+iy]
                    p1[itot] = constr
            p = p1

        if self.limy:
            p1 = copy.deepcopy(p)
            for iy,vy in enumerate(self.id_y):
                if self.yeven :
                    if iy!=self.len_y: continue
                    lastId=self.len_y
                else : #N odd
                    if iy!=(self.len_y-1): continue
                    lastId=self.len_y-1
                for iqt,vqt in enumerate(self.id_qt):
                    itot = iqt*(len(self.id_y))+iy
                    constr = 0.0
                    for k in range(0, lastId): 
                        # constr += np.power(-1., self.len_y+k+1)*p[ vqt*(len(self.id_y))+k]
                        if k%2!=0 : continue #odd terms auto-cancel at y=0.
                        constr += np.power(-1.,0.5*(k-lastId)-1) *p[ vqt*(len(self.id_y))+k]
                    p1[itot] = constr
            p = p1

        #print qt,y
        for iqt,vqt in enumerate(self.id_qt):
            for iy,vy in enumerate(self.id_y):
                itot = iqt*(len(self.id_y))+iy
                # print "evaluation debug:", p
                val += p[itot]*scipy.special.eval_chebyt(vqt, qt)*scipy.special.eval_chebyt(vy, y) 
        return val
    
    
    
class fit_func:

    def __init__(self, id_y,id_qt, constraints='qt->0,y-even'):
        self.id_qt = id_qt
        self.len_qt = int(len(id_qt)-1)
        self.id_y = id_y
        self.len_y = int(len(id_y)-1)
        self.nparams =  len(id_qt)*len(id_y)
        self.limqt = 'qt->0' in constraints
        self.limy = 'y->0' in constraints
        
    def __call__(self, x, parameters):
        y,qt = x[0],x[1]
        val = 0.0
        p = [0.]*self.nparams                
        
        for iqt,vqt in enumerate(self.id_qt):
            for iy,vy in enumerate(self.id_y):
                itot = iqt*(len(self.id_y))+iy
                p[itot] = parameters[itot]

        if self.limqt:
            p1 = copy.deepcopy(p)
            for iqt,vqt in enumerate(self.id_qt):
                if iqt!=self.len_qt: continue
                for iy,vy in enumerate(self.id_y):
                    itot = iqt*(len(self.id_y))+iy
                    constr = 0.0
                    for k in range(0, self.len_qt): 
                        constr += np.power(-1., self.len_qt+k+1)*p[ k*(len(self.id_y))+iy]
                    p1[itot] = constr
            p = p1

        if self.limy:
            p1 = copy.deepcopy(p)
            for iy,vy in enumerate(self.id_y):
                if iy!=self.len_y: continue
                for iqt,vqt in enumerate(self.id_qt):
                    itot = iqt*(len(self.id_y))+iy
                    constr = 0.0
                    for k in range(0, self.len_y): 
                        constr += np.power(-1., self.len_y+k+1)*p[ vqt*(len(self.id_y))+k]
                    p1[itot] = constr
            p = p1

        #print qt,y
        for iqt,vqt in enumerate(self.id_qt):
            for iy,vy in enumerate(self.id_y):
                itot = iqt*(len(self.id_y))+iy
                val += p[itot]*scipy.special.eval_chebyt(vqt, qt)*scipy.special.eval_chebyt(vy, y) 
        return val






def fit_coeff(fname="WJets.root", charge="WtoMuP", coeff="A4", constraint='y->0', qt_max = 24., y_max = 2.5, degreeY=4,degreeQt=3,Map01=False):

    print "Coeff=",coeff, "charge=",charge
    # -------------- prepare the histos for the fit ----------------------- #
    
    inputFile   = ROOT.TFile.Open(output_dir+'/hadded/'+fname)
    hA    = ROOT.gDirectory.Get("GENINCLUSIVE_"+charge+"_nominal/GENINCLUSIVE_"+charge+"_"+coeff)
    hAErr = ROOT.gDirectory.Get("GENINCLUSIVE_"+charge+"_nominal/GENINCLUSIVE_"+charge+"_"+coeff+"Err")
    hMC   = ROOT.gDirectory.Get("GENINCLUSIVE_"+charge+"_nominal/GENINCLUSIVE_"+charge+"_MC")
        
    #settings for the output 
    hA.SetTitle('coeff_'+charge+'_'+coeff)
    hAErr.SetTitle('coeffErr_'+charge+'_'+coeff)
    hMC.SetTitle('MC_'+charge+'_'+coeff)
    hA.SetName('coeff_'+charge+'_'+coeff)
    hAErr.SetName('coeffErr_'+charge+'_'+coeff)
    hMC.SetName('MC_'+charge+'_'+coeff)
    
    hA.GetXaxis().SetTitle('Y')
    hA.GetYaxis().SetTitle('q_{T} [GeV]')
    hAErr.GetXaxis().SetTitle('Y')
    hAErr.GetYaxis().SetTitle('q_{T} [GeV]')
    hMC.GetXaxis().SetTitle('Y')
    hMC.GetYaxis().SetTitle('q_{T} [GeV]')
    
    y_max_bin  = hMC.GetXaxis().FindBin( y_max )
    y_min_bin  = hMC.GetXaxis().FindBin( 0.0 )
    y_max_cut  = hMC.GetXaxis().GetBinLowEdge(y_max_bin+1)        
    y_min_cut  = 0.0   #hMC.GetXaxis().GetBinCenter(y_min_bin)        

    qt_max_bin = hMC.GetYaxis().FindBin( qt_max )
    qt_min_bin = hMC.GetYaxis().FindBin( 0.0 )
    qt_max_cut = hMC.GetYaxis().GetBinLowEdge(qt_max_bin+1)        
    qt_min_cut = 0.0    #hMC.GetYaxis().GetBinCenter(qt_min_bin)        
    
    # print qt_max_bin,qt_min_bin,qt_max_cut,qt_min_cut
    # print y_max_bin,y_min_bin,y_max_cut,y_min_cut
# 
    x,y = [], []
    if Map01 :
        for i in range(y_min_bin, y_max_bin+1):   x.append( (hMC.GetXaxis().GetBinCenter(i)- y_min_cut)/(y_max_cut-  y_min_cut)) #range between 0,1
        for i in range(qt_min_bin, qt_max_bin+1): y.append( (hMC.GetYaxis().GetBinCenter(i)-qt_min_cut)/(qt_max_cut-qt_min_cut)) #range between 0,1
    else :
        for i in range(y_min_bin, y_max_bin+1):   x.append( 2*(hMC.GetXaxis().GetBinCenter(i)- y_min_cut)/(y_max_cut-  y_min_cut) - 1.) #range between -1,1
        for i in range(qt_min_bin, qt_max_bin+1): y.append( 2*(hMC.GetYaxis().GetBinCenter(i)-qt_min_cut)/(qt_max_cut-qt_min_cut) - 1.) #range between -1,1 

    xx = array('f', x)
    yy = array('f', y)
    # print xx
    # print yy
    
    hA_cut = ROOT.TH2F("hfit_"+charge+"_"+coeff+'_'+str(degreeY)+str(degreeQt), "hfit_"+charge+"_"+coeff+'_'+str(degreeY)+str(degreeQt), len(xx)-1, xx, len(yy)-1, yy)
    hA_cut.GetXaxis().SetTitle('Y, 1='+str(y_max))
    hA_cut.GetYaxis().SetTitle('q_{T} [GeV], 1='+str(qt_max))
    
    # print "LORENZO'S ERROR PROPAGATION"
    for i in range(1, hA_cut.GetXaxis().GetNbins()+1):
        for j in range(1, hA_cut.GetYaxis().GetNbins()+1):
            
            
            # I don't know method (Lorenzo)
            mc_eff = hMC.GetBinContent(i,j)**2/hMC.GetBinError(i,j)**2
            A = hA.GetBinContent(i,j)/hMC.GetBinContent(i,j)
            A2 = hAErr.GetBinContent(i,j)/hMC.GetBinContent(i,j)
            A_err = math.sqrt(A2 - A**2)/math.sqrt(mc_eff)
            #print A, '+/-', A_err
            hA_cut.SetBinContent(i,j, A )
            hA_cut.SetBinError(i,j, A_err )
            
            # # num and den not correlated
            # hNum = hA.GetBinContent(i,j)
            # hDen = hMC.GetBinContent(i,j)
            # hNumErr = hAErr.GetBinContent(i,j)
            # hDenErr = hMC.GetBinError(i,j)
            # hA_cut_val = hNum/hDen
            # hA_cut_err = 1/(hDen)*math.sqrt(hNum*hDenErr+hDen*hNumErr)
            # hA_cut.SetBinContent(i,j, hA_cut_val )
            # hA_cut.SetBinError(i,j, hA_cut_err )
            
            
            #num and den correlated (efficiency like)
            # hNum = hA.GetBinContent(i,j)
            # hDen = hMC.GetBinContent(i,j)
            # hNumErr = hAErr.GetBinContent(i,j)
            # hDenErr = hMC.GetBinError(i,j)
            # hAntiNum = hDen-hNum
            # print hNum, math.sqrt(hNum), hDen, math.sqrt(hDen), hDenErr, hNumErr
            # hAntiNumErr=  math.sqrt(hDenErr**2-hNumErr**2)
            # hA_cut_val = hNum/hDen
            # hA_cut_err = 1/(hDen)*math.sqrt(hNum**2*hAntiNumErr**2+hAntiNum**2*hNumErr**2)
            # hA_cut.SetBinContent(i,j, hA_cut_val )
            # hA_cut.SetBinError(i,j, hA_cut_err )
            
            
    
    #hA_cut.Draw("colz")
    
    # id_y = [0,1,2] #3 poly in y
    # id_qt = [0,1,2,3] #4 poly in qt
    # id_y = [0,1,2,3,4] 
    # id_qt = [0,1,2,3] 

    id_y  = [] #poly in y
    id_qt = [] #poly in qt
    for yy in range(0,degreeY) :
        id_y.append(yy)
    for qq in range(0,degreeQt) :
        id_qt.append(qq)    
    

    #possible contraint: 'qt->0', 'y->0', 'qt->0,y->0'
    # constraint = 'y->0'
    #constraint = ''
    if Map01 :
        func = fit_func01(id_y,id_qt, constraint)
    else :
        func = fit_func(id_y,id_qt, constraint)
    nparams = len(id_qt)*len(id_y)
    
    if Map01 :
        fit = ROOT.TF2("fit_"+charge+"_"+coeff, func, 0, 1.0, 0, 1.0, nparams)    
    else :
        fit = ROOT.TF2("fit_"+charge+"_"+coeff, func, -1, 1.0, -1, 1.0, nparams)    
    
    
    for iqt,vqt in enumerate(id_qt):
        for iy,vy in enumerate(id_y):
            itot = iqt*(len(id_y))+iy
            fit.SetParName(itot, "T"+str(iqt)+"_"+"T"+str(iy))
            fit.SetParError(itot, 0.002)

    if 'qt->0' in constraint:
        for iqt,vqt in enumerate(id_qt):
            if iqt!=int(len(id_qt)-1): continue
            for iy,vy in enumerate(id_y):
                itot = iqt*(len(id_y))+iy
                fit.SetParName(itot, "T"+str(iqt)+"_"+"T"+str(iy))
                fit.SetParError(itot, 0.002)
                # print "qt->0: Fix parameter", itot
                fit.FixParameter(itot, 0.0)

    if 'y->0' in constraint:
        for iy,vy in enumerate(id_y):
            if iy!=int(len(id_y)-1): continue
            for iqt,vqt in enumerate(id_qt):
                itot = iqt*(len(id_y))+iy
                fit.SetParName(itot, "T"+str(iqt)+"_"+"T"+str(iy))
                fit.SetParError(itot, 0.002)
                # print "y->0: Fix parameter", itot
                fit.FixParameter(itot, 0.0)
    
    # res = hA_cut.Fit(fit, "RSV") #range, result, verbose
    # print "coeff=",coeff,", constraint=", constraint, ", f(0,qt)=", fit.Eval(-1,0.2), ", f(qt,0)=", fit.Eval(0.2,-1)
    # return
    res = hA_cut.Fit(fit, "RSQ") 

    fit.SetNpx(5000)

    #DEBUG block------------------------------------#
    print "Post fit debug:"
    # res.Print()
    # for i in range(nparams) :
        # print "par", i, "=",fit.GetParameter(i), "+/-",fit.GetParError(i) 
    # print coeff, degreeQt, degreeY, charge, fit.GetNDF()
    print ">>> chi2 reduced:", fit.GetChisquare()/fit.GetNDF(), "+/-", math.sqrt(2*fit.GetNDF())/fit.GetNDF()
    #------------------------------------------------#

    
    #addittional debug ---------------#
    # for y in [-1.0, 0.0, +1.0]:
    #     print 'f(qt=0, y=', y, ')=', fit.Eval(y, -1.0 )
    # for qt in [-1.0, 0.0, +1.0]:
    #     print 'f(qt=', qt, ', y=0)=', fit.Eval(-1.0, qt )
    #--------------------------------#
    
    
    #-------------------------pulls building ------------------------------#
    
    hPulls2D = hA_cut.Clone("hPulls2D_"+charge+"_"+coeff+'_'+str(degreeY)+str(degreeQt))
    hPulls2D.SetTitle("hPulls2D_"+charge+"_"+coeff+'_'+str(degreeY)+str(degreeQt))
    hPulls2D.SetName("hPulls2D_"+charge+"_"+coeff+'_'+str(degreeY)+str(degreeQt))
    hPulls2D.Reset()
    for vy in range(1, hPulls2D.GetXaxis().GetNbins()+1):
        for iq in range(1, hPulls2D.GetYaxis().GetNbins()+1):
            hPulls2D.SetBinContent( vy, iq, (fit.Eval( hPulls2D.GetXaxis().GetBinCenter(vy), hPulls2D.GetYaxis().GetBinCenter(iq) ) - hA_cut.GetBinContent(vy,iq))/hA_cut.GetBinError(vy,iq) )
    hPulls2D.SetMinimum(-4)
    hPulls2D.SetMaximum(+4)

    hPulls1D = ROOT.TH1F("hPulls1D_"+charge+"_"+coeff+'_'+str(degreeY)+str(degreeQt), "hPulls1D_"+charge+"_"+coeff+'_'+str(degreeY)+str(degreeQt), 25,-4,4)
    for vy in range(1, hPulls2D.GetXaxis().GetNbins()+1):
        for iq in range(1, hPulls2D.GetYaxis().GetNbins()+1):
            hPulls1D.Fill( hPulls2D.GetBinContent( vy, iq) )
    # hPulls1D.Sumw2()

    c_pull = ROOT.TCanvas("c_pull_"+charge+'_'+coeff+'_'+str(degreeY)+str(degreeQt), "c_pull_"+charge+'_'+coeff+'_'+str(degreeY)+str(degreeQt), 1200, 600)
    c_pull.cd()
    c_pull.Divide(2,1)

    c_pull.cd(1)
    hPulls2D.SetStats(0)
    hPulls2D.DrawCopy("colz")
    c_pull.cd(2)
    hPulls1D.Fit("gaus", "Q", "", -4,4)
    gaus = hPulls1D.GetFunction("gaus")
    hPulls1D.DrawCopy("hist")
    gaus.Draw("same")
    # hPulls1D.SetStats()
    # stats = hPulls1D.FindObject("stats")
    ROOT.gStyle.SetOptFit()
    

    c_pull.Update()
    
    c_scratch = ROOT.TCanvas("c_scratch"+charge+coeff+str(degreeY)+str(degreeQt), "c_scratch"+charge+coeff+str(degreeY)+str(degreeQt), 1800, 600)
    c_scratch.cd()
    # c_pull.cd()
    # c_pull.Draw()

    
    
    
    #---------------prepare the output ----------------#
   
    outDict ={}
    outDict['hh'+charge+coeff] = hA
    outDict['hh'+charge+coeff+'Err'] = hAErr
    outDict['hh'+charge+coeff+'MC'] = hMC
    outDict['fit'+charge+coeff] = hA_cut
    outDict['fit'+'Res'+charge+coeff] = res
    outDict['pull'+'c'+charge+coeff] = c_pull
    outDict['pull'+'1D'+charge+coeff] = hPulls1D
    outDict['pull'+'2D'+charge+coeff] = hPulls2D
    
    # raw_input()
    return outDict


def rebuilHistoDict(charge="WtoMuP", coeff="A4", constraint='y->0', qt_max = 24., y_max = 2.5, degreeY=4,degreeQt=3,Map01=False):
    inputFile   = ROOT.TFile.Open(output_dir+'/'+IN_NAME+'.root')
    
    path = 'Y'+str(degreeY)+'_Qt'+str(degreeQt)+'/'
  
    nameDict = { #name inside : [prefix, suffix,degSuffixFlag]
        'MC_' : ['hh','MC',False],
        'hPulls2D_' : ['pull2D','',True], #True
        'hPulls1D_' : ['pull1D','',True], #add _
        'hfit_' : ['fit','',True],
        'coeff_' : ['hh','',False],
        'coeffErr_' : ['hh','Err',False],
        'c_pull_' : ['pullc','',True]
    }
    
    outDict = {}
    
    for ind,val in nameDict.iteritems() :
        val2 = ''
        if val[2] :
            val2 = '_'+str(degreeY)+str(degreeQt)
        
        # if ind=='c_pull' : #remove these lins after next run
        #     getstring = path+ind+charge+coeff+val2
        # else :
        getstring=path+ind+charge+'_'+coeff+val2
        outDict[val[0]+charge+coeff+val[1]] = inputFile.Get(getstring)
    #fit result are missing-->rebuild the chi2 form the function
    outDict['fit'+'Res'+charge+coeff] = outDict['fit'+charge+coeff].GetFunction("fit_"+charge+"_"+coeff)
    
    return outDict
    


def Validation(hdict, signDict, coeffDict, degreeYList,degreeQtList) :
    
    valDict = {}
    
    # chi2 (single degree) analysis
    for yDeg in degreeYList :
        for qtDeg in degreeQtList :
            for s,sName in signDict.iteritems() :
                valDict[str(yDeg)+str(qtDeg)+'chi2'+s] = ROOT.TH1F("hChi2"+s+'_'+str(yDeg)+str(qtDeg),"hChi2"+s+'_'+str(yDeg)+str(qtDeg),len(coeffDict),-0.5,len(coeffDict)-0.5)
                valDict[str(yDeg)+str(qtDeg)+'chi2'+s].SetLineWidth(3)
                valDict[str(yDeg)+str(qtDeg)+'chi2'+s].GetXaxis().SetTitle("Angular Coefficient")
                valDict[str(yDeg)+str(qtDeg)+'chi2'+s].GetYaxis().SetTitle("#chi^{2}/NDF")
                valDict[str(yDeg)+str(qtDeg)+'chi2'+s].SetStats(0)
                valDict[str(yDeg)+str(qtDeg)+'chi2'+s].GetYaxis().SetRangeUser(0,6)
                binN=1
                for coeff,constr in coeffDict.iteritems() :
                    if not VALONLY :
                        valDict[str(yDeg)+str(qtDeg)+'chi2'+s].SetBinContent(binN,hdict[str(yDeg)+str(qtDeg)+s+coeff]['fit'+'Res'+sName+coeff].Chi2()/hdict[str(yDeg)+str(qtDeg)+s+coeff]['fit'+'Res'+sName+coeff].Ndf())
                        valDict[str(yDeg)+str(qtDeg)+'chi2'+s].SetBinError(binN,math.sqrt(2*hdict[str(yDeg)+str(qtDeg)+s+coeff]['fit'+'Res'+sName+coeff].Ndf())/hdict[str(yDeg)+str(qtDeg)+s+coeff]['fit'+'Res'+sName+coeff].Chi2())
                    else :
                        valDict[str(yDeg)+str(qtDeg)+'chi2'+s].SetBinContent(binN,hdict[str(yDeg)+str(qtDeg)+s+coeff]['fit'+'Res'+sName+coeff].GetChisquare()/hdict[str(yDeg)+str(qtDeg)+s+coeff]['fit'+'Res'+sName+coeff].GetNDF())
                        valDict[str(yDeg)+str(qtDeg)+'chi2'+s].SetBinError(binN,math.sqrt(2*hdict[str(yDeg)+str(qtDeg)+s+coeff]['fit'+'Res'+sName+coeff].GetNDF())/hdict[str(yDeg)+str(qtDeg)+s+coeff]['fit'+'Res'+sName+coeff].GetChisquare())

                    binN+=1
                    
            valDict[str(yDeg)+str(qtDeg)+'chi2_c'] = ROOT.TCanvas("c_chi2"+'_'+str(yDeg)+str(qtDeg), "c_chi2"+'_'+str(yDeg)+str(qtDeg), 800, 600)
            valDict[str(yDeg)+str(qtDeg)+'chi2_c'].cd()
            valDict[str(yDeg)+str(qtDeg)+'chi2_c'].SetGridx()
            valDict[str(yDeg)+str(qtDeg)+'chi2_c'].SetGridy()
            valDict[str(yDeg)+str(qtDeg)+'chi2'+'Plus'].SetLineColor(1)
            valDict[str(yDeg)+str(qtDeg)+'chi2'+'Minus'].SetLineColor(2)
            valDict[str(yDeg)+str(qtDeg)+'chi2'+'Plus'].Draw()
            valDict[str(yDeg)+str(qtDeg)+'chi2'+'Minus'].Draw("SAME")
            valDict[str(yDeg)+str(qtDeg)+'chi2_leg'] = ROOT.TLegend(0.7,0.8,0.95,0.95)
            for s,sname in signDict.iteritems() : 
                valDict[str(yDeg)+str(qtDeg)+'chi2_leg'].AddEntry(valDict[str(yDeg)+str(qtDeg)+'chi2'+s],s)
            valDict[str(yDeg)+str(qtDeg)+'chi2_leg'].Draw("SAME") 
    
    #chi2 varying degree analysis
    degreeYBins_temp = []
    degreeQtBins_temp =  []
    for yDeg in degreeYList :
        degreeYBins_temp.append(yDeg-0.5)
    degreeYBins_temp.append(degreeYList[-1]+0.5)
    for qtDeg in degreeQtList :
        degreeQtBins_temp.append(qtDeg-0.5)
    degreeQtBins_temp.append(degreeYList[-1]+0.5)
    

    
    degreeQtBins = array('f',degreeQtBins_temp)
    degreeYBins = array('f',degreeYBins_temp)
    for s,sName in signDict.iteritems() :
         for coeff,constr in coeffDict.iteritems() :
                valDict['h2_chi2'+s+coeff] = ROOT.TH2F("h2_chi2_"+s+"_"+coeff, "h2_chi2_"+s+"_"+coeff, len(degreeYList), degreeYBins , len(degreeQtList), degreeQtBins)
                binY = 0 
                valDict['h2_chi2'+s+coeff].GetXaxis().SetTitle("Y polinomial degree")
                valDict['h2_chi2'+s+coeff].GetYaxis().SetTitle("q_{T} polinomial degree")
                for yDeg in degreeYList :
                    binY+=1
                    binQt=0
                    for qtDeg in degreeQtList : 
                       binQt+=1
                       if not VALONLY :
                           valDict['h2_chi2'+s+coeff].SetBinContent(binY,binQt,hdict[str(yDeg)+str(qtDeg)+s+coeff]['fit'+'Res'+sName+coeff].Chi2()/hdict[str(yDeg)+str(qtDeg)+s+coeff]['fit'+'Res'+sName+coeff].Ndf())   
                           valDict['h2_chi2'+s+coeff].SetBinError(binY,binQt,math.sqrt(2*hdict[str(yDeg)+str(qtDeg)+s+coeff]['fit'+'Res'+sName+coeff].Ndf())/hdict[str(yDeg)+str(qtDeg)+s+coeff]['fit'+'Res'+sName+coeff].Chi2())
                       else :
                           valDict['h2_chi2'+s+coeff].SetBinContent(binY,binQt,hdict[str(yDeg)+str(qtDeg)+s+coeff]['fit'+'Res'+sName+coeff].GetChisquare()/hdict[str(yDeg)+str(qtDeg)+s+coeff]['fit'+'Res'+sName+coeff].GetNDF())   
                           valDict['h2_chi2'+s+coeff].SetBinError(binY,binQt,math.sqrt(2*hdict[str(yDeg)+str(qtDeg)+s+coeff]['fit'+'Res'+sName+coeff].GetNDF())/hdict[str(yDeg)+str(qtDeg)+s+coeff]['fit'+'Res'+sName+coeff].GetChisquare())
    
    #summary of width of the pulls
    for var in ['h2_pullsSigma', 'h2_pullsSigmaFit'] : #direct from histo o gaussian fit
        for s,sName in signDict.iteritems() :
            for coeff,constr in coeffDict.iteritems() :
                valDict[var+s+coeff] = ROOT.TH2F(var+s+"_"+coeff, var+s+"_"+coeff, len(degreeYList), degreeYBins , len(degreeQtList), degreeQtBins)
                binY = 0 
                valDict[var+s+coeff].GetXaxis().SetTitle("Y polinomial degree")
                valDict[var+s+coeff].GetYaxis().SetTitle("q_{T} polinomial degree")
                for yDeg in degreeYList :
                    binY+=1
                    binQt=0
                    for qtDeg in degreeQtList : 
                        binQt+=1
                        if 'Fit' in var :
                            valDict[var+s+coeff].SetBinContent(binY,binQt,hdict[str(yDeg)+str(qtDeg)+s+coeff]['pull1D'+sName+coeff].GetFunction("gaus").GetParameter(2))
                            valDict[var+s+coeff].SetBinError(binY,binQt,hdict[str(yDeg)+str(qtDeg)+s+coeff]['pull1D'+sName+coeff].GetFunction("gaus").GetParError(2))  
                        else :
                            valDict[var+s+coeff].SetBinContent(binY,binQt,hdict[str(yDeg)+str(qtDeg)+s+coeff]['pull1D'+sName+coeff].GetStdDev())   
                            valDict[var+s+coeff].SetBinError(binY,binQt,hdict[str(yDeg)+str(qtDeg)+s+coeff]['pull1D'+sName+coeff].GetStdDevError())
    
    #evaluating p-value for the F-test. see my logbook for details
    print "WARNING: harcoded number of point fitted: 19x19=361" 
    Npt=361#number of point fitted
    for kind in ['pval_alongY','pval_alongQt'] :
        for s,sName in signDict.iteritems() :
            for coeff,constr in coeffDict.iteritems() :
                valDict[kind+s+coeff] = ROOT.TH2F(kind+s+"_"+coeff, kind+s+"_"+coeff, len(degreeYList), degreeYBins , len(degreeQtList), degreeQtBins)
                binY = 0 
                valDict[var+s+coeff].GetXaxis().SetTitle("Y polinomial degree")
                valDict[var+s+coeff].GetYaxis().SetTitle("q_{T} polinomial degree")
                for yDeg in degreeYList :
                    binY+=1
                    binQt=0
                    for qtDeg in degreeQtList : 
                        binQt+=1  
                        if binQt==1 and binY==1 : continue #no deltaChi2 for first bin

                        #evaluate number of parameter
                        if not VALONLY :
                           NDFMax = hdict[str(yDeg)+str(qtDeg)+s+coeff]['fit'+'Res'+sName+coeff].Ndf()
                        else :
                            NDFMax = hdict[str(yDeg)+str(qtDeg)+s+coeff]['fit'+'Res'+sName+coeff].GetNDF()
                        parMax = Npt-NDFMax
                        
                        #evaluate chi2 in the bin and in the previous
                        chi2Max =  valDict['h2_chi2'+s+coeff].GetBinContent(binY,binQt)*NDFMax
                        # parmMin=parMax-1                        
                        if (kind=='pval_alongQt' and binQt!=1) or binY==1:#vertical delta
                            chi2Min =  valDict['h2_chi2'+s+coeff].GetBinContent(binY,binQt-1)*(NDFMax-1)
                        if (kind=='pval_alongY' and binY!=1) or binQt==1: #horizontal delta
                            chi2Min =  valDict['h2_chi2'+s+coeff].GetBinContent(binY-1,binQt)*(NDFMax-1)
                        
                        #evaluate F
                        Fobs = (chi2Min-chi2Max)*(Npt-parMax)/chi2Max
                        if Fobs>0 :
                            pvalue=1-scipy.stats.f.cdf(Fobs,1,(Npt-parMax))
                        else :
                            pvalue=1
                            #debug
                            # if s=='Minus' and coeff=='A1' :
                            #     print kind, qtDeg,yDeg, ", chi2(min,max)=", chi2Min/(NDFMax-1), chi2Max/NDFMax, ", val from histo=", valDict['h2_chi2'+s+coeff].GetBinContent(binY-1,binQt), ", bin=", binY,binQt 
                            #     if (chi2Min/(NDFMax-1))> (chi2Max/NDFMax) :
                            #         print "min, max", chi2Min, chi2Max
                        valDict[kind+s+coeff].SetBinContent(binY,binQt,pvalue)
                        
                        
    return valDict
    
        
def figureSaver(cumulativeDict, valDict, outputname,signDict, coeffDict,degreeYList,degreeQtList, validationList) :
    
    if not os.path.isdir(output_dir+'/'+outputname): os.system('mkdir '+output_dir+'/'+outputname)
    
    for s,sname in signDict.iteritems() :
        for coeff,constr in coeffDict.iteritems() : 
            for var in  validationList :      
                c_general = ROOT.TCanvas('c_general', 'c_general', 800, 600)
                c_general.cd()
                c_general.SetLogz()
                valDict[var+s+coeff].SetStats(0)
                valDict[var+s+coeff].SetContour(200)
                valDict[var+s+coeff].Draw('text colz')
                if "pval" in var :
                    valDict[var+s+coeff].GetZaxis().SetRangeUser(10**(-16),1)
                    c_general.SaveAs(output_dir+'/'+outputname+'/'+var+'_'+s+'_'+coeff+'.png')
    
    initDict = {
        'MC_' : ['hh','MC'],
        'coeff_' : ['hh',''],
        'coeffErr_' : ['hh','Err'],
    }
    
    for s,sname in signDict.iteritems() :
        for coeff,constr in coeffDict.iteritems() :
            for ind, val in initDict.iteritems() :
                    c_init = ROOT.TCanvas('c_init', 'c_init', 800, 600)
                    c_init.cd()
                    cumulativeDict[str(3)+str(3)+s+coeff][val[0]+sname+coeff+val[1]].SetStats(0)                        
                    cumulativeDict[str(3)+str(3)+s+coeff][val[0]+sname+coeff+val[1]].Draw('colz')
                    # c_init.SaveAs(output_dir+'/'+outputname+'/'+s+'_'+coeff+'_'+ind+'.png')

    
    for yDeg in degreeYList :
        for qtDeg in degreeQtList :
            for s,sname in signDict.iteritems() :
                for coeff,constr in coeffDict.iteritems() :
                    
                    c_fit3D = ROOT.TCanvas('c_fit3D', 'c_fit3D', 800, 600)
                    c_fit3D.cd()
                    cumulativeDict[str(yDeg)+str(qtDeg)+s+coeff]['fit'+sname+coeff].SetStats(0)                        
                    cumulativeDict[str(yDeg)+str(qtDeg)+s+coeff]['fit'+sname+coeff].DrawCopy('LEGO2')
                    # c_fit3D.SaveAs(output_dir+'/'+outputname+'/'+s+'_'+coeff+'_'+str(yDeg)+str(qtDeg)+'_Fit3D.png')
                    
                    c_fit = ROOT.TCanvas('c_fit', 'c_fit', 800, 600)
                    c_fit.cd()
                    cumulativeDict[str(yDeg)+str(qtDeg)+s+coeff]['fit'+sname+coeff].Draw('colz')
                    # c_fit.SaveAs(output_dir+'/'+outputname+'/'+s+'_'+coeff+'_'+str(yDeg)+str(qtDeg)+'_Fit.png')
                    
                    c_scratch = ROOT.TCanvas('c_scratch', 'c_scratch', 1200, 600)
                    c_scratch.cd()
                    ROOT.gROOT.SetBatch(True)
                    cumulativeDict[str(yDeg)+str(qtDeg)+s+coeff]['pullc'+sname+coeff].Draw()
                    cumulativeDict[str(yDeg)+str(qtDeg)+s+coeff]['pullc'+sname+coeff].SetCanvasSize(1200,600)
                    cumulativeDict[str(yDeg)+str(qtDeg)+s+coeff]['pullc'+sname+coeff].SaveAs(output_dir+'/'+outputname+'/'+s+'_'+coeff+'_'+str(yDeg)+str(qtDeg)+'_Pulls.png')
            
            # valDict[str(yDeg)+str(qtDeg)+'chi2_c'].SaveAs(output_dir+'/'+outputname+'/chi2_'+str(yDeg)+str(qtDeg)+'.png')
                    



if __name__ == "__main__":

    cumulativeDict = {} 
    valDict ={}   
    
    signDict = {
        'Plus' : 'WtoMuP',
        'Minus' : 'WtoMuN'
        }
        
    coeffDict = {
        'A0' : 'qt->0',
        'A1' : 'qt->0, y->0',
        'A2' : 'qt->0',
        'A3' : 'qt->0, y->0',
        'A4' : 'y->0'
    }
        
    #oder of Chebyshev polinomials:
    # degreeY=4
    # degreeQt=3
    degreeYList = [2,3,4,5,6,7]
    degreeQtList = [2,3,4,5,6,7]
    
    # degreeYList = [3,4]
    # degreeQtList = [3,4]
    
    
    #do the analysis
    print "analysis started..."
    for yDeg in degreeYList :
        for qtDeg in degreeQtList :
            for s,sname in signDict.iteritems() :
                for coeff,constr in coeffDict.iteritems() :
                    if not VALONLY :
                        tempDict = fit_coeff(charge=sname,coeff=coeff,constraint=constr,degreeY=yDeg,degreeQt=qtDeg,Map01=False)
                    else : #skip analyisis, do validation only
                        tempDict = rebuilHistoDict(charge=sname,coeff=coeff,constraint=constr,degreeY=yDeg,degreeQt=qtDeg,Map01=False)    
                    cumulativeDict[str(yDeg)+str(qtDeg)+s+coeff] = tempDict
        
   

    #validation of the fit
    print "validation...."
    valDict = Validation(hdict=cumulativeDict, signDict=signDict, coeffDict=coeffDict,degreeYList=degreeYList,degreeQtList=degreeQtList)

    #writing
    print "writing..."
    output = ROOT.TFile(output_dir+"/regularizationFit_LoreRange_rebuild.root", "recreate")
    output.cd()
    
    #general histos
    validationList=  ['h2_chi2','h2_pullsSigma', 'h2_pullsSigmaFit', 'pval_alongY','pval_alongQt']
    for s,sname in signDict.iteritems() :
        for coeff,constr in coeffDict.iteritems() :
            for var in validationList :
             valDict[var+s+coeff].Write()
    
    #degree dependent histos                
    for yDeg in degreeYList :
        for qtDeg in degreeQtList :
            direc = output.mkdir('Y'+str(yDeg)+'_Qt'+str(qtDeg))
            direc.cd()
            for s,sname in signDict.iteritems() :
                for coeff,constr in coeffDict.iteritems() :
                    # print "debuug",s,coeff,yDeg, qtDeg
                    for ind,val in cumulativeDict[str(yDeg)+str(qtDeg)+s+coeff].iteritems() :
                        # print ind
                        # for ii, vv in val.iteritems() :
                        if 'Res' in ind : continue #do not write the fit result (used in validation)
                        # print val
                        val.Write()
            for ind, val in valDict.iteritems() :
                if 'h2_chi2' in ind : continue
                if str(yDeg)+str(qtDeg) not in ind : continue 
                val.Write()
    
    print "saving figures"
    figureSaver(cumulativeDict = cumulativeDict, valDict=valDict, outputname='plots', signDict=signDict, coeffDict=coeffDict,degreeYList=degreeYList,degreeQtList=degreeQtList, validationList = validationList)
    
        
                 
       
