import sys
import random
from datetime import datetime
import pandas as pd
import glob
import os
import csv
from config import INPUT_DATA, EXPENSES_HIST, FAREWELLS, MENU, ANALISYS_PATH
from utils import expense_mgmt as exp 
from utils.utils import confirm
from utils.expense_mgmt import new_expense
from utils import analysis
from utils import basic as bsc

if not os.path.exists(INPUT_DATA):
    os.mkdir(INPUT_DATA)



def expense_desc():
    desc = input('Add a description: (optional) ')
    return desc

def add_expense():
    goback = bsc.show_selection_bckmenu(1)
    if goback:
        return
    print('Welcome to add expense. To add a new expense input the data required.')
    date_exp = exp.expense_date()
    amount = exp.expense_amount()    
    source = exp.expense_paymethod()
    category = exp.expense_category()
    desc = expense_desc()
    data = {'date_exp':date_exp.strftime('%m/%d/%Y'),
             'amount':amount,
             'source':source,
             'category':category,
             'desc':desc}

    input_summary(data)
    save = confirm('Do you want to save the record with this info? (yes/no)')
    if save:
        new_expense(data)
    return

def input_summary(data:dict):
    print('Input expense details...\n')
    tags = {'date_exp':'Expense Date', 
    'amount':'Amount(US$): ', 
    'source':'Payment Method', 
    'category':'Category', 
    'desc':'Description'}
    data_txt = ''.join([f'{tags[i[0]]}: {i[1]}\n' for i in data.items()])
    print(data_txt)
    
def read_history():
    path = f'{INPUT_DATA}/{EXPENSES_HIST}'
    return pd.read_csv(path, index_col=0)


if __name__ =="__main__":
    goback = True
    while goback:
        bsc.welcome()
        selection = bsc.get_selection()
        if 'exit' in MENU[selection].lower():
            # select an farewell sentence randomly
            print(FAREWELLS[random.randint(0, len(FAREWELLS)-1)])
            # exit
            sys.exit()
        elif selection==1:
            add_expense()
        elif selection==2:
            analysis.show_history()
        elif selection==3:
            analysis.expenses_analysis()
        
        if goback:
            continue
    print(FAREWELLS[random.randint(0, len(FAREWELLS)-1)])
            



    
    
