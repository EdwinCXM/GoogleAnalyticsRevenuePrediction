from matplotlib import pylab
import calendar
import numpy as np
import pandas as pd
import seaborn as sn
from scipy import stats
import missingno as msno
from datetime import datetime
import matplotlib.pyplot as plt
import warnings
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import json


def json_to_series(text):
    """
    Convert json string to a series of columns for pandas
    :param text: json string
    :return:
    """
    keys, values = zip(*[item for dct in json.loads(text) for item in dct.items()])
    return pd.Series(values, index=keys)


def degree_search(df, dep, highest_degree=5):
    """
    :param df: dataframe with numerical columns and the dependent variable column
    :param highest_degree: upper bound of degree when doing degree search
    :param dep: column name of dependent variable
    :return: df: original dataframe with columns to the power of optimal degree
    :return: degree_list: dictionary of degrees for columns
    """
    degree_dict = {}
    for col in df.columns:

        if col != dep:
            deg_scores = []
            for deg in range(1, highest_degree+1):
                x1 = df[[col]]**deg
                y1 = df[dep]
                reg = LinearRegression().fit(x1, y1)
                deg_scores.append(reg.score(x1, y1))
                print(deg_scores)
            df[col] = df[col]**(np.asarray(deg_scores).argmax()+1)
            degree_dict[col] = np.asarray(deg_scores).argmax()+1

    return df, degree_dict


def polynomial_search(x, y, highest_degree=3):
    """
    :param df: dataframe with numerical columns and the dependent variable column
    :param highest_degree: upper bound of degree when doing degree search
    :param dep: column name of dependent variable
    :return: df: original dataframe with columns to the power of optimal degree
    :return: degree_list: dictionary of degrees for columns
    """
    degree_dict = {}

    deg_scores = []
    for deg in range(1, highest_degree+1):
        poly = PolynomialFeatures(deg)
        x1 = poly.fit_transform(X=x)
        reg = LinearRegression().fit(x1, y)

        degree_dict[deg] = reg.score(x1, y)

    return degree_dict