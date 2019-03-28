from multiprocessing import Queue, Process, cpu_count

import numpy as np
import pandas as pd


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

