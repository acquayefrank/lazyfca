# lazyfca

Lazy Learning using FCA: This library does binary classification with attibutes/ features being categorical data 

## Setup Using Conda

> `conda env create --name <NAME OF ENVIRONMETN> --file environment.yml`

## Setup Using Pip

> `pip install -r requirements.txt`

## Experiments

To run experiments use lazy_learning.ipynb

## Known Issues

1. Navigate to src folder to run code else a `FileNotFoundError:` exception will be thrown. If you decide to run code from an arbitrary location, please provide the full path of the file

## Instructions

NB// Actual prediction code is placed within src folder

1. For training, three formatted csv files are expected, positive.csv, negative.csv and test.csv. Note that the last column in each file represents the class(+ve or -ve). This column should be explicitly labeled positive and negative escpecially in test.csv (If this is not done tests will fail) Also the header of this column should be labled Class

2. The file whose actual prediction is to be done is placed in neutral.csv. Remember that each column must be an attribute. Plus an additional empty column for prediction

3. Note that the number of features must much across all csv files

4. For convenience you can just replace the ones in this directory


#### Improvements

* Cross Validation
* Possible tests with other data sources
