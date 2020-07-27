import ROOT
import pickle
from HiggsAnalysis.CombinedLimit.DatacardParser import *
from collections import OrderedDict
from termcolor import colored
import math 

class fitUtils:
	def __init__(self, fIn, fMap, fileMap,shapeFile):

		#parser = argparse.ArgumentParser("")
		#parser.add_argument('-fileIn', '--fileIn', type=str, default=" ", help="name of input file containing templates and observed data")
		#parser.add_argument('-shapeFile', '--shapeFile', type=str, default=" ", help="name of shape file to be written containing inputs for fit")
		#args = parser.parse_args()

		self.shapeFile = shapeFile
		self.f = ROOT.TFile.Open(fIn)
		self.file = self.f.Get("templates")
                self.fmap = ROOT.TFile.Open(fMap)
		self.filemap = ROOT.TFile.Open(fileMap)
                self.imap = ROOT.TH2D
                self.imap = self.filemap.Get("AngCoeff/mapTot")
                self.closure = ROOT.TH2D("clos", "clos", self.imap.GetXaxis().GetNbins(),self.imap.GetXaxis().GetXbins().GetArray(),self.imap.GetYaxis().GetNbins(),self.imap.GetYaxis().GetXbins().GetArray())
                self.xsec = ROOT.TH2D
                self.xsec = self.filemap.Get("AngCoeff/sumw")

		self.templs = {}
                self.factors = {}
                self.helXsecs = OrderedDict()
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

                self.clist = ["L", "I", "T", "A", "P", "7", "8", "9", "UL"]
                for c in self.clist:
                        self.templs[c] = []
                
		self.processes = []
		self.signals = []
		self.shapeMap = {}
                self.helGroups = OrderedDict()
                self.rand = ROOT.TRandom3()
                #self.replica_data = replica_data
                #self.replica_acc = replica_acc

	def unrollTemplates(self, templ):
		# returns a th1 out of a th2

		nbins = (templ.GetNbinsX()+2)*(templ.GetNbinsY()+2)
		templ.Sumw2()
                new = templ.GetName()
                old = new + '_roll'
                templ.SetName(old)

                print new

                if not 'lowAcc' in new and not 'data' in new:

                        coeff = new.split('_')[3]
                        jbin = int(new.split('_')[1])
                        ibin = int(new.split('_')[5])

                        new = 'helXsecs_'+coeff+'_y_{}'.format(ibin)+'_pt_{}'.format(jbin)
                
                unrolledtempl = ROOT.TH1F(new, '', nbins, 0., nbins)
		
		for ibin in range(0, templ.GetNbinsX()+2):
			for ybin in range(0, templ.GetNbinsY()+2):
				
				bin1D = templ.GetBin(ibin,ybin)
				unrolledtempl.SetBinContent(bin1D, templ.GetBinContent(ibin,ybin))
				unrolledtempl.SetBinError(bin1D, templ.GetBinError(ibin,ybin))

		return unrolledtempl
        
	def project3Dto2D(self, th3):
		# returns a list of th2 ordered by rapidity bin
		th3.Sumw2()
		
		for ibin in range(1, th3.GetNbinsZ()+1):

			lowEdgeY = th3.GetZaxis().GetBinLowEdge(ibin)
			upEdgeY = th3.GetZaxis().GetBinUpEdge(ibin)

			th3.GetZaxis().SetRange(ibin, ibin)
			proj = th3.Project3D("y_{ibin}_yxe".format(ibin=ibin))
                        name = proj.GetName()
                        proj.SetName(name.replace('_yx', ''))

                        if proj.Integral()==0.0: 
                                print colored(proj.GetName(),'red')
                                continue 

                        coeff = name.split('_')[3]
                       
                        jbin = int(name.split('_')[1])

                        proj_unroll = self.unrollTemplates(proj)
                        #print colored(proj_unroll.GetName(), 'magenta'), colored(proj_unroll.Integral(), 'magenta')
                        self.templs[coeff].append(proj_unroll)
                        self.processes.append(proj_unroll.GetName())
                        if not "helXsecs_7" in proj_unroll.GetName() and not "helXsecs_8" in proj_unroll.GetName() and not "helXsecs_9" in proj_unroll.GetName() and not proj_unroll.Integral() == 0.0:
                                self.signals.append(proj_unroll.GetName())

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

        def acceptanceMap(self):
                
                for coeff, templ in self.templs.iteritems():
                        for t in templ:
                                
                                self.normTempl(t)
                

                for i in range(1, self.closure.GetNbinsX()+1):
                        for j in range(1, self.closure.GetNbinsY()+1):

                                hlist = []

                                for coeff, templ in self.templs.iteritems():

                                        for t in templ:
                                        
                                                s = 'y_{i}_pt_{j}'.format(i=i,j=j)
                                                
                                                if t.GetName().replace('helXsecs_'+coeff+'_', '') == s:

                                                        hlist.append(t)
                                yields = 0
                                for h in hlist:
                        
                                        yields=yields+h.Integral(0, h.GetNbinsX()+2)
                                
                                print i,j,yields
                                self.closure.SetBinContent(i,j,yields)


                self.closure.Divide(self.imap)
                out = ROOT.TFile('clos.root', 'recreate')
                out.cd()
                self.closure.Write()

        def xsecMap(self):

                shapeOut = ROOT.TFile(self.shapeFile+'_xsec.root', 'recreate')
                shapeOut.cd()

                out = ROOT.TFile('xsec.root', 'recreate')
                out.cd()

                self.xsec.Scale(61526.7/0.001) #xsec in fb
                self.xsec.Write()

                for coeff, templ in self.templs.iteritems():
                        
                        for t in templ:

                                name = t.GetName()
                                jbin = int(name.split('_')[5])
                                ibin = int(name.split('_')[3])

                                tmp = ROOT.TH1D(t.GetName(),t.GetName(), 1, 0., 1.)
                                cont = self.xsec.GetBinContent(ibin,jbin)
                                tmp.SetBinContent(1, cont)

                                nsum = (3./16./math.pi)
                                if not "UL" in coeff:
                                        hAC = ROOT.TH2D
                                        hAC = self.fmap.Get("harmonics{}".format(self.helXsecs[coeff]))
                                        
                                        nsum = nsum*hAC.GetBinContent(ibin,jbin)/self.factors[self.helXsecs[coeff]]
                                                                        
                                tmp.Scale(nsum)
                                shapeOut.cd()
                                tmp.Write()

                tmp = ROOT.TH1D("data_obs", "data_obs", 1, 0.,1.)
                tmp.SetBinContent(1, 1.)
                tmp.Write()

                tmp2 = ROOT.TH1D("lowAcc", "lowAcc", 1, 0.,1.)
                tmp2.SetBinContent(1, 0.)
                tmp2.Write()



        def fillSignalList(self):

                self.acceptanceMap()
                """
                for i in range(1, self.closure.GetNbinsX()+1):
                        for j in range(1, self.closure.GetNbinsY()+1):

                                if self.closure.GetBinContent(i,j) > 0.35:

                                        for coeff, templ in self.templs.iteritems():
                                                if "A5" in coeff or "A6" in coeff or "A7" in coeff: continue
                                                for t in templ:

                                                        s = '_pt{j}_y{i}'.format(i=i,j=j)
                                                
                                                        if t.GetName().replace(coeff, '') == s:

                                                                print colored('{} is signal'.format(t.GetName()),'green')
                                                                self.signals.append(t.GetName())
                                                                """
                                                        

        def writeShapeFile(self):

                shapeOut = ROOT.TFile(self.shapeFile+'.root', 'recreate')
                shapeOut.cd()

                #first templates
                for c,templ in self.templs.iteritems():
                        for t in templ:
                                #print colored(t.GetName(), 'blue')
                                t.Write()

                #lowAcc = self.file.Get('lowAcc_PDF_replica_{}'.format(self.replica_acc))
                self.file2 = self.f.Get("dataObs")
                lowAcc = self.file2.Get('lowAcc')
                lowAcc_unrolled = self.unrollTemplates(lowAcc)
                #lowAcc_unrolled.SetName('lowAcc')
                self.processes.append(lowAcc_unrolled.GetName())

                # then data obs

                #data = self.file.Get('data_obs_PDF_replica_{}'.format(self.replica_data))
                data = self.file2.Get('data_obs')
                data_unrolled = self.unrollTemplates(data)
                data_unrolled.SetName('data_obs')
                
                ##for i in range(1, data_unrolled.GetNbinsX()+1):
                        ##smear = math.sqrt(data_unrolled.GetBinContent(i))*self.rand.Gaus(0, 1)
                        ##data_unrolled.SetBinContent(i, data_unrolled.GetBinContent(i)+smear)

                
                shapeOut.cd()
                data_unrolled.Write()
                lowAcc_unrolled.Write() 

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
