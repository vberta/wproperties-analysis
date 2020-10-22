import ROOT
from array import array
import math
import copy
import argparse
import os
import numpy as np 
from obsminimization import pmin
import root_numpy as rootnp
import ctypes
import scipy
ROOT.gROOT.SetBatch(True)
ROOT.TH1.AddDirectory(False)
ROOT.TH2.AddDirectory(False)

import jax
import jax.numpy as jnp
# import numpy as onp
# from jax import grad, hessian, jacobian, config


#def of the chi2
# def chi2LBins(x, binScaleSq, binSigmaSq, hScaleSqSigmaSq, etas,*args):
# https://github.com/emanca/scipy-MuCal/blob/master/fittingFunctionsBinned.py#L223
# scaleSqSigmaSqModel / scaleSqBinned --> mia funzione di fit 
# scaleSqSigmaSqBinned / sigmaSqBinned --> valore parametri  
# hScaleSqSigmaSq-->cov matrix inverse, hessian 


# scaleSqBinned --> binScaleSq --> scaleSqSigmaSqBinned --> parametri? -->valori della grid in uscita dal fit
# sigmaSqBinned --> binSigmaSq --> scaleSqSigmaSqBinned --> parametri?
# NULLA         --> scaleSqSigmaSqModel --> funzione?
# hScaleSqSigmaSqBinned / hScaleSqSigmaSq 


# coeffDict = { #y plus, qt plus, y minus, qt minus, constraint y, constraint qt
#     'A0' :[2,3,2,3, VINCOLI],
#     'A1' :[5,4,5,4, ],
#     'A2' :[2,3,2,3, ],
#     'A3' :[4,3,4,3, ],
#     'A4' :[5,3,5,3, ],
#     'unpolarizedxsec':[3,3]
# }

def countPar(ny,nqt,ky,kqt) : #NOT USED
        Npar=ny*nqt
        if kqt :
            Npar-= ny
        if ky :
            Npar-= nqt
        if kqt and ky :
            Npar+=1 #the overlap between previous two loop
        return Npar 
            
def parPerCoeff(coeffList) : #NOT USED
    for li in coeffList :
        if li[0]!='unpolarizedxsec' : 
            NparPlus = countPar(li[1],li[2],li[5],li[6])
            NparMinus = countPar(li[3],li[4],li[5],li[6])
        else :
            NparPlus = li[1]/2
            NparMinus = li[1]/2
            if li[1]%2!=0 :
                NparPlus+=1
            if li[2]%2!=0 :
                NparMinus+=1
        coeffList[coeffList.index(li)].append(NparPlus)
        coeffList[coeffList.index(li)].append(NparMinus)    
        
        
def getFitRes(inFile, coeffList) :
    outDict = {}
    openFile = ROOT.TFile.Open(inFile)
    for li in coeffList :
        outDict[li[0]] = openFile.Get('coeff2D_reco/recoFitAC'+li[0])
    outDict['cov']=openFile.Get('matrices_reco/covariance_matrix_channelhelpois') #unrolled order: y0qt0a0.....y0qtNa0, y1qt0a0...y1qt0a0, ...
    return outDict 
    
def getRegFunc(inFile, coeffList) :
    outDict = {}
    openFile = ROOT.TFile.Open(inFile)
    for li in coeffList :
        if li[0]!='unpolarizedxsec' : 
            outDict[li[0]] = openFile.Get('Y'+str(li[1])+'_Qt'+str(li[2])+'/hfit_WtoMuP_'+li[0]+'_'+str(li[1])+str(li[2]))
        else :
            temph = openFile.Get('unpol_Y3/hfit_WtoMuP_unpol_3')
            for qt in range(1, temph.GetNbinsY()+1) :
                outDict[li[0]+str(qt)] = openFile.Get('unpol_Y'+str(li[1])+'/hfit_WtoMuP_unpol_3_'+str(qt))
            print "WARNING: unpolarized qt binning must be aligned to the fit qt binning!"
    return outDict

     
def chi2PostReg(modelPars,npFitRes, npCovMatInv, coeffList, npBinCenters,parNum) :
    
    # interPars = modelPars.copy()
    interPars = np.split(modelPars,parNum)
    
    fitModelList = []
    for li in coeffList :
        
        fitModelList.append(np.zeros(np.shape(npBinCenters)[0])) # list of  (y,qt), with lenght (Ny*Nqt) 

        if li[0]!=5 : #not unpol
            parsCoeffList = [] #last element must be used
            parsCoeffList.append(interPars[li[0]+np.shape(npFitRes)[2]])

            if li[5] : #contraint on y=0
                for iqt in range(li[2]) :
                    itot = iqt*(li[1])+li[1]
                    constr = 0.0
                    for k in range(0, li[1]-1): 
                        constr += np.power(-1., li[1]+k+1)*parsCoeffList[-1][iqt*li[1]+k]
                    parsCoeffList.append(jax.ops.index_update(parsCoeffList[-1], jax.ops.index[itot],constr))
                    
            if li[6] : #contraint on qt=0
                for iy in range(li[1]):
                    itot = li[2]*(li[1])+iy
                    constr = 0.0
                    for k in range(0, li[2]-1): 
                        constr += np.power(-1., li[2]+k+1)*parsCoeffList[-1][ k*li[1]+iy]
                    parsCoeffList.append(jax.ops.index_update(parsCoeffList[-1], jax.ops.index[itot],constr))
            
            for iy in range(li[1]) :
                for iqt in range(li[2]) :
                    itot = iqt*(li[1])+iy
                    fitModelList[-1] += parsCoeffList[-1][itot]*scipy.special.eval_chebyt(iy, npBinCenters[:,0])*scipy.special.eval_chebyt(iqt,npBinCenters[:,1]) 
        
        else : #unpol
            parsCoeffList = []
            # parsCoeffList.append(interPars[li[0]:])
            parsCoeffList.append(interPars[:np.shape(npFitRes)[2]])
            
            for iy in range(li[1]) : #contraint on odd degrees
                if iy%2!=0 :
                    for iqt in range(np.shape(npFitRes)[2]) : #binQt
                        parsCoeffList.append(jax.ops.index_update(parsCoeffList[-1], jax.ops.index[iqt,iy],0))
                        
            for iy in range(li[1]) :
                for iqt in range(np.shape(npFitRes)[2]) : #binQt
                    fitModelList[-1] += parsCoeffList[-1][iqt][iy]*scipy.special.eval_chebyt(iy,2*npBinCenters[:,0]-1)

        fitModelList[-1] = fitModelList[-1].reshape((jnp.shape(npFitRes)[1],jnp.shape(npFitRes)[2])) # reshape to (Ny x Nqt), like the fitRes histogram
        
    fitModel = jnp.stack(fitModelList,0)

 
    diff = npFitRes-fitModel
    diff = diff.flatten() 
    chi2 = jnp.matmul(diff.T, jnp.matmul(npCovMatInv, diff) )
    return chi2
    
    
def fitPostReg(fitRes,regFunc, coeffList) :
    
    #prepare fitRes
    dimY = fitRes['A0'].GetNbinsX()
    dimQt = fitRes['A0'].GetNbinsY()

    npCovMat = rootnp.hist2array(fitRes['cov'])
    npCovMat = npCovMat[:-1,:-1] #remove mass
    npCovMatInv = np.linalg.inv(npCovMat)
    
    
    #build the bin centers list

    binY,binQt = [], []
    for i in range(1, dimY+1):  binY.append( 2*(fitRes['A0'].GetXaxis().GetBinCenter(i)- 0.)/(fitRes['A0'].GetXaxis().GetBinLowEdge(dimY+1)-0.) - 1.) #range between -1,1
    for i in range(1, dimQt+1): binQt.append( 2*(fitRes['A0'].GetYaxis().GetBinCenter(i)- 0.)/(fitRes['A0'].GetYaxis().GetBinLowEdge(dimQt+1)-0.) - 1.) #range between -1,1 
    xx = array('f', binY)
    yy = array('f', binQt)
    
    npBinCenters = np.zeros((dimY*dimQt,2))
            
    hreb = ROOT.TH2F('hreb', 'hreb', len(xx)-1, xx, len(yy)-1, yy)
    for i in range(1, hreb.GetXaxis().GetNbins()+1): #y
        for j in range(1, hreb.GetYaxis().GetNbins()+1):#qt
            npBinCenters[(i-1)*(j-1)] = hreb.GetXaxis().GetBinCenter(i), hreb.GetYaxis().GetBinCenter(j)
            
    
    npFitResList = []
    for li in coeffList :           
        npFitResList.append(rootnp.hist2array(fitRes[li[0]])) #consider that the bin edges --> xx,yy
    npFitRes = np.stack(npFitResList,0)  #dimensions: coeff, y, qt = (6,6,8). if flatten--> q0y0a0...qNy0a0, q0y1a0....qNy1a0, ....
    
    
    
    #model init
    modelParsList = []
    parNum = []
    for li in coeffList :
        if li[0]!='unpolarizedxsec' : 
            func = regFunc[li[0]].GetFunction('fit_WtoMuP_'+li[0])
            modelParsC=np.zeros(func.GetNpar())
            for i in range(func.GetNpar()) :
                modelParsC[i] = func.GetParameter(i)
            modelParsList.append(modelParsC.copy())
            
            parNum.append(li[1]*li[2]+parNum[-1])

        else :
            for qt in range(1, regFunc['A0'].GetNbinsY()+1) :
                if qt%2==0 : continue # to allign skipped one bin every two the binning: quite bad approach, but it's relevant for init. val. only
                func = regFunc[li[0]+str(qt)].GetFunction('fit_WtoMuP_unpol')
                modelParsC=np.zeros(func.GetNpar())
                for i in range(func.GetNpar()) :
                    modelParsC[i] = func.GetParameter(i)
                modelParsList.append(modelParsC.copy())
                
                if len(parNum) >0 :
                    parNum.append(li[1]+parNum[-1])
                else :
                    parNum.append(li[1])

    # modelPars = np.stack(modelParsList,0) 
    parNum = parNum[:-1]
    modelPars = np.concatenate(modelParsList) #already flattened, otherwise YOU HAVE TO FLATTEN before pass it to the fit
    
    coeffListJAX = copy.deepcopy(coeffList)
    for li in coeffListJAX :
        if li[0] != 'unpolarizedxsec' : 
            li[0] = coeffListJAX.index(li)-1
        else :
            li[0] = 5
    
    # # DEBUGG---------------------------------------------------
    # print coeffListJAX
    # print "PAR NUM=",parNum
    # print "------------------------------------------------------"
    # print "not splitted=", modelPars
    # print "------------------------------------------------------"
    # interPars= np.split(modelPars,parNum)
    # print "ALL SPLITTED=", interPars
    # print "------------------------------------------------------"

    # print "not unpol=", 0+np.shape(npFitRes)[2], interPars[0+np.shape(npFitRes)[2]]
    # print "------------------------------------------------------"
    # print "UNPOL=", interPars[:np.shape(npFitRes)[2]]
    # # END OF DEBUGG---------------------------------------------------

    print "everything initialized, minimizer call..."
    # modelPars = pmin(chi2PostReg, modelPars, args=(npFitRes, npCovMatInv, coeffListJAX, npBinCenters,parNum), doParallel=False)
    
        
    #after fit results
    static_argnumsPF = (1,2,3,4,5)
    modelChi2Grad_eval = jax.jit(jax.value_and_grad(chi2PostReg), static_argnums=static_argnumsPF)
    modelHess_eval = jax.jit(jax.hessian(chi2PostReg), static_argnums=static_argnumsPF)
    
    modelChi2,modelGrad = modelChi2Grad_eval(modelPars, npFitRes, npCovMatInv, coeffListJAX, npBinCenters,parNum)
    modelHess = modelHess_eval(modelPars, npFitRes, npCovMatInv, coeffListJAX, npBinCenters,parNum)
    
    modelCov = 0.5*np.linalg.inv(modelHess)
    modelErr = np.sqrt(np.diag(modelCov))

    modelEDM = 0.5*np.matmul(np.matmul(fitGrad.T,modelCov),fitGrad)
    modelNDOF = dimY*dimQt - np.size(modelPars)
    
    print "*-------------------------------------------*"
    print "FIT RESULTS"
    print "edm=",modelEDM 
    print "chi2/dof=", modelChi2,"/",modelNDOF, "=", modelChi2/float(modelNDOF) 
    print "parameters=", modelPars
    print "errors=", modelErr
    print "relative uncertaintiy" , np.true_divide(modelErr,modelPars)
    print "*-------------------------------------------*"

    outFit = (modelPars,modelCov)
    
    return outFit

# def rebuildFitFunc(fitPars,cov, infoCoeff) :
    

# def plotterPostReg(fitResult, output, save, coeffList) :
#     for li in coeffList :
#         fitfunc = rebuildFitFunc(fitPars=fitResult[0],cov=fitResult[1],infoCoeff=li) #as TF1
    
    


parser = argparse.ArgumentParser("")

parser.add_argument('-o','--output', type=str, default='aposterioriFit',help="name of the output file")
parser.add_argument('-f','--fitInput', type=str, default='fitResult.root',help="name of the fit result root file, after plotter_fitResult")
parser.add_argument('-r','--regInput', type=str, default='../../regularization/TEST_2sign_MC/regularizationFit_range11_rebuild____nom_nom.root',help="name of the regularization study result root file")
parser.add_argument('-s','--save', type=int, default=False,help="save .png and .pdf canvas")

args = parser.parse_args()
OUTPUT = args.output
FITINPUT = args.fitInput
REGINPUT = args.regInput
SAVE= args.save

coeffList = []#y plus, qt plus, y minus, qt minus, constraint y, constraint qt
coeffList.append(['unpolarizedxsec', 3,3])
coeffList.append(['A0', 3,4,3,4, 0,1])
coeffList.append(['A1', 3,5,5,4, 1,1])
coeffList.append(['A2', 2,4,3,3, 0,1])
coeffList.append(['A3', 4,4,5,4, 1,1])
coeffList.append(['A4', 6,4,6,4, 1,0])

# parPerCoeff(coeffList=coeffList) #add number of free par per coeff to coeffList
fitResDict = getFitRes(inFile=FITINPUT, coeffList=coeffList)
regFuncDict = getRegFunc(inFile=REGINPUT, coeffList=coeffList)
fitPostRegResult = fitPostReg(fitRes=fitResDict, regFunc=regFuncDict, coeffList=coeffList)
# plotterPostReg(fitResult = fitPostRegResult, output=OUTPUT,save=SAVE, coeffList=coeffList)




 
