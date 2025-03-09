import pandas as pd
import matplotlib.pyplot as plt
from utils.utils import read_data, confirm
from config import ANALISYS_PATH
import os


def show_history():
    df = read_data()
    see = True
    i = 0
    while see:
        dfi = df.iloc[i:i+10, :]
        if dfi.empty:
            return
        print(dfi)
        more = confirm('See more data (yes/no): ')
        if more:
            i+=10
        else:
            see = False

def show_barplots(df:pd.DataFrame, datetime_columns:list):
    cols = [col for col in df.select_dtypes(include=['object', 'category']) if col not in datetime_columns]
    for col in cols:
        vals = df[col].value_counts()
        cats = vals.index
        values = vals.values
        plt.figure(figsize=(12, 15))
        plt.bar(cats, values)
        plt.xlabel('Categories')
        plt.ylabel('Count')
        plt.title(f'{col}')
        plt.xticks(rotation=90)
        plt.savefig(f'{ANALISYS_PATH}/expense_plot_{col}.png')
        os.system(f'start {ANALISYS_PATH}/expense_plot_{col}.png')

def show_date_line(df, datetime_columns):
    df_ts = df.groupby(list(datetime_columns))['amount'].mean()
    indx = df_ts.index
    vals = df_ts.values
    plt.figure()
    plt.plot(indx, vals)
    plt.xlabel('Date')
    plt.ylabel('Mean amount expense')
    plt.title('Expenses during time')
    plt.savefig(f'{ANALISYS_PATH}/expense_plot_date.png')
    os.system(f'start {ANALISYS_PATH}/expense_plot_date.png')

def show_pie_plot(df, cat_col):
    cat_cals = df[cat_col].value_counts()
    plt.figure()
    plt.pie(cat_cals.values, labels=cat_cals.index)
    plt.savefig(f'{ANALISYS_PATH}/categories_pieplot.png')
    os.system(f'start {ANALISYS_PATH}/categories_pieplot.png')

def expenses_analysis():
    if not os.path.exists(f'{ANALISYS_PATH}'):
        os.mkdir(f'{ANALISYS_PATH}')
    df = read_data()
    print('--------------------Quantitative values stats---------------')
    print(df.describe())
    datetime_columns = df.select_dtypes(include=['datetime64[ns]']).columns
    input('Plots are going to be opened as soon as you hit enter.')
    show_barplots(df, datetime_columns)
    show_date_line(df, datetime_columns)
    show_pie_plot(df, 'category')