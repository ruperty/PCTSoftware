# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 2023

@author: ryoung
"""

import csv


def read_data():
    file = 'configs.csv'
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(row)
            
            
read_data()