## wproperties-analysis
#Git repo gathering all submodules in the w properties analysis in CMS

## how to get this repository

```
git clone --recursive https://github.com/emanca/wproperties-analysis.git wproperties-analysis
cd wproperties-analysis/RDFprocessor/framework
```

## source root master nightlies slc7

`source /cvmfs/sft-nightlies.cern.ch/lcg/views/dev3/latest/x86_64-centos7-gcc8-opt/setup.sh`

`pip install --user -e .`

#To run on 2016 MC samples

```
cd wproperties-analysis/analysisOnData/
make
mkdir output
python runAnalysisOnMC.py
```