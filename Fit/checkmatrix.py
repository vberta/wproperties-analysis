import ROOT
import numpy as np
from root_numpy import hist2array

f = ROOT.TFile.Open('fit_Wplus_reco_reg.root')

hcov = f.Get('covariance_matrix_channelmu')
cov = hist2array(hcov)

hess = np.linalg.inv(cov)
print(hess.shape)
e, u = np.linalg.eigh(hess)
#print e
print(hcov.GetXaxis().GetBinLabel(np.argmax(u[:, 0])+1))
print(e[0], u[:, 0])

