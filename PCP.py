import numpy as np
from OpenGL.GL import *
import OpenGL.arrays.vbo as glvbo
from sklearn.preprocessing import MinMaxScaler

import COLORS


def getVertexAndColors(dataframe, class_count, feature_count, sample_count, count_per_class_array):
    df = dataframe

    # scale attributes to fit to graphic coordinate system -0.8 to 0.8
    scaler = MinMaxScaler((-0.8, 0.8))
    df[:] = scaler.fit_transform(df[:])

    # change into 3 coordinate numpy vertex array ie: [[0, 0, 0], [1, 1, 1]]
    # get x_coord
    x_coord_array = np.linspace(start=-0.8, stop=0.8, num=feature_count)
    x_coord = np.tile(x_coord_array, reps=sample_count)

    # get y_coord
    y_coord = df.to_numpy()
    y_coord = y_coord.ravel()

    # get z_coord
    z_coord = np.repeat(0, repeats=feature_count * sample_count)

    # combine into x,y,z elements
    vertex_array = np.column_stack((x_coord, y_coord, z_coord))

    # how to randomly generate more colors?
    colors = COLORS.getColors()
    class_color_array = colors.colors_array

    color_array = np.tile(class_color_array[0], reps=(count_per_class_array[0] * feature_count, 1))
    for i in range(1, class_count):
        temp_array = np.tile(class_color_array[i], reps=(count_per_class_array[i] * feature_count, 1))
        color_array = np.concatenate((color_array, temp_array))

    return vertex_array, color_array


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

    axis_color_array = np.tile([0, 0, 0], reps=(num_features * 2 + 2, 1))

    return axis_vertex_array, axis_color_array


class makePCP:
    def __init__(self, new_plot, dataframe, class_count, feature_count, sample_count,
                 count_per_class_array):

        data, color_array = getVertexAndColors(dataframe, class_count, feature_count, sample_count,
                                               count_per_class_array)

        data = data.astype('float32')
        color_array = color_array.astype('float32')

        axes_vertex_array, axes_color_array = get_axes(feature_count)
        axes_vertex_array = np.asarray(axes_vertex_array, dtype='float32')
        axes_color = axes_color_array.astype('float32')

        # get vertex array using getvertices class
        new_plot.makeCurrent()

        # make background white
        glClearColor(1, 1, 1, 1)

        # make buffers
        vbo_vertex = glvbo.VBO(data)
        vbo_color = glvbo.VBO(color_array)
        vbo_axis = glvbo.VBO(axes_vertex_array)
        vbo_axis_color = glvbo.VBO(axes_color)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # bind the buffers
        vbo_vertex.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, vbo_vertex)
        vbo_color.bind()
        glEnableClientState(GL_COLOR_ARRAY)
        glColorPointer(3, GL_FLOAT, 0, vbo_color)

        # prepare the indices for drawing several lines
        indices = np.arange(0, sample_count * feature_count, feature_count)
        num_vert_per_line = np.repeat(feature_count, sample_count * feature_count)

        # draw the plot samples
        glMultiDrawArrays(GL_LINE_STRIP, indices, num_vert_per_line, sample_count)

        # bind the buffers
        vbo_axis.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, vbo_axis)
        vbo_axis_color.bind()
        glEnableClientState(GL_COLOR_ARRAY)
        glColorPointer(3, GL_FLOAT, 0, vbo_axis_color)

        # prepare the indices for drawing several lines
        axis_ind = np.arange(0, (feature_count + 1) * 2, 2)
        axis_per_line = np.repeat(2, feature_count + 1)

        # draw axes
        glMultiDrawArrays(GL_LINES, axis_ind, axis_per_line, feature_count + 1)
