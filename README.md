# PretiMeth：precise prediction models for DNA methylation based on single methylation mark

**PretiMeth is a precise computational prediction method of the CpG site-specific methylation level in multiple tissues or cells**, it provides continuous methylation prediction values rather than methylation status and provides an independent accuracy for each CpG locus to allow users to screen high quality models(or CpGs).

The tool currently models and verifies the feasibility of 450K chips and 850K chip sites, and in theory, this method is suitable for whole-genome methylation computational prediction.

![image](https://github.com/JxTang-bioinformatics/PretiMeth/raw/master/images/web_picture0724_2.png)

The diagram of PretiMeth model.

-------------------------------------------------------------------------------------------------------------------------------------

**_Step 1: Before starting_**

The code of PretiMeth has been tested in Windows with Visual studio 2017 and Python 2.7 (and 3.6) and R 3.5.1.

(Finding methylation-similar loci on Visual studio 2017; Prediction on Python 2.7; Normalization for DML analysis on R 3.5.1)

**Note:** The code about finding methylated-similar loci is not a necessary procedure for users to use PretiMeth for prediction.

-------------------------------------------------------------------------------------------------------------------------------------

**_Step 2: QuickStart_**

You will need to download the trained model, source code, required data, extract them and **must locate them in the same directory**.

**For prediction**, you need to download necessary files as fallowing:

Main: https://github.com/JxTang-bioinformatics/PretiMeth/PredictionModel/prediction.py

Parameters of models: https://github.com/JxTang-bioinformatics/PretiMeth/PredictionModel/Parameter1.py
                      https://github.com/JxTang-bioinformatics/PretiMeth/PredictionModel/Parameter2.py

Demo Inputdata(450K): https://github.com/JxTang-bioinformatics/PretiMeth/PredictionModel/GSM2772516-23655.txt

-------------------------------------------------------------------------------------------------------------------------------------

**_Step 3: Analyzing your data_**

Your data should be in the correct format:

1) The given 450K data should be provided as one file (the file name named as you like, but make sure the same name given in prediction.py),

2) The first three columns of the given 450K data file has to be listed in the order of: [ ‘ID_REF’, ‘VALUE’, ‘Detection Pval’],

3) Missing values of the given 450K data file has to be filled with ‘null’ or NA.

In the command(CMD) of windows, you can use the following code to predict using PretiMeth:

python **path**+'/'+prediction.py **path** **InputDataName**

**Note:** 

**path** should be set to your directory with the downloaded PretiMeth necessary files and the files you want to predict. 

**InputDataName** like GSM2772516-23655.txt

-------------------------------------------------------------------------------------------------------------------------------------

**_Step 4: Output_**

In output file, there are two columns, the first column is the CpG ID, and the second column is the predicted methylation value.










