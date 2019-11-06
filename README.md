# PretiMeth：precise prediction models for DNA methylation based on single methylation mark

**PretiMeth is a precise computational prediction method of the CpG site-specific methylation level in multiple tissues or cells**, it provides continuous methylation prediction values rather than methylation status and provides an independent accuracy for each CpG locus to allow users to screen high quality models(or CpGs).

The tool currently models and verifies the feasibility of 450K chips and 850K chip sites, and in theory, this method is suitable for whole-genome methylation computational prediction.

![image](https://github.com/JxTang-bioinformatics/PretiMeth/raw/master/images/web_picture0724_2.png)

The diagram of PretiMeth model.

-------------------------------------------------------------------------------------------------------------------------------------

**_Step 1: Before starting_**

The code of PretiMeth has been tested in Windows with Visual studio 2017, Python 2.7 (and 3.6) and R 3.5.1.

(Finding methylation-similar loci on Visual studio 2017; Prediction on Python 2.7; Normalization for DML analysis on R 3.5.1)

**Note:** The code about finding methylated-similar loci is not a necessary procedure for users to use PretiMeth for prediction.

-------------------------------------------------------------------------------------------------------------------------------------

**_Step 2: QuickStart_**

You will need to download the trained model, source code, required data, extract them and **must locate them in the same directory**.

**For prediction**, you need to download necessary files as fallowing:

Main: https://github.com/JxTang-bioinformatics/PretiMeth/PredictionModel/prediction.py

Parameters of models: https://github.com/JxTang-bioinformatics/PretiMeth/PredictionModel/Parameter1.txt,
                      https://github.com/JxTang-bioinformatics/PretiMeth/PredictionModel/Parameter2.txt and 
                      https://github.com/JxTang-bioinformatics/PretiMeth/PredictionModel/logits_CV5_Evaluation.txt

Demo Inputdata(450K): https://github.com/JxTang-bioinformatics/PretiMeth/PredictionModel/GSM2772516-23655.txt

-------------------------------------------------------------------------------------------------------------------------------------

**_Step 3: Analyzing your data_**

Your data should be in the correct format:

1) The first three columns of the given 450K data file has to be listed in the order of: [ ‘ID_REF’, ‘VALUE’, ‘Detection Pval’],

2) Missing values of the given 450K data file has to be filled with ‘null’ or NA.

In the **_command(CMD)_** of windows, you can use the following code to use PretiMeth:

python **path(user settings)**/prediction.py **path(user settings)** **InputDataName(user settings)**

Just like: 

![image](https://github.com/JxTang-bioinformatics/PretiMeth/raw/master/images/cmd_demo.png)

**Note:** 

**path** should be set to your directory with the downloaded PretiMeth necessary files and the InputData. 

**InputDataName** like GSM2772516-23655.txt

-------------------------------------------------------------------------------------------------------------------------------------

**_Step 4: Output_**

In output file, there are nine columns, the first column is the CpG ID, the second column is the predicted methylation value, and the remaining other columns are the evaluation results of cross-validation for the corresponding CpG locus, which can be used to indicate the accuracy of the predicted result of the CpG locus.

-------------------------------------------------------------------------------------------------------------------------------------

You can also use PretiMeth by visiting one of our other websites via http://114.115.170.196/PretiMeth.






