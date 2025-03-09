from config import MENU

def welcome()->None:
    """
    Pretty prints the menu for the user.
    """
    print('\nWelcome to your Expense Tracker')
    print('----------------------------\n')

    print('Please select an option from the menu')
    menu_pp = ''.join([f'{i[0]}. {i[1]}\n' for i in MENU.items()])
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
    while selection not in range(1, len(MENU.keys())+1):
        try:
            options = f'1-{len(MENU.keys())}'
            selection = int(input(f'Please input the number of the option you want to select ({options}): '))
        except ValueError:
            selection = 0
        print(selection)
        if selection not in range(1, len(MENU.keys())+1):
            print('ERROR: Please enter a valid option!')
    return selection

def show_selection_bckmenu(selection:int, msg='To go back to the previous menu input 0, press enter otherwise.\n'):
    
    selection_txt = MENU[selection]
    print(f'\n------------{selection_txt}-----------------\n')
    confirm = input(msg)
    return True if confirm=='0' else False
    
