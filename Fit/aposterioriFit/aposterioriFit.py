import ROOT
from array import array
import math
import copy
import argparse
import os
import numpy as np 
from obsminimization import pmin
import root_numpy as rootnp



#def of the chi2
def chi2LBins(x, binScaleSq, binSigmaSq, hScaleSqSigmaSq, etas,*args):
https://github.com/emanca/scipy-MuCal/blob/master/fittingFunctionsBinned.py#L223
scaleSqSigmaSqModel / scaleSqBinned --> mia funzione di fit 
scaleSqSigmaSqBinned / sigmaSqBinned --> valore parametri  
hScaleSqSigmaSq-->cov matrix inverse, hessian 


scaleSqBinned --> binScaleSq --> scaleSqSigmaSqBinned --> parametri? -->valori della grid in uscita dal fit
sigmaSqBinned --> binSigmaSq --> scaleSqSigmaSqBinned --> parametri?
NULLA         --> scaleSqSigmaSqModel --> funzione?
hScaleSqSigmaSqBinned / hScaleSqSigmaSq 


# coeffDict = { #y plus, qt plus, y minus, qt minus, constraint y, constraint qt
#     'A0' :[2,3,2,3, VINCOLI],
#     'A1' :[5,4,5,4, ],
#     'A2' :[2,3,2,3, ],
#     'A3' :[4,3,4,3, ],
#     'A4' :[5,3,5,3, ],
#     'unpolarizedxsec':[3,3]
# }

def countPar(ny,nqt,ky,kqt) :
        Npar=ny*nqt
        if kqt :
            Npar-= ny
        if ky :
            Npar-= nqt
        if kqt and ky :
            Npar+=1 #the overlap between previous two loop
        return Npar 
            
def parPerCoeff(coeffList) :
    for li in coeffList :
        if li[0]!='unpolarizedxsec' : 
            NparPlus = countPar(li[1],li[2],li[5],li[6])
            NparMinus = countPar(li[3],li[4],li[5],li[6])
        else :
            NparPlus = li[1]/2
            NparMinus = li[1]/2
            if li[1]%2!=0 :
                NparPlus = NparPlus+=1
            if li[2]%2!=0 :
                NparMinus = NparMinus+=1
        coeffList[coeffList.index(li)].append(NparPlus)
        coeffList[coeffList.index(li)].append(NparMinus)    
        
        
def getFitRes(inFile, coeffList) :
    outDict = {}
    for li in coeffList :
        outDict[li[0]] = inFile.Get('coeff2D_reco/recoFitAC'+li[0])
    outDict['cov']=inFile.Get('matrices_reco/covariance_matix_channelhelpois')
    return outDict 
    
def getRegFunc(inFile, coeffList) :
    outDict = {}
    for li in coeffList :
        if li[0]!='unpolarizedxsec' : 
            outDict[li[0]] = inFile.Get('Y'+str(li[1])+'_Qt'+str(li[2])+'/hfit_WToMuP_'+li[0]+'_'+str(li[1])+str(li[2]))
        else :
            temph = inFile.Get('unpol_Y3/hfit_WToMuP_unpol_3_1')
            for qt in range(1, temph.GetNBinsX()+1) :
                outDict[c+str(qt)] = inFile.Get('unpol_'+str(li[1])+'/hfit_WToMuP_unpol_3_'+qt)
            print "WARNING: unpolarized qt binning must be aligned to the fit!"
    return outDict

     
def chi2PostReg(modelPars,npFitRes, npCovMatInv, coeffList, npBinCenters,parNum) :
    
    # 1) prodotto di flatten parametri (per ogni coeff separato) * griglia di 1,0 in base a coefficiente
    # 2) applico vincoli con operazioni di slicing per ogni coefficiente
    # 3) flatteno tutto
    
    # modelPars.reshape()#messo in forma sensata per il building (oppure no?)
    # buildfunc(modelParsReshaped) #costruisi la funzione usando i parametri
    # flatten(buildfunc)#allinea struttura di invcov e npFitRes
    
    interPars = modelPars.copy()
    interPars = np.split(interPars,parNum)
    
    fitModelList = []
    for li in coeffList :
        # parsTotCoeff = np.zeros(li[1]*li[2])
        # for iqt in range(li[2]) :
        #         for iy in range(li[1]) :
        #             parsTotCoeff
        
        fitModelC = np.zeros(np.shape(npBinCenters)[0]) # list of  (y,qt), with lenght (Ny*Nqt) 

        if li[0]!='unpolarizedxsec' : 
            parsCoeff = interPars[coeffList.index[li]]

            if li[5] : #contraint on y=0
                for iqt in range(li[2]) :
                    itot = iqt*(li[1])+li[1]
                    constr = 0.0
                    for k in range(0, li[1]-1): 
                        constr += np.power(-1., li[1]+k+1)*parsCoeff[iqt*li[1]+k]
                    parsCoeff[itot] = constr
                    
            if li[6] : #contraint on qt=0
                for iy in range(li[1]):
                    itot = iqt*(li[1])+iy
                    constr = 0.0
                    for k in range(0, li[2]-1): 
                        constr += np.power(-1., li[2]+k+1)*parsCoeff[ k*li[1]+iy]
                    parsCoeff[itot] = constr 
            
            for iy in range(li[1]) :
                for iqt in range(li[2]) :
                    itot = iqt*(li[1])+iy
                    fitModelC += parsCoeff[itot]*scipy.special.eval_chebyt(iy, npBinCenters[:,0])*scipy.special.eval_chebyt(iqt,npBinCenters[:,1]) 
        
        else : #unpol
            parsCoeff = interPars[coeffList.index[li]:]
            
            for iy in range(li[1]) : #contraint on odd degrees
                if iy%2!=0 :
                    for iqt in range(np.shape(npFitRes)[2]) : #binQt
                        parsCoeff[iqt][iy] = 0
                        
            for iy in range(li[1]) :
                for iqt in range(np.shape(npFitRes)[2]) : #binQt
                    fitModelC += parsCoeff[iqt][iy]*scipy.special.eval_chebyt(iy,npBinsCenters[:0]) 


        fitModelC.reshape(np.shape(npFitRes)[1],np.shape(npFitRes)[2]) # reshape to (Ny x Nqt), like the fitRes histogram
        fitModelList.append(fitModelC.copy())
        
    fitModel = np.stack(fitModelList,0)
 
    diff = npFitRes-fitModel
    diff = diff.flatten() #check that the order is the same of invCov! 
    chi2 = np.linalg.multi_dot( [diff.T, invCov, diff] )
    return chi2
    

# def fitPostRegBACKUP(fitRes,regFunc, coeffList) :
    
#     #prepare fitRes
#     # dimFlat= fitRes['cov'].getNbinsX()
#     dimY = outDict['A0'].GetNbinsX()
#     dimQt = outDict['A0'].GetNbinsY()
#     # dimC = 5
    
#     npCovMat = rootnp.hist2array(fitRes['cov'])
#     npCovMat = npCovMat[:-1,:-1] #remove mass
#     npCovMatInv = np.linalg.inv(npCovMat)
    
    
#     #build the bin centers list

#     binY,binQt = [], []
#     for i in range(1, dimY+1):  binY.append( 2*(fitRes['A0'].GetXaxis().GetBinCenter(i)- 0.)/(fitRes['A0'].GetXaxis().GetBinLowerEdge(dimY+1)-0.) - 1.) #range between -1,1
#     for i in range(1, dimQt+1): binQt.append( 2*(fitRes['A0'].GetYaxis().GetBinCenter(i)- 0.)/(fitRes['A0'].GetYAxis().GetBinLowerEdge(dimQt+1)-0.) - 1.) #range between -1,1 
#     xx = array('f', binY)
#     yy = array('f', binQt)
    
#     npBinCenters = np.zeros(binY*binQt,2)
            
#     hreb = ROOT.TH2F('hreb'+c, 'hreb'+c, len(xx)-1, xx, len(yy)-1, yy)
#     for i in range(1, hreb.GetXaxis().GetNbins()+1): #y
#         for j in range(1, hreb.GetYaxis().GetNbins()+1):#qt
#             npBinCenters[(i-1)*(j-1)] = hreb.GetXaxis().GetBinCenter(i), hreb.GetYaxis().GetBinCenter(j)
            
    
#     npFitResList = []
#     for li in coeffList :   
#         #         hreb.SetBinContent(i,j, fitRes[c].GetBinContent(i,j) )
#         #         hreb.SetBinError(i,j, fitRes[c].GetBinError(i,j) )        
#         # npFitResList.append(rootnp.hist2array(hreb))
        
#         npFitResList.append(rootnp.hist2array(fitRes[li[0]])) #consider that the bin edges --> xx,yy
#     npFitRes = np.stack(npFitResList,0)  #dimensions: coeff, y, qt
    
    
#     #model init
#     modelParsList = []
#     parNum = []
#     for li in coeffList :
#         if li[0]!='unpolarizedxsec' : 
#             func = regFunc[li[0]].GetFunction('fit_WtoMuP_'+li[0])
#             # modelParsC=np.zeros(func.GetNpar())
#             modelParsC=np.zeros(li[7])
#             for iy in range(li[1]) :
#                 for iqt in range(li[2]) :
#                     itot = iqt*(len(self.id_y))+iy #depend not on this loop but on the ROOT par number assigment
#                     if li[5] and iy==li[1] : continue
#                     if li[6] and iqt==li[2] : continue
#                     par = ctypes.c_double(0.)
#                     func.GetParameter(itot,par)
#                     modelParsC[itot] = func.value
#             modelParsList.append(modelParsC.copy())
#         else :
#             for qt in range(1, dimQt.GetNBinsX()+1) :
#                 func = outDict[c+str(qt)].GetFunction('fit_WtoMuP_unpol')
#                 # modelParsC=np.zeros(func.GetNpar())
#                 modelParsC=np.zeros(li[7])
#                 for i in range(0,func.GetNpar()) : 
#                     if i%2!=0 : continue 
#                     par = ctypes.c_double(0.)
#                     func.GetParameter(i,par)
#                     modelParsC[i] = func.value
#                 modelParsList.append(modelParsC.copy())
#         if len(parNum) >0 :
#             parNum.append(li[7]+parNum[-1])
#         else :
#             parNum.append(li[7])
    
#     # modelPars = np.stack(modelParsList,0) 
#     modelPars = np.concatenate(modelParsList) #already flat
    
    
#     #call of the minimizer, 
#     modelPars = pmin(chi2PostReg, modelPars.flatten(), args=(npFitRes, npCovMatInv, coeffDict, npBinCenters,parNum), doParallel=False)


def fitPostReg(fitRes,regFunc, coeffList) :
    
    #prepare fitRes
    # dimFlat= fitRes['cov'].getNbinsX()
    dimY = fitRes['A0'].GetNbinsX()
    dimQt = fitRes['A0'].GetNbinsY()
    # dimC = 5
    
    npCovMat = rootnp.hist2array(fitRes['cov'])
    npCovMat = npCovMat[:-1,:-1] #remove mass
    npCovMatInv = np.linalg.inv(npCovMat)
    
    
    #build the bin centers list

    binY,binQt = [], []
    for i in range(1, dimY+1):  binY.append( 2*(fitRes['A0'].GetXaxis().GetBinCenter(i)- 0.)/(fitRes['A0'].GetXaxis().GetBinLowerEdge(dimY+1)-0.) - 1.) #range between -1,1
    for i in range(1, dimQt+1): binQt.append( 2*(fitRes['A0'].GetYaxis().GetBinCenter(i)- 0.)/(fitRes['A0'].GetYAxis().GetBinLowerEdge(dimQt+1)-0.) - 1.) #range between -1,1 
    xx = array('f', binY)
    yy = array('f', binQt)
    
    npBinCenters = np.zeros(binY*binQt,2)
            
    hreb = ROOT.TH2F('hreb'+c, 'hreb'+c, len(xx)-1, xx, len(yy)-1, yy)
    for i in range(1, hreb.GetXaxis().GetNbins()+1): #y
        for j in range(1, hreb.GetYaxis().GetNbins()+1):#qt
            npBinCenters[(i-1)*(j-1)] = hreb.GetXaxis().GetBinCenter(i), hreb.GetYaxis().GetBinCenter(j)
            
    
    npFitResList = []
    for li in coeffList :   
        #         hreb.SetBinContent(i,j, fitRes[c].GetBinContent(i,j) )
        #         hreb.SetBinError(i,j, fitRes[c].GetBinError(i,j) )        
        # npFitResList.append(rootnp.hist2array(hreb))
        
        npFitResList.append(rootnp.hist2array(fitRes[li[0]])) #consider that the bin edges --> xx,yy
    npFitRes = np.stack(npFitResList,0)  #dimensions: coeff, y, qt
    
    
    #model init
    modelParsList = []
    parNum = []
    for li in coeffList :
        if li[0]!='unpolarizedxsec' : 
            func = regFunc[li[0]].GetFunction('fit_WtoMuP_'+li[0])
            modelParsC=np.zeros(func.GetNpar())
            for i in range(func.GetNpar()) :
                par = ctypes.c_double(0.)
                func.GetParameter(i,par)
                modelParsC[itot] = func.value
            modelParsList.append(modelParsC.copy())
            
            if len(parNum) >0 :
                parNum.append(li[1]*li[2]+parNum[-1])
            else :
                parNum.append(li[1]*li[2])
        else :
            for qt in range(1, dimregFunc[c+str(qt)].Qt.GetNBinsX()+1) :
                if qt%2==0 : continue # to allign skipped one bin every two the binning: quite bad approach, but it's relevant for init. val. only
                func = regFunc[c+str(qt)].GetFunction('fit_WtoMuP_unpol')
                # modelParsC=np.zeros(func.GetNpar())
                for i in range(func.GetNpar()) :
                    par = ctypes.c_double(0.)
                    func.GetParameter(i,par)
                    modelParsC[i] = func.value
                modelParsList.append(modelParsC.copy())
                parNum.append(li[1]+parNum[-1])

    # modelPars = np.stack(modelParsList,0) 
    modelPars = np.concatenate(modelParsList) #already flat
    
    
    #call of the minimizer, 
    modelPars = pmin(chi2PostReg, modelPars.flatten(), args=(npFitRes, npCovMatInv, coeffDict, npBinCenters,parNum), doParallel=False)





parser = argparse.ArgumentParser("")

parser.add_argument('-o','--output', type=str, default='fitResult',help="name of the output file")
parser.add_argument('-f','--fitInput', type=str, default='fitResult.root',help="name of the fit result root file, after plotter_fitResult")
parser.add_argument('-r','--regInput', type=str, default='../regularization/TEST_syst/regularizationFit_range11____nom_nom.root .root',help="name of the regularization study result root file")
parser.add_argument('-s','--save', type=int, default=False,help="save .png and .pdf canvas")

args = parser.parse_args()
OUTPUT = args.output
FITINPUT = args.fitInput
REGINPUT = args.regInput
SAVE= args.save

coeffList = []#y plus, qt plus, y minus, qt minus, constraint y, constraint qt
coeffList.append(['A0', 2,3,2,3, 0,1])
coeffList.append(['A1', 5,4,5,4, 1,1])
coeffList.append(['A2', 2,3,2,3, 0,1])
coeffList.append(['A3', 4,3,4,3, 1,1])
coeffList.append(['A4', 5,3,5,3, 1,0])
coeffList.append(['unpolarizedxsec', 3,3])

parPerCoeff(coeffList=coeffList) #add number of free par per coeff to coeffList
fitResDict = getFitRes(inFile=FITINPUT, coeffList=coeffList)
regFuncDict = getRegFunc(inFile=REGINPUT, coeffList=coeffList)
QUALCOSA = fitPostReg(fitRes=fitResDict, regFunc=regFuncDict, coeffList=coeffList)




 
