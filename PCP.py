"""
PCP.py holds the information to render a parallel coordinate plot

Author: Charles Recaido
Program: MSc in Computational Science
School: Central Washington University
"""

import numpy as np
from OpenGL.GL import *
import OpenGL.arrays.vbo as glvbo
from sklearn.preprocessing import MinMaxScaler
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtGui import QPainter, QColor, QFont, QFontMetricsF
from PyQt5.QtCore import Qt, QRectF

import COLORS


def getVertexAndColors(dataframe, class_count, feature_count, sample_count, count_per_class_array):
    df = dataframe.copy()

    # scale attributes to fit to graphic coordinate system -0.8 to 0.8
    scaler = MinMaxScaler((-0.8, 0.8))
    #df[:] = scaler.fit_transform(df[:])
    tmp = df.to_numpy().reshape(-1, 1)
    scaled = scaler.fit_transform(tmp).reshape(len(df), feature_count)
    df.loc[:] = scaled

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
    axis_vertex_array = [[0, 0, 0]]
    # add y-axes

    x_coord_array = np.linspace(start=-0.8, stop=0.8, num=num_features)
    y_coord_array_bottom = np.repeat(-0.8, num_features)
    y_coord_array_top = np.repeat(0.8, num_features)

    for i in range(num_features):
        axis_vertex_array.append([x_coord_array[i], y_coord_array_bottom[i], 0])
        axis_vertex_array.append([x_coord_array[i], y_coord_array_top[i], 0])

    axis_color_array = np.tile([0, 0, 0], reps=(num_features * 2 + 1, 1))
    axis_vertex_array = np.delete(axis_vertex_array, 0, 0)

    return axis_vertex_array, axis_color_array


def draw_axes_markers(painter, feature_count, width, height, fm):
    x_min = 0.1 * width
    x_max = width - x_min
    x_pos_array = np.linspace(x_min, x_max, feature_count)

    for i in range(feature_count):
        marker = 'X' + str(i+1)
        x_offset = fm.boundingRect(marker).width()/2
        painter.drawText(x_pos_array[i] - x_offset, height - (height*0.1) + 20, marker)


class makePlot(QOpenGLWidget):
    width = 800
    height = 600

    def __init__(self, dataframe, class_count, feature_count, sample_count,
                 count_per_class_array, parent=None):
        super(makePlot, self).__init__(parent)
        #print(dataframe)
        self.dataframe = dataframe
        self.class_count = class_count
        self.feature_count = feature_count
        self.sample_count = sample_count
        self.count_per_class_array = count_per_class_array

        # get vertice information
        data, color_array = getVertexAndColors(self.dataframe, self.class_count, self.feature_count, self.sample_count,
                                               self.count_per_class_array)
        self.data = data.astype('float32')
        self.color_array = color_array.astype('float32')

        axes_vertex_array, axes_color_array = get_axes(self.feature_count)
        self.axes_vertex_array = np.asarray(axes_vertex_array, dtype='float32')
        self.axes_color = axes_color_array.astype('float32')

    def initializeGL(self):
        # make background white
        glClearColor(1, 1, 1, 1)
        #glMatrixMode(GL_MODELVIEW)

    def resizeGL(self, w, h):
        self.width, self.height = w, h
        glViewport(0, 0, w, h)

    def paintGL(self):
        #print(self.data)
        vbo_vertex = glvbo.VBO(self.data)
        vbo_color = glvbo.VBO(self.color_array)
        vbo_axis = glvbo.VBO(self.axes_vertex_array)
        vbo_axis_color = glvbo.VBO(self.axes_color)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # bind the buffers
        vbo_vertex.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, vbo_vertex)
        vbo_color.bind()
        #glEnableClientState(GL_COLOR_ARRAY)
        glColorPointer(3, GL_FLOAT, 0, vbo_color)

        # prepare the indices for drawing several lines
        indices = np.arange(0, self.sample_count * self.feature_count, self.feature_count)
        num_vert_per_line = np.repeat(self.feature_count, self.sample_count * self.feature_count)

        # draw the plot samples
        glMultiDrawArrays(GL_LINE_STRIP, indices, num_vert_per_line, self.sample_count)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        vbo_vertex.unbind()
        vbo_color.unbind()


        # bind the buffers
        vbo_axis.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, vbo_axis)
        vbo_axis_color.bind()
        glEnableClientState(GL_COLOR_ARRAY)
        glColorPointer(3, GL_FLOAT, 0, vbo_axis_color)

        # prepare the indices for drawing several lines
        axis_ind = np.arange(0, self.feature_count * 2, 2)
        axis_per_line = np.repeat(2, self.feature_count)

        # draw axes
        glMultiDrawArrays(GL_LINES, axis_ind, axis_per_line, self.feature_count)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        vbo_axis.unbind()
        vbo_axis_color.unbind()


        painter = QPainter()
        painter.begin(self)
        painter.setPen(QColor('Black'))
        painter.setFont(QFont('Helvetica', 15))
        fm = QFontMetricsF(painter.font())
        painter.setRenderHints(painter.Antialiasing)
        draw_axes_markers(painter, self.feature_count, self.width, self.height, fm)
        title = 'Parallel Coordinate Plot'
        x_title_offset = fm.boundingRect(title).width()/2
        painter.drawText(self.width/2 - x_title_offset, 40, title)
        #painter.drawText()
        painter.end()



