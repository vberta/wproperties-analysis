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

#os.system("g++ -fPIC -Wall -O3 ../RDFprocessor/framework/module.cpp getWeights.cpp $(root-config --libs --cflags) -shared -o getWeights.so")

#os.system("g++ -fPIC -Wall -O3 ../RDFprocessor/framework/module.cpp ../RDFprocessor/framework/TH3weightsHelper.cpp templateBuilder.cpp $(root-config --libs --cflags) -shared -o templateBuilder.so")
os.system("g++ -fPIC -Wall -O3 ../RDFprocessor/framework/module.cpp ../RDFprocessor/framework/TH2weightsHelper.cpp dataObs.cpp $(root-config --libs --cflags) -shared -o dataObs.so")

ROOT.gInterpreter.Declare('#include "../RDFprocessor/framework/module.h"')
ROOT.gInterpreter.Declare('#include "defineHarmonics.h"')
ROOT.gSystem.Load('defineHarmonics.so')

ROOT.gInterpreter.Declare('#include "../RDFprocessor/framework/module.h"')
ROOT.gInterpreter.Declare('#include "AngCoeff.h"')
ROOT.gSystem.Load('AngCoeff.so')

ROOT.gInterpreter.Declare('#include "../RDFprocessor/framework/module.h"')
ROOT.gInterpreter.Declare('#include "getWeights.h"')
ROOT.gSystem.Load('getWeights.so')

ROOT.gInterpreter.Declare('#include "../RDFprocessor/framework/module.h"')
ROOT.gInterpreter.Declare('#include "templateBuilder.h"')
ROOT.gSystem.Load('templateBuilder.so')

ROOT.gInterpreter.Declare('#include "../RDFprocessor/framework/module.h"')
ROOT.gInterpreter.Declare('#include "dataObs.h"')
ROOT.gSystem.Load('dataObs.so')

ROOT.ROOT.EnableImplicitMT()

inputFile = '/scratchssd/emanca/wproperties-analysis/data/test_*.root'

p = RDFtree(outputDir = 'TEST', inputFile = inputFile, outputFile="test.root")
p.branch(nodeToStart = 'input', nodeToEnd = 'basicSelection', modules = [ROOT.defineHarmonics(), getLumiWeight(xsec=61526.7, inputFile=inputFile), basicSelection()])
p.branch(nodeToStart = 'basicSelection', nodeToEnd = 'AngCoeff', modules = [ROOT.AngCoeff()])
p.branch(nodeToStart = 'AngCoeff', nodeToEnd = 'templates', modules =[ROOT.getWeights(), ROOT.templateBuilder()])
p.branch(nodeToStart = 'AngCoeff', nodeToEnd = 'dataObs', modules =[ROOT.dataObs()])

p.getOutput()




