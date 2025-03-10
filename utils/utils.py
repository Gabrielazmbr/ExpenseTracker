from config import INPUT_DATA, EXPENSES_HIST
import pandas as pd



def read_data():
    files = f'{INPUT_DATA}/{EXPENSES_HIST}'
    df = pd.read_csv(files)
    for col in df.columns:
        if 'date' in col.lower():
            df[col] = pd.to_datetime(df[col])
    return df


def confirm(msg='Do you want to modify it? (yes/no): '):
    modify = input(msg)
    correct = True if modify.lower() in ['yes', 'y', 'true', 't'] or modify==1 else False
    return correct