"""
GLCSP.py holds the information to render a general line coordinate w/ scaffold plot

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

    space = 1.6 / (int(feature_count / 2) + 1)
    for i in range(feature_count):
        scaler = MinMaxScaler((0, space))
        df[df.columns[i]] = scaler.fit_transform(df[[df.columns[i]]])

    # get xy_coord [[0,0],[2,0]]
    xy_coord = df.to_numpy()
    xy_coord = xy_coord.ravel()
    xy_coord = np.reshape(xy_coord, (-1, 2))
    scaffold_axis = np.asarray([[0, 0]])
    j = 0
    for i in range(sample_count * int(feature_count / 2 + 1)):
        if i % int(feature_count / 2 + 1) == 0:
            if i == 0:
                scaffold_axis = np.asarray([[-0.8, -0.8]])
            else:
                scaffold_axis = np.append(scaffold_axis, [[-0.8, -0.8]], 0)
        else:
            scaffold_axis = np.append(scaffold_axis, [
                [scaffold_axis[i - 1][0] + xy_coord[j][0], scaffold_axis[i - 1][1] + xy_coord[j][1]]], 0)
            j += 1

    # how to randomly generate more colors?
    colors = COLORS.getColors()
    class_color_array = colors.colors_array

    color_array = np.tile(class_color_array[0], reps=(count_per_class_array[0] * int((feature_count / 2) + 1), 1))
    for i in range(1, class_count):
        temp_array = np.tile(class_color_array[i], reps=(count_per_class_array[i] * int((feature_count / 2) + 1), 1))
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

        data, color_array = getVertexAndColors(self.dataframe, self.class_count, self.feature_count,
                                               self.sample_count, self.count_per_class_array)
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
        indices = np.arange(0, self.sample_count * (int(self.feature_count / 2) + 1), int(self.feature_count / 2) + 1)
        num_vert_per_line = np.repeat(int(self.feature_count / 2) + 1, self.sample_count)

        # draw the plot samples
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