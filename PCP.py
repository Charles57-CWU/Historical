import numpy as np
from PyQt5.QtWidgets import QOpenGLWidget
from OpenGL.GL import *
import OpenGL.arrays.vbo as glvbo
import PCPGETVERTICES


# ====================================
# implement keyboard input later

# enter dataset name as string
dataset_name = 'iris_dataset.csv'
#dataset_name = 'hypercube.csv'
#dataset_name = 'page-blocks-reduced.csv'
#dataset_name = 'breast-cancer-wisconsin.csv'
#dataset_name = 'mnist_train.csv'

# ====================================
class makePCP:
    def __init__(self, new_plot):
        # get vertex array using getvertices class
        new_plot.makeCurrent()

        # get vertex array using getvertices class
        data_class = PCPGETVERTICES.getVerticesAndColors(dataset_name, ',', True, 'class')
        data, num_features, num_samples, color_array = data_class.getVertexAndColor()
        data = data.astype('float32')
        color_array = color_array.astype('float32')

        # get axes vertex array
        axes_vertex_array, axes_color = data_class.getAxis(num_features)
        axes_vertex_array = np.asarray(axes_vertex_array, dtype='float32')
        axes_color = axes_color.astype('float32')

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
        indices = np.arange(0, num_samples * num_features, num_features)
        num_vert_per_line = np.repeat(num_features, num_samples * num_features)

        # draw the plot samples
        glMultiDrawArrays(GL_LINE_STRIP, indices, num_vert_per_line, num_samples)

        # bind the buffers
        vbo_axis.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, vbo_axis)
        vbo_axis_color.bind()
        glEnableClientState(GL_COLOR_ARRAY)
        glColorPointer(3, GL_FLOAT, 0, vbo_axis_color)

        # prepare the indices for drawing several lines
        axis_ind = np.arange(0, (num_features + 1) * 2, 2)
        axis_per_line = np.repeat(2, num_features + 1)

        # draw axes
        glMultiDrawArrays(GL_LINES, axis_ind, axis_per_line, num_features + 1)