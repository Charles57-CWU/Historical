"""
DICP.py holds the information to render a dynamic in-line coordinate plot

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

    for i in range(2, feature_count):
        df[df.columns[i]] += df[df.columns[i - 2]]

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

    color_array = np.tile(class_color_array[0], reps=(count_per_class_array[0] * int((feature_count / 2)), 1))
    for i in range(1, class_count):
        temp_array = np.tile(class_color_array[i], reps=(count_per_class_array[i] * int((feature_count / 2)), 1))
        color_array = np.concatenate((color_array, temp_array))

    return xy_coord, color_array


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