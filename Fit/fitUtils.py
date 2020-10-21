import ROOT
import pickle
from termcolor import colored
import math
from HiggsAnalysis.CombinedLimit.DatacardParser import *
from collections import OrderedDict
import copy
from systToapply import systematicsDict

class fitUtils:
    def __init__(self, fmap, channel ="WPlus", doSyst=False):
        
        self.doSyst = doSyst
        self.processes = []
        self.signals = []

        #combine utils
        self.channel = channel
        self.shapeMap = {}
        self.helGroups = OrderedDict()
        self.sumGroups = OrderedDict()
        self.helMetaGroups = OrderedDict()
        
        self.templSystematics = systematicsDict

        #all the files that are needed
        self.fmap = ROOT.TFile.Open(fmap) #file containing the angular coefficient values and inclusive pt-y map
        #get the inclusive pt-y map to unfold
        self.imap = self.fmap.Get("accMaps/mapTot")
        self.xsec = self.fmap.Get("accMaps/sumw")
        #just a bunch of useful factors
        self.factors = {}
        self.factors["A0"] = 2.
        self.factors["A1"] = 2.*math.sqrt(2)
        self.factors["A2"] = 4.
        self.factors["A3"] = 4.*math.sqrt(2)
        self.factors["A4"] = 2.
        self.factors["A5"] = 2.
        self.factors["A6"] = 2.*math.sqrt(2)
        self.factors["A7"] = 4.*math.sqrt(2)

        self.helXsecs = OrderedDict()
        self.helXsecs["L"] = "A0"
        self.helXsecs["I"] = "A1"
        self.helXsecs["T"] = "A2"
        self.helXsecs["A"] = "A3"
        self.helXsecs["P"] = "A4"
        self.helXsecs["7"] = "A5"
        self.helXsecs["8"] = "A6"
        self.helXsecs["9"] = "A7"
        self.helXsecs["UL"] = "AUL"
    def fillProcessList(self):
        for hel in self.helXsecs:
            for i in range(1,7): #binsY
                for j in range(1,9): #binsPt
                    proc = 'helXsecs' + hel + '_y_{}'.format(i)+'_qt_{}'.format(j)
                    self.processes.append(proc)
                    if not "helXsecs7" in proc and not "helXsecs8" in proc and not "helXsecs9" in proc:
                        self.signals.append(proc)
        #bkg_list = ["DY","Diboson","Top","Fake","Tau","LowAcc"]
        bkg_list = ["LowAcc"]
        self.processes.extend(bkg_list)
    def shapeFile(self):

        shapeOutxsec = ROOT.TFile(self.channel+'_xsec.root', 'recreate')

        self.xsec.Scale(61526.7*1000.) #xsec in fb
        self.xsec.Write()
        
        for proc in self.processes:
            if proc in self.signals: #give the correct xsec to unfold
                
                iY = int(proc.split('_')[2])
                iQt = int(proc.split('_')[4])
                coeff = proc.split('_')[0].replace('helXsecs','')

                tmp = ROOT.TH1D(proc,proc, 1, 0., 1.)
                cont = self.xsec.GetBinContent(iY,iQt)
                tmp.SetBinContent(1, cont)
                nsum = (3./16./math.pi)
                
                if not "UL" in proc: #rescale for the releative xsec
                    hAC = self.fmap.Get("angularCoefficients/harmonics{}_nom_nom".format(self.helXsecs[coeff]))
                    nsum = nsum*hAC.GetBinContent(iY,iQt)/self.factors[self.helXsecs[coeff]]
                tmp.Scale(nsum)
                shapeOutxsec.cd()
                tmp.Write()
            else:
                tmp = ROOT.TH1D(proc, proc, 1, 0.,1.)
                if proc == "data_obs": tmp.SetBinContent(1, 1.)
                else: tmp.SetBinContent(1, 0.)
                shapeOutxsec.cd()
                tmp.Write()
    def fillHelGroup(self):

        for i in range(1, self.imap.GetNbinsX()+1):
            for j in range(1, self.imap.GetNbinsY()+1):

                s = 'y_{i}_qt_{j}'.format(i=i,j=j)
                self.helGroups[s] = []
                
                for hel in self.helXsecs:
                    if 'helXsecs'+hel+'_'+s in self.signals:

                        self.helGroups[s].append('helXsecs'+hel+'_'+s)
                                
                if self.helGroups[s] == []:
                    del self.helGroups[s]
    def fillHelMetaGroup(self):

        for i in range(1, 7):
            s = 'y_{i}'.format(i=i)
            self.helMetaGroups[s] = []
            for key in self.sumGroups:
                if s in key:
                    self.helMetaGroups[s].append(key)
            
            if self.helMetaGroups[s] == []:
                    del self.helMetaGroups[s]
        
        for j in range(1, 9):
            s = 'qt_{j}'.format(j=j)
            self.helMetaGroups[s] = []
            for key in self.sumGroups:
                if 'qt' in key and key.split('_')[2]==str(j):
                    self.helMetaGroups[s].append(key)
        
            if self.helMetaGroups[s] == []:
                    del self.helMetaGroups[s]
        #print self.helMetaGroups
    def fillSumGroup(self):

        for i in range(1, 7):
            s = 'y_{i}'.format(i=i)
            for hel in self.helXsecs:
                for signal in self.signals:
                    if 'helXsecs'+hel+'_'+s in signal:
                        self.sumGroups['helXsecs'+hel+'_'+s] = []
                        for j in range(1, 9):
                            if 'helXsecs'+hel+'_'+'y_{i}_qt_{j}'.format(i=i,j=j) in self.signals:
                                self.sumGroups['helXsecs'+hel+'_'+s].append('helXsecs'+hel+'_'+s+'_qt_{j}'.format(j=j))
        
        for j in range(1, 9):
            s = 'qt_{j}'.format(j=j)
            for hel in self.helXsecs:
                for signal in self.signals:
                    if signal.split('_')[0] == 'helXsecs'+hel and signal.split('_')[4] == str(j):
                        self.sumGroups['helXsecs'+hel+'_'+s] = []
                        for i in range(1, 7):
                            if 'helXsecs'+hel+'_'+'y_{i}_qt_{j}'.format(i=i,j=j) in self.signals:
                            #print i, signal, 'helXsecs'+hel+'_'+'y_{i}_pt_{j}'.format(i=i,j=j)
                            #print 'append', 'helXsecs'+hel+'_y_{i}_'.format(i=i)+s, 'to', 'helXsecs'+hel+'_'+s
                                self.sumGroups['helXsecs'+hel+'_'+s].append('helXsecs'+hel+'_y_{i}_'.format(i=i)+s)
        #print self.sumGroups
    def makeDatacard(self):

        self.DC = Datacard()

        ############## Setup the datacard (must be filled in) ###########################

        self.DC.bins =   [self.channel, self.channel+'_xsec'] # <type 'list'>
        self.DC.obs =    {} # <type 'dict'>
        self.DC.processes =  self.processes # <type 'list'>
        self.DC.signals =    self.signals # <type 'list'>
        self.DC.isSignal =   {} # <type 'dict'>
        for proc in self.processes:
            if proc in self.signals:
                self.DC.isSignal[proc] = True
            else:
                self.DC.isSignal[proc] = False
        self.DC.keyline = [] # <type 'list'> # not used by combine-tf
        self.DC.exp =    {} # <type 'dict'>
        self.DC.exp[self.channel] = {}
        self.DC.exp[self.channel+'_xsec'] = {}
        for proc in self.processes:
            self.DC.exp[self.channel][proc] = -1.00
            self.DC.exp[self.channel+'_xsec'][proc] = -1.00
        self.DC.systs =  [] # <type 'list'>
        ## list of [{bin : {process : [input file, path to shape, path to shape for uncertainty]}}]
        if self.doSyst:
            for syst in self.templSystematics: #loop over systematics
                if 'Nominal' in syst: continue
                for var in self.templSystematics[syst]["vars"]:
                    aux = {} #each sys will have a separate aux dict
                    aux[self.channel] = {}
                    aux[self.channel+'_xsec'] = {}
                    for proc in self.processes: 
                        if proc in self.templSystematics[syst]["procs"]:
                            aux[self.channel][proc] = 1.0
                            aux[self.channel+'_xsec'][proc] = 0.0
                        else:
                            if "Signal" in self.templSystematics[syst]["procs"] and "hel" in proc:
                                aux[self.channel][proc] = 1.0
                                aux[self.channel+'_xsec'][proc] = 0.0
                            else:
                                aux[self.channel][proc] = 0.0
                                aux[self.channel+'_xsec'][proc] = 0.0

                    self.DC.systs.append((var, False, self.templSystematics[syst]["type"], [], aux))
        
        self.DC.groups = {'mass': ['mass'], 
                          'pdfs': set(['LHEPdfWeightHess{}'.format(i+1) for i in range(60)]),
                          'alphaS': ['alphaS'],
                          'WHSFStat': set(["WHSFSyst0Eta{}".format(i) for i in range(1, 49)]+["WHSFSyst1Eta{}".format(i) for i in range(1, 49)]+["WHSFSyst2Eta{}".format(i) for i in range(1, 49)]),
                          'WHSFSyst': ['WHSFSystFlat']}  # <type 'dict'>
        
        self.DC.shapeMap = 	{self.channel: {'*': [self.channel+'.root', '$PROCESS', '$PROCESS_$SYSTEMATIC']},\
        self.channel+'_xsec': {'*': [self.channel+'_xsec.root', '$PROCESS', '$PROCESS_$SYSTEMATIC']}} # <type 'dict'>
        self.DC.hasShapes =  True # <type 'bool'>
        self.DC.flatParamNuisances =  {} # <type 'dict'>
        self.DC.rateParams =  {} # <type 'dict'>
        self.DC.extArgs =    {} # <type 'dict'>
        self.DC.rateParamsOrder  =  set([]) # <type 'set'>
        self.DC.frozenNuisances  =  set([]) # <type 'set'>
        self.DC.systematicsShapeMap =  {} # <type 'dict'>
        self.DC.nuisanceEditLines    =  [] # <type 'list'>
        self.DC.discretes    =  [] # <type 'list'>
        self.DC.helGroups = self.helGroups
        self.DC.sumGroups = self.sumGroups
        self.DC.helMetaGroups = self.helMetaGroups
        self.DC.noiGroups = {'mass':['mass']}

        filehandler = open('{}.pkl'.format(self.channel), 'w')
        pickle.dump(self.DC, filehandler)
