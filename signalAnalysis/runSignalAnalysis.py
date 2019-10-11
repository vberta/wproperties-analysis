import os
import sys
import ROOT
from math import *

from RDFtree import *

from getLumiWeight import *
from basicSelection import *


#os.system("g++ -fPIC -Wall -O3 ../RDFprocessor/framework/module.cpp defineHarmonics.cpp $(root-config --libs --cflags) -shared -o defineHarmonics.so")

############ this has to be compiled with TH2 helper
#os.system("g++ -fPIC -Wall -O3 ../RDFprocessor/framework/module.cpp ../RDFprocessor/framework/TH2weightsHelper.cpp AngCoeff.cpp $(root-config --libs --cflags) -shared -o AngCoeff.so")
#os.system("g++ -fPIC -Wall -O3 ../RDFprocessor/framework/module.cpp ../RDFprocessor/framework/TH2weightsHelper.cpp getACValues.cpp $(root-config --libs --cflags) -shared -o getACValues.so")

#os.system("g++ -fPIC -Wall -O3 ../RDFprocessor/framework/module.cpp ../RDFprocessor/framework/TH2weightsHelper.cpp defineSystWeight.cpp $(root-config --libs --cflags) -shared -o defineSystWeight.so")

#os.system("g++ -fPIC -Wall -O3 ../RDFprocessor/framework/module.cpp getWeights.cpp $(root-config --libs --cflags) -shared -o getWeights.so")

#os.system("g++ -fPIC -Wall -O3 ../RDFprocessor/framework/module.cpp ../RDFprocessor/framework/TH3weightsHelper.cpp templateBuilder.cpp $(root-config --libs --cflags) -shared -o templateBuilder.so")
#os.system("g++ -fPIC -Wall -O3 ../RDFprocessor/framework/module.cpp ../RDFprocessor/framework/TH2weightsHelper.cpp dataObs.cpp $(root-config --libs --cflags) -shared -o dataObs.so")
#os.system("g++ -fPIC -Wall -O3 ../RDFprocessor/framework/module.cpp ../RDFprocessor/framework/TH2weightsHelper.cpp getAccMap.cpp $(root-config --libs --cflags) -shared -o getAccMap.so")


ROOT.gInterpreter.Declare('#include "../RDFprocessor/framework/module.h"')
ROOT.gInterpreter.Declare('#include "defineHarmonics.h"')
ROOT.gSystem.Load('defineHarmonics.so')

ROOT.gInterpreter.Declare('#include "../RDFprocessor/framework/module.h"')
ROOT.gInterpreter.Declare('#include "AngCoeff.h"')
ROOT.gSystem.Load('AngCoeff.so')

ROOT.gInterpreter.Declare('#include "../RDFprocessor/framework/module.h"')
ROOT.gInterpreter.Declare('#include "getACValues.h"')
ROOT.gSystem.Load('getACValues.so')

ROOT.gInterpreter.Declare('#include "../RDFprocessor/framework/module.h"')
ROOT.gInterpreter.Declare('#include "defineSystWeight.h"')
ROOT.gSystem.Load('defineSystWeight.so')

ROOT.gInterpreter.Declare('#include "../RDFprocessor/framework/module.h"')
ROOT.gInterpreter.Declare('#include "getWeights.h"')
ROOT.gSystem.Load('getWeights.so')

ROOT.gInterpreter.Declare('#include "../RDFprocessor/framework/module.h"')
ROOT.gInterpreter.Declare('#include "templateBuilder.h"')
ROOT.gSystem.Load('templateBuilder.so')

ROOT.gInterpreter.Declare('#include "../RDFprocessor/framework/module.h"')
ROOT.gInterpreter.Declare('#include "dataObs.h"')
ROOT.gSystem.Load('dataObs.so')

ROOT.gInterpreter.Declare('#include "../RDFprocessor/framework/module.h"')
ROOT.gInterpreter.Declare('#include "getAccMap.h"')
ROOT.gSystem.Load('getAccMap.so')

cores = [64]

for c in cores:
	ROOT.ROOT.DisableImplicitMT()
	ROOT.ROOT.EnableImplicitMT(c)

	print "running with {} cores".format(c)


	inputFile = '/scratchssd/emanca/wproperties-analysis/data/test_*.root'

	p = RDFtree(outputDir = 'TEST', inputFile = inputFile, outputFile="test3.root")
	p.branch(nodeToStart = 'input', nodeToEnd = 'basicSelection', modules = [getLumiWeight(xsec=61526.7, inputFile=inputFile), ROOT.defineHarmonics(), basicSelection()])
	p.branch(nodeToStart = 'basicSelection', nodeToEnd = 'AngCoeff', modules = [ROOT.AngCoeff()])

	pdf = ROOT.vector('string')()
	for i in range(1,102):
		pdf.push_back('replica{}'.format(i))

	#p.branch(nodeToStart = 'basicSelection', nodeToEnd = 'AngCoeffPDF', modules = [ROOT.defineSystWeight("LHEPdfWeight"),ROOT.AngCoeff(pdf,"LHEPdfWeight")])
	p.getOutput()

	p.branch(nodeToStart = 'AngCoeff', nodeToEnd = 'AngCoeff2',modules = [ROOT.getACValues([h for h in p.getObjects('AngCoeff') if 'vector' in h.__cppname__][0])])
	#p.branch(nodeToStart = 'AngCoeffPDF', nodeToEnd = 'AngCoeffPDF2',modules = [ROOT.getACValues([h for h in p.getObjects('AngCoeff') if 'vector' in h.__cppname__][0])])

	maps = ROOT.vector(ROOT.RDF.RResultPtr('TH2D'))()
	for i in range(0,3):
		maps.push_back([h for h in p.getObjects('AngCoeff') if not 'vector' in h.__cppname__][i])

	p.branch(nodeToStart = 'AngCoeff2', nodeToEnd = 'accMap', modules =[ROOT.getAccMap(maps)])
	p.branch(nodeToStart = 'accMap', nodeToEnd = 'templates', modules =[ROOT.getWeights(), ROOT.templateBuilder()])
	p.branch(nodeToStart = 'accMap', nodeToEnd = 'dataObs', modules =[ROOT.dataObs()])

	p.getOutput()
	#p.saveGraph()




