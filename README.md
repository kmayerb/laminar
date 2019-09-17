# laminar
Laminar seeks to take most of the effort out of parallel processing in Python by providing user-friendly parallelization functions.

## Usage
### Requirements
laminar requires the numpy package to be installed in your working environment. laminar's companion module, laminar_examples.py, requires pandas.
While in your desired environment, simply enter: 

`pip install pandas`  
-or-  
`conda install pandas`  

in order to install both numpy and pandas into your environment. (numpy is a dependency of pandas and both will be downloaded together when you install pandas).

### Importing
You can use laminar by placing laminar.py in your project directory, then putting `import laminar` at the top of any file that you wish to use it in.  
In order to practice/test laminar with built-in functions and data, place `import laminar_examples` at the top of your python file.

### Using laminar
laminar currently consists of two functions that are designed to work with different data configurations, `laminar.iter_flow` and `laminar.list_flow`.

`laminar.iter_flow` is designed to work with a single iterable, such as a pandas DataFrame or a list. When you pass an iterable to `laminar.iter_flow`, it will automatically break your data up into chunks based on how many cores your machine has. It then queues up each chunk to be given to a core, which performs the work, then passes the data back, where it is recombined to give one result. For example, a list of 1,000,000 integers is broken into chunks of length 250,000 on a machine with four cores. Each chunk is summed (as an example) by a core, and the results from each core are returned in a dict of size N = # cores. You are then able to combine the results in whatever way fits the computation that you need. For example, if the function passed to `laminar.iter_flow` computes the sum, then the values in the results dict should be summed to produce a total for the entire iterable.

### Examples
To illustrate how one would use laminar in their workflow, we'll use some premade functions and data structures located in `laminar_examples`.

#### laminar_examples.single_total 
`laminar_examples.single_total` is a simple function that accepts a single iterable and returns the sum total of the values in that iterable. `laminar_examples.single_total([1, 2, 1])` returns `4`.

#### laminar_examples.multi_tally 
`laminar_examples.multi_tally` is a simple funtion that accepts a Pandas DataFrame and returns the number of rows that sum to greater than 25. `laminar_examples.multi_tally(pd.DataFrame({'Col1': [12, 12], 'Col2': [12, 14]})` returns `1` because the row at index 1 sums to `12 + 14 = 26`, which meets the function's criteria, but the row at index 0 sums to `12 + 12 = 24`, which does not.

#### laminar_examples.laminar_df
`laminar_examples.laminar_df` is a Pandas DataFrame that constitutes 3 columns ['Col1', 'Col2', 'Col3'], each of which contains different integer values.

| Col1 | Col2 | Col3 |
|:----:|:----:|:----:|
|1|6|11|
|2|7|12|
|3|8|13|
|4|9|14|
|5|10|15|
|2|12|22|
|4|6|16|
|...|...|...|

#### Example 1: Single iterable, single_total()
`laminar.iter_flow(laminar_examples.single_total, laminar_examples.laminar_df['Col1'])` returns `{'data[0-5]': 17,
 'data[12-17]': 60,
 'data[18-23]': 86,
 'data[24-29]': 115,
 'data[30-34]': 105,
 'data[35-39]': 120,
 'data[40-44]': 135,
 'data[6-11]': 37}`, which is a dictionary describing the results for each section of your data. Each key/value pair in the returned dict corresponds to a segment of the iterable that was broken out and given to a process, with the key containing which portion of the data the result matches to. To complete your analysis, you can use whichever function coincides with the intended behavior of your analysis. In this case, since we are summing values, we can use `sum()`.

The end result can look like one of these examples, although it doesn't have to:
`result = sum(laminar.iter_flow(laminar_examples.single_total, laminar_examples.laminar_df['Col1']).values())`

or

`result = laminar.iter_flow(laminar_examples.laminar_df['Col1'], laminar_examples.single_total)`

`result = sum(result.values())`

where

`result = 675`


#### Example 2: Pandas DataFrame, multi_tally()
`laminar.iter_flow(laminar_examples.multi_tally, laminar_examples.laminar_df)` returns
`{'data[0-5]': 3,  
 'data[12-17]': 6,  
 'data[18-23]': 6,  
 'data[24-29]': 6,  
 'data[30-34]': 5,  
 'data[35-39]': 5,  
 'data[40-44]': 5,  
 'data[6-11]': 6}`,  
 which is a dict of counts. Each count is the return value for a segment of the data that was broken out and given to a process. To complete your analysis, you can use whichever function coincides with the intended behavior of your analysis. In this case, since we are counting values, it makes sense to use `sum()`.

The end result can look like one of these examples, although it doesn't have to:  
`result = sum(laminar.iter_flow(laminar_examples.laminar_df, laminar_examples.multi_tally))`  

or

`result = laminar.iter_flow(laminar_examples.laminar_df, laminar_examples.multi_tally)`

`result = sum(result)`

where

`result = 42`


#### Example 3: List of single iterables, single_total()
`laminar.list_flow([laminar_examples.laminar_df[col] for col in laminar_examples.laminar_df.columns], laminar_examples.single_total)` returns `[675, 1800, 2925]`, which is a list of the totals for each column. With this usage, a user can pass a list of iterables to `list_flow`; each iterable will be passed to its own process. This is useful for when a user intends to use the same function on multiple iterables, which can be columns in the same DataFrame, or independent lists.

`columns_list = [laminar_examples.laminar_df[col] for col in laminar_examples.laminar_df.columns]`

`result = laminar.list_flow(columns_list, laminar_examples.single_total)`

where

`result = [675, 1800, 2925]`


#### Example 4: List of Pandas DataFrames, multi_tally()
`laminar.list_flow([laminar_examples.laminar_df]*3, laminar_examples.multi_tally)` returns `[42, 42, 42]`. The result values are the same because we passed a list of 3 identical DataFrames; feel free to test this with different DataFrames of your own making.

`data_frames_list = [laminar_examples.laminar_df]*3`

`result = laminar.list_flow(data_frames_list, laminar_examples.multi_tally)`

where

`result = [42, 42, 42]`

### Final Notes
Which laminar tool a user will use depends on the structure of their data and the function that will be applied to that data. `laminar.list_flow` is not confined to operating on Pandas DataFrames; any list of data objects can be passed to list_flow.

A basic rule of thumb is to use `laminar.iter_flow` for a single data object that one wishes to break into pieces in order to process it faster. `laminar.list_flow` is to be used in a situation where the user has multiple data objects that he or she wishes to be analyzed by the same function in parallel.
