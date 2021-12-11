import numpy as np
import pandas as pd


class getData:
    def __init__(self, file_name):
        df = pd.read_csv(file_name)

        class_column_name = 'class'

        # get class information
        self.number_of_classes = len(df[class_column_name].unique())
        self.class_names_array = df[class_column_name].unique()
        self.count_per_class_array = df[class_column_name].value_counts().tolist()

        # drop classes column
        df = df.drop(columns=class_column_name, axis=1)

        # get sample and feature counts
        self.number_of_samples = len(df.index)
        self.number_of_features = len(df.columns)
