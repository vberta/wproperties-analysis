# wproperties-analysis
Git repo gathering all submodules in the w properties analysis in CMS

## how to get this repository

```
git clone --recursive https://github.com/emanca/wproperties-analysis.git wproperties-analysis
cd wproperties-analysis/RDFprocessor/framework
```

## source root master nightlies slc7

`source /cvmfs/sft-nightlies.cern.ch/lcg/views/dev3/latest/x86_64-centos7-gcc8-opt/setup.sh`

`pip install --user -e .`

## How to run the analysis

Preliminary compile analysisOnData modules:
```
cd wproperties-analysis/analysisOnData/
make
```

To run the entire workflow (from wproperties-analysis/ directory):
```
python runTheMatrix.py --outputDir OUTPUT --bkgOutput BKGOUT --ncores 64 --bkgFile MYBKG --bkgPrep 1 --bkgAna 1 --prefit 1 --plotter 1
```

Description of the output:
* `./analysisOnData/BKGOUT/` : all prefit output (bkgPrep (aka step1) and prefit (aka step3))
    * `./analysisOnData/BKGOUT/` : .root files from step1 and step3
    * `./analysisOnData/BKGOUT/plot/` : prefit plots in .png, .pdf and .root
    * `./analysisOnData/BKGOUT/plot/hadded` : hadded root file needed for the prefit plots
* `./bkgAnalysis/BKGOUT/` : all the background output (bkgAna aka step2)
    * `./bkgAnalysis/BKGOUT/bkg_parameters_CFstatAna.root` : bkg parameters file, used to build the QCD
    * `./bkgAnalysis/BKGOUT/final_plots_CFstatAna.root` : bkg validation plot file (with systematics comparison)
    * `./bkgAnalysis/BKGOUT/bkg_SYSTNAME/` : single-systematic output and validation plot
    * `./bkgAnalysis/BKGOUT/bkgInput/` : prepared root file for the bkgAnalysis
    * `./bkgAnalysis/BKGOUT/bkgInput/hadded/` : hadded root file, the only required input of the bkgAna

For more details about the parameters of `runTheMatrix.py` there is documentation inside the file itself.




