#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 23:14:01 2019

@author: dgelleru
"""


from laminar import laminar
from laminar import laminar_examples as le


# Module Usage

# iter_flow: one iterable to break up; broken up into n chunks, where n = cores

# le.single_total reuturns sum, but can take odd=True to only sum odd numbers.
result = laminar.iter_flow(le.single_total, le.laminar_df['Col1'])

result = laminar.iter_flow(le.single_total, le.laminar_df['Col1'], True)
result = laminar.iter_flow(le.single_total, le.laminar_df['Col1'], odd=True)

# le.multi_tally returns count of rows that sum to greater than 25
result = laminar.iter_flow(le.multi_tally, le.laminar_df)

# list_flow: list of iterables; can contain more iterables than cores; processes
#            will pull from the queue until it is empty.

# create a list of pd.Series corresponding to laminar_df columns
columns_list = [le.laminar_df[col] for col in le.laminar_df.columns]
result = laminar.list_flow(le.single_total, columns_list, odd=True)

# Make a list of three copies of le.laminar_df
data_frames_list = [le.laminar_df]*3
result = laminar.list_flow(le.multi_tally, data_frames_list)


# Class Usage

my_lam = laminar.Laminar()

my_lam.show_processes()

my_lam.add_process('avg_s_length', lambda x: x.mean(), le.iris['sepal_length'])

my_lam.add_process('avg_s_width', lambda x: x.mean(), le.iris['sepal_width'])

my_lam.add_process('avg_p_length', lambda x: x.mean(), le.iris['petal_length'])

my_lam.add_process('avg_s_length', lambda x: x.mean(), le.iris['sepal_lngth'])

my_lam.drop_process('avg_s_length')

my_lam.add_process('avg_s_width', lambda x: x.mean(), le.iris['petal_width'])

my_lam.show_processes()

my_lam.launch_processes()

my_lam.get_results()

results = my_lam.get_results()

my_lam.show_processes()
