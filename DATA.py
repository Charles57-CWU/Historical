"""
DATA.py extracts certain information from a dataset

Author: Charles Recaido
Program: MSc in Computational Science
School: Central Washington University
"""

import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


class getData:
    def __init__(self, file_name):
        df = pd.read_csv(file_name)
        class_column_name = 'class'

        # get dataset name
        self.dataset_name = os.path.basename(file_name)

        # get class information
        self.class_count = len(df[class_column_name].unique())
        print(df[class_column_name].value_counts())
        self.class_names_array = df[class_column_name].value_counts().index.tolist()
        print(self.class_names_array)
        self.count_per_class_array = df[class_column_name].value_counts().tolist()
        print(self.count_per_class_array)

        df['class'] = pd.Categorical(df['class'], categories=self.class_names_array)
        df = df.sort_values(by='class')
        print(df)

        # drop classes column
        df = df.drop(columns=class_column_name, axis=1)

        #scaler = MinMaxScaler((0, 1))
        #df[:] = scaler.fit_transform(df[:])
        #print(df)


        # get sample and feature information
        self.feature_names_array = df.columns.tolist()
        self.sample_count = len(df.index)
        self.feature_count = len(df.columns)

        self.dataframe = df