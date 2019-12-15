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


def predict(model, data, columns):
    prediction = 'negative'
    for attribute in model:
        row = [data[key] for key in attribute]
        attributes =[list(support) for support in model[attribute]]
        for element in row:
            for attr in attributes:
                if element in attr:
                    prediction = 'positive'
    return prediction


def test_model(model, data_frame):
    columns = list(data_frame.columns)

    accuracy = 0
    recall = 0
    precision = 0
    F1 = 0

    true_positives = 0
    false_negatives = 0
    false_positives = 0
    number_of_correct_predictions = 0

    total_number_of_predictions = len(data_frame)
    for index, row in data_frame.iterrows():
        prediction = predict(model, row, columns)

        if prediction == row.Class:
            number_of_correct_predictions += 1
        
        if row.Class == 'positive' and prediction == 'positive':
            true_positives += 1

        if row.Class == 'positive' and prediction == 'negative':
            false_negatives += 1

        if row.Class == 'negative' and prediction == 'positive':
            false_positives += 1

    accuracy = number_of_correct_predictions/total_number_of_predictions
    t_p_plus_f_n = true_positives + false_negatives
    t_p_plus_f_p = true_positives +false_positives

    if t_p_plus_f_n:
        recall = true_positives/t_p_plus_f_n
    
    if t_p_plus_f_p:
        precision = true_positives/t_p_plus_f_p

    p_plus_r = precision + recall

    if p_plus_r:
        F1 = 2 * (precision * recall) / p_plus_r

    click.echo('accuracy = {}'.format(round(accuracy, 2)))
    click.echo('recall = {}'.format(round(recall, 2)))
    click.echo('precision = {}'.format(round(precision, 2)))
    click.echo('F1 Score = {}'.format(round(F1, 2)))
    click.echo("If you're happy with the test results run the script again with the flag --predict, else tweak the threshold for better results")


def make_predictions(model, data_frame):
    columns = list(data_frame.columns)
    for index, row in data_frame.iterrows():
        prediction = predict(model, row, columns)
        data_frame.at[index,'Class'] = prediction
    data_frame.to_csv('neutral.csv', index=False)


@click.command()
@click.option('--predict/--no-predict', default=False)
def main(predict):
    now = datetime. now()
    current_time = now.strftime("%H:%M:%S")
    click.echo("lazy learner  {}".format(current_time))
    click.echo("Follow the instructions below, enter blank for defaults:")

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

    if predict:
        make_predictions(model, df_neutral)
        click.echo("check neutral.csv file for results")
    else:
        test_model(model, df_test)


if __name__ == "__main__":
    main()
    

