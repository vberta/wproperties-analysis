#!/bin/sh

python plotter.py -b -o $1 -c DIMUON -v SelRecoZ_corrected_qt_SelRecoZ_corrected_y_SelRecoZ_corrected_mass  -p x -x "dimuon q_{T}"    -t qt
python plotter.py -b -o $1 -c DIMUON -v SelRecoZ_corrected_qt_SelRecoZ_corrected_y_SelRecoZ_corrected_mass  -p y -x "dimuon rapidity" -t y
python plotter.py -b -o $1 -c DIMUON -v SelRecoZ_corrected_qt_SelRecoZ_corrected_y_SelRecoZ_corrected_mass  -p z -x "dimuon mass"     -t mass
python plotter.py -b -o $1 -c DIMUON -v SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge -p x -x "#eta #mu_{1}"  -t eta1
python plotter.py -b -o $1 -c DIMUON -v SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge -p y -x "p_{T} #mu_{1}" -t pt1
python plotter.py -b -o $1 -c DIMUON -v SelMuon2_eta_SelMuon2_corrected_pt_SelMuon2_charge -p x -x "#eta #mu_{2}"  -t eta2
python plotter.py -b -o $1 -c DIMUON -v SelMuon2_eta_SelMuon2_corrected_pt_SelMuon2_charge -p y -x "p_{T} #mu_{2}" -t pt2
python plotter.py -b -o $1 -c DIMUON -v SelMuon1_pfRelIso04_all_SelMuon1_dxy_SelMuon1_charge -p x -x "rel. iso. #mu_{1}" -t iso1
python plotter.py -b -o $1 -c DIMUON -v SelMuon1_pfRelIso04_all_SelMuon1_dxy_SelMuon1_charge -p y -x "d_{xy} #mu_{1}" -t dxy1
python plotter.py -b -o $1 -c DIMUON -v SelMuon2_pfRelIso04_all_SelMuon2_dxy_SelMuon2_charge -p x -x "rel. iso. #mu_{2}" -t iso2
python plotter.py -b -o $1 -c DIMUON -v SelMuon2_pfRelIso04_all_SelMuon2_dxy_SelMuon2_charge -p y -x "d_{xy} #mu_{2}" -t dxy2

exit

python plotter.py -b -o $1 -c SIGNAL_Plus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p x -x "#eta #mu^{+}" -s NONE -t eta
python plotter.py -b -o $1 -c SIGNAL_Plus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "p_{T} #mu^{+}" -s NONE -t pt
python plotter.py -b -o $1 -c SIGNAL_Minus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p x -x "#eta #mu^{-}" -s NONE -t eta
python plotter.py -b -o $1 -c SIGNAL_Minus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "p_{T} #mu^{-}" -s NONE -t pt
python plotter.py -b -o $1 -c SIGNAL_Plus -v "SelMuon1_corrected_MET_nom_mt_SelMuon1_corrected_MET_nom_hpt_SelMuon1_charge" -p x -x "M_{T}" -s NONE -t mt
python plotter.py -b -o $1 -c SIGNAL_Plus -v "SelMuon1_corrected_MET_nom_mt_SelMuon1_corrected_MET_nom_hpt_SelMuon1_charge" -p y -x "h_{T}" -s NONE -t ht
python plotter.py -b -o $1 -c SIGNAL_Minus -v "SelMuon1_corrected_MET_nom_mt_SelMuon1_corrected_MET_nom_hpt_SelMuon1_charge" -p x -x "M_{T}" -s NONE -t mt
python plotter.py -b -o $1 -c SIGNAL_Minus -v "SelMuon1_corrected_MET_nom_mt_SelMuon1_corrected_MET_nom_hpt_SelMuon1_charge" -p y -x "h_{T}" -s NONE -t ht
python plotter.py -b -o $1 -c QCD_Plus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p x -x "#eta #mu^{+}" -s NONE -t eta
python plotter.py -b -o $1 -c QCD_Plus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "p_{T} #mu^{+}" -s NONE -t pt
python plotter.py -b -o $1 -c QCD_Minus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p x -x "#eta #mu^{-}" -s NONE -t eta
python plotter.py -b -o $1 -c QCD_Minus -v "SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge" -p y -x "p_{T} #mu^{-}" -s NONE -t pt
python plotter.py -b -o $1 -c QCD_Plus -v "SelMuon1_corrected_MET_nom_mt_SelMuon1_corrected_MET_nom_hpt_SelMuon1_charge" -p x -x "M_{T}" -s NONE -t mt
python plotter.py -b -o $1 -c QCD_Plus -v "SelMuon1_corrected_MET_nom_mt_SelMuon1_corrected_MET_nom_hpt_SelMuon1_charge" -p y -x "h_{T}" -s NONE -t ht
python plotter.py -b -o $1 -c QCD_Minus -v "SelMuon1_corrected_MET_nom_mt_SelMuon1_corrected_MET_nom_hpt_SelMuon1_charge" -p x -x "M_{T}" -s NONE -t mt
python plotter.py -b -o $1 -c QCD_Minus -v "SelMuon1_corrected_MET_nom_mt_SelMuon1_corrected_MET_nom_hpt_SelMuon1_charge" -p y -x "h_{T}" -s NONE -t ht
