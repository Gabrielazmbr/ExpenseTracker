import pandas as pd
import matplotlib.pyplot as plt
from utils.utils import read_data, confirm
from config import ANALISYS_PATH
import os
from utils import basic as bsc


def show_history():
    goback = bsc.show_selection_bckmenu(2)
    if goback:
        return
    print('Welcome to Show History. Here you can see the expenses submitted.')
    df = read_data()
    see = True
    i = 0
    while see:
        dfi = df.iloc[i:i+10, :]
        if dfi.empty:
            print('There is no more data to show.')
            return
        print(dfi)
        if not df.iloc[i+10:i+20, :].empty:
            more = confirm('See more data (yes/no): ')
            if more:
                i+=10
            else:
                see = False
        else:
            print('There is no more data to show.')
            return

def show_barplots(df:pd.DataFrame, datetime_columns:list):
    cols = [col for col in df.select_dtypes(include=['object', 'category']) if col not in datetime_columns]
    for col in cols:
        vals = df[col].value_counts()
        cats = vals.index
        values = vals.values
        plt.figure(figsize=(8, 12))
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
    goback = bsc.show_selection_bckmenu(3)
    if goback:
        return
    print('Welcome to Expenses Analysis. the following table shows dispersion measures of quantitative columns.')
    if not os.path.exists(f'{ANALISYS_PATH}'):
        os.mkdir(f'{ANALISYS_PATH}')
    df = read_data()
    print('--------------------Quantitative values stats---------------')
    print(df.describe())
    print('')
    print('--------------------Expended total---------------')
    print('')
    total = df['amount'].sum()
    print(f'$ {total:,.2f}')
    print('')
    print('--------------------Expendables by category---------------')
    print('')
    df_by_cat = df.groupby(['category'])['amount'].sum()
    df_by_cat = df_by_cat.apply(lambda x: f'$ {x:,.2f}')
    print(df_by_cat)
    print('')
    datetime_columns = df.select_dtypes(include=['datetime64[ns]']).columns
    inp = input('Plots are going to be opened as soon as you hit enter. Press 0 to abort.')
    if inp==0:
        return

    show_combined_plot(df, datetime_columns)

def show_combined_plot(df, datetime_columns):
    cols = [col for col in df.select_dtypes(include=['object', 'category']) if col not in datetime_columns]

    nrows = len(cols) + 2  # Add 2 more for the line plot and pie chart
    fig, axs = plt.subplots(nrows=nrows, figsize=(10, nrows * 4))  # Adjust figsize as needed
    fig.tight_layout(pad=5.0)  # Add padding between subplots

    # Plot barplots for categorical columns
    for i, col in enumerate(cols):
        vals = df[col].value_counts()
        cats = vals.index
        values = vals.values
        ax = axs[i]  # Select the subplot (axis) for this column
        ax.bar(cats, values)
        ax.set_xlabel('Categories')
        ax.set_ylabel('Count')
        ax.set_title(f'{col}')
        ax.tick_params(axis='x', rotation=90)

    # Plot the line plot for datetime columns
    df_ts = df.groupby(list(datetime_columns))['amount'].mean()
    indx = df_ts.index
    vals = df_ts.values
    ax = axs[len(cols)]  # Next subplot for the line plot
    ax.plot(indx, vals)
    ax.set_xlabel('Date')
    ax.set_ylabel('Mean amount expense')
    ax.set_title('Expenses during time')

    # Plot the pie chart for 'category'
    cat_cals = df['category'].value_counts()
    ax = axs[len(cols) + 1]  # Next subplot for the pie chart
    ax.pie(cat_cals.values, labels=cat_cals.index, autopct='%1.1f%%')
    ax.set_title('Categories Pie Chart')

    # Save the entire figure with all subplots
    plt.savefig(f'{ANALISYS_PATH}/expense_plots_combined.png')
    os.system(f'start {ANALISYS_PATH}/expense_plots_combined.png')
