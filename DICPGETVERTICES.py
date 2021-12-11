import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def getVertexAndColors(file_name, dataset_sep, headers, class_col_name):
    # get attributes into dataframe
    df = pd.read_csv(file_name, sep=dataset_sep)

    # get class information
    num_classes = len(df[class_col_name].unique())
    class_counts = df[class_col_name].value_counts().tolist()

    # drop classes column
    df = df.drop(columns=class_col_name, axis=1)

    sample_count = len(df.index)
    num_features = len(df.columns)

    for i in range(2, num_features):
        df[df.columns[i]] += df[df.columns[i-2]]

    # scale attributes to fit to graphic coordinate system -0.8 to 0.8
    scaler = MinMaxScaler((-0.8, 0.8))
    tmp = df.to_numpy().reshape(-1, 1)
    scaled = scaler.fit_transform(tmp).reshape(len(df), num_features)
    df.loc[:] = scaled
    #df[:] = scaler.fit_transform(df[:])
    print(df)

    # get xy_coord [[0,0],[2,0]]
    xy_coord = df.to_numpy()
    xy_coord = xy_coord.ravel()
    xy_coord = np.reshape(xy_coord, (-1, 2))

    # how to randomly generate more colors?
    colors = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 0], [0.5, 0.5, 0.5], [0.5, 0.5, 1], [1, 0.5, 0.5], [0.5, 1, 0.5]]

    color_array = np.tile(colors[0], reps=(class_counts[0]*int((num_features / 2)), 1))
    for i in range(1, num_classes):
        temp_array = np.tile(colors[i], reps=(class_counts[i]*int((num_features / 2)), 1))
        color_array = np.concatenate((color_array, temp_array))

    return xy_coord, num_features, sample_count, color_array


def get_axes(num_features):
    # add x-axis
    axis_vertex_array = [[-0.8, -0.8, 0], [0.8, -0.8, 0]]
    # add y-axes

    x_coord_array = np.linspace(start=-0.8, stop=0.8, num=num_features)
    y_coord_array_bottom = np.repeat(-0.8, num_features)
    y_coord_array_top = np.repeat(0.8, num_features)

    for i in range(num_features):
        axis_vertex_array.append([x_coord_array[i], y_coord_array_bottom[i], 0])
        axis_vertex_array.append([x_coord_array[i], y_coord_array_top[i], 0])

    axis_color_array = np.tile([0, 0, 0], reps=(num_features*2 + 2, 1))

    return axis_vertex_array, axis_color_array


class getVerticesAndColors:
    def __init__(self, file_name, dataset_sep, headers, class_col_name):
        self.file_name = file_name
        self.dataset_sep = dataset_sep
        self.headers = headers
        self.class_col_name = class_col_name

    # call function to get vertex and color information
    def getVertexAndColor(self):
        vertex_array, num_features, num_samples, color_array = getVertexAndColors(self.file_name, self.dataset_sep, self.headers, self.class_col_name)
        return vertex_array, num_features, num_samples, color_array

#test code
#p1 = getVerticesAndColors('mnist_train.csv', ',', True, 'class')
#p1.getVertexAndColor()
#p1.getAxis(9)
