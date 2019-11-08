import pandas as pd


def single_total(iterable, odd=False):
    """This example function sums the data contained in a single iterable, i.e.
    a list, tuple, set, pd.Series, etc.
    
    Args:
        iterable (list, tuple, set, pd.Series, etc): Any iterable that holds data
            that can be added together.
            
    Returns:
        total (int): Sum of passed iterable.
    """
    
    total = 0
    
    for item in iterable:
        if odd:
            if item % 2 != 0:
                total += int(item)
        else:
            total += int(item)
    
    return total


def multi_tally(pddf):
    """This example function sums each row of a Pandas DataFrame, then increases
    the total count if the sum is greater than 25.
    
    Args:
        pddf (:obj: pd.DataFrame): Pandas DataFrame. laminar_examples.laminar_df
            may be used as an example. It contains 3 columns ['Col1', 'Col2', 'Col3'],
            each of which contains integer values.
            
    Returns:
        total (int): Number of rows in pddf that summed to greater than 25.
        
    """
    
    total = 0
    
    for i in range(len(pddf)):
        if sum(pddf.iloc[i]) > 25:
            total += 1
    
    return total


__df = pd.DataFrame({'Col1': [1, 2, 3, 4, 5], 'Col2': [6, 7, 8, 9, 10], 'Col3': [11, 12, 13, 14, 15]})
__increasing_df = [__df*i for i in range(1, 10)]
laminar_df = pd.concat(__increasing_df)
laminar_df.reset_index(drop=True, inplace=True)
iris = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')