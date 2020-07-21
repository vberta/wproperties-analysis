# Background Analysis

To produce the bkg_parameters.root needed for the prefit plotter follow this procedure:
1. copy the output from "runAnalysisOnMC.py 1 0", "runAnalysisOnJetsMC.py 1 0", "runAnalysisData.py 1 0" in a folder called `InName/raw` (this name it is not hardcoded, but it should be the `--inputDir` parameter of the point 2.)
2. run: `python bkg_prepareHistos.py --inputDir InName/raw --outputDir InName`. Now in `InName/hadded` are store the two files needed tor the actual bkg analysis: WToMuNu.root (all the EWK) and Data.root
3. run `python bkg_config.py --mainAna 1 --CFAna 1  --syst 1 --compAna 1 --inputDir InName/hadded/ --outputDir OutName/`. Now inside `OutName` there is the bkg_parameters_CFstatAna.root, the required input for the prefit plotter. In addition there is also final_plots_CFstatAna.root, which containts the validation plots.

For more details about the parameters anche the workflow of bkg_config.py there is a detailed documentation at the beginning of the config