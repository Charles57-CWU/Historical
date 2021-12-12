import numpy as np
from OpenGL.GL import *
import OpenGL.arrays.vbo as glvbo
from sklearn.preprocessing import MinMaxScaler

import COLORS


def getVertexAndColors(dataframe, class_count, feature_count, count_per_class_array):
    df = dataframe

    for i in range(2, feature_count):
        df[df.columns[i]] += df[df.columns[i-2]]

    # scale attributes to fit to graphic coordinate system -0.8 to 0.8
    scaler = MinMaxScaler((-0.8, 0.8))
    tmp = df.to_numpy().reshape(-1, 1)
    scaled = scaler.fit_transform(tmp).reshape(len(df), feature_count)
    df.loc[:] = scaled

    # get xy_coord [[0,0],[2,0]]
    xy_coord = df.to_numpy()
    xy_coord = xy_coord.ravel()
    xy_coord = np.reshape(xy_coord, (-1, 2))

    # how to randomly generate more colors?
    colors = COLORS.getColors()
    class_color_array = colors.colors_array

    color_array = np.tile(class_color_array[0], reps=(count_per_class_array[0]*int((feature_count / 2)), 1))
    for i in range(1, class_count):
        temp_array = np.tile(class_color_array[i], reps=(count_per_class_array[i]*int((feature_count / 2)), 1))
        color_array = np.concatenate((color_array, temp_array))

    return xy_coord, color_array


class makeDICP:
    def __init__(self, new_plot, dataframe, class_count, feature_count, sample_count,
                 count_per_class_array):

        data, color_array = getVertexAndColors(dataframe, class_count, feature_count,
                                               count_per_class_array)
        data = data.astype('float32')
        color_array = color_array.astype('float32')

        # get vertex array using getvertices class
        new_plot.makeCurrent()

        glClearColor(1, 1, 1, 1)

        # make buffers
        vbo_vertex = glvbo.VBO(data)
        vbo_color = glvbo.VBO(color_array)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # bind the buffers
        vbo_vertex.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(2, GL_FLOAT, 0, vbo_vertex)
        vbo_color.bind()
        glEnableClientState(GL_COLOR_ARRAY)
        glColorPointer(3, GL_FLOAT, 0, vbo_color)

        # prepare the indices for drawing several lines
        indices = np.arange(0, sample_count * int(feature_count / 2), int(feature_count / 2))
        num_vert_per_line = np.repeat(int(feature_count / 2), sample_count)

        # draw the plot samples
        glMultiDrawArrays(GL_LINE_STRIP, indices, num_vert_per_line, sample_count)

        # draw axes
        glBegin(GL_LINES)
        glColor(0, 0, 0)
        glVertex2f(-0.8, -0.8)
        glVertex2f(0.8, -0.8)
        glEnd()

        glBegin(GL_LINES)
        glColor(0, 0, 0)
        glVertex2f(-0.8, -0.8)
        glVertex2f(-0.8, 0.8)
        glEnd()