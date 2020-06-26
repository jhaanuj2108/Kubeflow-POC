# The data set used in this example is from http://archive.ics.uci.edu/ml/datasets/Wine+Quality
import os
import warnings
import sys

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import argparse

import logging
logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2



def my_model(args):

    alpha = args.alpha
    l1_ratio = args.l1_ratio
    
    warnings.filterwarnings("ignore")
    np.random.seed(40)

    # Read the wine-quality csv file from the URL
    csv_url =\
        'http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv'
    try:
        data = pd.read_csv(csv_url, sep=';')
    except Exception as e:
        logger.exception(
            "Unable to download training & test CSV, check your internet connection. Error: %s", e)

    # Split the data into training and test sets. (0.75, 0.25) split.
    train, test = train_test_split(data)

    # The predicted column is "quality" which is a scalar from [3, 9]
    train_x = train.drop(["quality"], axis=1)
    test_x = test.drop(["quality"], axis=1)
    train_y = train[["quality"]]
    test_y = test[["quality"]]



    lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
    lr.fit(train_x, train_y)

    predicted_qualities = lr.predict(test_x)

    (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

    print('{}={}'.format("rmse", rmse))
            
            
if __name__ == '__main__':

    # This python script will be our MAIN entrypoint, hence parsing here the command line arguments.
    parser = argparse.ArgumentParser(description="Training my_model()",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--alpha', type=float, default=0.5,
                    help='Alpha value')
    parser.add_argument('--l1_ratio', type=float, default=0.5,
                    help='l1_ratio')


    args = parser.parse_args()
    my_model(args)
