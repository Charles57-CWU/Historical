"""
SPCP.py holds the information to render a shifted paired coordinate plot

Author: Charles Recaido
Program: MSc in Computational Science
School: Central Washington University
"""
import numpy as np
from OpenGL.GL import *
import OpenGL.arrays.vbo as glvbo
from sklearn.preprocessing import MinMaxScaler
from PyQt5.QtWidgets import QOpenGLWidget

import COLORS


def getVertexAndColors(dataframe, class_count, feature_count, count_per_class_array):
    df = dataframe.copy()

    section_array = np.linspace(start=-0.8, stop=0.8, num=int(feature_count / 2) + 1)

    # scale attributes to fit to graphic coordinate system -0.8 to 0.8

    j = 0
    for i in range(feature_count):
        if i % 2 != 0:
            scaler = MinMaxScaler((-0.8, 0.8))
            df[df.columns[i]] = scaler.fit_transform(df[[df.columns[i]]])
        else:
            scaler = MinMaxScaler((section_array[j], section_array[j + 1]))
            df[df.columns[i]] = scaler.fit_transform(df[[df.columns[i]]])
            j += 1

    # get xy_coord
    xy_coord = df.to_numpy()
    xy_coord = xy_coord.ravel()
    xy_coord = np.reshape(xy_coord, (-1, 2))

    # how to randomly generate more colors?
    colors = COLORS.getColors()
    class_color_array = colors.colors_array

    color_array = np.tile(class_color_array[0], reps=(count_per_class_array[0] * int((feature_count / 2)), 1))
    for i in range(1, class_count):
        temp_array = np.tile(class_color_array[i], reps=(count_per_class_array[i] * int((feature_count / 2)), 1))
        color_array = np.concatenate((color_array, temp_array))

    return xy_coord, color_array


def get_axes(feature_count):
    # add x-axis
    axis_vertex_array = [[-0.8, -0.8, 0], [0.8, -0.8, 0]]
    # add y-axes

    x_coord_array = np.linspace(start=-0.8, stop=0.8, num=feature_count)
    y_coord_array_bottom = np.repeat(-0.8, feature_count)
    y_coord_array_top = np.repeat(0.8, feature_count)

    for i in range(feature_count - 1):
        axis_vertex_array.append([x_coord_array[i], y_coord_array_bottom[i], 0])
        axis_vertex_array.append([x_coord_array[i], y_coord_array_top[i], 0])

    axis_color_array = np.tile([0, 0, 0], reps=(feature_count * 2 + 1, 1))
    return axis_vertex_array, axis_color_array


class makePlot(QOpenGLWidget):
    width = 800
    height = 600

    def __init__(self, dataframe, class_count, feature_count, sample_count,
                 count_per_class_array, parent=None):
        super(makePlot, self).__init__(parent)
        self.dataframe = dataframe
        self.class_count = class_count
        self.feature_count = feature_count
        self.sample_count = sample_count
        self.count_per_class_array = count_per_class_array

        data, color_array = getVertexAndColors(self.dataframe, self.class_count, self.feature_count,
                                               self.count_per_class_array)
        self.data = data.astype('float32')
        self.color_array = color_array.astype('float32')

        axes_vertex_array, axes_color_array = get_axes(int(self.feature_count / 2) + 1)
        self.axes_vertex_array = np.asarray(axes_vertex_array, dtype='float32')
        self.axes_color = axes_color_array.astype('float32')

    def initializeGL(self):
        # make background white
        glClearColor(1, 1, 1, 1)

    def resizeGL(self, w, h):
        self.width, self.height = w, h
        glViewport(0, 0, w, h)

    def paintGL(self):
        # make buffers
        vbo_vertex = glvbo.VBO(self.data)
        vbo_color = glvbo.VBO(self.color_array)
        vbo_axis = glvbo.VBO(self.axes_vertex_array)
        vbo_axis_color = glvbo.VBO(self.axes_color)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # bind the buffers
        vbo_vertex.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(2, GL_FLOAT, 0, vbo_vertex)
        vbo_color.bind()
        glEnableClientState(GL_COLOR_ARRAY)
        glColorPointer(3, GL_FLOAT, 0, vbo_color)

        # prepare the indices for drawing several lines
        indices = np.arange(0, self.sample_count * int(self.feature_count / 2), int(self.feature_count / 2))
        num_vert_per_line = np.repeat(int(self.feature_count / 2), self.sample_count)

        # draw the plot samples
        glMultiDrawArrays(GL_LINE_STRIP, indices, num_vert_per_line, int(self.sample_count/2))

        # bind the buffers
        vbo_axis.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, vbo_axis)
        vbo_axis_color.bind()
        glEnableClientState(GL_COLOR_ARRAY)
        glColorPointer(3, GL_FLOAT, 0, vbo_axis_color)

        # prepare the indices for drawing several lines
        axis_ind = np.arange(0, (self.feature_count + 1) * 2, 2)
        axis_per_line = np.repeat(2, self.feature_count + 1)

        # draw axes
        glMultiDrawArrays(GL_LINES, axis_ind, axis_per_line, self.feature_count + 1)
