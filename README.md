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

`laminar.iter_flow` is designed to work with a single iterable, such as a pandas DataFrame or a list. When you pass an iterable to `laminar.iter_flow`, it will automatically break your data up into chunks based on how many cores your machine has. It then queues up each chunk to be given to a core, which performs the work, then passes the data back, where it is recombined to give one result. For example, a list of 1,000,000 integers is broken into chunks of length 250,000 on a machine with four cores. Each chunk is summed by a core, the results from each core are returned in a list of length N = # cores. You are then able to combine the results in whatever way fits the computation that you need. For example, if the function passed to `laminar.iter_flow` computes the sum, then the results list should be summed to produce a total for the entire iterable.
