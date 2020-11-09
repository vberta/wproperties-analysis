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
            print("WARNING: unpolarized qt binning must be aligned to the fit qt binning!")
    return outDict

     
def chi2PostReg(modelPars,npFitRes, npCovMatInv, coeffList, npBinCenters,parNum) :#NOT USED, for now 
    
    # interPars = modelPars.copy()
    interPars = np.split(modelPars,parNum)
    
    fitModelList = []
    for li in coeffList :
        
        fitModelList.append(np.zeros(np.shape(npBinCenters)[0])) # list of  (y,qt), with lenght (Ny*Nqt) 

        if li[0]!=5 : #not unpol
            parsCoeffList = [] #last element must be used
            parsCoeffList.append(interPars[li[0]+np.shape(npFitRes)[2]])
            
            #rebuilt parsCoeffList with "holes"
            # parsCoeffList.append(np.zeros(li[1]*li[2]))
            # if not li[5] and not li[6] :
            #     for iy in range(li[1]) :
            #         for iqt in range(li[2]) :
            #             itot = iqt*(li[1])+iy
            #             parsCoeffList.append(jax.ops.index_update(parsCoeffList[-1], jax.ops.index[itot],parsCoeffList[-1]))
                        
            # if not li[5] and not li[6] :
            #     clist = list(parsCoeffList[-1])
            #     for iy in range(li[1]) :
            #             for iqt in range(li[2]) :
            #                 itot = iqt*(li[1])+iy
            #                 clist[itot] = parsCoeffList[itot]
            if li[5] :
                ylist = list(parsCoeffList[-1])
                for iy in range(li[1]) :
                    for iqt in range(li[2]) :
                        itot = iqt*(li[1])+iy
                        if iy==li[1]-1 :
                            ylist.insert(itot, 0.)
                parsCoeffList.append(jnp.asarray(ylist))
                
            if li[6] :
                qtlist = list(parsCoeffList[-1])
                for iy in range(li[1]) :
                    for iqt in range(li[2]) :
                        itot = iqt*(li[1])+iy
                        if iy==li[2]-1 :
                            qtlist.insert(itot, 0.)
                parsCoeffList.append(jnp.asarray(qtlist))
                        
                    
            if li[5] : #contraint on y=0
                for iqt in range(li[2]) :
                    itot = iqt*(li[1])+li[1]
                    constr = 0.0
                    for k in range(0, li[1]-1): 
                        constr += np.power(-1., li[1]+k+1)*parsCoeffList[-1][iqt*li[1]+k]
                    parsCoeffList.append(jax.ops.index_update(parsCoeffList[-1], jax.ops.index[itot],constr))
                    
            if li[6] : #costraint on qt=0
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
            
            qtList_of_interPars = []
            for iqt in range(np.shape(npFitRes)[2]) :
                clist = list(parsCoeffList[-1][iqt])
                for iy in range(li[1]) :
                    if iy%2!=0 :
                        clist.insert(iy, 0.)       
                qtList_of_interPars.append(jnp.asarray(clist))
            parsCoeffList.append(qtList_of_interPars)
            
            for iy in range(li[1]) : #contraint on odd degrees
                if iy%2!=0 :
                    for iqt in range(np.shape(npFitRes)[2]) : #binQt
                        parsCoeffList.append(jax.ops.index_update(parsCoeffList[-1], jax.ops.index[iqt,iy],0))
                        
            for iy in range(li[1]) :
                for iqt in range(np.shape(npFitRes)[2]) : #binQt
                    fitModelList[-1] += parsCoeffList[-1][iqt][iy]*scipy.special.eval_chebyt(iy,(npBinCenters[:,0]+1)/2.)#because the limits are 0,1

        fitModelList[-1] = fitModelList[-1].reshape((jnp.shape(npFitRes)[1],jnp.shape(npFitRes)[2])) # reshape to (Ny x Nqt), like the fitRes histogram
        
    fitModel = jnp.stack(fitModelList,0)
    print("this is wrong in the list there are all the not-required element ovewritten")

 
    diff = npFitRes-fitModel
    diff = diff.flatten() 
    chi2 = jnp.matmul(diff.T, jnp.matmul(npCovMatInv, diff) )
    return chi2
    
    
def fitPostReg(fitRes,regFunc, coeffList) :#NOT USED, for now 
    
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
            # modelParsC=np.zeros(func.GetNpar())
            # for i in range(func.GetNpar()) :
            #     modelParsC[i] = func.GetParameter(i)
            # modelParsList.append(modelParsC.copy())
            # parNum.append(li[1]*li[2]+parNum[-1])
            modelParsC=np.zeros(li[7])
            iset=0
            for iqt in range(li[2]) :
                for iy in range(li[1]) :
                    itot = iqt*li[1]+iy #depend not on this loop but on the ROOT par number assigment
                    if li[5] and iy==li[1]-1 : continue
                    if li[6] and iqt==li[2]-1 : continue     
                    modelParsC[iset] = func.GetParameter(itot)
                    iset+=1
            modelParsList.append(modelParsC.copy())            
            parNum.append(li[7]+parNum[-1])

        else :
            for qt in range(1, regFunc['A0'].GetNbinsY()+1) :
                if qt%2==0 : continue # to allign skipped one bin every two the binning: quite bad approach, but it's relevant for init. val. only
                func = regFunc[li[0]+str(qt)].GetFunction('fit_WtoMuP_unpol')
                modelParsC=np.zeros(li[3])
                # modelParsC=np.zeros(func.GetNpar())
                iset=0
                for i in range(func.GetNpar()) :
                    if i%2!=0 : continue 
                    modelParsC[iset] = func.GetParameter(i)
                    iset+=1
                modelParsList.append(modelParsC.copy())
                
                if len(parNum) >0 :
                    parNum.append(li[3]+parNum[-1])
                else :
                    parNum.append(li[3])
                    
                # if len(parNum) >0 :
                #     parNum.append(li[1]+parNum[-1])
                # else :
                #     parNum.append(li[1])

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

    print("everything initialized, minimizer call...")
    print("initial x=", modelPars)
    modelPars = pmin(chi2PostReg, modelPars, args=(npFitRes, npCovMatInv, coeffListJAX, npBinCenters,parNum), doParallel=False)
    
        
    # after fit results
    static_argnumsPF = (1,2,3,4,5)
    modelChi2Grad_eval = jax.jit(jax.value_and_grad(chi2PostReg), static_argnums=static_argnumsPF)
    modelHess_eval = jax.jit(jax.hessian(chi2PostReg), static_argnums=static_argnumsPF)
    
    modelChi2,modelGrad = modelChi2Grad_eval(modelPars, npFitRes, npCovMatInv, coeffListJAX, npBinCenters,parNum)
    modelHess = modelHess_eval(modelPars, npFitRes, npCovMatInv, coeffListJAX, npBinCenters,parNum)
    
    modelCov = 0.5*np.linalg.inv(modelHess)
    modelErr = np.sqrt(np.diag(modelCov))

    modelEDM = 0.5*np.matmul(np.matmul(fitGrad.T,modelCov),fitGrad)
    modelNDOF = dimY*dimQt - np.size(modelPars)
    
    print("*-------------------------------------------*")
    print("FIT RESULTS")
    print("edm=",modelEDM) 
    print("chi2/dof=", modelChi2,"/",modelNDOF, "=", modelChi2/float(modelNDOF)) 
    print("parameters=", modelPars)
    print("errors=", modelErr)
    print("relative uncertaintiy" , np.true_divide(modelErr,modelPars))
    print("*-------------------------------------------*")
    
    extraInfoDict = {
        'binY' : binY,
        'binQt' : binQt,
        'binCent' : npBinCenters,
        'npFitRes' : npFitRes
    }

    outFit = (modelPars,modelCov,extraInfoDict)
    
    return outFit









def chi2PolyFit(modelPars,npFitRes, npCovMatInv, coeffList, npBinCenters,parNum) :
    
    fitModelList = []
    valY = npBinCenters[:,0]
    valQt = npBinCenters[:,1]
    npBinCenters_res = npBinCenters.reshape(jnp.shape(npFitRes)[1],jnp.shape(npFitRes)[2],2)
    valYunpol=npBinCenters_res[:,0,0]
    # print "Y vals=", valYunpol


    icoeff = 0
    ipar=0
    # unpolMult=[1e5,1e3]    
    unpolMult=[1e5,1e5]    
    # npFitRes_rescaled = np.zeros(jnp.shape(npFitRes))
    for li in coeffList :
        if li[0]==5 :
            fitModelList_unpol = []
            for iqt in range(jnp.shape(npFitRes)[2]) :    
                # fitModelList_unpol.append(fitModelList_unpol[-1]+unpolMult*modelPars[0+ipar]+unpolMult*modelPars[1+ipar]*np.power(valYunpol,2))#+unpolMult*modelPars[2+ipar]*np.power(valYunpol,4))
                fitModelList_unpol.append(unpolMult[0]*modelPars[0+ipar]+unpolMult[1]*modelPars[1+ipar]*valYunpol+unpolMult[1]*modelPars[2+ipar]*np.power(valYunpol,2))#+unpolMult[1]*modelPars[2+ipar]*np.power(valYunpol,4))
                # fitModelList_unpol.append(fitModelList_unpol[-1]+modelPars[0+ipar]+modelPars[1+ipar]*np.power(valYunpol,2))#+modelPars[2+ipar]*np.power(valYunpol,4))
                ipar = ipar+parNum[icoeff]
                icoeff+=1
            fitModelList_unpol_stack = jnp.stack(fitModelList_unpol,0)
            # fitModelList.append(fitModelList_unpol_stack.reshape((jnp.shape(npFitRes)[1],jnp.shape(npFitRes)[2])))
            fitModelList.append(fitModelList_unpol_stack.T)
            # npFitRes_rescaled[0] = (1/10000000.)*npFitRes[0]
                       
        else :
            fitModelList_temp = []
            fitModelList_temp.append(np.zeros(jnp.shape(npBinCenters)[0])) # list of  (y,qt), with lenght (Ny*Nqt) 
            # fitModel_coeff = jnp.zeros(jnp.shape(npBinCenters)[0])
            effY = li[1]
            effQt = li[2]
            if li[5] : effY-= 1
            if li[6] : effQt-= 1
            if li[7] : effQt-= 1
            for iqt in range(0, effQt) :
                powQt = iqt
                if li[6] : powQt+= 1 
                if li[7] and li[0]!=4 : powQt+= 1 
                if li[7] and li[0]==4 and iqt>0 : powQt+=1
                for iy in range(0, effY) :
                   powY = iy
                   if li[5] : powY+= 1
                #    fitModel_coeff = jax.ops.index_update(fitModel_coeff,jax.ops.index[:],fitModel_coeff[:]+modelPars[iqt*(effY)+iy+ipar]*np.power(valY,powY)*np.power(valQt,powQt)  )
                #    print "A",li[0], "index=",iqt*(effY)+iy+ipar, "degY=",powY,", degQt=",powQt
                   fitModelList_temp.append(fitModelList_temp[-1]+modelPars[iqt*(effY)+iy+ipar]*np.power(valY,powY)*np.power(valQt,powQt) )
            ipar = ipar+parNum[icoeff]
            icoeff+=1       
            fitModelList.append(fitModelList_temp[-1].reshape((jnp.shape(npFitRes)[1],jnp.shape(npFitRes)[2]))) # reshape to (Ny x Nqt), like the fitRes histogram
            # fitModelList.append(jnp.reshape(fitModel_coeff,(jnp.shape(npFitRes)[1],jnp.shape(npFitRes)[2]))) # reshape to (Ny x Nqt), like the fitRes histogram
            # npFitRes_rescaled[li[0]+1] = npFitRes[li[0]+1]
            
    fitModel = jnp.stack(fitModelList,0)
    
    diff = npFitRes-fitModel
    # diff = npFitRes_rescaled-fitModel
    # diff = jax.ops.index_update(diff,jax.ops.index[0,:,:],diff[0,:,:]/10000000. )
   
   
   
   
    # print "shape res", jnp.shape(diff)
    # print 'POINTS='
    # print npFitRes[0]
    # print  npFitRes[1]
    # print "FIT="
    # print fitModel[0]
    # print fitModel[1]
    # print "diff"
    # print diff[0]
    # print diff[1]
    # print "diff ratio="
    # print diff[0]/npFitRes[0]
    # print diff[1]/npFitRes[1]
    # print "relative chi2 weight",  np.sum(diff,axis=(1,2))
    # print "relative chi2 weight", diff[0], diff[1], diff[2], diff[3],diff[4], diff[5], diff[6]
    
    diff = diff.flatten() 
    chi2 = jnp.matmul(diff.T, jnp.matmul(npCovMatInv, diff) )
    

    
    
    return chi2
    

def polyFit(fitRes,regFunc, coeffList) :
    
    # unpolMult = 1000
    dimY = fitRes[coeffList[0][0]].GetNbinsX()
    dimQt = fitRes[coeffList[0][0]].GetNbinsY()
    dimCoeff = len(coeffList)
    # print "dimY,dimQt=", dimY, dimQt   

    npCovMat = rootnp.hist2array(fitRes['cov'])
    npCovMat = npCovMat[0:dimCoeff*dimQt*dimY,0:dimCoeff*dimQt*dimY]
    # npCovMat = npCovMat[dimQt*dimY:6*dimQt*dimY,dimQt*dimY:6*dimQt*dimY]
    npCovMatInv = np.linalg.inv(npCovMat)
    
    npFitResList = []
    for li in coeffList :           
        npFitResList.append(rootnp.hist2array(fitRes[li[0]])) 
        # if 'unpol' in li[0] :
        #     npFitResList[-1] = (1/unpolMult)*npFitResList[-1]
    npFitRes = np.stack(npFitResList,0)  #dimensions: coeff, y, qt = (6,6,8). if flatten--> q0y0a0...qNy0a0, q0y1a0....qNy1a0, ....
    
    npBinCenters = np.zeros((dimQt*dimY,2))
    for iy in range(0, dimY): #y
        for iqt in range(0, dimQt):#qt
            itot = iy*(dimQt)+iqt
            npBinCenters[itot] = fitRes[li[0]].GetXaxis().GetBinCenter(iy+1), fitRes[li[0]].GetYaxis().GetBinCenter(iqt+1) 
    # print "BINCENTERS", npBinCenters
    # print "BINCENTER RESHAPE", np.reshape(npBinCenters,(6,8,2))
            
    #model init
    modelParsList = []
    parNum = []
    for li in coeffList :
        if li[0]=='unpolarizedxsec' : 
            print("Warning: hardcoded deg3 for Y unpolarized fit (in the chi2)")
            for qt in range(1, dimQt+1) :
                modelParsC=np.zeros(li[1])
                for yy in range(len(modelParsC)) :
                    modelParsC[yy] = 1.
                modelParsList.append(modelParsC.copy())
                parNum.append(len(modelParsC))
                print(li[0], "qt=",qt, "pars=", parNum[-1])
        else :
            effY = li[1]
            effQt = li[2]
            if li[5] : effY-= 1
            if li[6] : effQt-= 1
            if li[7] : effQt-= 1
            modelParsC=np.zeros((effY,effQt))
            for qt in range(0, effQt) :
                for y in range(0, effY) :
                   modelParsC[y,qt] = 1. 
            modelParsList.append(modelParsC.copy())
            print(li[0], "pars (y,qt)=", effY, effQt)
            parNum.append(effY*effQt)
            modelParsList[-1]=modelParsList[-1].flatten()
    modelPars = np.concatenate(modelParsList) #already flattened, otherwise YOU HAVE TO FLATTEN before pass it to the fit
    
    coeffListJAX = copy.deepcopy(coeffList)
    for li in coeffListJAX :
        if li[0] != 'unpolarizedxsec' : 
            li[0] = coeffListJAX.index(li)-1
        else :
            li[0] = 5
    
    print("everything initialized, minimizer call...")
    # print "initial x=", modelPars
    print("par num", parNum)
    modelPars = pmin(chi2PolyFit, modelPars, args=(npFitRes, npCovMatInv, coeffListJAX, npBinCenters,parNum), doParallel=False)

        
    # after fit results
    static_argnumsPF = (1,2,3,4,5)
    modelChi2Grad_eval = jax.jit(jax.value_and_grad(chi2PolyFit), static_argnums=static_argnumsPF)
    modelHess_eval = jax.jit(jax.hessian(chi2PolyFit), static_argnums=static_argnumsPF)
    
    modelChi2,modelGrad = modelChi2Grad_eval(modelPars, npFitRes, npCovMatInv, coeffListJAX, npBinCenters,parNum)
    modelHess = modelHess_eval(modelPars, npFitRes, npCovMatInv, coeffListJAX, npBinCenters,parNum)
    
    modelCov = 0.5*np.linalg.inv(modelHess)
    modelErr = np.sqrt(np.diag(modelCov))

    modelEDM = 0.5*np.matmul(np.matmul(modelGrad.T,modelCov),modelGrad)
    modelNDOF = dimCoeff*dimQt*dimY- np.size(modelPars)
    
    print("*-------------------------------------------*")
    print("FIT RESULTS")
    print("edm=",modelEDM) 
    print("chi2/dof=", modelChi2,"/",modelNDOF, "=", modelChi2/float(modelNDOF)) 
    print("parameters=", modelPars)
    print("errors=", modelErr)
    print("relative uncertaintiy" , np.true_divide(modelErr,modelPars))
    
    print("check covariance matrix:")
    print("is covariance semi positive definite?", np.all(np.linalg.eigvals(modelCov) >= 0))
    print("is covariance symmetric?", np.allclose(np.transpose(modelCov), modelCov))
    print("is covariance approx symmetric?", np.allclose(np.transpose(modelCov), modelCov, rtol=1e-05, atol=1e-06))
    # np.set_printoptions(threshold=np.inf)
    # print "hessian", modelHess
    # print "diag hessian", np.linalg.eig(modelHess)
    # e, u = np.linalg.eigh(modelHess)
    # print "e0=", e[...,0]
    # e2,u2 = np.linalg.eig(modelHess)
    # print "e0_as=", e2[...,0]
    # # print "sorted", np.sort(e2,1)
    # print "e=",e
    # print "e2=", e2
    # for i in e :
    #     if i<=0 : 
    #         print "e0, i=", i
    # for j in e2 :
    #     if j<=0 : 
    #         print "e0_as, j=", j
    # print "is hessian symmetric?", np.allclose(np.transpose(modelHess), modelHess)
    # print "is hessian approx symmetric?", np.allclose(np.transpose(modelHess), modelHess, rtol=1e-05, atol=1e-06)
    # print "is hessian semi posititive?", np.all(np.linalg.eigvals( modelHess) >= 0)
    print("*-------------------------------------------*")
    

    outFit = (modelPars,modelCov,npFitRes, npBinCenters,parNum)
    
    #DEBUG
    # deb = chi2PolyFit(modelPars, npFitRes, npCovMatInv, coeffListJAX, npBinCenters,parNum)

    
    return outFit



def rebuildPoly(fitPars,histo,npBinCenters,coeffList,parNum) :
    
    dimY = np.shape(histo)[1]
    dimQt = np.shape(histo)[2]
    
    output = np.zeros((len(coeffList),dimY,dimQt))  
    valY = npBinCenters[:,0]
    valQt = npBinCenters[:,1]
    npBinCenters_res = npBinCenters.reshape(dimY,dimQt,2)
    valYunpol=npBinCenters_res[:,0,0]
    # print valYunpol

    icoeff = 0
    ipar=0
    unpolMult=[1e5,1e5]
    for li in coeffList :
        if li[0]=='unpolarizedxsec' :
            for iqt in range(dimQt) :
                # print "binqt=", iqt
                output[0,:,iqt] = unpolMult[0]*fitPars[0+ipar]+unpolMult[1]*fitPars[1+ipar]*valYunpol+unpolMult[1]*fitPars[2+ipar]*np.power(valYunpol,2)#+unpolMult*fitPars[2+ipar]*np.power(valYunpol,4))
                ipar = ipar+parNum[icoeff]
                icoeff+=1
                # print output[0,:,iqt]                     
        else :
            # tempCoeff =np.zeros((dimQt*dimY,1))
            tempCoeff =np.zeros(np.shape(npBinCenters)[0])
            effY = li[1]
            effQt = li[2]
            if li[5] : effY-= 1
            if li[6] : effQt-= 1
            if li[7] : effQt-= 1
            for iqt in range(0, effQt) :
                powQt = iqt
                if li[6] : powQt+= 1 
                if li[7] and li[0]!=4 : powQt+= 1 
                if li[7] and li[0]==4 and iqt>0 : powQt+=1
                for iy in range(0, effY) :
                   powY = iy
                   if li[5] : powY+= 1
                   tempCoeff = tempCoeff+fitPars[iqt*(effY)+iy+ipar]*np.power(valY,powY)*np.power(valQt,powQt) 
            ipar = ipar+parNum[icoeff]
            icoeff+=1       
            output[coeffList.index(li)] = tempCoeff.reshape((dimY,dimQt)) # reshape to (Ny x Nqt), like the fitRes histogram
            
    return output
         
        
    
def errorPoly(fitPars,cov,histo,npBinCenters,coeffList,parNum) :
    ntoys = 10000
    covtoy ={}
    dimY = np.shape(histo)[1]
    dimQt = np.shape(histo)[2]
    
    toyVec = np.zeros((len(coeffList),dimY,dimQt,ntoys))  

    for itoy in range(ntoys) :
        covtoy[itoy] = np.random.multivariate_normal(fitPars, cov)
        toyVec[...,itoy] = rebuildPoly(fitPars=covtoy[itoy],histo=histo,npBinCenters=npBinCenters, coeffList=coeffList,parNum=parNum)
    sigmavec = np.std(toyVec,axis=-1)

    return sigmavec
       
    


# def evaluate_erf_error(self,ERFfitResult, ERFp0,ERFp1, ERFp2) :
#         ntoys = 1000
#         covtoy ={}
#         xvec = np.zeros(len(self.ptBinning)-1)
#         for xx in range(xvec.size) :
#             xvec[xx] = float(self.ptBinning[xx])+float((self.ptBinning[xx+1]-self.ptBinning[xx]))/2
#         yvec = np.zeros((xvec.size,ntoys))
#         parvec=np.zeros(3)
#         parvec[0] = ERFp0
#         parvec[1] = ERFp1
#         parvec[2] = ERFp2
#         covvec =np.zeros((3,3))

#         for xx in range (3) :
#             for yy in range (3) :
#                 covvec[xx][yy] = ROOT.TMatrixDRow(ERFfitResult,xx)(yy)

#         def my_erf(x,par) :
#             val = np.zeros(x.size)
#             val = par[0]*erf(par[1]*(x)+par[2])
#             return val

#         for itoy in range(ntoys) :
#             covtoy[itoy] = np.random.multivariate_normal(parvec, covvec)
#             yvec[:,itoy] = my_erf(xvec,covtoy[itoy])
#         sigmavec = np.std(yvec,axis=1)

#         return sigmavec




# def rebuildFitFunc(fitPars,cov, infoC,extra) :
 
#     interParsList = np.split(modelPars,parNum)
#     funcMatrix = np.zeros((np.shape(npFitRes)[1],np.shape(npFitRes)[2]))
#     matrixBinCenters = np.reshape(extra['binCent'],(np.shape(npFitRes)[1],np.shape(npFitRes)[2],2)) #CHECK ME! 
    
#     if infoC[0]!=5  :
#         interPars = interParsList[infoC[0]+np.shape(npFitRes)[2]].copy()
                    
#         if infoC[5] :
#             ylist = list(interPars)
#             for iy in range(infoC[1]) :
#                 for iqt in range(infoC[2]) :
#                     itot = iqt*(infoC[1])+iy
#                     if iy==infoC[1]-1 :
#                         ylist.insert(itot, 0.)
#             interPars = np.asarray(ylist)
            
#         if infoC[6] :
#             qtlist = list(interPars)
#             for iy in range(infoC[1]) :
#                 for iqt in range(infoC[2]) :
#                     itot = iqt*(infoC[1])+iy
#                     if iy==infoC[2]-1 :
#                         qtlist.insert(itot, 0.)
#             interPars = np.asarray(qtlist)
                    
#         if infoC[5] : #contraint on y=0
#             for iqt in range(infoC[2]) :
#                 itot = iqt*(infoC[1])+infoC[1]
#                 constr = 0.0
#                 for k in range(0, infoC[1]-1): 
#                     constr += np.power(-1., infoC[1]+k+1)*parsCoeffList[-1][iqt*infoC[1]+k]
#                 interPars[itot] = constr
                
#         if infoC[6] : #costraint on qt=0
#             for iy in range(infoC[1]):
#                 itot = infoC[2]*(infoC[1])+iy
#                 constr = 0.0
#                 for k in range(0, infoC[2]-1): 
#                     constr += np.power(-1., infoC[2]+k+1)*parsCoeffList[-1][ k*infoC[1]+iy]
#                 interPars[itot] = constr  
                            
#         for iy in range(infoC[1]) :
#             for iqt in range(infoC[2]) :
#                 itot = iqt*(infoC[1])+iy
#                 funcMatrix[:,:]+= interPars[itot]*scipy.special.eval_chebyt(iy, matrixBinCenters[:,:,0])*scipy.special.eval_chebyt(iqt,matrixBinCenters[:,:,1]) 
        
#     else : #unpol 
#         interPars = interParsList[:np.shape(npFitRes)[2]].copy()

#         for iqt in range(np.shape(npFitRes)[2]) :
#             clist = list(interPars[iqt])
#             for iy in range(infoC[1]) :
#                 if iy%2!=0 :
#                     clist.insert(iy, 0.)       
#             interPars[iqt] = np.asarray(clist)
        
#         # for interPars_qt in interPars :
    
#         for iy in range(infoC[1]) : #contraint on odd degrees
#             if iy%2!=0 :
#                 for iqt in range(np.shape(npFitRes)[2]) : #binQt
#                     interPars[iqt][iy] = 0.
                    
#         for iy in range(infoC[1]) :
#             for iqt in range(np.shape(npFitRes)[2]) : #binQt
#                 funcMatrix[:,:]+= interPars[iqt][iy]*scipy.special.eval_chebyt(iy, (matrixBinCenters[:,:,0]+1)/2)
    
#     xx = array('f', extra['binY'])
#     yy = array('f', extra['binQt'])
#     histo = ROOT.TH2("hPostRegFit"+infoC[0],"hPostRegFit"+infoC[0],len(xx)-1, xx, len(yy)-1, yy )
#     for iy in binY :
#         for iq in binQt :
#             histo.SetBinContent(iy,iqt, funcMatrix[iy,iqt])
#     return chi2   
   
    
    
def plotterPostReg(fitResult, output, save, coeffList,histo) :
    
    #build the error vector
    funcVec = rebuildPoly(fitPars=fitResult[0],histo=fitResult[2],npBinCenters=fitResult[3], coeffList=coeffList,parNum=fitResult[4])
    
    #build the function vector
    errorVec = errorPoly(fitPars=fitResult[0],cov=fitResult[1],histo=fitResult[2],npBinCenters=fitResult[3], coeffList=coeffList,parNum=fitResult[4])
    
    outFile = ROOT.TFile(output+".root", "recreate")
    for li in coeffList :
        h = histo[li[0]].Clone("post-fit-regularization_"+li[0])
        for y in range(1, h.GetNbinsX()+1) :
            for qt in range(1, h.GetNbinsY()+1) : 
                h.SetBinContent(y,qt,funcVec[coeffList.index(li)][y-1][qt-1])  
                h.SetBinError(y,qt,errorVec[coeffList.index(li)][y-1][qt-1])  
        outFile.cd()
        h.Write()
        
        
    


parser = argparse.ArgumentParser("")

parser.add_argument('-o','--output', type=str, default='aposterioriFit',help="name of the output file")
parser.add_argument('-f','--fitInput', type=str, default='fitResult.root',help="name of the fit result root file, after plotter_fitResult")
parser.add_argument('-r','--regInput', type=str, default='../../regularization/OUTPUT_poly/regularizationFit_range11_rebuild____nom_nom.root',help="name of the regularization study result root file")
parser.add_argument('-s','--save', type=int, default=False,help="save .png and .pdf canvas")

args = parser.parse_args()
OUTPUT = args.output
FITINPUT = args.fitInput
REGINPUT = args.regInput
SAVE= args.save

coeffList = []#y plus, qt plus, y minus, qt minus, constraint y, constraint qt,constrain C1
# coeffList.append(['unpolarizedxsec', 3,3])
# coeffList.append(['A0', 3,4,3,4, 0,1])
# coeffList.append(['A1', 3,5,5,4, 1,1])
# coeffList.append(['A2', 2,4,3,3, 0,1])
# coeffList.append(['A3', 4,4,5,4, 1,1])
# coeffList.append(['A4', 6,4,6,4, 1,0])

coeffList.append(['unpolarizedxsec', 3,3,-999,-999,0,0,0])
coeffList.append(['A0', 3,4,3,4, 0,1,1])
coeffList.append(['A1', 4,4,3,4, 1,1,0])
coeffList.append(['A2', 2,5,2,4, 0,1,1])
coeffList.append(['A3', 3,4,3,3, 0,1,0])
coeffList.append(['A4', 4,5,4,6, 1,0,0]) #5-->7 but no convergence! and last number=1

# parPerCoeff(coeffList=coeffList) #add number of free par per coeff to coeffList
fitResDict = getFitRes(inFile=FITINPUT, coeffList=coeffList)
regFuncDict = getRegFunc(inFile=REGINPUT, coeffList=coeffList)
# fitPostRegResult = fitPostReg(fitRes=fitResDict, regFunc=regFuncDict, coeffList=coeffList)
fitPostRegResult = polyFit(fitRes=fitResDict, regFunc=regFuncDict, coeffList=coeffList)
plotterPostReg(fitResult = fitPostRegResult, output=OUTPUT,save=SAVE, coeffList=coeffList,histo=fitResDict)




 
