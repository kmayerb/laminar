import pandas as pd


def single_total(iterable):
    
    total = 0
    
    for item in iterable:
        total += int(item)
    
    return total


def multi_tally(pddf):
    
    total = 0
    
    for i in range(len(pddf)):
        if sum(pddf.iloc[i]) > 25:
            total += 1
    
    return total


__df = pd.DataFrame({'Col1': [1, 2, 3, 4, 5], 'Col2': [6, 7, 8, 9, 10], 'Col3': [11, 12, 13, 14, 15]})
__increasing_df = [__df*i for i in range(1, 10)]
laminar_df = pd.concat(__increasing_df)