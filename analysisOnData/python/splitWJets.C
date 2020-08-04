#include "TROOT.h"
#include "TKey.h"
#include "TFile.h"
#include "TSystem.h"
#include "TTree.h"
      
void CopyDir(TDirectory *source) {
  //copy all objects and subdirs of directory source as a subdir of the current directory   
  //source->ls();
  TDirectory *savdir = gDirectory;
  TDirectory *adir = savdir->mkdir(source->GetName());
  adir->cd();
  //loop on all entries of this directory
  TKey *key;
  TIter nextkey(source->GetListOfKeys());
  while ((key = (TKey*)nextkey())) {
    const char *classname = key->GetClassName();
    TClass *cl = gROOT->GetClass(classname);
    if (!cl) continue;
    if (cl->InheritsFrom("TDirectory")) {
      source->cd(key->GetName());
      TDirectory *subdir = gDirectory;
      adir->cd();
      CopyDir(subdir);
      adir->cd();
    } else {
      source->cd();
      TObject *obj = key->ReadObj();
      adir->cd();
      obj->Write();
      delete obj;
    }
  }
  adir->SaveSelf(kTRUE);
  savdir->cd();
}

void CopyFile(TDirectory* f) {
  //Copy all objects and subdirs of file fname as a subdir of the current directory
  TDirectory *target = gDirectory;
  target->cd();
  CopyDir(f);
  delete f;
  target->cd();
} 

void splitWJets() {
  TFile* fin = TFile::Open("WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_plots.root");
  TFile *fout = new TFile("WToMu_plots.root","recreate");
  TKey *key;
  TIter nextkey(fin->GetDirectory("WToMu")->GetListOfKeys());
  while ((key = (TKey*)nextkey())) {
    TString dirname = "WToMu/" + TString(key->GetName());
    TDirectory* sdir = (TDirectory*)(fin->GetDirectory(dirname));
    //cout << "gDir:" << gDirectory->GetName() << endl;
    CopyFile(sdir);
  }   
  fout->Save();
  fout->Close();

  fout = new TFile("WToTau_plots.root","recreate");
  TIter wtoTaukey(fin->GetDirectory("WToTau")->GetListOfKeys());
  while ((key = (TKey*)wtoTaukey())) {
    TString dirname = "WToTau/" + TString(key->GetName());
    TDirectory* sdir = (TDirectory*)(fin->GetDirectory(dirname));
    //cout << "gDir:" << gDirectory->GetName() << endl;
    CopyFile(sdir);
  }   
  fout->Save();
  fout->Close();
  fin->Close();

}
