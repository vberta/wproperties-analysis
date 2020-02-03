#!/bin/sh

python plotter.py -b -o DIMUON_MEDIUM -c DIMUON -v SelRecoZ_corrected_qt_SelRecoZ_corrected_y_SelRecoZ_corrected_mass  -p x -x "dimuon q_{T}"    -t qt
python plotter.py -b -o DIMUON_MEDIUM -c DIMUON -v SelRecoZ_corrected_qt_SelRecoZ_corrected_y_SelRecoZ_corrected_mass  -p y -x "dimuon rapidity" -t y
python plotter.py -b -o DIMUON_MEDIUM -c DIMUON -v SelRecoZ_corrected_qt_SelRecoZ_corrected_y_SelRecoZ_corrected_mass  -p z -x "dimuon mass"     -t mass
python plotter.py -b -o DIMUON_MEDIUM -c DIMUON -v SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge -p x -x "#eta #mu_{1}"  -t eta1
python plotter.py -b -o DIMUON_MEDIUM -c DIMUON -v SelMuon1_eta_SelMuon1_corrected_pt_SelMuon1_charge -p y -x "p_{T} #mu_{1}" -t pt1
python plotter.py -b -o DIMUON_MEDIUM -c DIMUON -v SelMuon2_eta_SelMuon2_corrected_pt_SelMuon2_charge -p x -x "#eta #mu_{2}"  -t eta2
python plotter.py -b -o DIMUON_MEDIUM -c DIMUON -v SelMuon2_eta_SelMuon2_corrected_pt_SelMuon2_charge -p y -x "p_{T} #mu_{2}" -t pt2
