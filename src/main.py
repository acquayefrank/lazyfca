from collections import OrderedDict
from itertools import combinations
from datetime import datetime
import pandas as pd
import click


def read_csv(file_name):
    """
    Read input file and return dataframe object
    """
    df = pd.read_csv(file_name)
    return df

def compute_support(data_frame, headers):
    value_list = data_frame.groupby(headers).size().keys().tolist()
    count_list = data_frame.groupby(headers).size().tolist()

    values = [value if isinstance(value, tuple) else (value,) for value in value_list]
    counts = [count/len(data_frame) for count in count_list]

    results = dict(zip(values, counts))
    return results


def yield_colums(data_frame):
    columns = data_frame.columns[:-1] #eliminating label header
    for index, _ in enumerate(columns, start=1):
        for col in combinations(columns, index):
            yield col


def generate_support(data_frame):
    response_dict = {}
    for col in yield_colums(data_frame):
        response_dict[col] = compute_support(data_frame, list(col))
    return response_dict


def aggregation(df_positive, df_negative, threshold=0.2):

    positive_support = generate_support(df_positive)
    negative_support = generate_support(df_negative)
    positive = OrderedDict()
    for col in yield_colums(df_positive):
        try:
            res = {key: abs(positive_support[col][key] - negative_support[col].get(key, 0)) 
                            for key in negative_support[col].keys()} 
        except KeyError:
            res = {}
        positive.update({col: res})

    for key in yield_colums(df_positive):
        for k in list(positive[key]): 
            if positive[key][k]<= threshold:
                del positive[key][k]

    return positive


def predict(model, data_frame):
    pass


if __name__ == "__main__":
    now = datetime. now()
    current_time = now.strftime("%H:%M:%S")
    print("lazy learner ", current_time)
    print("Follow the instructions below, enter blank for defaults:")

    positive = click.prompt(
                "\nEnter the name of the positive file (e.g positive.csv): ", 
                type=str, 
                default='positive.csv'
                )
    negative = click.prompt(
                "\nEnter the name of the negative file (e.g negative.csv): ", 
                type=str, 
                default='negative.csv'
                )
    test = click.prompt(
                "\nEnter the name of the test file (e.g test.csv): ", 
                type=str, 
                default='test.csv'
                )
    neutral = click.prompt(
                "\nEnter the name of the neutral file (e.g neutral.csv): ", 
                type=str, 
                default='neutral.csv'
                )

    df_positive = read_csv(positive)
    df_negative = read_csv(negative)
    df_test = read_csv(test)
    df_neutral = read_csv(neutral)

    model = aggregation(df_positive, df_negative)
    

