# PretiMeth：precise prediction models for DNA methylation based on single methylation mark

**PretiMeth is a precise computational prediction method of the CpG site-specific methylation level in multiple tissues or cells**, it provides continuous methylation prediction values rather than methylation status and provides an independent accuracy for each CpG locus to allow users to screen high quality models(or CpGs).

The tool currently models and verifies the feasibility of 450K chips and 850K chip sites, and in theory, this method is suitable for whole-genome methylation computational prediction.

![image](https://github.com/JxTang-bioinformatics/PretiMeth/raw/master/images/web_picture0724_2.png)

The diagram of PretiMeth model.

**Installation:**

Download PretiMeth by

https://github.com/JxTang-bioinformatics/PretiMeth/PredictionModel/prediction.py


**_Before starting_**
The code of PretiMeth has been tested in Windows with Visual studio 2017 and Python 2.7 (and 3.6) and R 3.5.1.
(Finding methylation-similar loci on Visual studio 2017; Prediction on Python 2.7; Normalization for DML analysis on R 3.5.1)
**Note:** The code of finding methylated-similar loci is not a necessary procedure for users to use PretiMeth for prediction.


**_QuickStart_**
You will need to download the trained model, source code, required data, extract them and **must locate them in the same directory**.
**For prediction**, you need to download necessary files as fallowing:
Main: https://github.com/JxTang-bioinformatics/PretiMeth/PredictionModel/prediction.py
Parameters of models: https://github.com/JxTang-bioinformatics/PretiMeth/PredictionModel/Parameter1.py
                      https://github.com/JxTang-bioinformatics/PretiMeth/PredictionModel/Parameter2.py

If
