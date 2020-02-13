{

  TFile* _file_trigger_plus = TFile::Open("data/externalSF/fromWhelicity/smoothEfficiency_muons_plus_trigger.root");

  std::map<std::string, TH3D*> cmap;
  std::map<std::string, TH2D*> vmap;
  std::map<std::string, TH2D*> hmap;
  hmap.insert( std::pair<std::string, TH2D*>("trigger_plus",  (TH2D*)_file_trigger_plus->Get("scaleFactor") ) );
  cmap.insert( std::pair<std::string, TH3D*>("cov_mc_plus",   (TH3D*)_file_trigger_plus->Get("hist_ErfCovMatrix_vs_eta_mc")));
  vmap.insert( std::pair<std::string, TH2D*>("val_mc_plus",   (TH2D*)_file_trigger_plus->Get("hist_ErfParam_vs_eta_mc")));
  std::vector<std::string> data = {"mc"};
  std::vector<std::string> charges = {"plus"};
  std::vector<std::string> vars = {"Up","Down"};
  for(auto d : data){
    for(auto c : charges){
      TH3D* cov = cmap.at("cov_"+d+"_"+c);
      TH2D* val = vmap.at("val_"+d+"_"+c);
      for(int e = 0 ; e<3 ; e++ ){
	for(auto v : vars ){
	  TH2D* h = (TH2D*)hmap.at("trigger_"+c)->Clone(("trigger_"+d+"_"+c+"_eigen"+std::to_string(e)+v).c_str());
	  hmap.insert( std::pair<std::string, TH2D*>("trigger_"+d+"_"+c+"_eigen"+std::to_string(e)+v, h) );
	}
      }
      int nbins_eta = cov->GetXaxis()->GetNbins();
      for( int ieta = 1; ieta<=nbins_eta; ieta++ ){
	double eta = cov->GetXaxis()->GetBinCenter(ieta);
	cov->GetXaxis()->SetRange(ieta,ieta);
	TH2D* icov = (TH2D*)((TH2D*)cov->Project3D("yz"))->Clone((d+"_"+c+"_"+std::to_string(ieta)).c_str());
	int nbins_cov= icov->GetXaxis()->GetNbins();
	double data[9];
	for(int j = 0; j < nbins_cov; j++ ){
	  for(int k = 0; k < nbins_cov; k++ ){
	    data[j*nbins_cov+k] = icov->GetBinContent(j+1,k+1); 
	  }
	}
	TMatrixDSym Cov(3, data);     
	TVectorD eigvals(3);
	TMatrixD U = Cov.EigenVectors(eigvals);
	TMatrixD Uinv = U.InvertFast();
	TMatrixD dummy = U.InvertFast();
	//(Uinv*Cov*U).Print();
	//eigvals.Print();
	//U.Print();      
	//std::cout << v << std::to_string(ieta) << std::endl;	
	//Cov.Print();
	TVectorD coeffs(3);
	coeffs[0] = val->GetBinContent(ieta,1);
	coeffs[1] = val->GetBinContent(ieta,2);
	coeffs[2] = val->GetBinContent(ieta,3);
	//for(int e = 0 ; e<3 ; e++ ){
	//std::cout << "Input: " << coeffs[e] << " +/- " << TMath::Sqrt(Cov[e][e]) << std::endl;
	//}
	TVectorD eigen_coeffs = Uinv*coeffs;
	//for(int e = 0 ; e<3 ; e++ ){
	//std::cout << "Output: " << eigen_coeffs[e] << " +/- " << TMath::Sqrt(eigvals[e]) << std::endl;
	//}
	for(int e = 0 ; e<3 ; e++ ){
	  for(auto v : vars ){
	    TVectorD eigen_coeffs_mod(eigen_coeffs);
	    eigen_coeffs_mod[e] += (v=="Up"? 1.0 :-1.0)*TMath::Sqrt(eigvals[e]);
	    TVectorD coeffs_shift = U*eigen_coeffs_mod;
	    //cout << "Eig[" << e << "] --> " << coeffs_shift[0] << "," << coeffs_shift[1] << "," << coeffs_shift[2] << std::endl;
	    //cout << "Eig[" << e << "] + 1sigma : " << eff_shift << "/" << eff_nominal << " = " << eff_shift/eff_nominal <<  endl;
	    TH2D* h = hmap.at("trigger_"+d+"_"+c+"_eigen"+std::to_string(e)+v);
	    for(int ipt=1; ipt<=h->GetYaxis()->GetNbins(); ipt++){
	      double pt = h->GetYaxis()->GetBinCenter(ipt);
	      double eff_nominal = coeffs[0]*TMath::Erf(( pt - coeffs[1])/coeffs[2]);
	      double eff_shift   = coeffs_shift[0]*TMath::Erf((pt - coeffs_shift[1])/coeffs_shift[2]);
	      double old = h->GetBinContent(ieta,ipt);
	      double sf =  eff_nominal>0. ? eff_shift/eff_nominal : 1.0;
	      if(d=="mc" && sf>0.) sf = 1./sf;
	      h->SetBinContent(ieta,ipt, old*sf);
	      std::cout << "Eig[" << e << "] "+v+" at (" << eta << "," << pt << ") : " << setprecision(9) << sf <<  std::endl;	      
	    }
	  }
	}
	
      //Uinv.Print();
      //icov->Print("all");
    }
    }
  }

  /*
  TH2F* offset = (TH2F*)f->Get("fake_offset");
  TH2F* slope  = (TH2F*)f->Get("fake_slope");
  TH2F* cov    = (TH2F*)f->Get("fake_offset*slope");
  
  TH2F* lambda1 = (TH2F*)offset->Clone("lambda1");
  lambda1->Reset();
  TH2F* lambda2 = (TH2F*)offset->Clone("lambda2");
  lambda2->Reset();
  
  int binX = 1; 
  int binY = 10;

  double o = offset->GetBinContent(binX,binY);
  double s = slope->GetBinContent(binX,binY);
  //TVectorD pars()

  double V11 = offset->GetBinError(binX,binY)*offset->GetBinError(binX,binY);
  double V22 = slope->GetBinError(binX,binY)*slope->GetBinError(binX,binY);
  double V12 = cov->GetBinContent(binX,binY);

  cout << V12/TMath::Sqrt(V11*V22) << endl;

  const double data[4] = {V11,V12,V12,V22};
  TMatrixDSym Cov(2, data);
  TVectorD eigvals(2);
  TMatrixD U = Cov.EigenVectors(eigvals);
  Cov.Print();
  //eigvals.Print();
  //U.Print();  
  //TVectorD lambdas = U*
  */
}
