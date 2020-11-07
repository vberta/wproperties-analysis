import ROOT
from time import time
def main():
    print('creating histograms')
    histos = [ROOT.TH3D("h{}".format(n), "h", 50, 0, 1, 50, 0, 1, 50, 0, 1) for n in range(10000)]
    print('writing histograms')
    fout = ROOT.TFile.Open("f.root", "recreate")
    start = time()
    for h in histos:
        fout.mkdir(h.GetName())
        fout.cd(h.GetName())
        print((h.GetName()))
        h.Write()
    fout.Close();
    end = time()
    print(("time: {}".format(end - start)))
if __name__ == "__main__":
    main()
