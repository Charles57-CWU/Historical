import numpy as np
from OpenGL.GL import *
import OpenGL.arrays.vbo as glvbo
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtGui import QPainter, QColor, QFont, QFontMetricsF

import PLOT_OPENGL_INFORMATION


def drawPCPLabels(painter, feature_count, width, height, fm, feature_positions):
    x_min = 0.1 * width
    x_max = width - x_min
    x_pos_array = np.linspace(x_min, x_max, feature_count)

    for i in range(feature_count):
        marker = 'X' + str(feature_positions[i])
        x_offset = fm.boundingRect(marker).width() / 2
        painter.drawText(x_pos_array[i] - x_offset, height - (height * 0.1) + 20, marker)


def drawSPCLabels(painter, feature_count, width, height, fm, feature_positions):
    x_min = 0.1 * width
    x_max = width - x_min
    vert_pos_array = np.linspace(x_min, x_max, int(feature_count / 2) + 1)
    horiz_pos_array = np.linspace(x_min, x_max, feature_count + 1)

    j = 2
    for i in range(int(feature_count / 2)):
        # create the vertical markers
        y_marker = 'X' + str(feature_positions[j - 1])
        x_offset_vertical = fm.boundingRect(y_marker).width() / 2
        painter.drawText(vert_pos_array[i] - x_offset_vertical, height * 0.1 - 10, y_marker)
        # create the horizontal markers
        x_marker = 'X' + str(feature_positions[j - 2])
        x_offset_horizontal = fm.boundingRect(x_marker).width() / 2
        painter.drawText(horiz_pos_array[j - 1] - x_offset_horizontal, height - (height * 0.1) + 20, x_marker)

        j += 2


class makePlot(QOpenGLWidget):
    width = 800
    height = 600

    def __init__(self, dataframe, class_count, feature_count, sample_count,
                 count_per_class_array, feature_positions, plot_type, parent=None):
        super(makePlot, self).__init__(parent)

        # initialize variables
        self.plot_type = plot_type
        # class variables
        self.class_vertices = None
        self.class_colors = None
        self.all_class_index_starts = None
        self.current_class_index_starts = None
        self.all_class_vertex_count = None
        self.current_class_vertex_count = None
        self.sample_count = None
        # axes variables
        self.axes_vertices = None
        self.axes_color = None
        self.axes_index_starts = None
        self.axes_vertex_count = None
        self.axes_count = None
        self.plot_axes = True
        self.feature_positions = feature_positions


        # get plot information
        if self.plot_type:
            ini_plot_info = PLOT_OPENGL_INFORMATION.getPlotInfo(dataframe, class_count, feature_count, sample_count,
                                                                count_per_class_array, plot_type)
            """
            establish all classes and set them as current classes to display
            current classes to display can change later on 
            all classes will remain fixed as to not lose coordinate information when switching classes to display
            """
            # vertex information in (x, y) cartesian
            self.class_vertices = ini_plot_info.class_vertices.astype('float32')
            # self.current_class_vertices = self.all_class_vertices
            # color at each vertex in (R, G, B) - Note: RGB is scaled between 0 and 1
            self.class_colors = ini_plot_info.class_colors.astype('float32')
            # self.current_class_color = self.all_class_color
            # gets the starting index for each sample to plot
            self.all_class_index_starts = ini_plot_info.class_index_starts
            self.current_class_index_starts = self.all_class_index_starts
            # gets the number of vertices to plot per sample
            self.all_class_vertex_count = ini_plot_info.class_vertex_count
            self.current_class_vertex_count = self.all_class_vertex_count
            # number of samples to plot
            self.sample_count = sample_count
            self.current_sample_count = self.sample_count

            """
            establish axes to plot
            axes can be turned on/off later on
            """
            # vertex information in (x, y) cartesian
            self.axes_vertices = np.asarray(ini_plot_info.axes_vertices, dtype='float32')
            # color at each vertex in (R, G, B) - Note: RGB is scaled between 0 and 1
            self.axes_color = np.asarray(ini_plot_info.axes_colors, dtype='float32')
            # gets the starting index for each axis to plot
            self.axes_index_starts = ini_plot_info.axes_index_starts
            # gets the number of vertices to plot per axis
            self.axes_vertex_count = ini_plot_info.axes_vertex_count
            # number of axis to plot
            self.axes_count = ini_plot_info.axes_count
            """
            label information
            """
            self.title = ini_plot_info.title
            self.feature_count = feature_count

    def initializeGL(self):
        # make background white
        glClearColor(1, 1, 1, 1)

    def resizeGL(self, w, h):
        self.width, self.height = w, h
        glViewport(0, 0, w, h)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if self.plot_type:
            # ===========================DRAW PLOT SAMPLES=========================================
            # bind the buffers
            vbo_class_vertices = glvbo.VBO(self.class_vertices)
            vbo_class_vertices.bind()
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(2, GL_FLOAT, 0, vbo_class_vertices)

            vbo_class_colors = glvbo.VBO(self.class_colors)
            vbo_class_colors.bind()
            glEnableClientState(GL_COLOR_ARRAY)
            glColorPointer(3, GL_FLOAT, 0, vbo_class_colors)
            # draw the samples
            glMultiDrawArrays(GL_LINE_STRIP, self.current_class_index_starts, self.current_class_vertex_count,
                              self.current_sample_count)

            # unbind buffers
            glDisableClientState(GL_VERTEX_ARRAY)
            glDisableClientState(GL_COLOR_ARRAY)
            vbo_class_vertices.unbind()
            vbo_class_colors.unbind()

            # ===========================DRAW PLOT AXES=========================================
            if self.plot_axes:
                # bind the buffers
                vbo_axes_vertices = glvbo.VBO(self.axes_vertices)
                vbo_axes_vertices.bind()
                glEnableClientState(GL_VERTEX_ARRAY)
                glVertexPointer(2, GL_FLOAT, 0, vbo_axes_vertices)

                vbo_axes_color = glvbo.VBO(self.axes_color)
                vbo_axes_color.bind()
                glEnableClientState(GL_COLOR_ARRAY)
                glColorPointer(3, GL_FLOAT, 0, vbo_axes_color)

                # draw axes
                glMultiDrawArrays(GL_LINES, self.axes_index_starts, self.axes_vertex_count, self.axes_count)

                # unbind buffers
                glDisableClientState(GL_VERTEX_ARRAY)
                glDisableClientState(GL_COLOR_ARRAY)
                vbo_axes_vertices.unbind()
                vbo_axes_color.unbind()

            # ===========================DRAW PLOT TEXT=========================================
            # paint plot title and dimension markers
            painter = QPainter()
            painter.begin(self)

            # set color and font size
            painter.setPen(QColor('Black'))
            painter.setFont(QFont('Helvetica', 15))
            fm = QFontMetricsF(painter.font())

            # center and paint the plot markers
            if self.plot_type == 'PCP':
                drawPCPLabels(painter, self.feature_count, self.width, self.height, fm, self.feature_positions)
                # center and paint the title
                title = 'Parallel Coordinate Plot'
                x_title_offset = fm.boundingRect(title).width() / 2
                painter.drawText(self.width / 2 - x_title_offset, 40, title)

            elif self.plot_type == 'SPCP':
                drawSPCLabels(painter, self.feature_count, self.width, self.height, fm, self.feature_positions)
                title = 'Shifted Paired Coordinate Plot'
                x_title_offset = fm.boundingRect(title).width() / 2
                painter.drawText(self.width / 2 - x_title_offset, 20, title)
            else:
                # center and paint the title
                title = self.title
                x_title_offset = fm.boundingRect(title).width() / 2
                painter.drawText(self.width / 2 - x_title_offset, 40, title)

            painter.end()


