from module import *

class basicSelection(module):
   
    def __init__(self):
        
        self.myTH1 = []
        self.myTH2 = []
        self.myTH3 = []

        self.myTH1Group = []
        self.myTH2Group = []
        self.myTH3Group = []

    def run(self,d):

        self.d = d

        # self.d = self.d.Define("Wrap_preFSR_abs", "fabs(Wrap_preFSR)")\
        # .Filter("GenPart_pdgId[GenPart_preFSRMuonIdx]<0")\
        # .Define("Mupt_preFSR", "GenPart_pt[GenPart_preFSRMuonIdx]")\
        # .Define("Mueta_preFSR", "GenPart_eta[GenPart_preFSRMuonIdx]")
        
        self.d = self.d.Define("Wrap_preFSR_abs", "fabs(GenV_preFSR_y)")\
        .Filter("GenPart_pdgId[Idx_preFSR_mu1]<0")\
        .Define("Mupt_preFSR", "GenPart_pt[Idx_preFSR_mu1]")\
        .Define("Mueta_preFSR", "GenPart_eta[Idx_preFSR_mu1]")
        # Muon_genPartIdx
        
        self.d = self.d.Define("Wpt_preFSR","GenV_preFSR_qt")
        
        
        
        return self.d

    def getTH1(self):

        return self.myTH1

    def getTH2(self):

        return self.myTH2  

    def getTH3(self):

        return self.myTH3

    def getGroupTH1(self):

        return self.myTH1Group

    def getGroupTH2(self):

        return self.myTH2Group  

    def getGroupTH3(self):

        return self.myTH3Group  

    def reset(self):

        self.myTH1 = []
        self.myTH2 = []
        self.myTH3 = [] 

        self.myTH1Group = []
        self.myTH2Group = []
        self.myTH3Group = [] 
