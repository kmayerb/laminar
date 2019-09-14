from multiprocessing import Queue, Process, cpu_count

import numpy as np


def __converter(function, data_shard, queue, *args):
    """Module function that calls the passed function with the passed data_shard
    as an argument, then places the result in the queue.
    
    Args:
        function: Function object the user wishes to parallelize.
        queue: Multiprocessing queue that holds process results.
        data_shard: Data object that is a subset of the master data object passed
            to the laminar function.
            
    Returns:
        None
        
    """
    
    kwargs, args = args[-1], args[0]
    
    result = function(data_shard, *args, **kwargs)
    
    queue.put(result)


def iter_flow(function, data, *args, **kwargs):
    """Parallelization function that is intended to break up an iterable into data shards,
    then analyze each data shard in parallel. Returns a list of results from each
    data shard.
    
    Args:
        function: Function with which to analyze data.
        data (iterable): The iterable to be analyzed in parallel.
        *args: Positional arguments required by function.
        **kwargs: Keyword arguments required by function.
            - cores: Can be included in **kwargs. Number of cores to run in parallel. 
                    Default is number of cores present on the current machine.
            
    Returns:
        results (list): List of results from each parallel process.
            
    """
    
    cores = kwargs.pop('cores', cpu_count())
    
    if cores > cpu_count():
        cores = cpu_count()
    
    if len(data) > cores:
        
        data_split = np.array_split(data, cores)
        
    else:
        
        data_split = np.array_split(data, len(data))
    
    queue = Queue()
    
    processes = [Process(target=__converter, args=(function, data_shard, queue, args, kwargs)) for data_shard in data_split]
        
    for p in processes:
        p.start()
        
    for p in processes:
        p.join()
        
    results = [queue.get() for p in processes]
    
    return results


def list_flow(function, data_list, *args, **kwargs):
    """Parallelization function that is intended to send each data object in a list
    to its own process to be analyzed in parallel. Returns a list of results from
    each process.
    
    Args:
        data_lsit (list): List of data objects to be analyzed in parallel.
        function: Function with which to analyze data.
        cores: Number of cores to run in parallel. Default is number of cores present
            on the current machine.
            
    Returns:
        results (list): List of results from each parallel process.
        
    """
    
    cores = kwargs.pop('cores', cpu_count())
    
    if cores > cpu_count():
        cores = cpu_count()
            
    queue = Queue()
    
    processes = [Process(target=__converter, args=(function, dataset, queue, args, kwargs)) for dataset in data_list]
    
    for p in processes:
        p.start()
        
    for p in processes:
        p.join()
        
    results = [queue.get() for p in processes]
    
    return results
