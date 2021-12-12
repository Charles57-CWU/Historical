import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def getVertexAndColors(dataframe):
    df = dataframe
    class_col_name = 'class'

    # get class information
    num_classes = len(df[class_col_name].unique())
    print(num_classes)
    class_counts = df[class_col_name].value_counts().tolist()

    # drop classes column
    df = df.drop(columns=class_col_name, axis=1)

    # scale attributes to fit to graphic coordinate system -0.8 to 0.8
    scaler = MinMaxScaler((-0.8, 0.8))
    df[:] = scaler.fit_transform(df[:])

    # get sample and feature counts
    sample_count = len(df.index)
    num_features = len(df.columns)

    # change into 3 coordinate numpy vertex array ie: [[0, 0, 0], [1, 1, 1]]
    # get x_coord
    x_coord_array = np.linspace(start=-0.8, stop=0.8, num=num_features)
    x_coord = np.tile(x_coord_array, reps=sample_count)

    # get y_coord
    y_coord = df.to_numpy()
    y_coord = y_coord.ravel()

    # get z_coord
    z_coord = np.repeat(0, repeats=num_features * sample_count)

    # combine into x,y,z elements
    vertex_array = np.column_stack((x_coord, y_coord, z_coord))

    # how to randomly generate more colors?
    colors = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 0], [0.5, 0.5, 0.5], [0.5, 0.5, 1], [1, 0.5, 0.5], [0.5, 1, 0.5]]

    color_array = np.tile(colors[0], reps=(class_counts[0] * num_features, 1))
    for i in range(1, num_classes):
        temp_array = np.tile(colors[i], reps=(class_counts[i] * num_features, 1))
        color_array = np.concatenate((color_array, temp_array))

    return vertex_array, num_features, sample_count, color_array


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
    def __init__(self, dataframe):
        self.dataframe = dataframe

    # call function to get vertex and color information
    def getVertexAndColor(self):
        vertex_array, num_features, num_samples, color_array = getVertexAndColors(self.dataframe)
        return vertex_array, num_features, num_samples, color_array

    # call function to get axes information
    def getAxis(self, num_features):
        axes_vertex_array, axes_color_array = get_axes(num_features)
        return axes_vertex_array, axes_color_array

#test code
#p1 = getVerticesAndColors('iris_dataset.txt', ',', True, 'variety')
#p1.getVertexAndColor()
#p1.getAxis(9)
