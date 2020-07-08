#!/bin/bash
#hadd needed first time
if [ $2 -gt 0 ]
then
  cd $1
  mv SingleMuonData_plots.root Data_plots.root
  mv WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_plots.root WJets_plots.root
  hadd DYJets_plots.root DYJetsToLL_M-*
  hadd TTJets_plots.root TTJets*
  hadd SingleTop_plots.root  ST_t-channel_* ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1_plots.root 
  hadd TW_plots.root  ST_tW_*
  hadd Diboson_plots.root WW_TuneCUETP8M1_13TeV-pythia8_plots.root WZ_TuneCUETP8M1_13TeV-pythia8_plots.root ZZ_TuneCUETP8M1_13TeV-pythia8_plots.root
  cd -
fi
python plotter.py $1
