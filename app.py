import sys
import random
from datetime import datetime


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
    

def welcome():
    print('\nWelcome to your Expense Tracker')
    print('----------------------------\n')

    print('Please select an option from the menu')
    menu_pp = ''.join([f'{i[0]}. {i[1]}\n' for i in menu.items()])
    print(menu_pp)
    print('\n')
    
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
    

def input_date_manually():
    correct = False
    while not correct:
        month = input('Input the month of the date of the expense: (1-12) ')
        day = input('Input the day of the date of the expense: (1-31) ')
        year = input('Input the year of the date of the expense: () ')
        try:
            date_usr = datetime.strptime(f'{day}/{month}/{year}', '%d/%m/%Y')
            confirm = input(f'The date input is {date_usr}. Is it correct? (yes/no): ')
            correct = True if confirm.lower() in ['yes', 'y', 'true', 't'] else False
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
        sel = int(input("1. Input the date manually\n2. Today's date.\n"))

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
            amount = int(input('Input the expense amount'))
            print(f'The input expense was ${amount:,.2f}')
            mod = input('Do you want to modify it? (yes/no)')
            incorrect = False
            modify = False if mod.lower() in ['N','n'] else True 
        except ValueError:
            print('Please enter a valid value. ')
            incorrect = True
    return amount

def expense_paymethod():
    methods = {1: 'Credit Card', 2 : 'Debit Card', 3: 'Cash'}
    print('What was the payment method?')
    method = 0
    methods_txt = ''.join([f'{i[0]}. {i[1]}\n' for i in methods.items()])
    while method not in range(1,4):
        method = int(input(methods_txt))
    print(f'The selected method is {methods[method]}')
    
    return methods[method]

def add_expense():
    date_exp = expense_date()
    amount = expense_amount()    
    source = expense_paymethod()
    category = expense_category()
    desc = expense_desc()
    

if __name__ =="__main__":
    welcome()
    selection = get_selection()
    goback = True
    while goback:
        goback = show_selection_bckmenu(selection)
        if 'exit' in menu[selection].lower():
            # select an farewell sentence randomly
            print(farewells[random.randint(0, len(farewells))])
            # exit
            sys.exit()
        elif selection==1:
            add_expense()

        
            



    
    