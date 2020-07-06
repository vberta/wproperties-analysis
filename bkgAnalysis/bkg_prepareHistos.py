import sys
import ROOT
import os
import copy
import json
import argparse

import bkg_utils

class bkg_prepareHistos:
    def __init__(self, outDir, inputDir,extrap=True) :
        self.outDir = outDir
        self.inputDir = inputDir
        self.extrap = extrap
        
        self.systDict = copy.deepcopy(bkg_utils.bkg_systematics)
        self.sNameNom = ''
        self.sKindNom = 'Nominal'
        self.systDict.update({self.sKindNom:[self.sNameNom]})
    
    
    def fileListBuilder(self) :
        self.fileList = []
        with open('../analysisOnData/data/samples_2016.json') as f:
            samples = json.load(f)
        for sample in samples :
            if samples[sample]['datatype']=='DATA': 
                continue
            else :
                self.fileList.append(sample)
        
        
    def prepare(self) :
        varName = 'template'
        suffString = '_bkgselections_plots'
        regList = ["Signal", "Signal_aiso","Sideband","Sideband_aiso"]
        
        if self.extrap :
            for lcut, lbin in bkg_utils.looseCutDict.iteritems() :
                regList.append('Sideband'+lcut)
                regList.append('Sideband_aiso'+lcut)
                
        dirDict = {}

        for f in self.fileList : 
            # print "./"+self.inputDir+f+suffString+".root"
            inFile =  ROOT.TFile.Open("./"+self.inputDir+f+suffString+".root")
            outFile =  ROOT.TFile("./"+self.outDir+f+".root", "recreate")
            for r in regList :
                regExtrapFlag = self.isExtrapReg(r)
                # dirDict[f+r] =    outFile.mkdir('templates_'+r)
                for sKind, sList in self.systDict.iteritems():  
                    if sKind!='Nominal' and regExtrapFlag : #extrap region only for nominal
                        continue
                    # dirDict[f+r+sKind] = ROOT.gDirectory.mkdir(sKind)                          
                    # dirDict[f+r+sKind] =    outFile.mkdir('templates_'+r+'/'+sKind,'templates_'+r+'/'+sKind)
                    if not outFile.GetDirectory('templates_'+r+'/'+sKind):                           
                        outFile.mkdir('templates_'+r+'/'+sKind)
                    for sName in sList : 
                        inFile.cd()
                        if sKind!=self.sKindNom :
                            systName = '_'+sName
                        else :
                            systName = sName
                        # print 'templates_'+r+'/'+sKind+'/'+varName+systName
                        if ROOT.gDirectory.Get('templates_'+r+'/'+sKind+'/'+varName+systName)==None : #this syst is not present
                            print "no syst in:", f, r, sKind, systName
                            h = inFile.Get('templates_'+r+'/'+self.sKindNom+'/'+varName+self.sNameNom)
                            h.SetName(varName+systName)
                        else :
                            h = inFile.Get('templates_'+r+'/'+sKind+'/'+varName+systName)
                        # outFile.cd()
                        # dirDict[f+r].cd()
                        # dirDict[f+r+sKind].cd()
                        outFile.cd('templates_'+r+'/'+sKind)
                        # print  dirDict[f+r+sKind]
                        h.Write()
                # ROOT.gDirectory.cd('templates_'+r)
                        
    def h_add(self) :
        cmdList = []
        if not os.path.isdir(self.outDir+'/hadded'): os.system('mkdir '+self.outDir+'/hadded')
        
        cmdList.append('hadd ./'+self.outDir+'hadded/WToMuNu.root ./'+self.outDir+'*.root')
        cmdList.append('cp  ./'+self.inputDir+'SingleMuonData_bkgselections_plots.root ./'+self.outDir+'hadded/Data.root')
                
        for i in cmdList :
            os.system(i)

    def isExtrapReg(self, reg) :
        FlagOut = False
        for lcut, lbin in bkg_utils.looseCutDict.iteritems() :
                if reg == 'Sideband_aiso'+lcut:
                    FlagOut = True
                if reg == 'Sideband'+lcut:
                    FlagOut = True
        return  FlagOut 


parser = argparse.ArgumentParser("")
parser.add_argument('-inputDir', '--inputDir',type=str, default='./data/', help="input dir name")
parser.add_argument('-outputDir', '--outputDir',type=str, default='./bkg_V2/', help="output dir name")

args = parser.parse_args()
inputDir = args.inputDir
outputDir = args.outputDir

preparator = bkg_prepareHistos(outDir=outputDir+'/', inputDir=inputDir+'/',extrap=True)
preparator.fileListBuilder()
preparator.prepare()
preparator.h_add()

