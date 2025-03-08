import sys
import random
from datetime import datetime
import pandas as pd
import glob
import os
import csv


INPUT_DATA = 'history_data'
EXPENSES_HIST = 'expenses_history.csv'

farewells = ["Thank you for using the Expense Tracker. Goodbye!",
            "Your session has ended. See you next time!",
            "Goodbye! Stay on top of your finances!",
            "Thanks for tracking your expenses. Have a great day!",
            "You're all set! See you again soon!",
            "Session closed. Take care and keep track of your spending!",
            "Goodbye, and good luck with your budget!",
            "Thank you for using the tracker. Wishing you a smart financial journey!",
            "Thanks for managing your expenses. See you later!",
            "Your expenses are saved. Goodbye, and stay financially aware!"]


menu = {1:'Add an expense', 
            2:'See my expense history',
            3:'View expenses summary',
            4: 'Exit!'}

if not os.path.exists(INPUT_DATA):
    os.mkdir(INPUT_DATA)


def welcome():
    print('\nWelcome to your Expense Tracker')
    print('----------------------------\n')

    print('Please select an option from the menu')
    menu_pp = ''.join([f'{i[0]}. {i[1]}\n' for i in menu.items()])
    print(menu_pp)
    
def get_selection()->int:
    """
    Get the user's input number that has to be part of the menu keys. 
    Keeps asking for the selection if the input is invalid.

    Returns:
    selection
        int number

    """
    selection = 0
    while selection not in range(1, len(menu.keys())+1):
        try:
            options = f'1-{len(menu.keys())}'
            selection = int(input(f'Please input the number of the option you want to select ({options}): '))
        except ValueError:
            selection = 0
        print(selection)
        if selection not in range(1, len(menu.keys())+1):
            print('ERROR: Please enter a valid option!')
    return selection

def show_selection_bckmenu(selection:int):
    selection_txt = menu[selection]
    print(f'\n------------{selection_txt}-----------------\n')
    confirm = input('To go back to the previous menu input 0, press enter otherwise.\n')
    return True if confirm=='0' else False
    
def confirm(msg='Do you want to modify it? (yes/no): '):
    modify = input(msg)
    correct = True if modify.lower() in ['yes', 'y', 'true', 't'] or modify==1 else False
    return correct

def input_date_manually():
    correct = False
    while not correct:
        month = input('Input the month of the date of the expense: (1-12) ')
        day = input('Input the day of the date of the expense: (1-31) ')
        year = input('Input the year of the date of the expense: () ')
        try:
            date_usr = datetime.strptime(f'{day}/{month}/{year}', '%d/%m/%Y')
            print(f'The date input is {date_usr}.')
            correct = confirm()
            if correct:
                return date_usr
        except ValueError:
            print(f'The date input is {day}/{month}/{year} and seems to be incorrect. Please'\
                    ' check it and input the date again.')
            correct = False

def expense_date():
    """
    Get the date of the expense. User can input the date by day, month and year, or
    use today's date.

    Returns:
    date_usr:
        datetime
    """
    print('What is the expense date?\n')
    sel = 0
    
    while sel!=1 and sel!=2:
        try:
            sel = int(input("1. Input the date manually\n2. Today's date.\n"))
        except ValueError:
            sel = 0
    
    if sel ==1:
        date_usr = input_date_manually().date()
    elif sel==2:
        date_usr = datetime.today().date()

    return date_usr

def expense_amount():
    incorrect = True
    modify = True
    while incorrect or modify:
        try:
            amount = int(input('Input the expense amount: '))
            print(f'The input expense was: ${amount:,.2f}')
            modify = confirm()
            incorrect = False
            if not modify:
                return amount
        except ValueError:
            print('Please enter a valid value. ')
            incorrect = True

def expense_paymethod():
    methods = {1: 'Credit Card', 2 : 'Savings Card', 3: 'Cash'}
    modify, incorrect = True, True
    methods_txt = ''.join([f'{i[0]}. {i[1]}\n' for i in methods.items()])
    while incorrect or modify:
        print('What was the payment method?')
        try:
            method = int(input(methods_txt))
        except ValueError:
            print('Please select a valid option')
            incorrect = True
            continue
        try:
            print(f'The selected method is: {methods[method]}')
            modify = confirm()
            incorrect = False
            if not modify:
                return methods[method]
        except KeyError:
            print('Please select a valid option')
            incorrect = True

def read_data(col):
    files = glob.glob(f'{INPUT_DATA}/{EXPENSES_HIST}.csv')
    try:
        df = pd.read_csv(files[0])
        return df[col].unique()
    except IndexError:
        return

def add_category(categories=None):
    modify = True
    if categories is None:
        categories = []
    while modify:
        new_cat = input('Enter a new category: ')
        print(f'The new category is: {new_cat}')
        modify = confirm()
        if not modify:
            categories.append(new_cat)
            return new_cat, categories


def select_or_add_cat(categories):
    cat_menu = {1:'Add a new category', 2: 'Select a category'}
    cat_menu_txt = ''.join([f'{i[0]}. {i[1]}\n' for i in cat_menu.items()]) 
    sel = 0 
    while sel not in range(1,3):
        print(cat_menu_txt)
        sel = int(input('Select an option'))
        if sel not in range(1,3):
            sel = 0
    if sel ==1:
        return add_category(categories)
    elif sel==2:
        category = select_category(categories)
        return category, categories

def select_category(categories):
    modify = True
    while modify:
        cats_sels = {n+1:i for n,i in enumerate(categories)}
        cats_sels_txt = ''.join([f'{i[0]}. {i[1]}\n' for i in cats_sels.items()])
        cat_num = int(input(cats_sels_txt))
        print(f'The selected category is: {cats_sels[cat_num]}')
        modify = confirm()
        if not modify:
            return cats_sels[cat_num]

def read_categories_file():
    try:
        with open(f'{INPUT_DATA}/categories.txt', 'r') as f:
            data = f.readlines()
    except FileNotFoundError:
        data = None
    return data

def expense_category():
    categories = read_categories_file()
    if categories is None:
        category, categories = add_category()
    else:
        category, categories = select_or_add_cat(categories)
    save_categories(categories)
    return category

def save_categories(cats):
    file = f'{INPUT_DATA}/categories.txt'
    exists = os.path.exists(file)
    if exists:
        mode='a'
    else:
        mode='w'
    with open(file, mode) as f:
        f.writelines([cat+'\n' for cat in cats])

    print('Categories updated successfully!')

def expense_desc():
    desc = input('Add a description: (optional) ')
    return desc

def add_expense():
    date_exp = expense_date()
    amount = expense_amount()    
    source = expense_paymethod()
    category = expense_category()
    desc = expense_desc()
    data = {'date_exp':date_exp,
             'amount':f'{amount:,.2f}',
             'source':source,
             'category':category,
             'desc':desc}

    input_summary(data)

def input_summary(data:dict):
    print('Input expense details...\n')
    tags = {'date_exp':'Expense Date', 
    'amount':'Amount(US$): ', 
    'source':'Payment Method', 
    'category':'Category', 
    'desc':'Description'}
    data_txt = ''.join([f'{tags[i[0]]}: {i[1]}\n' for i in data.items()])
    print(data_txt)
    save = confirm('Do you want to save the record with this info? (yes/no)')
    if save:
        new_expense(data)

def new_expense(data):
    path = f'{INPUT_DATA}/{EXPENSES_HIST}'
    data = list(data.values())
    if not os.path.exists(path):
        mode = 'w'
        data.insert(0, ['date_exp','amount','source','category','desc'])
    else:
        mode = 'a'
    with open(path, mode=mode, newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

if __name__ =="__main__":
    goback = True
    while goback:
        welcome()
        selection = get_selection()
        goback = show_selection_bckmenu(selection)
        if goback:
            continue
        if 'exit' in menu[selection].lower():
            # select an farewell sentence randomly
            print(farewells[random.randint(0, len(farewells))])
            # exit
            sys.exit()
        elif selection==1:
            add_expense()

        
            



    
    