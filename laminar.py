from multiprocessing import Queue, Process, cpu_count

import numpy as np


def __converter(function, queue, data_shard):
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
    
    result = function(data_shard)
    
    queue.put(result)


def iter_flow(data, function, cores=cpu_count()):
    """Parallelization function that is intended to break up an iterable into data shards,
    then analyze each data shard in parallel. Returns a list of results from each
    data shard.
    
    Args:
        data: The iterable to be analyzed in parallel.
        function: Function with which to analyze data.
        cores: Number of cores to run in parallel. Default is number of cores present
            on the current machine.
            
    Returns:
        results (list): List of results from each parallel process.
            
    """
    
    if cores > cpu_count():
        cores = cpu_count()
    
    if len(data) > cores:
        
        data_split = np.array_split(data, cores)
        
    else:
        
        data_split = np.array_split(data, len(data))
    
    queue = Queue()
    
    processes = [Process(target=__converter, args=(function, queue, data_shard)) for data_shard in data_split]
    
    for p in processes:
        p.start()
        
    for p in processes:
        p.join()
        
    results = [queue.get() for p in processes]
    
    return results


def list_flow(data_list, function, cores=cpu_count()):
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
    
    if cores > cpu_count():
        cores = cpu_count()
            
    queue = Queue()
    
    processes = [Process(target=__converter, args=(function, queue, dataset)) for dataset in data_list]
    
    for p in processes:
        p.start()
        
    for p in processes:
        p.join()
        
    results = [queue.get() for p in processes]
    
    return results
