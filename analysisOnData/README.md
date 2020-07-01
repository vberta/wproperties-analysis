#Compile the full package
`make`
#To compile after editing a single file
`make fast`

#To run on 2016 MC samples

```
mkdir output
python runAnalysisOnMC.py
```
#To run on 2016 DATA samples
#The config runAnalysisOnData.py accepts 2 arguments: python runAnalysisOnData.py <arg1> <arg2> 
#arg1: 0 for only Signal region selection, 1 for background regions selection
#arg2: 0 to run over full sample, 1 to run a test job with 100 events

#Secon
#Run only signal selection over full sample
`python runAnalysisOnData.py 0 0`

#Run backaground selections over full sample
`python runAnalysisOnData.py 1 0`
