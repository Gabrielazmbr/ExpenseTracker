from datetime import datetime
from utils.utils import confirm
from config import INPUT_DATA, EXPENSES_HIST
import csv
import os


def read_categories_file():
    try:
        with open(f'{INPUT_DATA}/categories.txt', 'r') as f:
            data = f.readlines()
        return [i.replace('\n','') for i in data]
    except FileNotFoundError:
        data = None
        return data

def new_expense(data):
    path = f'{INPUT_DATA}/{EXPENSES_HIST}'
    if not os.path.exists(path):
        mode = 'w'
        all_data = []
        all_data.append(list(data.keys()))
        all_data.append(list(data.values()))
    else:
        mode = 'a'
        all_data = [data.values()]
    with open(path, mode=mode, newline='') as file:
        writer = csv.writer(file)
        for row in all_data:
            writer.writerow(row)

def save_categories(new_cat):
    file = f'{INPUT_DATA}/categories.txt'
    exists = os.path.exists(file)
    cats_ex = read_categories_file()
    mode ='a' if exists else 'w'
    if cats_ex is None or new_cat not in cats_ex or not exists:
        cats = [new_cat]
    with open(file, mode) as f:
        f.writelines([cat+'\n' for cat in cats])
        print('Categories updated successfully!')

def input_date_manually():
    correct = False
    while not correct:
        month = input('Input the month of the date of the expense: (1-12) ')
        day = input('Input the day of the date of the expense: (1-31) ')
        year = input('Input the year of the date of the expense: () ')
        try:
            date_usr = datetime.strptime(f'{day}/{month}/{year}', '%d/%m/%Y')
            print(f'The input date is {date_usr.date()}')
            modify = confirm()
            if not modify:
                return date_usr
        except ValueError:
            print(f'The date input is {day}/{month}/{year} and seems to be incorrect. Please'\
                    ' check it and input the date again.')
            correct = False

def expense_category():
    categories = read_categories_file()
    if categories is None:
        category, categories = add_category()
    else:
        category, categories = select_or_add_cat(categories)
    save_categories(category)
    return category

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



def add_category(categories=None):
    modify = True
    if categories is None:
        categories = []
    while modify:
        new_cat = input('Enter a new category: ')
        if new_cat!='':
            print(f'The new category is: {new_cat}')
            modify = confirm()
            if not modify:
                categories.append(new_cat)
                return new_cat, categories


def select_or_add_cat(categories):
    cat_menu = {1:'Add a new category', 2: 'Select a category'}
    cat_menu_txt = ''.join([f'{i[0]}. {i[1]}\n' for i in cat_menu.items()]) 
    sel = 0 
    goback = True
    while sel not in range(1,len(cat_menu)+1) or goback:
        print('\nExistent categories:\n'+cat_menu_txt)
        try:
            sel = int(input('Please select an option\n'))
        except ValueError:
            sel=0
            print('Please select a valid option.')
            continue
        if sel not in range(1,len(cat_menu)+1):
            sel = 0
            continue
        if sel ==1:
            category, categories = add_category(categories)
            return category, categories
        elif sel==2:
            category = select_category(categories)
            if category is None:
                goback = True
            else:
                goback = False
                return category, categories


def select_category(categories):
    modify = True
    while modify:
        cats_sels = {n+1:i for n,i in enumerate(categories)}
        cats_sels_txt = ''.join([f'{i[0]}. {i[1]}\n' for i in cats_sels.items()])
        try:
            cat_num = int(input(cats_sels_txt+'\nOr press 0 to go back to the previous menu'))
        except ValueError:
            modify = True
            continue
        if cat_num==0:
            return
        print(f'The selected category is: {cats_sels[cat_num]}')
        modify = confirm()
        if not modify:
            return cats_sels[cat_num]