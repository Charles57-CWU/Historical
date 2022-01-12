"""
DATA.py extracts certain information from a dataset

Author: Charles Recaido
Program: MSc in Computational Science
School: Central Washington University
"""

import os
import numpy as np
import pandas as pd


class getData:
    def __init__(self, file_name):
        df = pd.read_csv(file_name)
        class_column_name = 'class'
        self.class_names_array = df[class_column_name].unique()

        # get dataset name
        self.dataset_name = os.path.basename(file_name)

        # get class information
        self.class_count = len(df[class_column_name].unique())
        self.count_per_class_array = df[class_column_name].value_counts().tolist()

        # drop classes column
        df = df.drop(columns=class_column_name, axis=1)


        # get sample and feature information
        self.feature_names_array = df.columns.tolist()
        self.sample_count = len(df.index)
        self.feature_count = len(df.columns)

        self.dataframe = df