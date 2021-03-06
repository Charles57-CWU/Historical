import numpy as np
from OpenGL.GL import *
import OpenGL.arrays.vbo as glvbo
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtGui import QPainter, QColor, QFont, QFontMetricsF

import PLOT_OPENGL_INFORMATION
import CONVEX_HULL


def drawPCPLabels(painter, feature_count, width, height, fm, feature_positions, feature_names):
    x_min = 0.1 * width
    x_max = width - x_min
    x_pos_array = np.linspace(x_min, x_max, feature_count)

    for i in range(feature_count):
        #marker = 'X' + str(feature_positions[i] - 1)
        marker = feature_names[i]
        x_offset = fm.boundingRect(marker).width() / 2
        painter.drawText(x_pos_array[i] - x_offset, height - (height * 0.1) + 35, marker)


def drawSPCLabels(painter, feature_count, width, height, fm, feature_positions):
    x_min = 0.1 * width
    x_max = width - x_min
    vert_pos_array = np.linspace(x_min, x_max, int(feature_count / 2) + 1)
    horiz_pos_array = np.linspace(x_min, x_max, feature_count + 1)

    j = 2
    for i in range(int(feature_count / 2)):
        # create the vertical markers
        y_marker = 'X' + str(feature_positions[j - 1] - 1)
        x_offset_vertical = fm.boundingRect(y_marker).width() / 2
        painter.drawText(vert_pos_array[i] - x_offset_vertical, height * 0.1 - 10, y_marker)
        # create the horizontal markers
        x_marker = 'X' + str(feature_positions[j - 2] - 1)
        x_offset_horizontal = fm.boundingRect(x_marker).width() / 2
        painter.drawText(horiz_pos_array[j - 1] - x_offset_horizontal, height - (height * 0.1) + 30, x_marker)

        j += 2


def drawTitle(painter, class_names, class_count, fm, width, height):
    space = '                '
    title = ''

    colors = [QColor(255, 0, 0), QColor(0, 255, 0), QColor(0, 0, 255), QColor(255, 0, 255)]

    for i in range(3):
        if i == (2):
            title += class_names[i]
        else:
            title += (class_names[i] + space)

    x_title_offset = fm.boundingRect(title).width() / 2

    spacer = 0
    painter.setPen(colors[0])
    painter.drawText(width / 2 - (x_title_offset - spacer), height - (height * 0.1) + 70, class_names[0])
    for i in range(1, 3):
        painter.setPen(colors[i])
        spacer += fm.boundingRect((class_names[i-1] + space)).width()
        painter.drawText(width / 2 - (x_title_offset - spacer), height - (height * 0.1) + 70, class_names[i])


def drawHulls(hulls, class_count):
    colors = [#[1, 0, 0, 0.3],
              [0, 1, 0, 0.3], [0, 0, 1, 0.3]]
    print('here?')
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glDepthMask(GL_FALSE)

    for i in range(class_count):

        if i == 0:
            glColor4f(0, 1, 0, 0.2)
        elif i == 1:
            glColor4f(0, 0, 1, 0.2)
        else:
            glColor4f(0, 0, 1, 0.2)
        arr = np.asarray(hulls[i], dtype='float32')
        glBegin(GL_POLYGON)
        print('k')
        for j in range(len(arr)):
            print(j)
            glVertex2f(arr[j][0], arr[j][1])
        glEnd()
    glDepthMask(GL_TRUE)
    glDisable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)


class makePlot(QOpenGLWidget):
    width = 800
    height = 600

    def __init__(self, dataframe, class_count, feature_count, sample_count,
                 count_per_class_array, feature_positions, plot_type, feature_names, class_names, parent=None):
        super(makePlot, self).__init__(parent)

        # initialize variables
        self.plot_type = plot_type
        # class variables
        self.class_vertices = None
        self.class_dict = None

        self.class_colors = None
        self.class_color_dict = None

        self.class_index_starts = None
        self.class_vertex_count = None
        self.current_sample_count = None
        # axes variables
        self.axes_vertices = None
        self.axes_color = None
        self.axes_index_starts = None
        self.axes_vertex_count = None
        self.axes_count = None
        self.plot_axes = True
        self.feature_positions = feature_positions
        # marker variables
        self.marker_dict = None
        self.marker_color_dict = None
        self.marker_vertices = None
        self.marker_colors = None
        self.marker_index_starts = None
        self.marker_vertex_count = None
        self.current_marker_count = None

        self.plot_markers = True

        self.class_names = class_names
        self.class_count = class_count
        self.feature_names = feature_names
        self.convex_hull = []

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
            self.class_dict = ini_plot_info.class_dict
            self.class_vertices = self.class_dict[0]
            for i in range(1, len(self.class_dict)):
                self.class_vertices = np.concatenate((self.class_vertices, self.class_dict[i]))
            self.class_vertices = self.class_vertices.astype('float32')

            self.class_color_dict = ini_plot_info.class_color_dict
            self.class_colors = self.class_color_dict[0]
            for i in range(1, len(self.class_color_dict)):
                self.class_colors = np.concatenate((self.class_colors, self.class_color_dict[i]))
            self.class_colors = self.class_colors.astype('float32')

            # gets the starting index for each sample to plot
            self.class_index_starts = ini_plot_info.class_index_starts
            # gets the number of vertices to plot per sample
            self.class_vertex_count = ini_plot_info.class_vertex_count
            # number of samples to plot
            self.current_sample_count = sample_count

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
            establish markers to plot
            markers can be turned on/off later on
            """
            print('lol5')
            self.marker_dict = ini_plot_info.marker_dict
            self.marker_vertices = self.marker_dict[0]
            for i in range(1, len(self.marker_dict)):
                self.marker_vertices = np.concatenate((self.marker_vertices, self.marker_dict[i]))
            self.marker_vertices = self.marker_vertices.astype('float32')

            self.marker_color_dict = ini_plot_info.marker_color_dict
            self.marker_colors = self.marker_color_dict[0]
            for i in range(1, len(self.marker_color_dict)):
                self.marker_colors = np.concatenate((self.marker_colors, self.marker_color_dict[i]))
            self.marker_colors = self.marker_colors.astype('float32')
            # marker information in (x, y) cartesian
            # color at each vertex in (R, G, B) - Note: RGB is scaled between 0 and 1
            # gets the starting index for each marker to plot
            self.marker_index_starts = ini_plot_info.marker_index_starts
            # gets the number of vertices to plot per marker
            self.marker_vertex_count = ini_plot_info.marker_vertex_count
            # number of markers to plot
            self.current_marker_count = ini_plot_info.marker_count
            """
            label information
            """
            self.title = ini_plot_info.title
            self.feature_count = feature_count
            print('lol3')

    #            if self.plot_type == 'ACP_OPT':
#                hull = CONVEX_HULL.convexhull(self.class_dict, self.feature_count, self.class_count, count_per_class_array)
#                self.convex_hull = hull.points_dict
            #    print(self.convex_hull[0])
            #    print('t?')


    def initializeGL(self):
        # make background white
        glClearColor(1, 1, 1, 1)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-0.125, 1.125, -0.125, 1.125, 0, 1)
        glEnable(GL_PROGRAM_POINT_SIZE)
        glPointSize(5)


    def resizeGL(self, w, h):
        self.width, self.height = w, h
        glViewport(0, 0, w, h)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if self.plot_type:
            # =====================
            # ======DRAW PLOT SAMPLES=========================================
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
            glMultiDrawArrays(GL_LINE_STRIP, self.class_index_starts, self.class_vertex_count,
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

            # ===========================DRAW PLOT MARKERS=========================================
            if self.plot_markers:
                # bind the buffers
                vbo_marker_vertices = glvbo.VBO(self.marker_vertices)
                vbo_marker_vertices.bind()
                glEnableClientState(GL_VERTEX_ARRAY)
                glVertexPointer(2, GL_FLOAT, 0, vbo_marker_vertices)

                vbo_marker_color = glvbo.VBO(self.marker_colors)
                vbo_marker_color.bind()
                glEnableClientState(GL_COLOR_ARRAY)
                glColorPointer(3, GL_FLOAT, 0, vbo_marker_color)

                # draw axes
                #if self.plot_type == 'AP' or self.plot_type == 'GLCSP' or self.plot_type == 'GLCSP_OPT':
                #    glMultiDrawArrays(GL_TRIANGLES, self.marker_index_starts, self.marker_vertex_count, self.current_marker_count)

                glMultiDrawArrays(GL_POINTS, self.marker_index_starts, self.marker_vertex_count, self.current_marker_count)

                # unbind buffers
                glDisableClientState(GL_VERTEX_ARRAY)
                glDisableClientState(GL_COLOR_ARRAY)
                vbo_marker_vertices.unbind()
                vbo_marker_color.unbind()

 #           if self.plot_type == 'ACP_OPT':
#                drawHulls(self.convex_hull, self.class_count)

            # ===========================DRAW PLOT TEXT=========================================
            # paint plot title and dimension markers
            painter = QPainter()
            painter.begin(self)

            # set color and font size
            painter.setPen(QColor('Black'))
            painter.setFont(QFont('Helvetica', 25))
            fm = QFontMetricsF(painter.font())

            # center and paint the plot markers
            if self.plot_type == 'PCP':
                #drawPCPLabels(painter, self.feature_count, self.width, self.height, fm, self.feature_positions, self.feature_names)
                # center and paint the title
                title = ''
                #for ele in self.class_names:
                #    title += '\t\t' + ele
                #drawTitle(painter, self.class_names, self.class_count, fm, self.width, self.height)

            elif self.plot_type == 'SPCP':
                drawSPCLabels(painter, self.feature_count, self.width, self.height, fm, self.feature_positions)
                title = 'Shifted Paired Coordinate Plot'
                x_title_offset = fm.boundingRect(title).width() / 2
                painter.drawText(self.width / 2 - x_title_offset, 20, title)
            else:
                # center and paint the title
                title = self.title
                x_title_offset = fm.boundingRect(title).width() / 2
                #painter.drawText(self.width / 2 - x_title_offset, 40, title)

            painter.end()


