INPUT_DATA = 'history_data'
EXPENSES_HIST = 'expenses_history.csv'
ANALISYS_PATH = 'analysis_plots'

DEBUG = False
if DEBUG:
    INPUT_DATA = 'test'
    EXPENSES_HIST = 'dummy_data.csv'


FAREWELLS = ["Thank you for using the Expense Tracker. Goodbye!",
            "Your session has ended. See you next time!",
            "Goodbye! Stay on top of your finances!",
            "Thanks for tracking your expenses. Have a great day!",
            "You're all set! See you again soon!",
            "Session closed. Take care and keep track of your spending!",
            "Goodbye, and good luck with your budget!",
            "Thank you for using the tracker. Wishing you a smart financial journey!",
            "Thanks for managing your expenses. See you later!",
            "Your expenses are saved. Goodbye, and stay financially aware!"]


MENU = {1:'Add an expense', 
            2:'See my expense history',
            3:'View expenses summary',
            4: 'Exit!'}