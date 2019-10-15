from multiprocessing import Queue, Process, cpu_count

import numpy as np


def __converter(name, function, data_shard, queue, *args):
    """Module function that calls the passed function with the passed data_shard
    as an argument, then places the result in the queue. Also passes through any
    args required for the function (if passed in).
    
    Args:
        function: Function object the user wishes to parallelize.
        data_shard: Data object that is a subset of the master data object passed
            to the laminar function.
        queue: Multiprocessing queue that holds process results.
            
    Returns:
        None
        
    """
    
    kwargs, args = args[-1], args[0]
    
    result = function(data_shard, *args, **kwargs)
    
    queue.put((name, result))
    

def iter_flow(function, data, *args, **kwargs):
    """Parallelizes analysis of a list.
    
    Parallelization function that breaks up an iterable into data shards,
    then analyzes each data shard in parallel. Returns a list of results from each
    data shard.
    
    Args:
        function: Function with which to analyze data.
        data (iterable): The iterable to be analyzed in parallel.
        *args: Positional arguments required by function.
        **kwargs: Keyword arguments required by function.
            - cores: Can be included in **kwargs. Number of cores to run in parallel. 
                    Default is number of cores present on the current machine.
            
    Returns:
        results (dict): Dictionary of results from each parallel process, named
            according to position in data iterable.
            
        Example: 
            {'data[0-25]': 17,
             'data[26-50]': 37,
             'data[51-75]': 60,
             'data[76-100]': 86,
             'data[101-125]: 115,
             'data[126-150]': 105,
             'data[151-175]': 120,
             'data[176-200]': 135}
            
    """
        
    cores = kwargs.pop('cores', cpu_count())
    
    if cores > cpu_count():
        cores = cpu_count()
    
    if len(data) > cores:
        
        data_split = np.array_split(data, cores)
        
    else:
        
        data_split = np.array_split(data, len(data))
    
    queue = Queue()
    
    processes = []    
    
    end = -1
    for dataset in data_split:
        start = end + 1
        end += len(dataset)
        name = f"data[{start}-{end}]"
        new_process = Process(target=__converter, args=(name, function, dataset, queue, args, kwargs))
        processes.append(new_process)
    
    for p in processes:
        p.start()
        
    for p in processes:
        p.join()
    
    results = {}
    for p in processes:
        q = queue.get()
        results[q[0]] = q[1]
    
    return results


def list_flow(function, data_list, *args, **kwargs):
    """Parallelizes analysis of a list.
    
    Parallelization function that sends each data object in a list to its own 
    process to be analyzed in parallel. Returns a list of results from each process.
    
    Args:
        function: Function with which to analyze data.
        data_lsit (list): List of data objects to be analyzed in parallel.
        *args: Positional arguments required by function.
        **kwargs: Keyword arguments required by function.
            - cores: Can be included in **kwargs. Number of cores to run in parallel. 
                    Default is number of cores present on the current machine.
            
    Returns:
        results (dict): Dictionary of results from each parallel process, named
            according to position in data_list iterable.
            
        Example:
            {'data_position_0': 675,
            'data_position_1': 1800,
            'data_position_2': 2925}

        
    """
    
    cores = kwargs.pop('cores', cpu_count())
    
    if cores > cpu_count():
        cores = cpu_count()
            
    queue = Queue()
    
    processes = []
    
    i = 0
    for dataset in data_list:
        name = f"data_position_{i}"
        new_process = Process(target=__converter, args=(name, function, dataset, queue, args, kwargs))
        processes.append(new_process)
        i += 1
    
    for p in processes:
        p.start()
        
    for p in processes:
        p.join()
    
    results = {}
    for p in processes:
        q = queue.get()
        results[q[0]] = q[1]
    
    return results
