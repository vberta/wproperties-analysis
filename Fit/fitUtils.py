import ROOT
import pickle
from termcolor import colored
import math
from HiggsAnalysis.CombinedLimit.DatacardParser import *
from collections import OrderedDict

class fitUtils:
	def __init__(self, ftemplates, fmap, fbkg):

		self.ftemplates = ROOT.TFile.Open(ftemplates) #file containing the N-dimensional templates
        self.fmap = ROOT.TFile.Open(fmap) #file containing the angular coefficient values and inclusive pt-y map
        self.fbkg = ROOT.TFile.Open(fbkg) #file containing bkg templates (may be the same as the signal one in the future)
		
        #get a list of the 3D templates
        self.templates3D = []
        for key in self.ftemplates.Get('templates').GetListOfKeys():
            if not 'TH3' in key.GetClassName(): continue
            print key.GetName()
            self.templates3D.append(self.ftemplates.Get('templates').Get(key.GetName()))
        
        #get the inclusive pt-y map
        self.imap = ROOT.TH2D
        self.imap = self.fmap.Get("mapTot")
        #use this histogram to check that histograms are correctly normalised
        self.closure = ROOT.TH2D("clos", "clos", self.imap.GetXaxis().GetNbins(),self.imap.GetXaxis().GetXbins().GetArray(),self.imap.GetYaxis().GetNbins(),self.imap.GetYaxis().GetXbins().GetArray())

        #organise the projected templates into helXsecs
        self.templates2D = {}
        self.clist = ["L", "I", "T", "A", "P", "7", "8", "9", "UL"]
            for c in self.clist:
                self.templates2D[c] = []
        #add low acceptance templates
        self.templates2D["lowAcc"] = self.ftemplates.Get('dataObs').Get('lowAcc')
        #add bkg templates
        self.templates2D["DY"] = self.fbkg.Get('templates').Get("DY")
        #add data
        self.templates2D["data_obs"] = self.ftemplates.Get('dataObs').Get('data_obs')

        #just a bunch of useful factors
        self.factors = {}
        self.factors["A0"]= 2.
        self.factors["A1"]=2.*math.sqrt(2)
        self.factors["A2"]=4.
        self.factors["A3"]=4.*math.sqrt(2)
        self.factors["A4"]=2.
        self.factors["A5"]=2.
        self.factors["A6"]=2.*math.sqrt(2)
        self.factors["A7"]=4.*math.sqrt(2)

        self.helXsecs["L"] = "A0"
        self.helXsecs["I"] = "A1" 
        self.helXsecs["T"] = "A2" 
        self.helXsecs["A"] = "A3" 
        self.helXsecs["P"] = "A4" 
        self.helXsecs["7"] = "A5" 
        self.helXsecs["8"] = "A6" 
        self.helXsecs["9"] = "A7" 
        self.helXsecs["UL"] = "AUL" 
        
        #combine utils
        self.shapeFile='testbkg'
        self.processes = []
		self.signals = []
		self.shapeMap = {}
        self.helGroups = OrderedDict()

    def project3Dto2D(self):
		# returns a list of th2 ordered by rapidity bin
        for th3 in self.templates3D:
            th3.Sumw2()
		
		    for ibin in range(1, th3.GetNbinsZ()+1):

			    lowEdgeY = th3.GetZaxis().GetBinLowEdge(ibin)
			    upEdgeY = th3.GetZaxis().GetBinUpEdge(ibin)

			    th3.GetZaxis().SetRange(ibin, ibin)
			    proj = th3.Project3D("y_{ibin}_yxe".format(ibin=ibin))
                
                name = proj.GetName()
                name = name.replace('_yx', '')
                
                coeff = name.split('_')[3]
                jbin = int(name.split('_')[1])
                ibin = int(name.split('_')[5])
                
                new = 'helXsecs_'+coeff+'_y_{}'.format(ibin)+'_pt_{}'.format(jbin)
                
                proj.SetName(new)

                if proj.Integral()==0.0: #debug line
                    print colored(proj.GetName(),'red')
                    continue 

                coeff = name.split('_')[3]
                self.templates2D[coeff].append(proj)
                
	def unrollTemplates(self):
		# returns a th1 out of a th2
  
        for kind,templList in self.templates2D.iteritems()
            for templ in templList:
		        nbins = (templ.GetNbinsX()+2)*(templ.GetNbinsY()+2)
		        templ.Sumw2()
                new = templ.GetName()
                old = new + '_roll'
                templ.SetName(old)
   
                unrolledtempl = ROOT.TH1F(new, '', nbins, 0., nbins)
		
		        for ibin in range(0, templ.GetNbinsX()+2):
			        for ybin in range(0, templ.GetNbinsY()+2):
				
				        bin1D = templ.GetBin(ibin,ybin)
				        unrolledtempl.SetBinContent(bin1D, templ.GetBinContent(ibin,ybin))
				        unrolledtempl.SetBinError(bin1D, templ.GetBinError(ibin,ybin))

                self.processes.append(unrolledtempl.GetName())
                if kind in self.clist:
                    self.normTempl(unrolledtempl)
                    if not "helXsecs_7" in unrolledtempl.GetName() and not "helXsecs_8" in unrolledtempl.GetName() and not "helXsecs_9" in unrolledtempl.GetName() and not unrolledtempl.Integral() == 0.0:
                        self.signals.append(unrolledtempl.GetName())
                
                shapeOut = ROOT.TFile(self.shapeFile+'.root', 'recreate')
                shapeOut.cd()
                unrolledtempl.Write()

    def normTempl(self, t):

        name = t.GetName()
        coeff = name.split('_')[1]
        jbin = int(name.split('_')[5])
        ibin = int(name.split('_')[3])

        nsum = (3./16./math.pi)*self.imap.GetBinContent(ibin,jbin)

        if not "UL" in coeff:
            hAC = ROOT.TH2D
            hAC = self.fmap.Get("harmonics{}".format(self.helXsecs[coeff]))
            nsum = nsum*hAC.GetBinContent(ibin,jbin)/self.factors[self.helXsecs[coeff]]
             
        t.Scale(nsum)

    def xsecMap(self):

        shapeOut = ROOT.TFile(self.shapeFile+'_xsec.root', 'recreate')
        shapeOut.cd()

        out = ROOT.TFile('xsec.root', 'recreate')
        out.cd()

        self.xsec.Scale(61526.7/0.001) #xsec in fb
        self.xsec.Write()

        for kind,templList in self.templates2D.iteritems()
            if kind in self.clist:
                for t in templList:
                        
                    name = t.GetName()
                    jbin = int(name.split('_')[5])
                    ibin = int(name.split('_')[3])
                    tmp = ROOT.TH1D(t.GetName(),t.GetName(), 1, 0., 1.)
                    cont = self.xsec.GetBinContent(ibin,jbin)
                    tmp.SetBinContent(1, cont)

                    nsum = (3./16./math.pi)
                        if not "UL" in kind:
                            hAC = ROOT.TH2D
                            hAC = self.fmap.Get("harmonics{}".format(self.helXsecs[kind]))
                                        
                            nsum = nsum*hAC.GetBinContent(ibin,jbin)/self.factors[self.helXsecs[kind]]
                                                                        
                    tmp.Scale(nsum)
                    shapeOut.cd()
                    tmp.Write()

            tmp = ROOT.TH1D(kind, kind, 1, 0.,1.)
            if kind == "data_obs": tmp.SetBinContent(1, 1.)
            else tmp.SetBinContent(1, 0.)
            tmp.Write()

    def fillShapeMap(self):

        self.shapeMap['bin1'] = {}
        self.shapeMap['Wplus'] = {}
        # first data
        self.shapeMap['bin1']["data_obs"] = [self.shapeFile+'.root', "data_obs"]
        self.shapeMap['Wplus']["data_obs"] = [self.shapeFile+'_xsec.root', "data_obs"]
        # then the rest
        for proc in self.processes:
                
            self.shapeMap['bin1'][proc] = [self.shapeFile+'.root', proc]
            self.shapeMap['Wplus'][proc] = [self.shapeFile+'_xsec.root', proc]

    def fillHelGroup(self):

        for i in range(1, self.imap.GetNbinsX()+1):
            for j in range(1, self.imap.GetNbinsY()+1):

                s = 'y_{i}_pt_{j}'.format(i=i,j=j)
                self.helGroups[s] = []
                for hel in self.helXsecs:
                    if 'helXsecs_'+hel+'_'+s in self.signals:

                        self.helGroups[s].append('helXsecs_'+hel+'_'+s)
                                
                if self.helGroups[s] == []:
                    del self.helGroups[s]

	def makeDatacard(self):

		self.DC = Datacard()

		############## Setup the datacard (must be filled in) ###########################

		self.DC.bins =   ['bin1', 'Wplus'] # <type 'list'>
		self.DC.obs =    {} # <type 'dict'>
		self.DC.processes =  self.processes # <type 'list'>
		self.DC.signals =    self.signals # <type 'list'>
		self.DC.isSignal =   {} # <type 'dict'>
		for proc in self.processes:

                        if proc in self.signals:
			        self.DC.isSignal[proc] = True
                        else:
                                self.DC.isSignal[proc] = False

		self.DC.keyline =    [] # <type 'list'>
		self.DC.exp =    {} # <type 'dict'>
		self.DC.exp['bin1'] = {}
                self.DC.exp['Wplus'] = {}
		for proc in self.processes:
			self.DC.exp['bin1'][proc] = -1.00
                        self.DC.exp['Wplus'][proc] = -1.00
		self.DC.systs =  [] # <type 'list'>
		## list of [{bin : {process : [input file, path to shape, path to shape for uncertainty]}}]
		self.DC.shapeMap =   self.shapeMap # <type 'list'> 
		self.DC.hasShapes =  True # <type 'bool'>
		self.DC.flatParamNuisances =  {} # <type 'dict'>
		self.DC.rateParams =  {} # <type 'dict'>
		self.DC.extArgs =    {} # <type 'dict'>
		self.DC.rateParamsOrder  =  set([]) # <type 'set'>
		self.DC.frozenNuisances  =  set([]) # <type 'set'>
		self.DC.systematicsShapeMap =  {} # <type 'dict'>
		self.DC.nuisanceEditLines    =  [] # <type 'list'>
		self.DC.groups   =  {} # <type 'dict'>
		self.DC.discretes    =  [] # <type 'list'>
                self.DC.helGroups = self.helGroups


		filehandler = open('{}.pkl'.format(self.shapeFile), 'w')
        pickle.dump(self.DC, filehandler)
