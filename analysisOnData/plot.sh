#!/bin/sh

#python plotter.py -b -o $1 -c DIMUON -v SelRecoZ_corrected_qt_SelRecoZ_corrected_y_SelRecoZ_corrected_mass  -p x -x "dimuon q_{T}"    -t qt
#python plotter.py -b -o $1 -c DIMUON -v SelRecoZ_corrected_qt_SelRecoZ_corrected_y_SelRecoZ_corrected_mass  -p y -x "dimuon rapidity" -t y
#python plotter.py -b -o $1 -c DIMUON -v SelRecoZ_corrected_qt_SelRecoZ_corrected_y_SelRecoZ_corrected_mass  -p z -x "dimuon mass"     -t mass
#python plotter.py -b -o $1 -c DIMUON -v SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge -p x -x "#eta #mu_{1}"  -t eta1
#python plotter.py -b -o $1 -c DIMUON -v SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge -p y -x "p_{T} #mu_{1}" -t pt1
#python plotter.py -b -o $1 -c DIMUON -v SelMuon2_eta_SelMuon2_corrected_pt_SelMuon2_charge -p x -x "#eta #mu_{2}"  -t eta2
#python plotter.py -b -o $1 -c DIMUON -v SelMuon2_eta_SelMuon2_corrected_pt_SelMuon2_charge -p y -x "p_{T} #mu_{2}" -t pt2
#python plotter.py -b -o $1 -c DIMUON -v SelMuon1_pfRelIso04_all_SelMuon1_dxy_SelMuon1_charge -p x -x "rel. iso. #mu_{1}" -t iso1
#python plotter.py -b -o $1 -c DIMUON -v SelMuon1_pfRelIso04_all_SelMuon1_dxy_SelMuon1_charge -p y -x "d_{xy} #mu_{1}" -t dxy1
#python plotter.py -b -o $1 -c DIMUON -v SelMuon2_pfRelIso04_all_SelMuon2_dxy_SelMuon2_charge -p x -x "rel. iso. #mu_{2}" -t iso2
#python plotter.py -b -o $1 -c DIMUON -v SelMuon2_pfRelIso04_all_SelMuon2_dxy_SelMuon2_charge -p y -x "d_{xy} #mu_{2}" -t dxy2


#python plotter.py -b -o $1 -c SIGNAL_Plus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "p_{T} #mu^{+}" -s NONE -l 19_23 -t pt_0p5
#python plotter.py -b -o $1 -c SIGNAL_Plus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "p_{T} #mu^{+}" -s NONE -l 24_28 -t pt_1p0
#python plotter.py -b -o $1 -c SIGNAL_Plus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "p_{T} #mu^{+}" -s NONE -l 29_32 -t pt_1p5
#python plotter.py -b -o $1 -c SIGNAL_Plus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "p_{T} #mu^{+}" -s NONE -l 33_34 -t pt_1p9
#python plotter.py -b -o $1 -c SIGNAL_Plus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "p_{T} #mu^{+}" -s NONE -l 35_35 -t pt_2p1
#python plotter.py -b -o $1 -c SIGNAL_Plus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "p_{T} #mu^{+}" -s NONE -l 36_36 -t pt_2p4

#python plotter.py -b -o $1 -c SIGNAL_Minus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "p_{T} #mu^{+}" -s NONE -l 19_23 -t pt_0p5
#python plotter.py -b -o $1 -c SIGNAL_Minus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "p_{T} #mu^{+}" -s NONE -l 24_28 -t pt_1p0
#python plotter.py -b -o $1 -c SIGNAL_Minus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "p_{T} #mu^{+}" -s NONE -l 29_32 -t pt_1p5
#python plotter.py -b -o $1 -c SIGNAL_Minus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "p_{T} #mu^{+}" -s NONE -l 33_34 -t pt_1p9
#python plotter.py -b -o $1 -c SIGNAL_Minus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "p_{T} #mu^{+}" -s NONE -l 35_35 -t pt_2p1
#python plotter.py -b -o $1 -c SIGNAL_Minus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "p_{T} #mu^{+}" -s NONE -l 36_36 -t pt_2p4

#python plotter.py -b -o $1 -c SIGNAL_Plus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p x -x "#eta #mu^{+}" -s NONE -t eta
#python plotter.py -b -o $1 -c SIGNAL_Plus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "p_{T} #mu^{+}" -s NONE -t pt
#python plotter.py -b -o $1 -c SIGNAL_Minus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p x -x "#eta #mu^{-}" -s NONE -t eta
#python plotter.py -b -o $1 -c SIGNAL_Minus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "p_{T} #mu^{-}" -s NONE -t pt
#python plotter.py -b -o $1 -c SIGNAL_Plus -v "SelMuon1_corrected_MET_nom_mt_SelMuon1_corrected_MET_nom_hpt_SelMuon1_charge" -p x -x "M_{T}" -s NONE -t mt
#python plotter.py -b -o $1 -c SIGNAL_Plus -v "SelMuon1_corrected_MET_nom_mt_SelMuon1_corrected_MET_nom_hpt_SelMuon1_charge" -p y -x "h_{T}" -s NONE -t ht
#python plotter.py -b -o $1 -c SIGNAL_Minus -v "SelMuon1_corrected_MET_nom_mt_SelMuon1_corrected_MET_nom_hpt_SelMuon1_charge" -p x -x "M_{T}" -s NONE -t mt
#python plotter.py -b -o $1 -c SIGNAL_Minus -v "SelMuon1_corrected_MET_nom_mt_SelMuon1_corrected_MET_nom_hpt_SelMuon1_charge" -p y -x "h_{T}" -s NONE -t ht
#python plotter.py -b -o $1 -c QCD_Plus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p x -x "#eta #mu^{+}" -s NONE -t eta
#python plotter.py -b -o $1 -c QCD_Plus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "p_{T} #mu^{+}" -s NONE -t pt
#python plotter.py -b -o $1 -c QCD_Minus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p x -x "#eta #mu^{-}" -s NONE -t eta
#python plotter.py -b -o $1 -c QCD_Minus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "p_{T} #mu^{-}" -s NONE -t pt
#python plotter.py -b -o $1 -c QCD_Plus -v "SelMuon1_corrected_MET_nom_mt_SelMuon1_corrected_MET_nom_hpt_SelMuon1_charge" -p x -x "M_{T}" -s NONE -t mt
#python plotter.py -b -o $1 -c QCD_Plus -v "SelMuon1_corrected_MET_nom_mt_SelMuon1_corrected_MET_nom_hpt_SelMuon1_charge" -p y -x "h_{T}" -s NONE -t ht
#python plotter.py -b -o $1 -c QCD_Minus -v "SelMuon1_corrected_MET_nom_mt_SelMuon1_corrected_MET_nom_hpt_SelMuon1_charge" -p x -x "M_{T}" -s NONE -t mt
#python plotter.py -b -o $1 -c QCD_Minus -v "SelMuon1_corrected_MET_nom_mt_SelMuon1_corrected_MET_nom_hpt_SelMuon1_charge" -p y -x "h_{T}" -s NONE -t ht

#python plotter.py -b -o $1 -c SIGNAL_Plus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p x -x "muon #eta" -s "ISO,Trigger,nom,corrected,LHE" -q -t eta_quad_all
#python plotter.py -b -o $1 -c SIGNAL_Plus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p x -x "muon #eta" -s "ISO,Trigger,nom,corrected" -q -t eta_quad_noLHE
#python plotter.py -b -o $1 -c SIGNAL_Plus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p x -x "muon #eta" -s "LHEScaleWeight_muR2p0_muF1p0,LHEScaleWeight_muR0p5_muF1p0" -q -t eta_muR
#python plotter.py -b -o $1 -c SIGNAL_Plus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p x -x "muon #eta" -s "LHEScaleWeight_muR1p0_muF2p0,LHEScaleWeight_muR1p0_muF0p5" -q -t eta_muF
#python plotter.py -b -o $1 -c SIGNAL_Plus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p x -x "muon #eta" -s "LHEScaleWeight_muR2p0_muF2p0,LHEScaleWeight_muR0p5_muF0p5" -q -t eta_muRmuF
#python plotter.py -b -o $1 -c SIGNAL_Plus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p x -x "muon #eta" -s "LHEPdfWeight" -q -t eta_PDF

#python plotter.py -b -o $1 -c SIGNAL_Plus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "muon p_{T} [GeV]" -s "ISO,Trigger,nom,corrected,LHE" -q -t pt_quad_all
#python plotter.py -b -o $1 -c SIGNAL_Plus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "muon p_{T} [GeV]" -s "ISO,Trigger,nom,corrected" -q -t pt_quad_noLHE
#python plotter.py -b -o $1 -c SIGNAL_Plus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "muon p_{T} [GeV]" -s "LHEScaleWeight_muR2p0_muF1p0,LHEScaleWeight_muR0p5_muF1p0" -t pt_muR
#python plotter.py -b -o $1 -c SIGNAL_Plus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "muon p_{T} [GeV]" -s "LHEScaleWeight_muR1p0_muF2p0,LHEScaleWeight_muR1p0_muF0p5" -t pt_muF
#python plotter.py -b -o $1 -c SIGNAL_Plus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "muon p_{T} [GeV]" -s "LHEScaleWeight_muR2p0_muF2p0,LHEScaleWeight_muR0p5_muF0p5" -t pt_muRmuF
#python plotter.py -b -o $1 -c SIGNAL_Plus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "muon p_{T} [GeV]" -s "LHEPdfWeight" -q -t pt_PDF

#python plotter.py -b -o $1 -c SIGNAL_Minus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p x -x "muon #eta" -s "ISO,Trigger,nom,corrected,LHE" -q -t eta_quad_all
#python plotter.py -b -o $1 -c SIGNAL_Minus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p x -x "muon #eta" -s "ISO,Trigger,nom,corrected" -q -t eta_quad_noLHE
#python plotter.py -b -o $1 -c SIGNAL_Minus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p x -x "muon #eta" -s "LHEScaleWeight_muR2p0_muF1p0,LHEScaleWeight_muR0p5_muF1p0" -t eta_muR
#python plotter.py -b -o $1 -c SIGNAL_Minus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p x -x "muon #eta" -s "LHEScaleWeight_muR1p0_muF2p0,LHEScaleWeight_muR1p0_muF0p5" -t eta_muF
#python plotter.py -b -o $1 -c SIGNAL_Minus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p x -x "muon #eta" -s "LHEScaleWeight_muR2p0_muF2p0,LHEScaleWeight_muR0p5_muF0p5" -t eta_muRmuF
#python plotter.py -b -o $1 -c SIGNAL_Minus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p x -x "muon #eta" -s "LHEPdfWeight" -q -t eta_PDF

#python plotter.py -b -o $1 -c SIGNAL_Minus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "muon p_{T} [GeV]" -s "ISO,Trigger,nom,corrected,LHE" -q -t pt_quad_all
#python plotter.py -b -o $1 -c SIGNAL_Minus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "muon p_{T} [GeV]" -s "ISO,Trigger,nom,corrected" -q -t pt_quad_noLHE
#python plotter.py -b -o $1 -c SIGNAL_Minus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "muon p_{T} [GeV]" -s "LHEScaleWeight_muR2p0_muF1p0,LHEScaleWeight_muR0p5_muF1p0" -t pt_muR
#python plotter.py -b -o $1 -c SIGNAL_Minus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "muon p_{T} [GeV]" -s "LHEScaleWeight_muR1p0_muF2p0,LHEScaleWeight_muR1p0_muF0p5" -t pt_muF
#python plotter.py -b -o $1 -c SIGNAL_Minus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "muon p_{T} [GeV]" -s "LHEScaleWeight_muR2p0_muF2p0,LHEScaleWeight_muR0p5_muF0p5" -t pt_muRmuF
#python plotter.py -b -o $1 -c SIGNAL_Minus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "muon p_{T} [GeV]" -s "LHEPdfWeight" -q -t pt_PDF

python plotter.py -b  -o DIMUON_WLIKE  -c DIMUON -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_corrected_MET_nom_Wlike_mt" -p z -x "W-like m_{T} [GeV], leading #mu" -t "Wlike_mt_quad_met" -s nom_unclustEnUp,nom_unclustEnDown,nom_jesTotalUp,nom_jesTotalDown -q
python plotter.py -b  -o DIMUON_WLIKE  -c DIMUON -v "SelMuon2_eta_SelMuon2_corrected_pt_SelMuon2_corrected_MET_nom_Wlike_mt" -p z -x "W-like m_{T} [GeV], trailing #mu" -t "Wlike_mt_quad_met" -s nom_unclustEnUp,nom_unclustEnDown,nom_jesTotalUp,nom_jesTotalDown -q
python plotter.py -b  -o DIMUON_WLIKE  -c DIMUON -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_corrected_MET_nom_Wlike_mt" -p z -x "W-like m_{T} [GeV], leading #mu" -t "Wlike_mt_quad_scales" -s LHEScale -q
python plotter.py -b  -o DIMUON_WLIKE  -c DIMUON -v "SelMuon2_eta_SelMuon2_corrected_pt_SelMuon2_corrected_MET_nom_Wlike_mt" -p z -x "W-like m_{T} [GeV], trailing #mu" -t "Wlike_mt_quad_scales" -s LHEScale -q
python plotter.py -b  -o DIMUON_WLIKE  -c DIMUON -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_corrected_MET_nom_Wlike_mt" -p z -x "W-like m_{T} [GeV], leading #mu" -t "Wlike_mt_quad_other" -s Trigger,ISO,corrected -q
python plotter.py -b  -o DIMUON_WLIKE  -c DIMUON -v "SelMuon2_eta_SelMuon2_corrected_pt_SelMuon2_corrected_MET_nom_Wlike_mt" -p z -x "W-like m_{T} [GeV], trailing #mu" -t "Wlike_mt_quad_other" -s Trigger,ISO,corrected -q
