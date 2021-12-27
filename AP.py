"""
AP.py holds the information to render an angle plot

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


def getVertexAndColors(dataframe, class_count, feature_count, sample_count, count_per_class_array):
    df = dataframe.copy()

    scaler = MinMaxScaler((0, 90))
    df[:] = scaler.fit_transform(df[:])

    # get y_coord
    y_coord = df.to_numpy()
    y_coord = y_coord.ravel()
    print(df)

    x_coord_array = np.linspace(start=-0.8, stop=0.8, num=feature_count)
    print(x_coord_array)
    space = 1.6 / feature_count
    scaffold_axis = np.asarray([[-0.8, -0.8]])
    print(np.shape(y_coord))

    for i in range(1, sample_count * feature_count):
        if i % feature_count == 0:
            scaffold_axis = np.append(scaffold_axis, [[-0.8, -0.8]], 0)

        else:
            new_x = np.abs(np.cos(np.radians(y_coord[i])) * space)
            new_y = np.abs(np.sin(np.radians(y_coord[i])) * space)
            scaffold_axis = np.append(scaffold_axis, [
                [scaffold_axis[i - 1][0] + new_x, scaffold_axis[i - 1][1] + new_y]], 0)

    print(scaffold_axis)
    # how to randomly generate more colors?
    colors = COLORS.getColors()
    class_color_array = colors.colors_array

    color_array = np.tile(class_color_array[0], reps=(count_per_class_array[0] * feature_count, 1))
    for i in range(1, class_count):
        temp_array = np.tile(class_color_array[i], reps=(count_per_class_array[i] * feature_count, 1))
        color_array = np.concatenate((color_array, temp_array))

    return scaffold_axis, color_array


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

        data, color_array = getVertexAndColors(self.dataframe, self.class_count,
                                               self.feature_count,
                                               self.sample_count,
                                               self.count_per_class_array)
        self.data = data.astype('float32')
        self.color_array = color_array.astype('float32')

    # initialize the buffers
    def initializeGL(self):
        # make background white
        glClearColor(1, 1, 1, 1)

    # for resizing plot
    def resizeGL(self, w, h):
        self.width, self.height = w, h
        glViewport(0, 0, w, h)

    # paint the plot
    def paintGL(self):
        vbo_vertex = glvbo.VBO(self.data)
        vbo_color = glvbo.VBO(self.color_array)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # bind the buffers
        vbo_vertex.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(2, GL_FLOAT, 0, vbo_vertex)
        vbo_color.bind()
        glEnableClientState(GL_COLOR_ARRAY)
        glColorPointer(3, GL_FLOAT, 0, vbo_color)

        # prepare the indices for drawing several lines
        indices = np.arange(0, self.sample_count * self.feature_count, self.feature_count)
        num_vert_per_line = np.repeat(self.feature_count, self.sample_count * self.feature_count)

        # draw the samples
        glMultiDrawArrays(GL_LINE_STRIP, indices, num_vert_per_line, self.sample_count)

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
