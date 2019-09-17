from multiprocessing import Queue, Process, cpu_count

import numpy as np


def __converter(function, data_shard, queue, *args):
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
    
    queue.put(result)


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
            {'data_position_0': 17,
             'data_position_1': 37,
             'data_position_2': 60,
             'data_position_3': 86,
             'data_position_4': 115,
             'data_position_5': 105,
             'data_position_6': 120,
             'data_position_7': 135}
            
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
        new_process = Process(name="data[{}-{}]".format(start, end), target=__converter, args=(function, dataset, queue, args, kwargs))
        processes.append(new_process)
    
    for p in processes:
        p.start()
        
    for p in processes:
        p.join()
        
    results = {p.name: queue.get() for p in processes}
    
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
    
    #processes = [Process(target=__converter, args=(function, dataset, queue, args, kwargs)) for dataset in data_list]
    
    processes = []
    
    i = 0
    for dataset in data_list:
        new_process = Process(name="data_position_{}".format(i), target=__converter, args=(function, dataset, queue, args, kwargs))
        processes.append(new_process)
        i += 1
    
    for p in processes:
        p.start()
        
    for p in processes:
        p.join()
    
    results = {p.name: queue.get() for p in processes}
    
    return results
