#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 23:14:01 2019

@author: dgelleru
"""


from laminar import laminar
from laminar import laminar_examples as le

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
