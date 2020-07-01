Compile the full package
`make`

To compile after editing a single file
`make fast`

Create the output directory where the ourput root files will be saved.
`mkdir output`

Configuration files: There are two configuration files runAnalysisOnData.py/runAnalysisOnMC.py to run in DATA/MC samples. Both configs accept 2 arguments.

arg1: 0 for only Signal region selection, 1 for background regions selection

arg2: 0 to run over full sample, 1 to run a test job with 10 events

To run on 2016 MC samples

```
Run only signal selection over full sample
python runAnalysisOnMC.py 0 0

Run backaground selections over full sample
python runAnalysisOnMC.py 1 0
```

To run on 2016 DATA samples

Run only signal selection over full sample
`python runAnalysisOnData.py 0 0`

Run backaground selections over full sample
`python runAnalysisOnData.py 1 0`
