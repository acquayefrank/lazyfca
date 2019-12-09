# lazyfca

Lazy Learning using FCA: This library does binary classification with attibutes/ features being categorical data 

## Setup Using Conda

> `conda env create --name <NAME OF ENVIRONMETN> --file environment.yml`

## Setup Using Pip

> `pip install -r requirements.txt`

## Exeriments

To run experiments use lazy_learning.ipynb

## Instructions

NB// Actual prediction code is placed within src folder

1. For training, three formatted csv files are expected, positive.csv, negative.csv and test.csv. Note that the last column in each file represents the class(+ve or -ve).

2. The file whose actual prediction is to be done is placed in neutral.csv. Remember that each column must be an attribute. Plus an additional empty column for prediction

3. Note that the number of features must much across all csv files

4. For convenience you can just replace the ones in this directory


#### TODO

* Precesion
* Recall
* F1 Score
* Cross Validation
* Report
* Possible tests with other data sources
* Actual Prediction Function
