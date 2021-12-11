import numpy as np
from PyQt5.QtWidgets import QOpenGLWidget
from OpenGL.GL import *
import OpenGL.arrays.vbo as glvbo
import DICPGETVERTICES

# ====================================
# implement keyboard input later

# enter dataset name as string
#dataset_name = 'iris_dataset.csv'
#dataset_name = 'hypercube.csv'
#dataset_name = 'page-blocks-reduced.csv'
dataset_name = 'breast-cancer-wisconsin-new-feature-even.csv'
#dataset_name = 'mnist_train.csv'


# ====================================
class makeDICP:
    def __init__(self, new_plot):
        # get vertex array using getvertices class
        new_plot.makeCurrent()

        data_class = DICPGETVERTICES.getVerticesAndColors(dataset_name, ',', True, 'class')
        data, num_features, num_samples, color_array = data_class.getVertexAndColor()
        data = data.astype('float32')
        color_array = color_array.astype('float32')

        glClearColor(1, 1, 1, 1)

        # make buffers
        vbo_vertex = glvbo.VBO(data)
        vbo_color = glvbo.VBO(color_array)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor(1, 0, 0)

        # bind the buffers
        vbo_vertex.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(2, GL_FLOAT, 0, vbo_vertex)
        vbo_color.bind()
        glEnableClientState(GL_COLOR_ARRAY)
        glColorPointer(3, GL_FLOAT, 0, vbo_color)

        # prepare the indices for drawing several lines
        indices = np.arange(0, num_samples * int(num_features / 2), int(num_features / 2))
        num_vert_per_line = np.repeat(int(num_features / 2), num_samples)

        # draw the plot samples
        glMultiDrawArrays(GL_LINE_STRIP, indices, num_vert_per_line, num_samples)

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