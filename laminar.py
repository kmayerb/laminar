from multiprocessing import Queue, Process, cpu_count
import time

import numpy as np


def __converter(function, queue, data_shard):
    
    result = function(data_shard)
    
    queue.put(result)


def iter_flow(data, function, cores=cpu_count()):
    
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
